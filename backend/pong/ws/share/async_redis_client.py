# type: ignore
# TODO: redis-pyはまだ型ヒントが整備されていないので型ヒントを無視するようにするが他に良い方法があれば変更
from typing import Final

import redis.asyncio as redis
from django.conf import settings


class AsyncRedisClient:
    """
    Redisを使ってSetのデータ管理を行う汎用クラス。(必要であれば他のデータ構造も増やす)
    シングルトンパターンを使い、Redisクライアントを1つだけ作成して再利用する。

    keyの命名規則:
        <キーとするリソース名>:<そのID>:<値に追加するリソースの集合名>
    """

    _instance = None
    HOST: Final[str] = "redis"
    PORT: Final[int] = 6379
    DB: Final[int] = int(settings.REDIS_STORE_DB)  # デフォルトのデータベース
    PASSWORD: Final[str] = settings.REDIS_PASSWORD

    @classmethod
    async def get_client(cls) -> redis.Redis:
        """
        非同期の Redis クライアントを取得する。
        シングルトンとしてインスタンスを1つだけ作成する。

        Exceptions：
            redis.exceptions.ConnectionError: Redisサーバーに接続できない場合。
        """
        if cls._instance is None:
            cls._instance = redis.Redis(
                host=cls.HOST,
                port=cls.PORT,
                db=cls.DB,
                password=cls.PASSWORD,
                decode_responses=True,
            )
        return cls._instance

    @classmethod
    def _generate_key(
        cls, namespace: str, identifier: str, resource: str
    ) -> str:
        """統一されたキーのフォーマットを作成。"""
        return f"{namespace}:{identifier}:{resource}"

    @classmethod
    async def sadd_value(
        cls, namespace: str, identifier: str, resource: str, value: str
    ) -> int:
        """
        指定したキーの Set に値を追加する。
        - `namespace="user", identifier="123", resource="channels"` → `"user:123:channels"` に `value` を追加

        Exceptions：
            redis.exceptions.ConnectionError: Redisサーバーに接続できない場合。
            redis.exceptions.ResponseError: 登録した型と取り出す型が違う場合。
        """
        client = await cls.get_client()
        key = cls._generate_key(namespace, identifier, resource)
        await client.sadd(key, value)

        return await client.scard(key)

    @classmethod
    async def srem_value(
        cls, namespace: str, identifier: str, resource: str, value: str
    ) -> int:
        """
        指定したキーの Set から値を削除し、空ならキーごと削除する。

        Exceptions：
            redis.exceptions.ConnectionError: Redisサーバーに接続できない場合。
            redis.exceptions.ResponseError: 登録した型と取り出す型が違う場合。
        """
        client = await cls.get_client()
        key = cls._generate_key(namespace, identifier, resource)
        await client.srem(key, value)

        count = await client.scard(key)
        if count == 0:  # セットが空ならキーを削除
            await client.delete(key)

        return count

    @classmethod
    async def smembers_value(
        cls, namespace: str, identifier: str, resource: str
    ) -> set[str]:
        """
        指定したキーの Set に含まれるすべての値をsetで取得。

        Exceptions：
            redis.exceptions.ConnectionError: Redisサーバーに接続できない場合。
            redis.exceptions.ResponseError: 登録した型と取り出す型が違う場合。
        """
        client = await cls.get_client()
        key = cls._generate_key(namespace, identifier, resource)
        return await client.smembers(key)

    @classmethod
    async def exists(
        cls, namespace: str, identifier: str, resource: str
    ) -> bool:
        """
        指定したキーが1つ以上存在するか確認。
        ワイルドカードなどで複数に合致することもあるので、1以上だったらTrueを返す。

        Exceptions：
            redis.exceptions.ConnectionError: Redisサーバーに接続できない場合。
        """
        client = await cls.get_client()
        key = cls._generate_key(namespace, identifier, resource)
        return await client.exists(key) > 0

    @classmethod
    async def delete_key(
        cls, namespace: str, identifier: str, resource: str
    ) -> int:
        """
        指定したキーを削除。
        keyでワイルドカードが使用されれば複数のキーが削除される場合もある。
        存在しないキーを削除してもエラーにはならず、0を返す

        Exceptions：
            redis.exceptions.ConnectionError: Redisサーバーに接続できない場合。
        """
        client = await cls.get_client()
        key = cls._generate_key(namespace, identifier, resource)
        return await client.delete(key)

    @classmethod
    async def close(cls) -> None:
        """
        Redis クライアントを閉じる。

        Exceptions：
            redis.exceptions.ConnectionError: Redisサーバーに接続していないときにclose使用とした場合。
        """
        if cls._instance:
            await cls._instance.close()
            cls._instance = None
