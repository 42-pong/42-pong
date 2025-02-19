from typing import Final

import redis.asyncio as redis
from django.conf import settings


class AsyncRedisClient:
    _instance = None
    HOST: Final[str] = "redis"
    PORT: Final[int] = 6379
    DB: Final[int] = 1  # デフォルトのデータベース

    @classmethod
    async def get_client(cls) -> redis.Redis:
        """
        非同期の Redis クライアントを取得する。
        シングルトンとしてインスタンスを1つだけ作成する。
        """
        if cls._instance is None:
            cls._instance = redis.Redis(
                host=cls.HOST,
                port=cls.PORT,
                db=cls.DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
            )
        return cls._instance

    @classmethod
    async def close(cls) -> None:
        """
        Redis クライアントを閉じる。
        """
        if cls._instance:
            await cls._instance.close()
            cls._instance = None
