import pytest
from unittest.mock import AsyncMock

# AsyncRedisClientをtype: ignoreしているのでそのimport先でもtype: ignoreが必要
from ws.share.async_redis_client import AsyncRedisClient  # type: ignore


# defaultでscope=functionなので関数ごとに呼ばれる
@pytest.fixture(autouse=True)
def reset_redis_client():
    """
    テスト実行ごとにシングルトンのインスタンスをリセット
    すべてのテストでRedisインスタンスはモックで作成しているのでcloseする必要はない
    """
    AsyncRedisClient._instance = None


@pytest.mark.asyncio
async def test_get_client_called_once(mocker):
    """get_client() を100回呼んでも Redis インスタンスが1回しか作成されないことを確認"""
    mock_redis = mocker.patch("redis.asyncio.Redis", autospec=True)

    for _ in range(100):
        client = await AsyncRedisClient.get_client()
        assert client is AsyncRedisClient._instance  # シングルトン確認

    mock_redis.assert_called_once()


@pytest.mark.asyncio
async def test_close(mocker):
    """close() 関数が Redis の close() を正しく呼び出しているかをテスト"""
    mock_redis_instance = AsyncMock()
    mocker.patch("redis.asyncio.Redis", return_value=mock_redis_instance)

    await AsyncRedisClient.get_client()
    await AsyncRedisClient.close()

    mock_redis_instance.close.assert_called_once()

