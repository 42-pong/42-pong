from rest_framework import serializers

from accounts import constants as accounts_constants
from accounts.player import models as player_models
from accounts.player import serializers as player_serializers
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
    # get_is_friend()の返り値が格納される
    is_friend = serializers.SerializerMethodField()
    # todo: is_blocked,is_online,win_match,lose_match追加

    class Meta:
        model = player_models.Player
        fields = (
            accounts_constants.UserFields.ID,
            accounts_constants.UserFields.USERNAME,
            accounts_constants.UserFields.EMAIL,
            accounts_constants.PlayerFields.DISPLAY_NAME,
            accounts_constants.PlayerFields.AVATAR,
            users_constants.UsersFields.IS_FRIEND,
            # todo: is_blocked,is_online,win_match,lose_match追加
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

    def update(
        self, player: player_models.Player, validated_data: dict
    ) -> player_models.Player:
        """
        Playerインスタンスを更新するupdate()のオーバーライド
        """
        player.display_name = validated_data.get(
            accounts_constants.PlayerFields.DISPLAY_NAME, player.display_name
        )
        # todo: avatarも新しいものを代入・save()のupdate_fieldsにも追加

        # create()をオーバーライドしない場合、update()内でsave()は必須
        player.save(
            update_fields=[accounts_constants.PlayerFields.DISPLAY_NAME]
        )
        return player
