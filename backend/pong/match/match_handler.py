import asyncio
from enum import Enum
from typing import Any, Final

import numpy as np

from . import geometry_utils


class Stage(Enum):
    NONE = 0
    INIT = 1
    READY = 2
    PLAY = 3
    END = 4


class MatchHandler:
    """
    Pongゲームのマッチロジックおよび通信を処理するクラス。
    原点（0, 0）は左上
    """

    # クラス定数
    HEIGHT: Final[int] = 400
    WIDTH: Final[int] = 600
    PLAYER_HEIGHT: Final[int] = 60
    PLAYER_WIDTH: Final[int] = 10
    PLAYER_SPEED: Final[int] = 5
    BALL_RADIUS: Final[int] = 10
    BALL_SPEED: Final[int] = 2

    def __init__(self, channel_layer: Any, channel_name: str):
        """
        MatchHandlerの初期化。

        :param channel_layer: チャネルレイヤー
        :param channel_name: チャネル名
        """
        self.stage_handlers = {
            "INIT": self._handle_init,
            "READY": self._handle_ready,
            "PLAY": self._handle_play,
            "END": self._handle_end,
        }
        self.channel_layer: Any = channel_layer
        self.channel_name: str = channel_name
        self.stage: Stage = Stage.NONE
        self.player1: np.ndarray = np.array(2)
        self.player2: np.ndarray = np.array(2)
        self.ball: np.ndarray = np.array(2)
        self.ball_speed: np.ndarray = np.array(2)
        self.score1: int = 0
        self.score2: int = 0
        self.local_play: bool = False
        self.group_name: str = ""

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

    # ハンドラーメソッド
    async def handle(self, payload: dict) -> None:
        """
        プレイヤーからの入力を受け取り、ステージごとに処理を振り分ける。

        :param payload: プレイヤーからのデータを含むペイロード
        """
        data: dict = payload.get("data", {})
        stage: str = payload.get("stage", "")
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
        self.stage = Stage.INIT
        # 初期化
        self._reset_state()
        # プレイモードによって所属させるグループを返る
        if data.get("mode") == "local":
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
                "paddle1": {"x": self.player1[0], "y": self.player1[1]},
                "paddle2": {"x": self.player2[0], "y": self.player2[1]},
                "ball": {"x": self.ball[0], "y": self.ball[1]},
            },
        )
        await self._send_to_group(message)

    async def _handle_ready(self, data: dict) -> None:
        """
        ゲームの準備が整った状態で処理を行う。

        :param data: 準備状態に必要なデータ
        """
        self.stage = Stage.READY
        message = self._build_message("READY", {})
        await self._send_to_group(message)

        # ゲーム状況の更新をする非同期処理を並列で実行する
        if self.stage == Stage.READY:
            asyncio.create_task(self._send_match_state())
            self.stage = Stage.PLAY

    async def _handle_play(self, data: dict) -> None:
        """
        プレイヤーの動きに基づいてゲーム状態を更新。

        :param data: プレイヤーの移動情報
        """
        self._move_paddle(player_move=data)

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

    # ゲームロジック関係のメソッド
    def _move_paddle(self, player_move: dict) -> None:
        """
        プレイヤーのパドルを移動させる。

        :param player_move: プレイヤーの移動情報
        """
        match player_move.get("move"):
            case "UP":
                if player_move.get("team") == "1" and self.player1[1] > 0:
                    self.player1[1] -= self.PLAYER_SPEED
                elif player_move.get("team") == "2" and self.player2[1] > 0:
                    self.player2[1] -= self.PLAYER_SPEED

            case "DOWN":
                if (
                    player_move.get("team") == "1"
                    and self.player1[1] + self.PLAYER_HEIGHT < self.HEIGHT
                ):
                    self.player1[1] += self.PLAYER_SPEED
                elif (
                    player_move.get("team") == "2"
                    and self.player2[1] + self.PLAYER_HEIGHT < self.HEIGHT
                ):
                    self.player2[1] += self.PLAYER_SPEED

    def _update_match_state(self) -> None:
        """
        ボールの移動や、ボールと壁・パドルとの衝突、得点の判定を行い、ゲーム状態を更新する。
        """
        # ボールの移動
        self.ball[0] += self.ball_speed[0]
        self.ball[1] += self.ball_speed[1]

        # 上下の壁との衝突判定
        if self.ball[1] - self.BALL_RADIUS <= 0:
            self.ball_speed[1] = abs(self.ball_speed[1])
        elif self.ball[1] + self.BALL_RADIUS >= self.HEIGHT:
            self.ball_speed[1] = -abs(self.ball_speed[1])

        # パドルとの衝突判定
        self._process_ball_paddle_collision(self.player1, True)
        self._process_ball_paddle_collision(self.player2, False)

        # 得点判定
        if self.ball[0] + self.BALL_RADIUS <= 0:
            self.score2 += 1
            self._reset_ball()
        elif self.ball[0] - self.BALL_RADIUS >= self.WIDTH:
            self.score1 += 1
            self._reset_ball()

        # 勝利判定
        if self.score1 >= 5 or self.score2 >= 5:
            self.stage = Stage.END

    def _process_ball_paddle_collision(
        self, player_pos: np.ndarray, is_player1: bool
    ) -> None:
        """
        ボールとパドルの衝突判定と衝突時の処理

        Args:
            player_pos (np.ndarray): プレーヤーの位置
            is_player1 (bool): プレイヤー1のパドルかどうか
        """
        # 衝突判定
        if (
            self.ball[0] - self.BALL_RADIUS
            <= player_pos[0] + self.PLAYER_WIDTH
            and self.ball[0] + self.BALL_RADIUS >= player_pos[0]
            and self.ball[1] - self.BALL_RADIUS
            <= player_pos[1] + self.PLAYER_HEIGHT
            and self.ball[1] + self.BALL_RADIUS >= player_pos[1]
        ):
            # ボールのx座標がパドルの側面に当たった場合
            # ボールの中心がパドルの端よりも自陣側に過ぎていたらx軸方向に跳ね返さない
            if (
                self.ball[1] >= player_pos[1]
                and self.ball[1] <= player_pos[1] + self.PLAYER_HEIGHT
            ):
                if (
                    is_player1
                    and self.ball[0] > player_pos[0] + self.PLAYER_WIDTH
                ):
                    self.ball_speed[0] = abs(self.ball_speed[0])
                elif self.ball[0] < player_pos[0]:
                    self.ball_speed[0] = -abs(self.ball_speed[0])

            # ボールのy座標がパドルの上下面に当たった場合
            if (
                self.ball[0] >= player_pos[0]
                and self.ball[0] <= player_pos[0] + self.PLAYER_WIDTH
            ):
                if self.ball[1] <= player_pos[1]:
                    self.ball_speed[1] = -abs(self.ball_speed[1])
                elif self.ball[1] >= player_pos[1] + self.PLAYER_HEIGHT:
                    self.ball_speed[1] = abs(self.ball_speed[1])

    async def _send_match_state(self) -> None:
        """
        ゲーム状態を60FPSで定期的に送信する。

        ゲームが終了するまで繰り返し実行される。
        """
        last_update = asyncio.get_event_loop().time()
        while self.stage != Stage.END:
            await asyncio.sleep(1 / 60)
            current_time = asyncio.get_event_loop().time()
            delta = current_time - last_update
            if delta >= 1 / 60:
                self._update_match_state()
                game_state = self._build_message(
                    "PLAY",
                    {
                        "paddle1": {
                            "x": self.player1[0],
                            "y": self.player1[1],
                        },
                        "paddle2": {
                            "x": self.player2[0],
                            "y": self.player2[1],
                        },
                        "ball": {"x": self.ball[0], "y": self.ball[1]},
                        "score1": self.score1,
                        "score2": self.score2,
                    },
                )
                await self._send_to_group(game_state)
                last_update = current_time
            else:
                await asyncio.sleep(1 / 60 - delta)

        # ENDステージの処理
        await self._handle_end()

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
        self.stage = Stage.NONE
        # playerの位置は左上とする
        self.player1 = np.array([10, self.HEIGHT / 2 - self.PLAYER_HEIGHT / 2])
        self.player2 = np.array(
            [
                self.WIDTH - self.PLAYER_WIDTH - 10,
                self.HEIGHT / 2 - self.PLAYER_HEIGHT / 2,
            ]
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
        self.ball = np.array([self.WIDTH / 2, self.HEIGHT / 2])
        self.ball_speed = np.array([self.BALL_SPEED, self.BALL_SPEED])

    def _build_message(self, stage: str, data: dict) -> dict:
        """
        メッセージを作成。

        :param stage: ステージ名
        :param data: ステージに関連するデータ
        :return: 作成したメッセージ
        """
        return {"category": "MATCH", "payload": {"stage": stage, "data": data}}

    # --------------
    # 静的関数
    # --------------

    @staticmethod
    def intersect_ball_and_paddle(
        v1: np.ndarray, v2: np.ndarray, v3: np.ndarray, v4: np.ndarray
    ) -> bool:
        """
        ボールの移動前と移動後の点を結ぶ軌跡とパドルの辺の交差判定

        Parameters:
            v1: ボールの移動前の位置ベクトル (x, y)
            v2: ボールの移動後の位置ベクトル (x, y)
            v3: パドルの辺の片方の位置ベクトル (x, y)
            v4: パドルの辺のもう片方の位置ベクトル (x, y)

        Return:
            交差していればTrue、そうでなければFalse
            ただし、ボールが移動したときにパドルと交差したかを知りたいので、移動する前の点がすでに交差している場合はFalseを返す
        """
        # ボールの移動前の位置ベクトルから他の位置ベクトルへのベクトルを計算
        v1_v2: np.ndarray = v2 - v1
        v1_v3: np.ndarray = v3 - v1
        v1_v4: np.ndarray = v4 - v1

        # 片方の壁の位置ベクトルから他の位置ベクトルへのベクトルを計算
        v3_v1: np.ndarray = v1 - v3
        v3_v2: np.ndarray = v2 - v3
        v3_v4: np.ndarray = v4 - v3

        # ボールの移動前後の位置がそれぞれパドルの逆側にいて、それがパドルの範囲にあるか
        is_crossing: bool = geometry_utils.check_opposite_sides(
            v1_v2, v1_v3, v1_v4
        ) and geometry_utils.check_opposite_sides(v3_v4, v3_v1, v3_v2)

        # ボールの移動後の位置がパドル上にいるか
        # パドルの両端がボールの移動の軌跡にちょうど当たるか
        is_point_on_other_line: bool = (
            geometry_utils.is_internally_devided(v1, v2, v3)
            or geometry_utils.is_internally_devided(v1, v2, v4)
            or geometry_utils.is_internally_devided(v3, v4, v2)
        )

        # 特別条件: vec1 が vec3-vec4 の線分上の場合は False を返す
        is_v1_on_line = geometry_utils.is_internally_devided(v3, v4, v1)

        # 交差判定
        return is_crossing or (is_point_on_other_line and not is_v1_on_line)

    @staticmethod
    def intersect_ball_and_wall(
        v1: np.ndarray, v2: np.ndarray, v3: np.ndarray, v4: np.ndarray
    ) -> bool:
        """
        ボールの移動前と移動後の点を結ぶ軌跡と壁(直線)の交差判定

        Parameters:
            v1: ボールの移動前の位置ベクトル (x, y)
            v2: ボールの移動後の位置ベクトル (x, y)
            v3: 壁のある点の位置ベクトル (x, y)
            v4: 壁のもう一つの点の位置ベクトル (x, y)

        Return:
            交差すればTrue、それ以外はFalse
            ただし、ボールが移動したときにパドルと交差したかを知りたいので、移動する前の点がすでに交差している場合はFalseを返す
        """
        # 片方の壁の位置ベクトルから他の位置ベクトルへのベクトルを計算
        v3_v1: np.ndarray = v1 - v3
        v3_v2: np.ndarray = v2 - v3
        v3_v4: np.ndarray = v4 - v3

        # 交差判定
        # v3_v4は直線として扱うので、v3_v1, v3_v2が直線v3_v4の逆側にあるか、
        # ちょうどv2(ボールの移動先の位置)がv3_v4直線を内分しているれば交差していると判定する
        return geometry_utils.check_opposite_sides(
            v3_v4, v3_v1, v3_v2
        ) or geometry_utils.is_on_the_line(v3, v4, v2)
