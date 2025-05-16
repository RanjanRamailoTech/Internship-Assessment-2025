import redis
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisService:
    _instance: Optional['RedisService'] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RedisService, cls).__new__(cls)

            cls._instance.redis_client = redis.Redis(
                host='localhost',
                port=6381,
                decode_responses=True
            )
            logger.info(f"Created new RedisService instance at {id(cls._instance)}")
        else:
            logger.info(f"Returning existing RedisService instance at {id(cls._instance)}")
        return cls._instance
    
    def set_value(self, key: str, value: str) -> None:
        self.redis_client.set(key, value)
        logger.info(f"Set {key} = {value}")
    
    def get_value(self, key: str) -> Optional[str]:
        value = self.redis_client.get(key)
        logger.info(f"Got {key} = {value}")
        return value


def main():
    redis_service1 = RedisService()
    redis_service1.set_value("test_key", "test_value")
    
    redis_service2 = RedisService()
    value = redis_service2.get_value("test_key")
    
    logger.info(f"Instance 1 ID: {id(redis_service1)}")
    logger.info(f"Instance 2 ID: {id(redis_service2)}")
    logger.info(f"Are instances same? {redis_service1 is redis_service2}")

if __name__ == "__main__":
    main()