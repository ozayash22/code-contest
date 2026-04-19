import redis
from app.core.config import settings

"""Basic connection example.
"""

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    username="default",
    password=settings.REDIS_PASSWORD,
)

success = redis_client.set('foo', 'bar')
# True

result = redis_client.get('foo')
print(result)