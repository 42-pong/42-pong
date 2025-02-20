from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

# AsyncRedisClientをtype: ignoreしているのでそのimport先でもtype: ignoreが必要
from ws.share.async_redis_client import AsyncRedisClient  # type: ignore

"""
test内で使われているassert関数の説明
- mock_redis_instance.<method_name>.assert_called_once()はmethod_nameが一度だけ呼び出されたかをテストする。
- mock_redis_instance.<method_name>.assert_called_once_with()は引数を渡すとその引数で呼び出されたかもテストできる。

2つのmockの説明
- AsyncMock(unittest)
    - 非同期のモックオブジェクトを作成。非同期のモックオブジェクトはpytestにないためunittestのものを使用。
    - （autospec=True） を使用すると、モックオブジェクトが実際のオブジェクトと同じインターフェース（メソッドや属性）を持つことになります。
- mocker(pytest)
    - メソッドをモックし、AsyncMock()で作ったモックオブジェクトを返り値に指定。
"""


# defaultでscope=functionなので関数ごとに呼ばれる
@pytest.fixture(autouse=True)
def reset_redis_client() -> None:
    """
    テスト実行ごとにシングルトンのインスタンスをリセット
    すべてのテストでRedisインスタンスはモックで作成しているのでcloseする必要はない
    """
    AsyncRedisClient._instance = None


@pytest.mark.asyncio
async def test_get_client_called_once(mocker: MockerFixture) -> None:
    """get_client() を100回呼んでも Redis インスタンスが1回しか作成されないことを確認"""
    # AsyncRedisClient.get_client()内で使用されるredis.asyncio.Redisをモック
    mock_redis = mocker.patch("redis.asyncio.Redis", autospec=True)

    for _ in range(100):
        client = await AsyncRedisClient.get_client()
        assert client is AsyncRedisClient._instance  # シングルトン確認

    mock_redis.assert_called_once()


@pytest.mark.asyncio
async def test_close(mocker: MockerFixture) -> None:
    """close() 関数が Redis の close() を正しく呼び出しているかをテスト"""
    mock_redis_instance = AsyncMock()
    # AsyncRedisClient.get_client()内で使用されるredis.asyncio.Redisをモック
    mocker.patch("redis.asyncio.Redis", return_value=mock_redis_instance)

    await AsyncRedisClient.get_client()
    await AsyncRedisClient.close()

    mock_redis_instance.close.assert_called_once()


@pytest.mark.asyncio
async def test_sadd_value(mocker: MockerFixture) -> None:
    """sadd_value() が Redis の sadd_value() を正しく呼び出しているかをテスト"""
    mock_redis_instance = AsyncMock()
    # AsyncRedisClient.get_client()をモック
    mocker.patch.object(
        AsyncRedisClient, "get_client", return_value=mock_redis_instance
    )

    await AsyncRedisClient.sadd_value("user", "123", "channels", "general")

    mock_redis_instance.sadd.assert_called_once_with(
        "user:123:channels", "general"
    )


@pytest.mark.asyncio
async def test_srem_value(mocker: MockerFixture) -> None:
    """srem_value() が Redis の srem_value() を正しく呼び出し、セットが空なら delete_key() を呼ぶかテスト"""
    mock_redis_instance = AsyncMock()
    # AsyncRedisClient.get_client()をモック
    mocker.patch.object(
        AsyncRedisClient, "get_client", return_value=mock_redis_instance
    )

    mock_redis_instance.scard.return_value = 0  # 削除後にセットが空になる想定
    await AsyncRedisClient.srem_value("user", "123", "channels", "general")

    mock_redis_instance.srem.assert_called_once_with(
        "user:123:channels", "general"
    )
    mock_redis_instance.scard.assert_called_once_with("user:123:channels")
    mock_redis_instance.delete.assert_called_once_with("user:123:channels")


@pytest.mark.asyncio
async def test_smembers_value(mocker: MockerFixture) -> None:
    """smembers_value() が Redis の smembers_value() を正しく呼び出しているかをテスト"""
    mock_redis_instance = AsyncMock()
    # AsyncRedisClient.get_client()をモック
    mocker.patch.object(
        AsyncRedisClient, "get_client", return_value=mock_redis_instance
    )
    mock_redis_instance.smembers.return_value = {"general", "random"}

    result = await AsyncRedisClient.smembers_value("user", "123", "channels")

    mock_redis_instance.smembers.assert_called_once_with("user:123:channels")
    assert result == {"general", "random"}


@pytest.mark.asyncio
async def test_exists(mocker: MockerFixture) -> None:
    """exists() が Redis の exists() を正しく呼び出しているかをテスト"""
    mock_redis_instance = AsyncMock()
    # AsyncRedisClient.get_client()をモック
    mocker.patch.object(
        AsyncRedisClient, "get_client", return_value=mock_redis_instance
    )
    mock_redis_instance.exists.return_value = 1  # キーが存在する場合

    result = await AsyncRedisClient.exists("user", "123", "channels")

    mock_redis_instance.exists.assert_called_once_with("user:123:channels")
    assert result


@pytest.mark.asyncio
async def test_delete_key(mocker: MockerFixture) -> None:
    """delete_key() が Redis の delete_key() を正しく呼び出しているかをテスト"""
    mock_redis_instance = AsyncMock()
    # AsyncRedisClient.get_client()をモック
    mocker.patch.object(
        AsyncRedisClient, "get_client", return_value=mock_redis_instance
    )

    await AsyncRedisClient.delete_key("user", "123", "channels")

    mock_redis_instance.delete.assert_called_once_with("user:123:channels")
