import os
from typing import Optional

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Count, Q
from rest_framework import serializers

from accounts import constants as accounts_constants
from accounts.player import models as player_models
from accounts.player import serializers as player_serializers
from matches import constants as matches_constants
from users.blocks import constants as blocks_constants
from users.blocks import models as blocks_models
from users.friends import constants as friends_constants
from users.friends import models as friends_models

from . import constants as users_constants


class UsersSerializer(serializers.Serializer):
    """
    users app全体で共通のシリアライザ
    Playerとそれに紐づくUserから、返しても良い情報のみをまとめてシリアライズする

    Usage:
        - __init__時にkwargsにfieldsを渡すことで、返す情報を動的に変更可能
        - is_friendを使用する際は、get_is_friend()で使用するためcontextにUSER_IDを渡す必要がある
    """

    id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    # todo: 別のserializerをネストする方法で他に良い書き方があれば変更する
    display_name = player_serializers.PlayerSerializer().fields[
        accounts_constants.PlayerFields.DISPLAY_NAME
    ]
    avatar = player_serializers.PlayerSerializer().fields[
        accounts_constants.PlayerFields.AVATAR
    ]
    # `get_{field名}()`の返り値が格納される
    is_friend = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()
    match_wins = serializers.SerializerMethodField()
    match_losses = serializers.SerializerMethodField()

    class Meta:
        model = player_models.Player
        fields = (
            accounts_constants.UserFields.ID,
            accounts_constants.UserFields.USERNAME,
            accounts_constants.UserFields.EMAIL,
            accounts_constants.PlayerFields.DISPLAY_NAME,
            accounts_constants.PlayerFields.AVATAR,
            users_constants.UsersFields.IS_FRIEND,
            users_constants.UsersFields.IS_BLOCKED,
            users_constants.UsersFields.MATCH_WINS,
            users_constants.UsersFields.MATCH_LOSSES,
        )

    # args,kwargsは型ヒントが複雑かつそのままsuper()に渡したいためignoreで対処
    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        # fieldを動的に変更するための引数を取得
        fields: tuple[str] | None = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            # 取得したfields以外をfieldから削除
            allowed: set[str] = set(fields)
            existing: set[str] = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_is_friend(self, player: player_models.Player) -> bool:
        """
        playerがログインユーザーのフレンドであるかどうかを取得する

        Args:
            player: Playerインスタンス

        Returns:
            bool: ログインユーザーのフレンドであればTrue、そうでなければFalse
        """
        if not hasattr(self, "_friendships_cache"):
            # ログインユーザーのフレンド全員をsetでキャッシュしておく
            user_id: int = self.context[
                friends_constants.FriendshipFields.USER_ID
            ]
            self._friendships_cache: set[int] = set(
                friends_models.Friendship.objects.filter(
                    user_id=user_id
                ).values_list("friend_id", flat=True)
            )
        return player.user.id in self._friendships_cache

    def get_is_blocked(self, player: player_models.Player) -> bool:
        """
        playerがログインユーザーにブロックされているかどうかを取得する

        Args:
            player: Playerインスタンス

        Returns:
            bool: ログインユーザーにブロックされていればTrue、そうでなければFalse
        """
        if not hasattr(self, "_blocked_relationships_cache"):
            # ログインユーザーにブロックされているユーザー全員をsetでキャッシュしておく
            user_id: int = self.context[
                blocks_constants.BlockRelationshipFields.USER_ID
            ]
            self._blocked_relationships_cache: set[int] = set(
                blocks_models.BlockRelationship.objects.filter(
                    user_id=user_id
                ).values_list("blocked_user_id", flat=True)
            )
        return player.user.id in self._blocked_relationships_cache

    def _get_match_stats(
        self, player: player_models.Player, result: str
    ) -> int:
        if not hasattr(self, "_match_stats_cache"):
            # playerの勝敗数を一度だけ取得してキャッシュしておく
            self._match_stats_cache: dict[str, int] = (
                player.match_participations.aggregate(
                    wins=Count(
                        accounts_constants.PlayerFields.ID,
                        filter=Q(is_win=True),
                    ),
                    losses=Count(
                        accounts_constants.PlayerFields.ID,
                        filter=Q(
                            match__status=matches_constants.MatchFields.StatusEnum.COMPLETED.value,
                            is_win=False,
                        ),
                    ),
                )
            )
        return self._match_stats_cache[result]

    def get_match_wins(self, player: player_models.Player) -> int:
        """
        playerが勝利したmatchの数を取得する

        Args:
            player: Playerインスタンス

        Returns:
            int: 勝利した試合数
        """
        return self._get_match_stats(player, "wins")

    def get_match_losses(self, player: player_models.Player) -> int:
        """
        playerが敗北したmatchの数を取得する
        matchのstatusがCOMPLETEDかつis_win==Falseのものをカウントする

        Args:
            player: Playerインスタンス

        Returns:
            int: 敗北した試合数
        """
        return self._get_match_stats(player, "losses")

    def validate(self, data: dict) -> dict:
        """
        validate()のオーバーライド
        """
        # avatar更新時
        if accounts_constants.PlayerFields.AVATAR in data:
            avatar: Optional[InMemoryUploadedFile] = data[
                accounts_constants.PlayerFields.AVATAR
            ]
            # 更新時(既にinstanceが存在している時)にNoneの場合はエラー
            if self.instance and avatar is None:
                raise serializers.ValidationError(
                    {
                        accounts_constants.PlayerFields.AVATAR: "This field may not be blank."
                    }
                )
        return data

    def _update_avatar(
        self, player: player_models.Player, new_avatar: InMemoryUploadedFile
    ) -> InMemoryUploadedFile:
        # 更新前の画像を削除してから新しい画像を保存する
        player.avatar.delete(save=False)

        # ファイル名を変更
        # mypyにnew_avatar.nameがNoneの可能性を指摘されるが、ImageFieldのvalidatorでextensionがあることは確認済みのため無視
        _, extension = os.path.splitext(new_avatar.name)  # type: ignore[type-var]
        # todo: 一意なためusernameをファイル名にしているが、良くない場合はuuidなどを追加する
        new_avatar.name = f"avatars/{player.user.username}{extension}"
        return new_avatar

    def update(
        self, player: player_models.Player, validated_data: dict
    ) -> player_models.Player:
        """
        Playerインスタンスを更新するupdate()のオーバーライド
        更新するフィールドに新しい値を代入し、update_fieldsに指定する
        display_nameはapplication/json、avatarはmultipart/form-dataで受け取るため、
        どちらかのみ更新される
        """
        update_fields: list[str] = []

        # display_nameがあれば更新
        if accounts_constants.PlayerFields.DISPLAY_NAME in validated_data:
            player.display_name = validated_data[
                accounts_constants.PlayerFields.DISPLAY_NAME
            ]
            update_fields.append(accounts_constants.PlayerFields.DISPLAY_NAME)

        # avatarがあれば更新
        if accounts_constants.PlayerFields.AVATAR in validated_data:
            new_avatar: InMemoryUploadedFile = validated_data[
                accounts_constants.PlayerFields.AVATAR
            ]
            player.avatar = self._update_avatar(player, new_avatar)
            update_fields.append(accounts_constants.PlayerFields.AVATAR)

        # create()をオーバーライドしない場合、update()内でsave()は必須
        player.save(update_fields=update_fields)
        return player
