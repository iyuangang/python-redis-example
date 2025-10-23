"""
Redis配置模块
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class RedisConfig:
    """Redis配置类"""
    
    # Redis连接配置
    HOST = os.getenv('REDIS_HOST', '192.168.148.56')
    PORT = int(os.getenv('REDIS_PORT', 6379))
    PASSWORD = os.getenv('REDIS_PASSWORD', None)
    DB = int(os.getenv('REDIS_DB', 0))
    
    # 连接池配置
    MAX_CONNECTIONS = int(os.getenv('REDIS_MAX_CONNECTIONS', 20))
    CONNECTION_TIMEOUT = int(os.getenv('REDIS_CONNECTION_TIMEOUT', 5))
    
    @classmethod
    def get_connection_params(cls):
        """获取连接参数字典"""
        params = {
            'host': cls.HOST,
            'port': cls.PORT,
            'db': cls.DB,
            'decode_responses': True,  # 自动解码响应为字符串
            'socket_connect_timeout': cls.CONNECTION_TIMEOUT,
            'socket_timeout': cls.CONNECTION_TIMEOUT,
        }
        
        if cls.PASSWORD:
            params['password'] = cls.PASSWORD
            
        return params
