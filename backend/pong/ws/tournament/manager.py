from channels.layers import get_channel_layer  # type: ignore

from ..share import player_data


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
        self.channel_layer = get_channel_layer()

    async def add_participant(
        self, participant: player_data.PlayerData
    ) -> None:
        """
        参加者を追加。DBにも参加テーブルを作成する。
        参加者が4人になったらトーナメントを開始する。
        """
        pass

    async def remove_participant(
        self, participant: player_data.PlayerData
    ) -> None:
        """
        参加者を削除。DBから参加テーブルを削除する。
        """
        pass

    async def _start_tournament(self) -> None:
        """
        トーナメント開始処理。
        トーナメントの状態を変更し、Consumerへ通知する。
        リソースを作成した後に、ラウンドを作成する。
        """
        pass

    async def _progress_rounds(self) -> None:
        """
        ラウンド進行処理。
        participantを2人組にして、それぞれにマッチを作成。
        すべてのmatchが終わるのを待ち、まだ優勝者が決まらなければもう一度ラウンドを進行し、決まればトーナメントを終了する。
        """
        pass

    async def _end_tournament(self) -> None:
        """
        トーナメント終了処理。
        """
        pass

    async def cancel_tournament(self) -> None:
        """
        トーナメント中止処理。
        """
        pass

    async def _notify_participants(self, message: str) -> None:
        """
        トーナメント参加者へ通知する関数。
        """
        pass
