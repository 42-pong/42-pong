import asyncio
from dataclasses import dataclass
from typing import Any, Final

from . import match_enums, ws_constants


@dataclass
class PosStruct:
    x: int
    y: int


class MatchHandler:
    """
    Pongゲームのマッチロジックおよび通信を処理するクラス。
    原点（0, 0）は左上
    """

    # クラス定数
    HEIGHT: Final[int] = 400
    WIDTH: Final[int] = 600
    PADDLE_HEIGHT: Final[int] = 60
    PADDLE_WIDTH: Final[int] = 10
    PADDLE_SPEED: Final[int] = 5
    BALL_SIZE: Final[int] = 10
    BALL_SPEED: Final[int] = 2

    # クラス属性
    stage: match_enums.Stage
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

    # ハンドラーメソッド
    async def handle(self, payload: dict) -> None:
        """
        プレイヤーからの入力を受け取り、ステージごとに処理を振り分ける。

        :param payload: プレイヤーからのデータを含むペイロード
        """
        data: dict = payload.get(ws_constants.DATA_KEY, {})
        stage: str = payload.get(match_enums.Stage.key(), "")
        handler = self.stage_handlers.get(stage)

        # TODO: ステージごとのバリデーションも実装する必要あり
        # TODO: 適切なエラーハンドリングを実装
        if callable(handler):
            await handler(data)

    async def _handle_init(self, data: dict) -> None:
        """
        ゲームの初期化処理。

        :param data: 初期化に必要なデータ
        """
        self.stage = match_enums.Stage.INIT
        # プレイモードによって所属させるグループを返る
        if data.get(match_enums.Mode.key()) == match_enums.Mode.LOCAL.value:
            self.group_name = "solo_match"

        await self._add_to_group()
        # TODO: remoteの場合のグループ作成方法は別で考える

        # localモードの場合teamやdisplay_nameは必要ない
        # TODO: ここら辺べた書きになっているから何か他にいい方法がないか
        message = self._build_message(
            match_enums.Stage.INIT,
            {
                match_enums.Team.key(): match_enums.Team.Empty.value,
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
        ゲームの準備が整った状態で処理を行う。

        :param data: 準備状態に必要なデータ
        """
        self.stage = match_enums.Stage.READY
        message = self._build_message(match_enums.Stage.READY, {})
        await self._send_to_group(message)

        # ゲーム状況の更新をする非同期処理を並列で実行する
        if self.stage == match_enums.Stage.READY:
            asyncio.create_task(self._send_match_state())
            self.stage = match_enums.Stage.PLAY

    async def _handle_play(self, data: dict) -> None:
        """
        プレイヤーの動きに基づいてゲーム状態を更新。

        :param data: プレイヤーの移動情報
        """
        self._move_paddle(paddle_move=data)

    async def _handle_end(self) -> None:
        """
        プレーヤーがmatchを退出したときの処理を行う。
        """
        await self._remove_from_group()
        self._reset_state()  # 初期化

    async def _end_process(self) -> None:
        """
        ゲーム終了時の処理。

        勝者を決定し、グループから退出し、ゲーム状態を初期化。
        """
        win_team: str = (
            match_enums.Team.One.value
            if self.score1 > self.score2
            else match_enums.Team.Two.value
        )
        message = self._build_message(
            match_enums.Stage.END,
            {"win": win_team, "score1": self.score1, "score2": self.score2},
        )
        await self._send_to_group(message)
        # matchが終わったのでグループから削除
        await self._remove_from_group()
        # 初期化
        self._reset_state()

    # ゲームロジック関係のメソッド
    def _move_paddle(self, paddle_move: dict) -> None:
        """
        プレイヤーのパドルを移動させる。

        :param paddle_move: プレイヤーの移動情報
        """
        match paddle_move.get(match_enums.Move.key()):
            case match_enums.Move.UP.value:
                if (
                    paddle_move.get(match_enums.Team.key())
                    == match_enums.Team.One.value
                    and self.paddle1.y > 0
                ):
                    self.paddle1.y -= self.PADDLE_SPEED
                elif (
                    paddle_move.get(match_enums.Team.key())
                    == match_enums.Team.Two.value
                    and self.paddle2.y > 0
                ):
                    self.paddle2.y -= self.PADDLE_SPEED

            case match_enums.Move.DOWN.value:
                if (
                    paddle_move.get(match_enums.Team.key())
                    == match_enums.Team.One.value
                    and self.paddle1.y + self.PADDLE_HEIGHT < self.HEIGHT
                ):
                    self.paddle1.y += self.PADDLE_SPEED
                elif (
                    paddle_move.get(match_enums.Team.key())
                    == match_enums.Team.Two.value
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
        if self.score1 >= 5 or self.score2 >= 5:
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
        ゲーム状態を60FPSで定期的に送信する。

        ゲームが終了するまで繰り返し実行される。
        """
        last_update = asyncio.get_event_loop().time()
        while self.stage != match_enums.Stage.END:
            await asyncio.sleep(1 / 60)
            current_time = asyncio.get_event_loop().time()
            delta = current_time - last_update
            if delta >= 1 / 60:
                self._update_match_state()
                game_state = self._build_message(
                    match_enums.Stage.PLAY,
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
                await asyncio.sleep(1 / 60 - delta)

        # ENDステージの処理
        await self._end_process()

    # グループ関係のメソッド
    async def _add_to_group(self) -> None:
        """
        マッチをグループに追加。

        チャネル名を指定したグループに参加させる。
        """
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def _remove_from_group(self) -> None:
        """
        マッチをグループから削除。

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

    # ヘルパーメソッド
    def _reset_state(self) -> None:
        """
        ゲームの状態をリセット。

        ゲームのステージ、スコア、プレイヤーの位置、ボールの位置を初期状態に戻す。
        """
        self.stage = match_enums.Stage.NONE
        # paddleの位置は左上とする
        self.paddle1 = PosStruct(
            x=10, y=int(self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2)
        )
        self.paddle2 = PosStruct(
            x=self.WIDTH - self.PADDLE_WIDTH - 10,
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

    def _build_message(self, stage: match_enums.Stage, data: dict) -> dict:
        """
        メッセージを作成。

        :param stage: ステージ名
        :param data: ステージに関連するデータ
        :return: 作成したメッセージ
        """
        return {
            ws_constants.Category.key(): ws_constants.Category.MATCH.value,
            ws_constants.PAYLOAD_KEY: {
                match_enums.Stage.key(): stage.value,
                ws_constants.DATA_KEY: data,
            },
        }
