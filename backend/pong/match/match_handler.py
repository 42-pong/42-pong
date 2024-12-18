import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Any


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
    Handles the match logic and communication for a pong game.
    """

    """
    クラス定数
    """
    HEIGHT = 400
    WIDTH = 600
    PLAYER_HEIGHT = 60
    PLAYER_WIDTH = 10
    PLAYER_SPEED = 5
    BALL_RADIUS = 10

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
        self.channel_layer = channel_layer
        self.channel_name = channel_name
        self._reset_state()

    """
    ハンドラーメソッド
    """

    async def handle(self, payload: dict) -> None:
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
        message = self._build_message("READY", {})
        await self._send_to_group(message)

        # ゲーム状況の更新をする非同期処理を並列で実行する
        asyncio.create_task(self.send_match_state())

    async def _handle_play(self, player_move: dict) -> None:
        await self._move_pedal(player_move)

    async def _handle_end(self) -> None:
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

    async def _move_pedal(self, player_move: dict) -> None:
        # プレイヤーの動き（y座標）に基づいて位置を更新
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

    def _move_ball(self) -> None:
        # ボールの位置を更新
        self.ball.x += self.ball_speed.x
        self.ball.y += self.ball_speed.y

        # 上下の壁との衝突判定
        if (
            self.ball.y - self.BALL_RADIUS < 0
            or self.ball.y + self.BALL_RADIUS > self.HEIGHT
        ):
            self.ball_speed.y = -self.ball_speed.y  # ボールのY軸速度を反転

        # プレイヤーとの衝突判定
        if (
            self.ball.x - self.BALL_RADIUS < self.player1.x + self.PLAYER_WIDTH
            and self.player1.y
            < self.ball.y
            < self.player1.y + self.PLAYER_HEIGHT
        ):  # プレイヤー1との接触
            self.ball_speed.x = -self.ball_speed.x  # ボールのX軸速度を反転
        elif (
            self.player2.x < self.ball.x + self.BALL_RADIUS
            and self.player2.y
            < self.ball.y
            < self.player2.y + self.PLAYER_HEIGHT
        ):  # プレイヤー2との接触
            self.ball_speed.x = -self.ball_speed.x  # ボールのX軸速度を反転

        # 点数判定
        if self.ball.x < self.player1.x:
            self.score2 += 1
            self._reset_ball()
        elif self.player2.x + self.PLAYER_WIDTH < self.ball.x:
            self.score1 += 1
            self._reset_ball()

        if self.score1 == 5 or self.score2 == 5:
            self.stage = Stage.END

    async def send_match_state(self) -> None:
        """60FPSでゲームデータを定期的に送信"""
        while self.stage != Stage.END:
            await asyncio.sleep(1 / 60)  # 60FPSで待機
            self._move_ball()

            # 現在のゲーム状態を送信
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
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def _remove_from_group(self) -> None:
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def _send_to_group(self, message: dict) -> None:
        await self.channel_layer.group_send(
            self.group_name, {"type": "group.message", "message": message}
        )

    """
    ヘルパーメソッド
    """

    def _reset_state(self) -> None:
        # 初期化
        self.stage = Stage.INIT
        # playerの位置は描画する左下を(0, 0)とする
        self.player1 = PosStruct(x=10, y=230)
        self.player2 = PosStruct(x=580, y=230)
        self._reset_ball()
        self.score1 = 0
        self.score2 = 0
        self.local_play = False
        self.group_name = ""

    def _reset_ball(self) -> None:
        self.ball: PosStruct = PosStruct(
            x=int(self.WIDTH / 2), y=int(self.HEIGHT / 2)
        )
        self.ball_speed: PosStruct = PosStruct(x=2, y=2)

    def _build_message(self, stage: str, data: dict) -> dict:
        return {"category": "MATCH", "payload": {"stage": stage, "data": data}}
