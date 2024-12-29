import numpy as np


def cross2d(vec1: np.ndarray, vec2: np.ndarray) -> int:
    """
    2次元ベクトルの外積を計算します。

    Parameters:
        vec1: 最初の2次元ベクトル。
        vec2: 2番目の2次元ベクトル。

    Return:
        vec1とvec2の外積。
    """
    return vec1[0] * vec2[1] - vec1[1] * vec2[0]


def check_opposite_sides(
    segment_vec: np.ndarray, point_vec1: np.ndarray, point_vec2: np.ndarray
) -> bool:
    """
    2つの点がある線分の両側に存在するかどうかを判定する関数

    Parameters:
        segment_vec: 線分を表す2次元ベクトル。
        point_vec1: 点を表す2次元ベクトル。
        point_vec2: 点を表す2次元ベクトル。

    Return:
        両側に存在すればTrueを返す。
    """
    return (
        cross2d(segment_vec, point_vec1) * cross2d(segment_vec, point_vec2)
    ) < 0


def is_internally_divided(
    v1: np.ndarray, v2: np.ndarray, p: np.ndarray
) -> bool:
    """
    点pが線分v1-v2を内分した点であるかどうかを判定する関数

    Parameters:
        v1: 線分の始点 (x, y)
        v2: 線分の終点 (x, y)
        p: 判定する点 (x, y)

    Return:
        点pが線分v1-v2上にある場合True、それ以外はFalse
    """
    # ベクトルv1 -> p と v2 -> p を計算
    v1_p = p - v1
    v1_v2 = v2 - v1
    # 線分v1 -> v2 上で内分点・外分点を判定
    cross_product = cross2d(v1_p, v1_v2)  # 外積 (z成分のみ)

    # 外積が0なら2つの線分は並行にあることがわかる
    if not cross_product == 0:
        return False

    # 点pが線分v1-v2上にあるかを確認するために以下を調べる
    # 0 <= v1_pとv1_v2の内積 <= v1_v2の2乗
    dot_product1 = np.dot(v1_p, v1_v2)
    dot_product2 = np.dot(v1_v2, v1_v2)
    if (0 <= dot_product1) and (dot_product1 <= dot_product2):
        return True

    return False


def is_on_the_line(v1: np.ndarray, v2: np.ndarray, p: np.ndarray) -> bool:
    """
    点pが無限に伸びる直線v1-v2上にあるかどうかを判定する関数

    Parameters:
        v1: 直線の始点 (x, y)
        v2: 直線の終点 (x, y)
        p: 判定する点 (x, y)

    Return:
        点pが直線v1-v2上にある場合True、それ以外はFalse
    """
    # ベクトルv1 -> p と v2 -> p を計算
    v1_p = p - v1
    v1_v2 = v2 - v1
    # 線分v1 -> v2 上で内分点・外分点を判定
    cross_product = cross2d(v1_p, v1_v2)  # 外積 (z成分のみ)

    # 外積が0なら2つの線分は並行にあることがわかる
    if not cross_product == 0:
        return False

    return True
