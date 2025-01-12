import asyncio
from dataclasses import dataclass
from typing import Any, Final, Optional

from . import match_enums, ws_constants
from .serializers import match_serializer


@dataclass
class PosStruct:
    x: int
    y: int


class MatchHandler:
    """
    Pongゲームのマッチロジックおよび通信を処理するクラス。
    座標の原点（0, 0）は左上
    """

    # クラス定数
    HEIGHT: Final[int] = 400
    WIDTH: Final[int] = 600
    PADDLE_POS_FROM_GOAL: Final[int] = WIDTH // 100
    PADDLE_HEIGHT: Final[int] = 60
    PADDLE_WIDTH: Final[int] = 10
    PADDLE_SPEED: Final[int] = 5
    BALL_SIZE: Final[int] = 10
    BALL_SPEED: Final[int] = 2
    FPS: Final[float] = 1 / 60
    WINNING_SCORE: Final[int] = 5

    # クラス属性
    stage: Optional[match_enums.Stage]
    paddle1: PosStruct
    paddle2: PosStruct
    ball: PosStruct
    ball_speed: PosStruct
    score1: int
    score2: int
    local_play: bool
    group_name: str
    channel_layer: Any
    channel_name: str

    def __init__(self, channel_layer: Any, channel_name: str):
        """
        MatchHandlerの初期化。

        :param channel_layer: チャネルレイヤー
        :param channel_name: チャネル名
        """
        self.stage_handlers = {
            match_enums.Stage.INIT.value: self._handle_init,
            match_enums.Stage.READY.value: self._handle_ready,
            match_enums.Stage.PLAY.value: self._handle_play,
            match_enums.Stage.END.value: self._handle_end,
        }
        self.channel_layer = channel_layer
        self.channel_name = channel_name
        self._reset_state()

    def __str__(self) -> str:
        """
        MatchHandlerオブジェクトを文字列として表現。

        :return: MatchHandlerオブジェクトの文字列表現
        """
        return (
            f"MatchHandler(stage={self.stage}, "
            f"paddle1={self.paddle1}, paddle2={self.paddle2}, "
            f"ball={self.ball}, score1={self.score1}, score2={self.score2})"
        )

    def __repr__(self) -> str:
        """
        MatchHandlerオブジェクトを詳細に表現。

        :return: MatchHandlerオブジェクトの詳細な文字列表現
        """
        return (
            f"MatchHandler(stage={self.stage}, "
            f"paddle1={self.paddle1}, paddle2={self.paddle2}, "
            f"ball={self.ball}, ball_speed={self.ball_speed}, "
            f"score1={self.score1}, score2={self.score2}, "
            f"local_play={self.local_play}, group_name={self.group_name}, "
            f"channel_layer={self.channel_layer}, channel_name={self.channel_name})"
        )

    # ===================
    # ハンドラーメソッド
    # ===================
    async def handle(self, payload: dict) -> None:
        """
        プレイヤーからの入力を受け取り、ステージごとに処理を振り分ける。

        :param payload: プレイヤーから送られてきたペイロード
        """
        serializer = match_serializer.MatchInputSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        data: dict = serializer.validated_data[ws_constants.DATA_KEY]
        stage: str = serializer.validated_data[match_enums.Stage.key()]
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
        self.stage = match_enums.Stage.INIT
        # プレイモードによって所属させるグループを変える
        if data[match_enums.Mode.key()] == match_enums.Mode.LOCAL.value:
            self.group_name = "solo_match"
        elif data[match_enums.Mode.key()] == match_enums.Mode.REMOTE.value:
            self.group_name = "remote_match"

        await self._add_to_group()
        # TODO: remoteの場合のグループ作成方法は別で考える

        # LOCALモードの場合teamやdisplay_nameは必要ない
        # TODO: ここら辺べた書きになっているから何か他にいい方法がないか
        message = self._build_message(
            {
                match_enums.Team.key(): match_enums.Team.EMPTY.value,
                "display_name1": "",
                "display_name2": "",
                "paddle1": {"x": self.paddle1.x, "y": self.paddle1.y},
                "paddle2": {"x": self.paddle2.x, "y": self.paddle2.y},
                "ball": {"x": self.ball.x, "y": self.ball.y},
            },
        )
        await self._send_to_group(message)

    async def _handle_ready(self, data: dict) -> None:
        """
        READYステージのメッセージが送られてきたときの処理
        プレイヤーの準備が整ったことがdataによってわかるので、ゲームを開始する。

        :param data: 準備状態に必要なデータ
        """
        self.stage = match_enums.Stage.READY
        message = self._build_message({})
        await self._send_to_group(message)

        # ゲーム状況の更新をしてプレーヤーに非同期で送信し続ける処理を開始する
        self.stage = match_enums.Stage.PLAY
        asyncio.create_task(self._send_match_state())

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
        win_team: str = (
            match_enums.Team.ONE.value
            if self.score1 > self.score2
            else match_enums.Team.TWO.value
        )
        message = self._build_message(
            {"win": win_team, "score1": self.score1, "score2": self.score2},
        )
        await self._send_to_group(message)
        await self.cleanup()

    # ==============================
    # ゲームロジック関係のメソッド
    # ==============================
    def _move_paddle(self, paddle_move: dict) -> None:
        """
        プレイヤーの入力に合わせてパドルを移動させる。

        :param paddle_move: パドルの移動情報
        """
        match paddle_move[match_enums.Move.key()]:
            case match_enums.Move.UP.value:
                if (
                    paddle_move[match_enums.Team.key()]
                    == match_enums.Team.ONE.value
                    and self.paddle1.y > 0
                ):
                    self.paddle1.y -= self.PADDLE_SPEED
                elif (
                    paddle_move[match_enums.Team.key()]
                    == match_enums.Team.TWO.value
                    and self.paddle2.y > 0
                ):
                    self.paddle2.y -= self.PADDLE_SPEED

            case match_enums.Move.DOWN.value:
                if (
                    paddle_move[match_enums.Team.key()]
                    == match_enums.Team.ONE.value
                    and self.paddle1.y + self.PADDLE_HEIGHT < self.HEIGHT
                ):
                    self.paddle1.y += self.PADDLE_SPEED
                elif (
                    paddle_move[match_enums.Team.key()]
                    == match_enums.Team.TWO.value
                    and self.paddle2.y + self.PADDLE_HEIGHT < self.HEIGHT
                ):
                    self.paddle2.y += self.PADDLE_SPEED

    def _update_match_state(self) -> None:
        """
        ボールの移動や、ボールと壁・パドルとの衝突、得点の判定を行い、ゲーム状態を更新する。
        """
        # ボールの移動
        self.ball.x += self.ball_speed.x
        self.ball.y += self.ball_speed.y

        # 上下の壁との衝突判定
        if self.ball.y - self.BALL_SIZE <= 0:
            self.ball_speed.y = abs(self.ball_speed.y)
        elif self.ball.y + self.BALL_SIZE >= self.HEIGHT:
            self.ball_speed.y = -abs(self.ball_speed.y)

        # パドルとの衝突判定
        self._process_ball_paddle_collision(self.paddle1, True)
        self._process_ball_paddle_collision(self.paddle2, False)

        # 得点判定
        if self.ball.x + self.BALL_SIZE <= 0:
            self.score2 += 1
            self._reset_ball()
        elif self.ball.x - self.BALL_SIZE >= self.WIDTH:
            self.score1 += 1
            self._reset_ball()

        # 勝利判定
        if (
            self.score1 >= self.WINNING_SCORE
            or self.score2 >= self.WINNING_SCORE
        ):
            self.stage = match_enums.Stage.END

    def _process_ball_paddle_collision(
        self, paddle_pos: PosStruct, is_paddle1: bool
    ) -> None:
        """
        ボールとパドルの衝突判定と衝突時の処理

        Args:
            paddle_pos (PosStruct): パドルの位置
            is_paddle1 (bool): パドルがteam1のものかどうか
        """
        # 衝突判定
        if (
            self.ball.x - self.BALL_SIZE <= paddle_pos.x + self.PADDLE_WIDTH
            and self.ball.x + self.BALL_SIZE >= paddle_pos.x
            and self.ball.y - self.BALL_SIZE
            <= paddle_pos.y + self.PADDLE_HEIGHT
            and self.ball.y + self.BALL_SIZE >= paddle_pos.y
        ):
            # ボールのx座標がパドルの側面に当たった場合
            # ボールの中心がパドルの端よりも自陣側に過ぎていたらx軸方向に跳ね返さない
            if (
                self.ball.y >= paddle_pos.y
                and self.ball.y <= paddle_pos.y + self.PADDLE_HEIGHT
            ):
                if (
                    is_paddle1
                    and self.ball.x > paddle_pos.x + self.PADDLE_WIDTH
                ):
                    self.ball_speed.x = abs(self.ball_speed.x)
                elif self.ball.x < paddle_pos.x:
                    self.ball_speed.x = -abs(self.ball_speed.x)

            # ボールのy座標がパドルの上下面に当たった場合
            if (
                self.ball.x >= paddle_pos.x
                and self.ball.x <= paddle_pos.x + self.PADDLE_WIDTH
            ):
                if self.ball.y <= paddle_pos.y:
                    self.ball_speed.y = -abs(self.ball_speed.y)
                elif self.ball.y >= paddle_pos.y + self.PADDLE_HEIGHT:
                    self.ball_speed.y = abs(self.ball_speed.y)

    async def _send_match_state(self) -> None:
        """
        ゲーム状態を指定したFPSで定期的に送信する。

        ゲームが終了するまで繰り返し実行される。
        """
        last_update = asyncio.get_event_loop().time()
        while self.stage != match_enums.Stage.END:
            await asyncio.sleep(self.FPS)
            current_time = asyncio.get_event_loop().time()
            delta = current_time - last_update
            if delta >= self.FPS:
                self._update_match_state()
                if self.stage == match_enums.Stage.END:
                    break
                game_state = self._build_message(
                    {
                        "paddle1": {"x": self.paddle1.x, "y": self.paddle1.y},
                        "paddle2": {"x": self.paddle2.x, "y": self.paddle2.y},
                        "ball": {"x": self.ball.x, "y": self.ball.y},
                        "score1": self.score1,
                        "score2": self.score2,
                    },
                )
                await self._send_to_group(game_state)
                last_update = current_time
            else:
                await asyncio.sleep(self.FPS - delta)

        # ENDステージの処理
        await self._end_process()

    # ======================
    # グループ関係のメソッド
    # ======================
    async def _add_to_group(self) -> None:
        """
        Consumerをグループに追加。

        チャネル名を指定したグループに登録する。
        """
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def _remove_from_group(self) -> None:
        """
        Consuerをグループから削除。

        チャネル名を指定したグループから退出させる。
        """
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def _send_to_group(self, message: dict) -> None:
        """
        グループにメッセージを送信。

        :param message: 送信するメッセージ
        """
        await self.channel_layer.group_send(
            self.group_name, {"type": "group.message", "message": message}
        )

    # ==================
    # ヘルパーメソッド
    # ==================
    def _reset_state(self) -> None:
        """
        ゲームの状態をリセット。
        オブジェクトの座標が指す位置はすべて左上とする

        ゲームのステージ、スコア、パドルの位置、ボールの位置を初期状態に戻す。
        """
        self.stage = None
        self.paddle1 = PosStruct(
            x=self.PADDLE_POS_FROM_GOAL,
            y=int(self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2),
        )
        self.paddle2 = PosStruct(
            x=self.WIDTH - self.PADDLE_WIDTH - self.PADDLE_POS_FROM_GOAL,
            y=int(self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2),
        )
        self._reset_ball()
        self.score1 = 0
        self.score2 = 0
        self.local_play = False
        self.group_name = ""

    def _reset_ball(self) -> None:
        """
        ボールの位置と速度をリセット。

        ボールを中央に配置し、速度を設定する。
        """
        self.ball: PosStruct = PosStruct(
            x=int(self.WIDTH / 2 - self.BALL_SIZE / 2),
            y=int(self.HEIGHT / 2 - self.BALL_SIZE / 2),
        )
        self.ball_speed: PosStruct = PosStruct(
            x=self.BALL_SPEED, y=self.BALL_SPEED
        )

    async def cleanup(self) -> None:
        """
        ゲーム終了後のクリーンナップ処理
        グループから削除し、状態を初期化する
        """
        if self.group_name:
            await self._remove_from_group()
        self._reset_state()

    def _build_message(self, data: dict) -> dict:
        """
        プレーヤーに送るメッセージを作成。

        :param data: ステージに関連するデータ
        :return: 作成したメッセージ
        """
        return {
            ws_constants.Category.key(): ws_constants.Category.MATCH.value,
            ws_constants.PAYLOAD_KEY: {
                match_enums.Stage.key(): self.stage.value
                if self.stage is not None
                else "",
                ws_constants.DATA_KEY: data,
            },
        }
