from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional

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

    def __init__(self):
        self._reset_state()

    """
    ハンドラーメソッド
    """
    async def handle(self, payload: dict):
        data: dict = payload["data"]
        response: dict

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

    async def _handle_init(self, data: dict):
        pass

    async def _handle_ready(self, data: dict):
        pass

    async def _handle_play(self, player_move: dict):
        pass

    async def _handle_end(self, data: dict):
        pass

    """
    ゲームロジック関係のメソッド
    """

    async def _move_pedal(self, player_move: dict):
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

    def _move_ball(self):
        # ボールの位置を更新
        self.ball.x += self.ball_speed.x
        self.ball.y += self.ball_speed.y

        # 上下の壁との衝突判定
        if self.ball.y - self.BALL_RADIUS < 0 or self.ball.y + self.BALL_RADIUS > self.HEIGHT:
            self.ball_speed.y = -self.ball_speed.y  # ボールのY軸速度を反転

        # プレイヤーとの衝突判定
        if (
            self.ball.x - self.BALL_RADIUS < self.player1.x + self.PLAYER_WIDTH
            and self.player1.y < self.ball.y < self.player1.y + self.PLAYER_HEIGHT
        ):  # プレイヤー1との接触
            self.ball_speed.x = -self.ball_speed.x  # ボールのX軸速度を反転
        elif (
            self.player2.x < self.ball.x + self.BALL_RADIUS
            and self.player2.y < self.ball.y < self.player2.y + self.PLAYER_HEIGHT
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

    """
    ヘルパーメソッド
    """

    def _reset_state(self):
        # 初期化
        self.stage = Stage.INIT
        # playerの位置は描画する左下を(0, 0)とする
        self.player1 = PosStruct(x=10, y=230)
        self.player2 = PosStruct(x=580, y=230)
        self._reset_ball()
        self.score1 = 0
        self.score2 = 0

    def _reset_ball(self):
        self.ball: PosStruct = PosStruct(x=self.WIDTH / 2, y=self.HEIGHT / 2)
        self.ball_speed: PosStruct = PosStruct(x=2, y=2)
