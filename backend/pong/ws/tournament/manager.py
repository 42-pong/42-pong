import asyncio
import random

from channels.layers import get_channel_layer  # type: ignore

from matches import constants as match_db_constants
from tournaments import constants as tournament_db_constants
from ws.match import match_manager
from ws.share import constants as ws_constants

from ..match import async_db_service as match_service
from ..match import constants as match_ws_constants
from ..share import channel_handler, player_data
from . import async_db_service as tournament_service
from . import constants as tournament_ws_constants


class TournamentManager:
    """
    4人のConsumerとやり取りをしながらトーナメント進行をするためのクラス

    4人と専用のチャネルレイヤーを持つためにユニークなグループ名を持つ。
    基本的にConsumerからは関数を通してアクションを受け取って、チャネルレイヤーを通してConsumerに通知する。

    group_name: 'tournament_{tournament_id}'
    """

    def __init__(self, tournament_id: int) -> None:
        self.tournament_id: int = tournament_id
        self.group_name: str = f"tournament_{self.tournament_id}"
        self.participants: list[
            player_data.PlayerData
        ] = []  # 参加者の情報のリスト
        self.channel_handler = channel_handler.ChannelHandler(
            get_channel_layer(), None
        )
        self.waiting_for_participants = (
            asyncio.Event()
        )  # 参加者を待機するイベント

    async def add_participant(
        self, participant: player_data.PlayerData
    ) -> None:
        """
        参加者を追加。DBにも参加テーブルを作成する。
        参加者が4人になったらトーナメントを開始する。
        """
        self.participants.append(participant)
        # TODO: 参加レコードを作成
        await self._send_player_reload_message()

        if len(self.participants) == 4:
            # 4人集まったらイベントをセットしてトーナメントを開始
            self.waiting_for_participants.set()

    async def remove_participant(
        self, participant: player_data.PlayerData
    ) -> int:
        """
        参加者を削除。DBから参加テーブルを削除する。

        Returns:
            int: 削除後の参加者数を返す。
        """
        if participant in self.participants
            self.participants.remove(participant)
        # TODO: 参加レコードを削除
        if len(self.participants) == 0:
            # キャンセル処理
            await self.cancel_tournament()
            return 0

        await self._send_player_reload_message()
        return len(self.participants)

    async def run(self) -> None:
        """
        トーナメントのすべての進行を管理する関数
        """
        # 4人参加するまで待機。
        await self.waiting_for_participants.wait()

        # トーナメントの開始処理を行う。
        await self._start_tournament()

        # ラウンドを1つずつ進める。
        # もし次のラウンドが残っていれば再び実行される。
        await self._progress_rounds(self.participants)

        # トーナメントの終了処理を行う。
        await self._end_tournament()

    async def _start_tournament(self) -> None:
        """
        トーナメント開始処理。
        トーナメントの状態を変更し、Consumerへ通知する。
        リソースを作成した後に、ラウンドを作成する。
        """
        # TODO: トーナメント開始アナウンスを送信。
        # TODO: トーナメントの状態をON_GOINGに更新

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
            # TODO: Error処理
            if update_result.is_error():
                return update_result  # エラー発生時は処理を中断
            return
    

        # ラウンド作成
        round_result = await tournament_service.create_round(
            self.tournament_id, round_number
        )
        # TODO: Error処理
        if round_result.is_error():
            return round_result  # エラー発生時は処理を中断
        # TODO: ラウンド開始をアナウンス

        round_id = round_result.value[tournament_db_constants.RoundFields.ID]

        # ラウンドの1対1マッチに振り分ける
        matchups = self._pair_participants(participants)
        # MatchManagerを作成し、並列で実行する
        match_results = await self._run_matches(round_id, matchups)
        # 勝者・敗者処理
        next_round_participants = await self._process_results(
            round_number, match_results
        )

        # TODO: ラウンドの状態を更新
        # TODO: ラウンド終了をアナウンス

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
        pass

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
            if update_result.is_error():
                return update_result  # エラー発生時は処理を中断
            next_round_participants.append(winner)
        return next_round_participants

    async def _end_tournament(self) -> None:
        """
        トーナメント終了処理。
        """
        # TODO: 参加者が全員いなくなるのを待ってから、manager_registryから削除?
        # TODO: 優勝者のランクを更新
        await self._send_tournament_reload_message()

    async def cancel_tournament(self) -> None:
        """
        トーナメント中止処理。
        """
        # トーナメント開始後のキャンセル処理
        # TODO: すべてのNOT_STARTEDのリソースをCANCELEDに変更

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

    def _build_announce_message(self, type: str, data: dict) -> dict:
        """
        プレーヤーに送るアナウンスメッセージを作成。

        :param data: ステージに関連するデータ
        :return: 作成したメッセージ
        """
        # TODO: チャットを実装したら実装
        return {}

    def send_group_chat(self, user_id: int, content: str) -> None:
        """
        プレーヤーがグループチャットに送信したメッセージを全員に再送信する関数。
        ChatHandlerから呼ばれる。
        """
        # TODO: チャットを実装したら実装
        pass
