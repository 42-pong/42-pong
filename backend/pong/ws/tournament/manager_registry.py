import asyncio
import logging

from ..share import player_data
from . import manager

logger = logging.getLogger(__name__)


class TournamentManagerRegistry:
    """
    トーナメント進行クラス（TournamentManager）を操作する関数を提供するクラス
    Consumerはこのクラスの関数を通して、自分が参加するトーナメントの進行クラスにアクションを送る。
    """

    def __init__(self) -> None:
        self.tournaments: dict[
            int, manager.TournamentManager
        ] = {}  # { tournament_id: TournamentManager }
        self.tasks: dict[
            int, asyncio.Task
        ] = {}  # { tournament_id: asyncio.Task } トーナメントIDと対応するタスクを保持
        self.lock = asyncio.Lock()

    async def create_tournament(
        self, tournament_id: int, participant: player_data.PlayerData
    ) -> None:
        """
        tournament_id に TournamentManager を作成し、トーナメントを開始。
        終了後に回収する。
        """
        async with self.lock:
            if tournament_id in self.tournaments:
                return  # 既にトーナメントが存在する場合は何もしない

            tournament_manager = manager.TournamentManager(
                tournament_id, participant
            )
            self.tournaments[tournament_id] = tournament_manager

            # `run()` を非同期タスクとして実行し、並列処理を可能にする
            task = asyncio.create_task(
                self._run_tournament(tournament_id, tournament_manager)
            )
            self.tasks[tournament_id] = task  # タスクを保存

    async def _run_tournament(
        self, tournament_id: int, tournament_manager: manager.TournamentManager
    ) -> None:
        """
        トーナメントのメイン処理を非同期タスクとして実行し、終了後に削除する。
        """
        try:
            await tournament_manager.run()  # トーナメントのメインループ
        except asyncio.CancelledError:
            return
        finally:
            await self.delete_tournament(tournament_id)  # 終了時に削除

    async def delete_tournament(self, tournament_id: int) -> None:
        """
        tournament_id に対応する TournamentManager を削除
        """
        async with self.lock:
            if tournament_id in self.tournaments:
                del self.tournaments[tournament_id]  # トーナメントを削除
                if tournament_id in self.tasks:
                    del self.tasks[tournament_id]  # タスクを削除

    async def add_participant(
        self, tournament_id: int, participant: player_data.PlayerData
    ) -> bool:
        """
        指定した TournamentManager に参加者を追加
        """
        async with self.lock:
            if tournament_id not in self.tournaments:
                return False  # トーナメントが存在しない場合は何もしない

            tournament_manager = self.tournaments[tournament_id]
            return await tournament_manager.add_participant(
                participant
            )  # 参加者を追加

    async def remove_participant(
        self, tournament_id: int, participant: player_data.PlayerData
    ) -> None:
        """
        指定した TournamentManager から参加者を削除
        """

        async with self.lock:
            if tournament_id not in self.tournaments:
                return  # トーナメントが存在しない場合は何もしない

            tournament_manager = self.tournaments[tournament_id]
            remaining_participants = (
                await tournament_manager.remove_participant(participant)
            )  # 参加者を削除

            # もし参加者が残っていなければ、トーナメントをキャンセルし実行中のトーナメントタスクを止める
            if remaining_participants == 0:
                task = self.tasks.get(tournament_id)
                if task is not None:
                    task.cancel()  # タスクをキャンセル
                    await task  # キャンセルしたタスクの完了を待機


# === グローバルな MatchManagerRegistry インスタンス ===
global_tournament_registry = TournamentManagerRegistry()
