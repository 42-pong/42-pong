from dataclasses import dataclass
from typing import Final, Optional

from . import constants


@dataclass
class PosStruct:
    x: int
    y: int


class PongLogic:
    """
    Pongゲームのロジックを担当するクラス。
    DB操作もメッセージのやり取りも行わない。

    matchの全体の更新はこのクラスを作成側で以下の関数を繰り返すことで行う。
        - self.update_game_status()
    また、プレーヤーパドルは以下の関数で更新する。
        - self.move_paddle_up()
        - self.move_paddle_down()
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

    def __init__(self) -> None:
        """
        ゲーム情報を初期化
        """
        self.paddle1_pos = PosStruct(
            x=self.PADDLE_POS_FROM_GOAL,
            y=self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2,
        )
        self.paddle2_pos = PosStruct(
            x=self.WIDTH - self.PADDLE_WIDTH - self.PADDLE_POS_FROM_GOAL,
            y=self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2,
        )
        self.ball_pos: PosStruct = PosStruct(
            x=self.WIDTH // 2 - self.BALL_SIZE // 2,
            y=self.HEIGHT // 2 - self.BALL_SIZE // 2,
        )
        self.ball_speed: PosStruct = PosStruct(
            x=self.BALL_SPEED, y=self.BALL_SPEED
        )
        self.score1 = 0
        self.score2 = 0

    def __str__(self) -> str:
        """
        PongLogicオブジェクトを文字列として表現。

        :return: PongLogicオブジェクトの文字列表現
        """
        return (
            f"PongLogic(paddle1_pos={self.paddle1_pos}, paddle2_pos={self.paddle2_pos}, "
            f"ball_pos={self.ball_pos}, score1={self.score1}, score2={self.score2})"
        )

    def __repr__(self) -> str:
        """
        PongLogicオブジェクトを詳細に表現。

        :return: PongLogicオブジェクトの詳細な文字列表現
        """
        return (
            f"PongLogic(paddle1_pos={self.paddle1_pos}, paddle2_pos={self.paddle2_pos}, "
            f"ball_pos={self.ball_pos}, ball_speed={self.ball_speed}, "
            f"score1={self.score1}, score2={self.score2})"
        )

    async def update_game_state(self) -> Optional[str]:
        """
        ゲームを1フレーム更新する関数。

        Returns:
            Optional[str]:
                "1" | "2": 得点した場合はそのチーム名を返す。
                None: 得点していなければNoneを返す。
        """
        await self.move_ball()
        await self.check_collisions()
        result: Optional[str] = await self.check_score()
        return result

    async def move_ball(self) -> None:
        """
        ボールの移動関数
        """
        x, y = self.ball_pos.x, self.ball_pos.y
        x += self.ball_speed.x
        y += self.ball_speed.y

        # 上下の壁に当たった場合に上下の進行方向を変える
        if y <= 0 or y >= self.HEIGHT - self.BALL_SIZE:
            self.ball_speed.y = -self.ball_speed.y

        self.ball_pos = PosStruct(x, y)

    async def check_collisions(self) -> None:
        """
        ボールとパドルの接触判定
        接触していれば、ボールの進行方向を変える。
        """
        # ボールの四隅の座標
        ball_left = self.ball_pos.x
        ball_right = self.ball_pos.x + self.BALL_SIZE
        ball_top = self.ball_pos.y
        ball_bottom = self.ball_pos.y + self.BALL_SIZE

        # パドル1（左側プレイヤー）との衝突判定
        paddle1_posleft = self.paddle1_pos.x
        paddle1_posright = self.paddle1_pos.x + self.PADDLE_WIDTH
        paddle1_postop = self.paddle1_pos.y
        paddle1_posbottom = self.paddle1_pos.y + self.PADDLE_HEIGHT

        if (
            paddle1_posleft
            <= ball_right
            <= paddle1_posright  # ボールの右側がパドルの左端に接触
            and paddle1_postop <= ball_bottom
            and ball_top <= paddle1_posbottom
        ):  # ボールの上下がパドルの範囲内
            self.ball_speed.x = -self.ball_speed.x

        # パドル2（右側プレイヤー）との衝突判定
        paddle2_posleft = self.paddle2_pos.x
        paddle2_posright = self.paddle2_pos.x + self.PADDLE_WIDTH
        paddle2_postop = self.paddle2_pos.y
        paddle2_posbottom = self.paddle2_pos.y + self.PADDLE_HEIGHT

        if (
            paddle2_posleft
            <= ball_left
            <= paddle2_posright  # ボールの左側がパドルの右端に接触
            and paddle2_postop <= ball_bottom
            and ball_top <= paddle2_posbottom
        ):  # ボールの上下がパドルの範囲内
            self.ball_speed.x = -self.ball_speed.x

    async def check_score(self) -> Optional[str]:
        """
        ボールが得点ラインを超えたか判定
        超えていれば

        Return:
            Optional[str]: "1" | "2" | None 得点したチーム名
        """
        x, _ = self.ball_pos.x, self.ball_pos.y
        if x + self.BALL_SIZE <= 0:
            self.score2 += 1
            await self.reset_ball()
            return constants.Team.TWO.value
        elif x >= self.WIDTH:
            self.score1 += 1
            await self.reset_ball()
            return constants.Team.ONE.value
        return None

    async def move_paddle_up(self, team: str) -> None:
        """
        引数で受け取ったチームのパドルを上に動かす関数
        """
        if team == constants.Team.ONE.value:
            y = self.paddle1_pos.y
            if y > 0:
                self.paddle1_pos = PosStruct(
                    self.paddle1_pos.x, y - self.PADDLE_SPEED
                )
        elif team == constants.Team.TWO.value:
            y = self.paddle2_pos.y
            if y > 0:
                self.paddle2_pos = PosStruct(
                    self.paddle2_pos.x, y - self.PADDLE_SPEED
                )

    async def move_paddle_down(self, team: str) -> None:
        """
        引数で受け取ったチームのパドルを下に動かす関数
        """
        if team == constants.Team.ONE.value:
            y = self.paddle1_pos.y
            if y < self.HEIGHT - self.PADDLE_HEIGHT:
                self.paddle1_pos = PosStruct(
                    self.paddle1_pos.x, y + self.PADDLE_SPEED
                )
        elif team == constants.Team.TWO.value:
            y = self.paddle2_pos.y
            if y < self.HEIGHT - self.PADDLE_HEIGHT:
                self.paddle2_pos = PosStruct(
                    self.paddle2_pos.x, y + self.PADDLE_SPEED
                )

    async def reset_ball(self) -> None:
        """
        ボールを開始位置に動かす関数
        """
        self.ball_pos = PosStruct(self.WIDTH // 2, self.HEIGHT // 2)
        # TODO: ボールの動き出す方向変えてもいいかも
        self.ball_speed.x = self.BALL_SPEED
        self.ball_speed.y = self.BALL_SPEED

    async def game_end(self) -> bool:
        """
        ゲームが終了したか判定する関数
        """
        return (
            self.score1 >= self.WINNING_SCORE
            or self.score2 >= self.WINNING_SCORE
        )

    async def get_winner(self) -> str:
        """
        ゲームの勝利チームを返す関数

        Returns:
            str: "1" | "2" 勝利したチーム名
        """
        if self.score1 > self.score2:
            return constants.Team.ONE.value
        return constants.Team.TWO.value
