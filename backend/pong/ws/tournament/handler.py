from typing import Any


class TournamentHandler:
    """
    トーナメントイベントのハンドラークラス
    主に以下の役割を果たす
        - Tournamentイベントのメッセージの処理と送信
        - ChannelLayerのグループ参加・退出を管理
        - Redisを通して、Tournament進行管理インスタンスとやり取り
    """

    def __init__(self, channel_layer: Any, channel_name: str):
        """
        TournamentHandlerの初期化。

        :param channel_layer: チャネルレイヤー
        :param channel_name: チャネル名
        """
        self.channel_layer = channel_layer
        self.channel_name = channel_name

    def __str__(self) -> str:
        """
        TournamentHandlerオブジェクトを文字列として表現したものを返す。
        """
        return f"TournamentHandler(channel_name={self.channel_name})"

    def __repr__(self) -> str:
        """
        デバッグ用途でTournamentHandlerオブジェクトの詳細な表現の文字列を返す。
        """
        return f"TournamentHandler(channel_layer={self.channel_layer!r}, channel_name={self.channel_name!r})"
