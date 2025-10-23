"""
Redis客户端连接管理
"""
import redis
from redis.connection import ConnectionPool
from config import RedisConfig
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisClient:
    """Redis客户端管理类"""
    
    _instance = None
    _pool = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._create_pool()
            self.initialized = True
    
    def _create_pool(self):
        """创建连接池"""
        try:
            params = RedisConfig.get_connection_params()
            self._pool = ConnectionPool(
                max_connections=RedisConfig.MAX_CONNECTIONS,
                **params
            )
            logger.info("Redis连接池创建成功")
        except Exception as e:
            logger.error(f"创建Redis连接池失败: {e}")
            raise
    
    def get_connection(self):
        """获取Redis连接"""
        try:
            if self._pool is None:
                self._create_pool()
            return redis.Redis(connection_pool=self._pool)
        except Exception as e:
            logger.error(f"获取Redis连接失败: {e}")
            raise
    
    def test_connection(self):
        """测试Redis连接"""
        try:
            conn = self.get_connection()
            conn.ping()
            logger.info("Redis连接测试成功")
            return True
        except Exception as e:
            logger.error(f"Redis连接测试失败: {e}")
            return False
    
    def close(self):
        """关闭连接池"""
        if self._pool:
            self._pool.disconnect()
            logger.info("Redis连接池已关闭")
