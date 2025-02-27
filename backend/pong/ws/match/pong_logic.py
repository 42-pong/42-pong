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
        pass

    async def check_collisions(self) -> None:
        """
        ボールとパドルの接触判定
        接触していれば、ボールの進行方向を返る。
        """
        pass

    async def check_score(self) -> Optional[str]:
        """
        ボールが得点ラインを超えたか判定
        超えていれば

        Return:
            Optional[str]: "1" | "2" | None 得点したチーム名
        """
        pass

    async def move_paddle_up(self, team: str) -> None:
        """
        引数で受け取ったチームのパドルを上に動かす関数
        """
        pass

    async def move_paddle_down(self, team: str) -> None:
        """
        引数で受け取ったチームのパドルを下に動かす関数
        """
        pass

    async def reset_ball(self) -> None:
        """
        ボールを開始位置に動かす関数
        """
        pass

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
