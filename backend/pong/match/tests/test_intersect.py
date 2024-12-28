import unittest

import numpy as np

from ..match_handler import MatchHandler


class IntersectTest(unittest.TestCase):
    """
    Pongゲームでボールとパドルや壁の接触を判定する以下のMatchHandlerクラスのstatic関数のテスト
    - MatchHandler.intersect_ball_and_paddle()
    - MatchHandler.intersect_ball_and_wall()

    Attributes:
        ball_before: ボールの移動前の位置
        ball_after: ボールの移動後の位置
        paddle1: パドルの片端の位置
        paddle2: パドルのもう片端の位置
        wall1: 壁の片端の位置
        wall2: 壁のもう片端の位置
    """

    def setUp(self) -> None:
        """
        クラス変数の初期化
        """
        self.paddle1 = np.array([2, 4])
        self.paddle2 = np.array([2, 0])
        self.wall1 = np.array([2, 2])
        self.wall2 = np.array([4, 2])

    def test_intersect_ball_and_paddle(self) -> None:
        """
        ボールの軌道とパドルが交差
        = 線分が交差
        """
        ball_before: np.ndarray = np.array([0, 0])
        ball_after: np.ndarray = np.array([4, 4])

        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle1, self.paddle2
            )
        )
        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle1, self.paddle2
            )
        )
        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle2, self.paddle1
            )
        )
        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle2, self.paddle1
            )
        )

    def test_not_intersect_ball_and_paddle(self) -> None:
        """
        ボールの軌道とパドルが交差しない
        = 線分が交差しない
        """
        ball_before: np.ndarray = np.array([3, 4])
        ball_after: np.ndarray = np.array([6, 5])

        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle1, self.paddle2
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle1, self.paddle2
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle2, self.paddle1
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle2, self.paddle1
            )
        )

    def test_intersect_ball_and_paddle_at_the_both_endpoints(self) -> None:
        """
        ボールの端とパドルの端同士が接触するケース
        = 線分同士の端点でちょうど接触するケース
        * ボールの移動前の位置が接触している場合はFalseを返す
        """
        ball_before: np.ndarray = np.array([0, 2])
        ball_after: np.ndarray = np.array([2, 4])

        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle1, self.paddle2
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle1, self.paddle2
            )
        )
        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle2, self.paddle1
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle2, self.paddle1
            )
        )

    def test_intersect_paddle_edge_on_ball(self) -> None:
        """
        ボールの軌道がパドルの端に接触するケース
        = 片方の線の端点がもう片方の線上に接触するケース
        """
        ball_before: np.ndarray = np.array([0, 2])
        ball_after: np.ndarray = np.array([4, 6])

        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle1, self.paddle2
            )
        )
        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle1, self.paddle2
            )
        )
        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle2, self.paddle1
            )
        )
        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle2, self.paddle1
            )
        )

    def test_intersect_ball_edge_on_paddle(self) -> None:
        """
        ボールの軌道の端点がパドルに接触するケース
        = 片方の線上でちょうど接触するケース
        * ボールの移動前の位置が接触している場合はFalseを返す
        """
        ball_before: np.ndarray = np.array([4, 0])
        ball_after: np.ndarray = np.array([2, 3])

        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle1, self.paddle2
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle1, self.paddle2
            )
        )
        self.assertTrue(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle2, self.paddle1
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle2, self.paddle1
            )
        )

    def test_intersect_ball_and_extended_wall(self) -> None:
        """
        直線v3-v4と線分v1-v2が交差するケース
        実際のPongゲームでは上下の壁を無限に伸びた線分として扱える。
        """
        ball_before: np.ndarray = np.array([2, 0])
        ball_after: np.ndarray = np.array([7, 5])

        self.assertTrue(
            MatchHandler.intersect_ball_and_wall(
                ball_before, ball_after, self.wall1, self.wall2
            )
        )
        self.assertTrue(
            MatchHandler.intersect_ball_and_wall(
                ball_after, ball_before, self.wall1, self.wall2
            )
        )
        self.assertTrue(
            MatchHandler.intersect_ball_and_wall(
                ball_before, ball_after, self.wall2, self.wall1
            )
        )
        self.assertTrue(
            MatchHandler.intersect_ball_and_wall(
                ball_after, ball_before, self.wall2, self.wall1
            )
        )

    def test_not_intersect_ball_and_extended_wall(self) -> None:
        """
        直線v3-v4と線分v1-v2が交差しないケース
        実際のPongゲームでは上下の壁を無限に伸びた線分として扱える。
        """
        ball_before: np.ndarray = np.array([1, 4])
        ball_after: np.ndarray = np.array([3, 3])

        self.assertFalse(
            MatchHandler.intersect_ball_and_wall(
                ball_before, ball_after, self.wall1, self.wall2
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_wall(
                ball_after, ball_before, self.wall1, self.wall2
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_wall(
                ball_before, ball_after, self.wall2, self.wall1
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_wall(
                ball_after, ball_before, self.wall2, self.wall1
            )
        )

    def test_parallel_ball_and_paddle(self) -> None:
        """
        ボールとパドルが並行
        """
        ball_before: np.ndarray = np.array([1, 0])
        ball_after: np.ndarray = np.array([1, 4])

        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle1, self.paddle2
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle1, self.paddle2
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_before, ball_after, self.paddle2, self.paddle1
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_paddle(
                ball_after, ball_before, self.paddle2, self.paddle1
            )
        )

    def test_parallel_ball_and_wall(self) -> None:
        """
        ボールと壁が並行
        """
        ball_before: np.ndarray = np.array([2, 4])
        ball_after: np.ndarray = np.array([4, 4])

        self.assertFalse(
            MatchHandler.intersect_ball_and_wall(
                ball_before, ball_after, self.wall1, self.wall2
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_wall(
                ball_after, ball_before, self.wall1, self.wall2
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_wall(
                ball_before, ball_after, self.wall2, self.wall1
            )
        )
        self.assertFalse(
            MatchHandler.intersect_ball_and_wall(
                ball_after, ball_before, self.wall2, self.wall1
            )
        )
