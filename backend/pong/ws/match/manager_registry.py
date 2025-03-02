import asyncio
from typing import Optional

from ws.share import player_data

from . import match_manager


class MatchManagerRegistry:
    """
    MatchManagerにConsumerからアクセスするための関数。

    リモート対戦の場合はTournamentManagerが生成し、MatchManagerを登録する。
    ローカル対戦の場合はMatchHandlerが作成し、MatchManagerを登録する。

    試合が始まったら、Consumerの入力をこのクラスを通してMatchManagerに渡す。
    """

    def __init__(self) -> None:
        self.managers: dict[
            int, match_manager.MatchManager
        ] = {}  # { tournament_id: TournamentManager }
        self.lock = asyncio.Lock()

    async def register_match_manager(
        self, match_id: int, manager: match_manager.MatchManager
    ) -> None:
        """
        渡されたmatch_idでMatchManagerを登録
        すでに登録済みなら無視する。
        """
        async with self.lock:
            if match_id not in self.managers:
                self.managers[match_id] = manager

    async def delete_match(self, match_id: int) -> None:
        """
        渡されたmatch_idのMatchManagerがあれば削除する
        存在しない場合は何もしない
        """
        async with self.lock:
            if match_id in self.managers:
                del self.managers[match_id]

    async def get_match(
        self, match_id: int
    ) -> Optional[match_manager.MatchManager]:
        """
        渡されたmatch_idのMatchManagerがあれば返す。
        なければNoneを返す
        """
        return self.managers.get(match_id, None)

    ###########################################################
    # MatchManagerの関数を呼び出す関数
    ###########################################################

    async def init_action(
        self, match_id: int, player: player_data.PlayerData
    ) -> None:
        async with self.lock:
            if match_id in self.managers:
                await self.managers[match_id].handle_init_action(player)

    async def init_ready(
        self, match_id: int, player: player_data.PlayerData
    ) -> None:
        async with self.lock:
            if match_id in self.managers:
                await self.managers[match_id].handle_ready_action(player)

    async def paddle_up(self, match_id: int, team: str) -> None:
        async with self.lock:
            if match_id in self.managers:
                await self.managers[match_id]._paddle_up(team)

    async def paddle_down(self, match_id: int, team: str) -> None:
        async with self.lock:
            if match_id in self.managers:
                await self.managers[match_id]._paddle_down(team)

    async def exit_match(self, match_id: int, exited_team: str) -> None:
        async with self.lock:
            if match_id in self.managers:
                await self.managers[match_id].player_exited(exited_team)
