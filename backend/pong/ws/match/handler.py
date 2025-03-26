import asyncio
from typing import Optional

from ..share import constants as ws_constants
from ..share import player_data
from . import constants as match_constants
from . import manager_registry, match_manager
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
        self.is_local_play: bool = True
        self.match_id: int = 0
        self.match_manager: Optional[match_manager.MatchManager] = None
        self.player_data: player_data.PlayerData = player_data.PlayerData(
            channel_name=channel_name,
            user_id=None,
            participation_name=None,
        )

    def __str__(self) -> str:
        """
        MatchHandlerオブジェクトを文字列として表現。

        :return: MatchHandlerオブジェクトの文字列表現
        """
        return (
            f"MatchHandler(stage={self.stage}, "
            f"player_data={self.player_data})"
        )

    def __repr__(self) -> str:
        """
        MatchHandlerオブジェクトを詳細に表現。

        :return: MatchHandlerオブジェクトの詳細な文字列表現
        """
        return (
            f"MatchHandler(stage={self.stage}, "
            f"is_local_play={self.is_local_play}, "
            f"match_manager={self.match_manager}, "
            f"player_data={self.player_data})"
        )

    # ===================
    # ハンドラーメソッド
    # ===================
    async def handle(self, payload: dict, user_id: Optional[int]) -> None:
        """
        プレイヤーからの入力を受け取り、ステージごとに処理を振り分ける。

        :param payload: プレイヤーから送られてきたペイロード
        """
        # ログイン後の初回にプレーヤーデータを作成
        if self.player_data.user_id is None and user_id is not None:
            self.player_data = player_data.PlayerData(
                channel_name=self.player_data.channel_name,
                user_id=user_id,
                participation_name=None,
            )

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
        # localなら来ないので、例外でないようにgetで取得
        match_id: int = data.get(match_constants.MATCH_ID, 0)
        mode: str = data[match_constants.Mode.key()]
        # プレイモードによって所属させるグループを変える
        if mode == match_constants.Mode.LOCAL.value:
            self.is_local_play = True
            # マッチマネジャーを作成して、ローカルゲームのセットアップを行う。
            self.match_manager = match_manager.MatchManager(
                match_id, self.player_data, None, mode
            )
            self.local_match_task = asyncio.create_task(
                self.match_manager.run()
            )
            await self.match_manager.handle_init_action(self.player_data)
        elif mode == match_constants.Mode.REMOTE.value:
            self.is_local_play = False
            self.match_id = match_id
            await manager_registry.global_registry.init_action(
                self.match_id, self.player_data
            )

        # TODO: remoteの場合のグループ作成方法は別で考える

        # LOCALモードの場合teamやdisplay_nameは必要ない

    async def _handle_ready(self, data: dict) -> None:
        """
        READYステージのメッセージが送られてきたときの処理
        プレイヤーの準備が整ったことがdataによってわかるので、ゲームを開始する。

        :param data: 準備状態に必要なデータ
        """
        self.stage = match_constants.Stage.READY
        if self.is_local_play and self.match_manager is not None:
            await self.match_manager.handle_ready_action(self.player_data)
        else:
            await manager_registry.global_registry.ready_action(
                self.match_id, self.player_data
            )

        # ゲーム状況の更新をしてプレーヤーに非同期で送信し続ける処理を開始する
        self.stage = match_constants.Stage.PLAY

    async def _handle_play(self, data: dict) -> None:
        """
        PLAYステージのメッセージが送られてきたときの処理
        プレーヤーのパドルの動きに基づいてゲーム状態を更新。

        :param data: パドルの移動情報
        """
        team: str = data[match_constants.Team.key()]
        move: str = data[match_constants.Move.key()]

        if self.is_local_play and self.match_manager is not None:
            if move == match_constants.Move.UP.value:
                await self.match_manager.paddle_up(team)
            elif move == match_constants.Move.DOWN.value:
                await self.match_manager.paddle_down(team)
        else:
            if move == match_constants.Move.UP.value:
                await manager_registry.global_registry.paddle_up(
                    self.match_id, team
                )
            elif move == match_constants.Move.DOWN.value:
                await manager_registry.global_registry.paddle_down(
                    self.match_id, team
                )

    async def _handle_end(self, data: dict) -> None:
        """
        ENDステージのメッセージが送られてきたときの処理
        プレーヤーがmatchを退出したときの処理を行う。
        """
        if self.is_local_play:
            if self.local_match_task and not self.local_match_task.done():
                self.local_match_task.cancel()  # タスクをキャンセル
                try:
                    # キャンセル後、タスクが終了するのを待つ
                    await self.local_match_task
                except asyncio.CancelledError:
                    pass
        else:
            await manager_registry.global_registry.exit_match(
                self.match_id, self.player_data
            )

        await self.cleanup()

    async def cleanup(self) -> None:
        """
        ゲーム終了後のクリーンナップ処理
        グループから削除し、状態を初期化する
        """
        if self.match_id != 0:
            await manager_registry.global_registry.exit_match(
                self.match_id, self.player_data
            )
        self.stage = None
        self.is_local_play = True
        self.match_manager = None
        self.match_id = 0
