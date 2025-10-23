"""
Redis CRUD操作类
提供基本的增删改查操作
"""
import json
import logging
from typing import Any, Dict, List, Optional, Union
from redis_client import RedisClient

logger = logging.getLogger(__name__)

class RedisCRUD:
    """Redis CRUD操作类"""
    
    def __init__(self, key_prefix: str = ""):
        """
        初始化Redis CRUD操作类
        
        Args:
            key_prefix: 键前缀，用于命名空间隔离
        """
        self.client = RedisClient()
        self.redis = self.client.get_connection()
        self.key_prefix = key_prefix
        logger.info(f"RedisCRUD初始化完成，键前缀: {key_prefix}")
    
    def _get_key(self, key: str) -> str:
        """生成完整的键名"""
        return f"{self.key_prefix}:{key}" if self.key_prefix else key
    
    def create(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        创建/设置键值对
        
        Args:
            key: 键名
            value: 值（支持字符串、数字、字典、列表等）
            expire: 过期时间（秒），None表示永不过期
            
        Returns:
            bool: 操作是否成功
        """
        try:
            full_key = self._get_key(key)
            
            # 如果值是字典或列表，转换为JSON字符串
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            
            if expire:
                result = self.redis.setex(full_key, expire, value)
            else:
                result = self.redis.set(full_key, value)
            
            logger.info(f"创建键值对成功: {full_key}")
            return result
            
        except Exception as e:
            logger.error(f"创建键值对失败: {e}")
            return False
    
    def read(self, key: str, parse_json: bool = True) -> Optional[Any]:
        """
        读取键值
        
        Args:
            key: 键名
            parse_json: 是否尝试解析JSON
            
        Returns:
            键值，如果键不存在返回None
        """
        try:
            full_key = self._get_key(key)
            value = self.redis.get(full_key)
            
            if value is None:
                logger.info(f"键不存在: {full_key}")
                return None
            
            # 尝试解析JSON
            if parse_json and isinstance(value, str):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    pass  # 不是JSON格式，返回原始字符串
            
            logger.info(f"读取键值成功: {full_key}")
            return value
            
        except Exception as e:
            logger.error(f"读取键值失败: {e}")
            return None
    
    def update(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        更新键值（与create相同，但语义更清晰）
        
        Args:
            key: 键名
            value: 新值
            expire: 过期时间（秒），None表示永不过期
            
        Returns:
            bool: 操作是否成功
        """
        return self.create(key, value, expire)
    
    def delete(self, key: str) -> bool:
        """
        删除键
        
        Args:
            key: 键名
            
        Returns:
            bool: 操作是否成功
        """
        try:
            full_key = self._get_key(key)
            result = self.redis.delete(full_key)
            
            if result > 0:
                logger.info(f"删除键成功: {full_key}")
                return True
            else:
                logger.info(f"键不存在: {full_key}")
                return False
                
        except Exception as e:
            logger.error(f"删除键失败: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        检查键是否存在
        
        Args:
            key: 键名
            
        Returns:
            bool: 键是否存在
        """
        try:
            full_key = self._get_key(key)
            result = self.redis.exists(full_key)
            logger.info(f"检查键存在性: {full_key} -> {bool(result)}")
            return bool(result)
            
        except Exception as e:
            logger.error(f"检查键存在性失败: {e}")
            return False
    
    def get_ttl(self, key: str) -> int:
        """
        获取键的剩余生存时间
        
        Args:
            key: 键名
            
        Returns:
            int: 剩余秒数，-1表示永不过期，-2表示键不存在
        """
        try:
            full_key = self._get_key(key)
            ttl = self.redis.ttl(full_key)
            logger.info(f"获取键TTL: {full_key} -> {ttl}秒")
            return ttl
            
        except Exception as e:
            logger.error(f"获取键TTL失败: {e}")
            return -2
    
    def set_expire(self, key: str, seconds: int) -> bool:
        """
        设置键的过期时间
        
        Args:
            key: 键名
            seconds: 过期时间（秒）
            
        Returns:
            bool: 操作是否成功
        """
        try:
            full_key = self._get_key(key)
            result = self.redis.expire(full_key, seconds)
            logger.info(f"设置键过期时间: {full_key} -> {seconds}秒")
            return bool(result)
            
        except Exception as e:
            logger.error(f"设置键过期时间失败: {e}")
            return False
    
    def get_all_keys(self, pattern: str = "*") -> List[str]:
        """
        获取所有匹配的键
        
        Args:
            pattern: 匹配模式，默认为"*"匹配所有
            
        Returns:
            List[str]: 键列表
        """
        try:
            search_pattern = f"{self.key_prefix}:{pattern}" if self.key_prefix else pattern
            keys = self.redis.keys(search_pattern)
            
            # 如果使用了前缀，需要去掉前缀
            if self.key_prefix:
                keys = [key.replace(f"{self.key_prefix}:", "") for key in keys]
            
            logger.info(f"获取匹配键: {search_pattern} -> {len(keys)}个键")
            return keys
            
        except Exception as e:
            logger.error(f"获取键列表失败: {e}")
            return []
    
    def batch_create(self, data: Dict[str, Any], expire: Optional[int] = None) -> bool:
        """
        批量创建键值对
        
        Args:
            data: 键值对字典
            expire: 过期时间（秒）
            
        Returns:
            bool: 操作是否成功
        """
        try:
            pipe = self.redis.pipeline()
            
            for key, value in data.items():
                full_key = self._get_key(key)
                
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                
                if expire:
                    pipe.setex(full_key, expire, value)
                else:
                    pipe.set(full_key, value)
            
            pipe.execute()
            logger.info(f"批量创建成功: {len(data)}个键值对")
            return True
            
        except Exception as e:
            logger.error(f"批量创建失败: {e}")
            return False
    
    def batch_delete(self, keys: List[str]) -> int:
        """
        批量删除键
        
        Args:
            keys: 键列表
            
        Returns:
            int: 成功删除的键数量
        """
        try:
            full_keys = [self._get_key(key) for key in keys]
            result = self.redis.delete(*full_keys)
            logger.info(f"批量删除成功: {result}个键")
            return result
            
        except Exception as e:
            logger.error(f"批量删除失败: {e}")
            return 0
