import asyncio
from typing import Optional

from ..share import constants as ws_constants
from . import constants as match_constants
from . import serializers as match_serializers


class MatchHandler:
    """
    Pongゲーム時にクライアントとの通信を処理するクラス。
    """

    def __init__(self, channel_name: str):
        """
        MatchHandlerの初期化。

        :param channel_layer: チャネルレイヤー
        :param channel_name: チャネル名
        """
        self.stage: Optional[match_constants.Stage] = None
        self.stage_handlers = {
            match_constants.Stage.INIT.value: self._handle_init,
            match_constants.Stage.READY.value: self._handle_ready,
            match_constants.Stage.PLAY.value: self._handle_play,
            match_constants.Stage.END.value: self._handle_end,
        }
        self.is_local: bool = True

    def __str__(self) -> str:
        """
        MatchHandlerオブジェクトを文字列として表現。

        :return: MatchHandlerオブジェクトの文字列表現
        """
        return f"MatchHandler(stage={self.stage})"

    def __repr__(self) -> str:
        """
        MatchHandlerオブジェクトを詳細に表現。

        :return: MatchHandlerオブジェクトの詳細な文字列表現
        """
        return (
            f"MatchHandler(stage={self.stage}, "
            f"local_play={self.local_play}, "
            f"channel_handler={self.channel_handler!r})"
        )

    # ===================
    # ハンドラーメソッド
    # ===================
    async def handle(self, payload: dict) -> None:
        """
        プレイヤーからの入力を受け取り、ステージごとに処理を振り分ける。

        :param payload: プレイヤーから送られてきたペイロード
        """
        serializer = match_serializers.MatchInputSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        data: dict = serializer.validated_data[ws_constants.DATA_KEY]
        stage: str = serializer.validated_data[match_constants.Stage.key()]
        handler = self.stage_handlers[stage]

        # TODO: ステージごとのバリデーションも実装する必要あり
        # TODO: 適切なエラーハンドリングを実装
        # TODO: ステージが順番通りに来ているか確認する処理必要
        if callable(handler):
            await handler(data)

    async def _handle_init(self, data: dict) -> None:
        """
        INITステージのメッセージが送られてきたときの処理
        ゲームの初期化処理。
        初期配置情報などを送信する。

        :param data: 初期化に必要なデータ
        """
        self.stage = match_constants.Stage.INIT
        # プレイモードによって所属させるグループを変える
        if (
            data[match_constants.Mode.key()]
            == match_constants.Mode.LOCAL.value
        ):
            TODO: マッチマネジャーを作成して、ローカルゲームのセットアップを行う。
        elif (
            data[match_constants.Mode.key()]
            == match_constants.Mode.REMOTE.value
        ):
            self.is_local = False

        # TODO: remoteの場合のグループ作成方法は別で考える

        # LOCALモードの場合teamやdisplay_nameは必要ない

    async def _handle_ready(self, data: dict) -> None:
        """
        READYステージのメッセージが送られてきたときの処理
        プレイヤーの準備が整ったことがdataによってわかるので、ゲームを開始する。

        :param data: 準備状態に必要なデータ
        """
        self.stage = match_constants.Stage.READY

        # ゲーム状況の更新をしてプレーヤーに非同期で送信し続ける処理を開始する
        self.stage = match_constants.Stage.PLAY

    async def _handle_play(self, data: dict) -> None:
        """
        PLAYステージのメッセージが送られてきたときの処理
        プレーヤーのパドルの動きに基づいてゲーム状態を更新。

        :param data: パドルの移動情報
        """
        self._move_paddle(paddle_move=data)

    async def _handle_end(self, data: dict) -> None:
        """
        ENDステージのメッセージが送られてきたときの処理
        プレーヤーがmatchを退出したときの処理を行う。
        """
        await self.cleanup()

    async def _end_process(self) -> None:
        """
        ゲーム終了時の処理。

        ENDステージのメッセージを送信し、クリーンナップ処理を行う。
        """
        await self.cleanup()

    async def cleanup(self) -> None:
        """
        ゲーム終了後のクリーンナップ処理
        グループから削除し、状態を初期化する
        """
        self.stage = None
        self.is_local = True
