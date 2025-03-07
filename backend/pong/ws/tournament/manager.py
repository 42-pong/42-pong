import asyncio
import logging
import random
from typing import Optional

from channels.db import database_sync_to_async  # type: ignore
from channels.layers import get_channel_layer  # type: ignore

from matches import constants as match_db_constants
from tournaments import constants as tournament_db_constants
from ws.chat import constants as chat_constants
from ws.match import manager_registry, match_manager
from ws.share import constants as ws_constants

from ..match import async_db_service as match_service
from ..match import constants as match_ws_constants
from ..share import channel_handler, player_data
from . import async_db_service as tournament_service
from . import constants as tournament_ws_constants

logger = logging.getLogger(__name__)


class TournamentManager:
    """
    4人のConsumerとやり取りをしながらトーナメント進行をするためのクラス

    4人と専用のチャネルレイヤーを持つためにユニークなグループ名を持つ。
    基本的にConsumerからは関数を通してアクションを受け取って、チャネルレイヤーを通してConsumerに通知する。

    group_name: 'tournament_{tournament_id}'
    """

    def __init__(
        self, tournament_id: int, participant: player_data.PlayerData
    ) -> None:
        self.tournament_id: int = tournament_id
        self.group_name: str = f"tournament_{self.tournament_id}"
        self.participants: list[player_data.PlayerData] = [
            participant
        ]  # 参加者の情報のリスト
        self.channel_handler = channel_handler.ChannelHandler(
            get_channel_layer(), None
        )
        self.waiting_for_participants = (
            asyncio.Event()
        )  # 参加者を待機するイベント
        self.match_manager_registry = manager_registry.global_registry

    async def add_participant(
        self, participant: player_data.PlayerData
    ) -> bool:
        """
        参加者を追加。DBにも参加テーブルを作成する。
        参加者が4人になったらトーナメントを開始する。
        """
        # 型チェック用
        if (
            participant.user_id is None
            or participant.participation_name is None
        ):
            return False
        # 参加レコードを作成
        create_result = await database_sync_to_async(
            tournament_service.create_participation
        )(
            self.tournament_id,
            participant.user_id,
            participant.participation_name,
        )
        if create_result.is_error:
            return False

        # 先にいるトーナメント参加者全員にリロードメッセージを送信
        await self._send_player_reload_message()

        # 新規参加者をグループに追加
        await self.channel_handler.add_to_group(
            self.group_name, participant.channel_name
        )

        self.participants.append(participant)

        if len(self.participants) == 4:
            # 4人集まったらイベントをセットしてトーナメントを開始
            self.waiting_for_participants.set()
            return True

        # await self.send_group_announcement(
        #    chat_constants.GroupAnnouncement.MessageType.JOIN.value,
        #    participant,
        #    None,
        # )
        return True

    async def remove_participant(
        self, participant: player_data.PlayerData
    ) -> int:
        """
        参加者を削除。DBから参加テーブルを削除する。

        Returns:
            int: 削除後の参加者数を返す。
        """
        # 参加レコードを削除
        delete_result = await tournament_service.delete_participation(
            self.tournament_id, participant.user_id
        )
        if delete_result.is_error:
            # 残りが一人なわけではないが、0以外の値を返したい
            return 1

        if participant in self.participants:
            self.participants.remove(participant)

        # 退出者をグループから削除
        await self.channel_handler.remove_from_group(
            self.group_name, participant.channel_name
        )

        # 参加者がいなくなったらキャンセル処理をして、
        if len(self.participants) == 0:
            # キャンセル処理
            await self.cancel_tournament()
            return 0

        # トーナメント参加者全員にリロードメッセージを送信
        await self._send_player_reload_message()
        # await self.send_group_announcement(
        #    chat_constants.GroupAnnouncement.MessageType.LEAVE.value,
        #    participant,
        #    None,
        # )
        return len(self.participants)

    async def run(self) -> None:
        """
        トーナメントのすべての進行を管理する関数
        """
        try:
            # 4人参加するまで待機。
            await self.waiting_for_participants.wait()

            # トーナメントの開始処理を行う。
            await self._start_tournament()

            # ラウンドを1つずつ進める。
            # もし次のラウンドが残っていれば再び実行される。
            await self._progress_rounds(self.participants)

            # トーナメントの終了処理を行う。
            await self._end_tournament()
        except Exception as e:
            # データベース操作によるエラーをキャッチ
            logger.error(f"Error: {e}")
            await self.cancel_tournament()

    async def _start_tournament(self) -> None:
        """
        トーナメント開始処理。
        トーナメントの状態を変更し、Consumerへ通知する。
        リソースを作成した後に、ラウンドを作成する。
        """
        # TODO: トーナメント開始アナウンスを送信。
        update_result = await tournament_service.update_tournament_status(
            self.tournament_id,
            tournament_db_constants.TournamentFields.StatusEnum.ON_GOING.value,
        )

        if update_result.is_error:
            logger.error(f"Error: {update_result.unwrap_error()}")

        # トーナメント情報を更新するように通知
        await self._send_tournament_reload_message()

    async def _progress_rounds(
        self, participants: list[player_data.PlayerData], round_number: int = 1
    ) -> None:
        """
        トーナメントのラウンドを進行し、参加者が1人になるまでラウンドを繰り返す。
        """
        # ラウンドに進んだ人数が1人になったらラウンド進行を終了
        if len(participants) <= 1:
            # 残った人が優勝
            update_result = (
                await tournament_service.update_participation_ranking(
                    self.tournament_id, participants[0].user_id, 1
                )
            )
            if update_result.is_error:
                logger.error(f"Error: {update_result.unwrap_error()}")
            return

        # ラウンド作成
        create_result = await tournament_service.create_round(
            self.tournament_id,
            round_number,
            tournament_db_constants.RoundFields.StatusEnum.ON_GOING.value,
        )
        if create_result.is_error:
            logger.error(f"Error: {create_result.unwrap_error()}")

        # TODO: ラウンド開始をアナウンス
        await self._send_tournament_reload_message()

        # 新規ラウンド時に10秒待機
        await asyncio.sleep(10)

        value = create_result.unwrap()
        round_id = value[tournament_db_constants.RoundFields.ID]

        # ラウンドの1対1マッチに振り分ける
        matchups = self._pair_participants(participants)
        # MatchManagerを作成し、並列で実行する
        match_results = await self._run_matches(round_id, matchups)
        # 勝者・敗者処理
        next_round_participants = await self._process_results(
            round_number, match_results
        )

        update_result = await tournament_service.update_round_status(
            round_id,
            tournament_db_constants.RoundFields.StatusEnum.COMPLETED.value,
        )
        if update_result.is_error:
            logger.error(f"Error: {update_result.unwrap_error()}")

        # TODO: ラウンド終了をアナウンス
        await self._send_tournament_reload_message()

        await self._progress_rounds(next_round_participants, round_number + 1)

    def _pair_participants(
        self, participants: list[player_data.PlayerData]
    ) -> list[tuple[player_data.PlayerData, player_data.PlayerData]]:
        """
        残りの参加者をランダムにペアリングして1対1のマッチを作成する。

        :return: 1対1マッチのリスト
        """
        random.shuffle(participants)
        matchups = [
            (participants[i], participants[i + 1])
            for i in range(0, len(participants) - 1, 2)
        ]
        return matchups

    async def _run_matches(
        self,
        round_id: int,
        matchups: list[tuple[player_data.PlayerData, player_data.PlayerData]],
    ) -> list[tuple[int, player_data.PlayerData, player_data.PlayerData]]:
        """
        各マッチを並列で実行し、結果を返す。

        :param matchups: 1対1のマッチリスト
        :return: 各マッチの結果 (勝者, 敗者) のリスト
        """
        # マッチ作成と参加レコード作成
        create_tasks = [match_service.create_match(round_id) for _ in matchups]
        create_results = await asyncio.gather(*create_tasks)
        await self._send_tournament_reload_message()

        self.valid_matches = []
        self.match_manager_tasks = []  # バックグラウンドで実行する run() タスクを格納

        for (player1, player2), create_result in zip(matchups, create_results):
            self.participation_tasks = []

            if create_result.is_error:
                logger.error(f"Error: {create_result.unwrap_error()}")

            value = create_result.unwrap()
            match_id = value[match_db_constants.MatchFields.ID]

            # 参加レコード作成
            self.participation_tasks.append(
                match_service.create_participation(
                    match_id,
                    player1.user_id,
                    team=match_ws_constants.Team.ONE.value,
                )
            )
            self.participation_tasks.append(
                match_service.create_participation(
                    match_id,
                    player2.user_id,
                    team=match_ws_constants.Team.TWO.value,
                )
            )
            # 参加レコードを並列作成
            participation_results = await asyncio.gather(
                *self.participation_tasks
            )
            for result in participation_results:
                if result.is_error:
                    logger.error(f"Error: {result.unwrap_error()}")

            # MatchManager 作成と登録
            manager = match_manager.MatchManager(
                match_id=match_id,
                player1=player1,
                player2=player2,
                mode=match_ws_constants.Mode.REMOTE.value,
            )

            # MatchManagerRegistryにMatchManagerを追加
            await self.match_manager_registry.register_match_manager(
                match_id, manager
            )
            # 試合をバックグラウンドで実行
            self.match_manager_tasks.append(asyncio.create_task(manager.run()))

            # 試合開始を 各consumer に通知
            # await self.send_group_announcement(
            #    chat_constants.GroupAnnouncement.MessageType.MATCH_START.value,
            #    player1,
            #    player2,
            # )
            await asyncio.sleep(5)
            await self._send_assign_match_message(match_id, player1)
            await self._send_assign_match_message(match_id, player2)

            self.valid_matches.append((match_id, manager, player1, player2))

        # バックグラウンドタスクの結果を収集
        match_results = await asyncio.gather(*self.match_manager_tasks)

        final_results = []
        for match_winner, (match_id, manager, player1, player2) in zip(
            match_results, self.valid_matches
        ):
            # 型チェックの関係で必要
            # 実際にはNoneが入ることはないはず
            if match_winner is None:
                continue

            # 試合結果を保持
            if match_winner.channel_name == player1.channel_name:
                winner = player1
                loser = player2
            else:
                winner = player2
                loser = player1
            final_results.append((match_id, winner, loser))

        return final_results

    async def _process_results(
        self,
        round_number: int,
        match_results: list[
            tuple[int, player_data.PlayerData, player_data.PlayerData]
        ],
    ) -> list[player_data.PlayerData]:
        """
        マッチの結果をアナウンスし、敗者を削除する。

        :param match_results: 各マッチのIDと結果 (勝者, 敗者) のリスト
        """
        next_round_participants = []
        for match_id, winner, loser in match_results:
            # 敗者のランキングを更新
            ranking = 4
            if round_number == 2:
                ranking = 2

            update_result = (
                await tournament_service.update_participation_ranking(
                    self.tournament_id, loser.user_id, ranking
                )
            )
            if update_result.is_error:
                logger.error(f"Error: {update_result.unwrap_error()}")
            next_round_participants.append(winner)
        return next_round_participants

    async def _end_tournament(self) -> None:
        """
        トーナメント終了処理。
        """
        # TODO: 参加者が全員いなくなるのを待ってから、manager_registryから削除?
        update_result = await tournament_service.update_tournament_status(
            self.tournament_id,
            tournament_db_constants.TournamentFields.StatusEnum.COMPLETED.value,
        )
        # TODO: Error処理
        if update_result.is_error:
            logger.error(f"Error: {update_result.unwrap_error()}")

        await self._send_tournament_reload_message()

    async def cancel_tournament(self) -> None:
        """
        トーナメント中止処理。
        """
        # トーナメント開始後のキャンセル処理
        # 状態がCOMPLETEDではない子のトーナメントに紐づくリソースをすべてCANCELEDに変更
        update_result = await tournament_service.cancel_uncompleted_tournament(
            self.tournament_id,
        )
        if update_result.is_error:
            logger.error(f"Error: {update_result.unwrap_error()}")

    async def _send_player_reload_message(self) -> None:
        """
        参加者が変わったことをConsumerに伝える関数
        これを受け取ったプレーヤーはRESTAPIで情報を取得し、画面を更新する。
        """
        message = self._build_tournament_message(
            tournament_ws_constants.Type.RELOAD.value,
            {
                tournament_ws_constants.Event.key(): tournament_ws_constants.Event.PLAYER_CHANGE.value
            },
        )
        await self.channel_handler.send_to_group(self.group_name, message)

    async def _send_tournament_reload_message(self) -> None:
        """
        トーナメントの状態が変わったことをConsumerに伝える関数
        これを受け取ったプレーヤーはRESTAPIで情報を取得し、画面を更新する。
        """
        message = self._build_tournament_message(
            tournament_ws_constants.Type.RELOAD.value,
            {
                tournament_ws_constants.Event.key(): tournament_ws_constants.Event.TOURNAMENT_STATE_CHANGE.value
            },
        )
        await self.channel_handler.send_to_group(self.group_name, message)

    async def _send_assign_match_message(
        self, match_id: int, player: player_data.PlayerData
    ) -> None:
        """
        トーナメントの状態が変わったことをConsumerに伝える関数
        これを受け取ったプレーヤーはRESTAPIで情報を取得し、画面を更新する。
        """
        message = self._build_tournament_message(
            tournament_ws_constants.Type.ASSIGNED.value,
            {tournament_ws_constants.MATCH_ID: match_id},
        )
        await self.channel_handler.send_to_consumer(
            message, player.channel_name
        )

    def _build_tournament_message(self, type: str, data: dict) -> dict:
        """
        プレーヤーに送るトーナメントメッセージを作成。

        :param data: ステージに関連するデータ
        :return: 作成したメッセージ
        """
        return {
            ws_constants.Category.key(): ws_constants.Category.TOURNAMENT.value,
            ws_constants.PAYLOAD_KEY: {
                tournament_ws_constants.Type.key(): type,
                ws_constants.DATA_KEY: data,
            },
        }

    def _build_chat_message(self, type: str, data: dict) -> dict:
        """
        プレーヤーに送るアナウンスメッセージを作成。

        :param data: ステージに関連するデータ
        :return: 作成したメッセージ
        """
        return {
            ws_constants.Category.key(): ws_constants.Category.CHAT.value,
            ws_constants.PAYLOAD_KEY: {
                chat_constants.Type.key(): type,
                ws_constants.DATA_KEY: data,
            },
        }

    async def send_group_chat(self, message: dict) -> None:
        """
        プレーヤーがグループチャットに送信したメッセージを全員に再送信する関数。
        ChatHandlerから呼ばれる。
        """
        await self.channel_handler.send_to_group(self.group_name, message)

    async def send_group_announcement(
        self,
        msg_type: str,
        player1: player_data.PlayerData,
        player2: Optional[player_data.PlayerData],
    ) -> None:
        """
        トーナメント中にトーナメント待機画面へ送るメッセージ
        """
        message = self._build_chat_message(
            chat_constants.Type.GROUP_ANNOUNCEMENT.value,
            {
                chat_constants.MESSAGE_TYPE: msg_type,
                chat_constants.GroupAnnouncement.PLAYER1: player1.user_id,
                chat_constants.GroupAnnouncement.PLAYER2: player2.user_id
                if player2 is not None and player2.user_id is not None
                else None,
            },
        )
        await self.channel_handler.send_to_group(self.group_name, message)
