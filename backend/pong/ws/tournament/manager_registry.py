from ..share import player_data
from . import manager


class TournamentManagerRegistry:
    """
    トーナメント進行クラス（TournamentManager）を操作する関数を提供するクラス
    Consumerはこのクラスの関数を通して、自分が参加するトーナメントの進行クラスにアクションを送る。
    """

    def __init__(self) -> None:
        self.tournaments: dict[
            int, manager.TournamentManager
        ] = {}  # { tournament_id: TournamentManager }

    async def create_tournament(self, tournament_id: int) -> None:
        """
        tournament_id に TournamentManager を作成し、トーナメントを開始。
        終了後に回収する。
        """
        pass

    async def delete_tournament(self, tournament_id: int) -> None:
        """
        tournament_id に対応する TournamentManager を削除
        """
        pass

    async def add_participant(
        self, tournament_id: int, participant: player_data.PlayerData
    ) -> None:
        """
        指定した TournamentManager に参加者を追加
        """
        pass

    async def remove_participant(
        self, tournament_id: int, participant: player_data.PlayerData
    ) -> None:
        """
        指定した TournamentManager から参加者を削除
        """
        pass
