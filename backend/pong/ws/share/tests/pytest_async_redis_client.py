import pytest

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
