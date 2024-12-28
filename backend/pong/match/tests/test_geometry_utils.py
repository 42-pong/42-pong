import unittest

import numpy as np

from ..geometry_utils import (
    check_opposite_sides,
    cross2d,
    is_internally_devided,
    is_on_the_line,
)


class TestGeometryUtils(unittest.TestCase):
    """
    geometry_utilsモジュールの関数をテストするクラス。

    各テストケースは、2次元ベクトル計算における幾何学的な条件を確認するために設計されています。
    """

    def test_cross2d_positive(self) -> None:
        """
        正の外積を計算するテスト。
        """
        vec1 = np.array([1, 0])
        vec2 = np.array([0, 1])
        result = cross2d(vec1, vec2)
        self.assertEqual(result, 1)

    def test_cross2d_negative(self) -> None:
        """
        負の外積を計算するテスト。
        """
        vec1 = np.array([0, 1])
        vec2 = np.array([1, 0])
        result = cross2d(vec1, vec2)
        self.assertEqual(result, -1)

    def test_cross2d_zero(self) -> None:
        """
        外積が0になる場合のテスト。
        """
        vec1 = np.array([1, 1])
        vec2 = np.array([2, 2])
        result = cross2d(vec1, vec2)
        self.assertEqual(result, 0)

    def test_cross2d_same(self) -> None:
        """
        同じベクトルの場合のテスト。
        """
        vec1 = np.array([1, 1])
        vec2 = np.array([1, 1])
        self.assertEqual(cross2d(vec1, vec2), 0)  # 外積が0

    def test_cross2d_zero_vetor(self) -> None:
        """
        片方がゼロベクトルの場合のテスト
        外積が0になる場合のテスト。
        """
        vec1 = np.array([0, 0])
        vec2 = np.array([1, 1])
        self.assertEqual(cross2d(vec1, vec2), 0)  # 外積が0

    def test_check_opposite_sides_true(self) -> None:
        """
        点が線分の両側に存在する場合のテスト。
        両側に存在するため、結果がTrueであることを確認します。
        """
        segment_vec = np.array([1, 0])
        point_vec1 = np.array([0, 1])
        point_vec2 = np.array([0, -1])
        result = check_opposite_sides(segment_vec, point_vec1, point_vec2)
        self.assertTrue(result)

    def test_check_opposite_sides_false(self) -> None:
        """
        点が線分の両側に存在しない場合のテスト。
        両側に存在しないため、結果がFalseであることを確認します。
        """
        segment_vec = np.array([1, 0])
        point_vec1 = np.array([0, 1])
        point_vec2 = np.array([0, 1])
        result = check_opposite_sides(segment_vec, point_vec1, point_vec2)
        self.assertFalse(result)

    def test_check_opposite_sides_point_on_segment(self) -> None:
        """
        片方の点が線分上にある場合のテスト。
        点が線分上にあるため、結果がFalseであることを確認します。
        """
        segment_vec = np.array([1, 0])
        point_vec1 = np.array([0, 0])
        point_vec2 = np.array([0, -1])
        result = check_opposite_sides(segment_vec, point_vec1, point_vec2)
        self.assertFalse(result)

    def test_check_opposite_sides_both_points_on_segment(self) -> None:
        """
        両方の点が線分上にある場合のテスト。
        両方の点が線分上にあるため、結果がFalseであることを確認します。
        """
        segment_vec = np.array([1, 0])
        point_vec1 = np.array([0, 0])
        point_vec2 = np.array([1, 0])
        result = check_opposite_sides(segment_vec, point_vec1, point_vec2)
        self.assertFalse(result)

    def test_is_internally_devided_true(self) -> None:
        """
        点が線分を内分する場合のテスト。
        点pが線分v1-v2上にあるため、結果がTrueであることを確認します。
        """
        v1 = np.array([0, 0])
        v2 = np.array([2, 2])
        p = np.array([1, 1])
        result = is_internally_devided(v1, v2, p)
        self.assertTrue(result)

    def test_is_internally_devided_false(self) -> None:
        """
        点が線分を内分しない場合のテスト。
        点pが線分v1-v2上にないため、結果がFalseであることを確認します。
        """
        v1 = np.array([0, 0])
        v2 = np.array([2, 2])
        p = np.array([1, 3])
        result = is_internally_devided(v1, v2, p)
        self.assertFalse(result)

    def test_is_internally_devided_collinear_but_not_on_segment(self) -> None:
        """
        点が同じ直線上にはあるが線分上にはない場合のテスト。
        点pが直線上にあるが線分v1-v2上にないため、結果がFalseであることを確認します。
        """
        v1 = np.array([0, 0])
        v2 = np.array([2, 2])
        p = np.array([3, 3])
        result = is_internally_devided(v1, v2, p)
        self.assertFalse(result)

    def test_is_on_the_line_true(self) -> None:
        """
        点が無限直線上にある場合のテスト。
        点pが直線v1-v2上にあるため、結果がTrueであることを確認します。
        """
        v1 = np.array([0, 0])
        v2 = np.array([2, 2])
        p = np.array([4, 4])
        result = is_on_the_line(v1, v2, p)
        self.assertTrue(result)

    def test_is_on_the_line_false(self) -> None:
        """
        点が無限直線上にない場合のテスト。
        点pが直線v1-v2上にないため、結果がFalseであることを確認します。
        """
        v1 = np.array([0, 0])
        v2 = np.array([2, 2])
        p = np.array([1, 2])
        result = is_on_the_line(v1, v2, p)
        self.assertFalse(result)
