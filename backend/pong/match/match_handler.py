import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Any, Final


class Stage(Enum):
    INIT = 1
    READY = 2
    PLAY = 3
    END = 4


@dataclass
class PosStruct:
    x: int
    y: int


# TODO: docstring追加
class MatchHandler:
    """
    Pongゲームのマッチロジックおよび通信を処理するクラス。
    原点（0, 0）は左上
    """

    """
    クラス定数
    """
    HEIGHT: Final[int] = 400
    WIDTH: Final[int] = 600
    PLAYER_HEIGHT: Final[int] = 60
    PLAYER_WIDTH: Final[int] = 10
    PLAYER_SPEED: Final[int] = 5
    BALL_RADIUS: Final[int] = 10

    """
    クラス属性
    """
    stage: Stage
    player1: PosStruct
    player2: PosStruct
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
            f"player1={self.player1}, player2={self.player2}, "
            f"ball={self.ball}, score1={self.score1}, score2={self.score2})"
        )

    def __repr__(self) -> str:
        """
        MatchHandlerオブジェクトを詳細に表現。

        :return: MatchHandlerオブジェクトの詳細な文字列表現
        """
        return (
            f"MatchHandler(stage={self.stage}, "
            f"player1={self.player1}, player2={self.player2}, "
            f"ball={self.ball}, ball_speed={self.ball_speed}, "
            f"score1={self.score1}, score2={self.score2}, "
            f"local_play={self.local_play}, group_name={self.group_name}, "
            f"channel_layer={self.channel_layer}, channel_name={self.channel_name})"
        )

    """
    ハンドラーメソッド
    """

    async def handle(self, payload: dict) -> None:
        """
        プレイヤーからの入力を受け取り、ステージごとに処理を振り分ける。

        :param payload: プレイヤーからのデータを含むペイロード
        """
        data: dict = payload["data"]

        # TODO: ステージごとのバリデーションも実装する必要あり
        match payload["stage"]:
            case "INIT":
                await self._handle_init(data)
                self.stage = Stage.READY
            case "READY":
                await self._handle_ready(data)
                self.stage = Stage.PLAY
            case "PLAY":
                await self._handle_play(player_move=data)
            case "END":
                # TODO: エラー処理
                # これが送られてくるのは途中でプレーヤーが画面遷移した場合
                pass
            case _:
                # TODO: エラー処理
                pass

    async def _handle_init(self, data: dict) -> None:
        """
        ゲームの初期化処理。

        :param data: 初期化に必要なデータ
        """
        # プレイモードによって所属させるグループを返る
        if data["mode"] == "local":
            self.group_name = "solo_match"

        await self._add_to_group()
        # TODO: remoteの場合のグループ作成方法は別で考える

        # localモードの場合teamやdisplay_nameは必要ない
        # TODO: ここら辺べた書きになっているから何か他にいい方法がないか
        message = self._build_message(
            "INIT",
            {
                "team": "",
                "display_name1": "",
                "display_name2": "",
                "pedal1": {"x": self.player1.x, "y": self.player1.y},
                "pedal2": {"x": self.player2.x, "y": self.player2.y},
                "ball": {"x": self.ball.x, "y": self.ball.y},
            },
        )
        await self._send_to_group(message)

    async def _handle_ready(self, data: dict) -> None:
        """
        ゲームの準備が整った状態で処理を行う。

        :param data: 準備状態に必要なデータ
        """
        message = self._build_message("READY", {})
        await self._send_to_group(message)

        # ゲーム状況の更新をする非同期処理を並列で実行する
        if self.stage == Stage.READY:
            asyncio.create_task(self._send_match_state())

    async def _handle_play(self, player_move: dict) -> None:
        """
        プレイヤーの動きに基づいてゲーム状態を更新。

        :param player_move: プレイヤーの移動情報
        """
        self._move_pedal(player_move)

    async def _handle_end(self) -> None:
        """
        ゲーム終了時の処理。

        勝者を決定し、グループから退出し、ゲーム状態を初期化。
        """
        win_player: str = "1" if self.score1 > self.score2 else "2"
        message = self._build_message(
            "END",
            {"win": win_player, "score1": self.score1, "score2": self.score2},
        )
        await self._send_to_group(message)
        # matchが終わったのでグループから削除
        await self._remove_from_group()
        # 初期化
        self._reset_state()

    """
    ゲームロジック関係のメソッド
    """

    def _move_pedal(self, player_move: dict) -> None:
        """
        プレイヤーのパドルを移動させる。

        :param player_move: プレイヤーの移動情報
        """
        match player_move["move"]:
            case "UP":
                if player_move["team"] == "1" and self.player1.y > 0:
                    self.player1.y -= self.PLAYER_SPEED
                elif player_move["team"] == "2" and self.player2.y > 0:
                    self.player2.y -= self.PLAYER_SPEED

            case "DOWN":
                if (
                    player_move["team"] == "1"
                    and self.player1.y + self.PLAYER_HEIGHT < self.HEIGHT
                ):
                    self.player1.y += self.PLAYER_SPEED
                elif (
                    player_move["team"] == "2"
                    and self.player2.y + self.PLAYER_HEIGHT < self.HEIGHT
                ):
                    self.player2.y += self.PLAYER_SPEED

    def _update(self) -> None:
        """
        ゲーム状態の更新
        """
        # ボールの移動
        self.ball.x += self.ball_speed.x
        self.ball.y += self.ball_speed.y

        # 上下の壁との衝突判定
        if self.ball.y - self.BALL_RADIUS <= 0:
            self.ball_speed.y = abs(self.ball_speed.y)
        elif self.ball.y + self.BALL_RADIUS >= self.HEIGHT:
            self.ball_speed.y = -abs(self.ball_speed.y)

        # パドルとの衝突判定
        self._process_ball_paddle_collision(self.player1, True)
        self._process_ball_paddle_collision(self.player2, False)

        # 得点判定
        if self.ball.x + self.BALL_RADIUS <= 0:
            self.score2 += 1
            self._reset_ball()
        elif self.ball.x - self.BALL_RADIUS >= self.WIDTH:
            self.score1 += 1
            self._reset_ball()

        # 勝利判定
        if self.score1 >= 5 or self.score2 >= 5:
            self.stage = Stage.END

    def _process_ball_paddle_collision(
        self, player_pos: PosStruct, is_player1: bool
    ) -> None:
        """
        ボールとパドルの衝突判定と衝突時の処理

        Args:
            player_pos (PosStruct): プレーヤーの位置
            is_player1 (bool): プレイヤー1のパドルかどうか
        """
        # 衝突判定
        if (
            self.ball.x - self.BALL_RADIUS <= player_pos.x + self.PLAYER_WIDTH
            and self.ball.x + self.BALL_RADIUS >= player_pos.x
            and self.ball.y - self.BALL_RADIUS
            <= player_pos.y + self.PLAYER_HEIGHT
            and self.ball.y + self.BALL_RADIUS >= player_pos.y
        ):
            # ボールのx座標がパドルの側面に当たった場合
            # ボールの中心がパドルの端よりも自陣側に過ぎていたらx軸方向に跳ね返さない
            if (
                self.ball.y >= player_pos.y
                and self.ball.y <= player_pos.y + self.PLAYER_HEIGHT
            ):
                if (
                    is_player1
                    and self.ball.x > player_pos.x + self.PLAYER_WIDTH
                ):
                    self.ball_speed.x = abs(self.ball_speed.x)
                elif self.ball.x < player_pos.x:
                    self.ball_speed.x = -abs(self.ball_speed.x)

            # ボールのy座標がパドルの上下面に当たった場合
            if (
                self.ball.x >= player_pos.x
                and self.ball.x <= player_pos.x + self.PLAYER_WIDTH
            ):
                if self.ball.y <= player_pos.y:
                    self.ball_speed.y = -abs(self.ball_speed.y)
                elif self.ball.y >= player_pos.y + self.PLAYER_HEIGHT:
                    self.ball_speed.y = abs(self.ball_speed.y)

    async def _send_match_state(self) -> None:
        """
        ゲーム状態を60FPSで定期的に送信する。

        ゲームが終了するまで繰り返し実行される。
        """
        while self.stage != Stage.END:
            await asyncio.sleep(1 / 60)
            self._update()

            game_state = self._build_message(
                "PLAY",
                {
                    "pedal1": {"x": self.player1.x, "y": self.player1.y},
                    "pedal2": {"x": self.player2.x, "y": self.player2.y},
                    "ball": {"x": self.ball.x, "y": self.ball.y},
                    "score1": self.score1,
                    "score2": self.score2,
                },
            )
            await self._send_to_group(game_state)

        # ENDステージの処理
        await self._handle_end()

    """
    グループ関係のメソッド
    """

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

    """
    ヘルパーメソッド
    """

    def _reset_state(self) -> None:
        """
        ゲームの状態をリセット。

        ゲームのステージ、スコア、プレイヤーの位置、ボールの位置を初期状態に戻す。
        """
        self.stage = Stage.INIT
        # playerの位置は描画する左上を(0, 0)とする
        self.player1 = PosStruct(x=10, y=170)
        self.player2 = PosStruct(x=580, y=170)
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
            x=int(self.WIDTH / 2), y=int(self.HEIGHT / 2)
        )
        self.ball_speed: PosStruct = PosStruct(x=2, y=2)

    def _build_message(self, stage: str, data: dict) -> dict:
        """
        メッセージを作成。

        :param stage: ステージ名
        :param data: ステージに関連するデータ
        :return: 作成したメッセージ
        """
        return {"category": "MATCH", "payload": {"stage": stage, "data": data}}
