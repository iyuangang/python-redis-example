# Redis CRUD 最佳实践

这是一个最简单的Python操作Redis CRUD的最佳实践示例，提供了完整的增删改查功能。

## 功能特性

- ✅ 完整的CRUD操作（创建、读取、更新、删除）
- ✅ 连接池管理，支持高并发
- ✅ 自动JSON序列化/反序列化
- ✅ 键过期时间管理
- ✅ 批量操作支持
- ✅ 键存在性检查
- ✅ 命名空间隔离（键前缀）
- ✅ 完善的错误处理和日志记录
- ✅ 单例模式连接管理

## 项目结构

```
redis-test/
├── requirements.txt      # 项目依赖
├── config.py            # Redis配置
├── redis_client.py      # Redis连接管理
├── redis_crud.py        # CRUD操作类
├── example.py           # 完整使用示例
├── simple_example.py    # 简单使用示例
└── README.md            # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动Redis服务

确保Redis服务正在运行：

```bash
# Windows
redis-server

# Linux/Mac
sudo systemctl start redis
# 或者
redis-server
```

### 3. 运行示例

#### 简单示例（推荐新手）

```bash
python simple_example.py
```

#### 完整示例

```bash
python example.py
```

## 基本使用

### 1. 创建CRUD实例

```python
from redis_crud import RedisCRUD

# 基本使用
crud = RedisCRUD()

# 使用键前缀（推荐用于多项目环境）
crud = RedisCRUD(key_prefix="myapp")
```

### 2. 基本CRUD操作

```python
# 创建/设置数据
crud.create("user:name", "张三")
crud.create("user:age", 25)
crud.create("user:info", {"name": "李四", "age": 30})

# 读取数据
name = crud.read("user:name")
age = crud.read("user:age")
user_info = crud.read("user:info")

# 更新数据
crud.update("user:age", 26)

# 删除数据
crud.delete("user:name")

# 检查键是否存在
exists = crud.exists("user:age")
```

### 3. 高级功能

```python
# 设置过期时间
crud.create("session:token", "abc123", expire=3600)  # 1小时后过期

# 获取剩余时间
ttl = crud.get_ttl("session:token")

# 设置过期时间
crud.set_expire("user:session", 1800)  # 30分钟后过期

# 批量操作
batch_data = {
    "product:1": {"name": "iPhone", "price": 9999},
    "product:2": {"name": "MacBook", "price": 12999}
}
crud.batch_create(batch_data)

# 批量删除
crud.batch_delete(["product:1", "product:2"])

# 获取所有键
all_keys = crud.get_all_keys()
user_keys = crud.get_all_keys("user:*")
```

## 配置说明

### 环境变量配置

创建 `.env` 文件（可选）：

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
REDIS_MAX_CONNECTIONS=20
REDIS_CONNECTION_TIMEOUT=5
```

### 代码配置

在 `config.py` 中修改配置：

```python
class RedisConfig:
    HOST = 'localhost'
    PORT = 6379
    PASSWORD = None
    DB = 0
    MAX_CONNECTIONS = 20
    CONNECTION_TIMEOUT = 5
```

## 最佳实践

### 1. 键命名规范

```python
# 使用冒号分隔命名空间
crud.create("user:123:profile", user_data)
crud.create("session:abc123", session_data)
crud.create("cache:product:456", product_data)
```

### 2. 数据类型处理

```python
# 字符串
crud.create("name", "张三")

# 数字
crud.create("age", 25)

# 字典/列表（自动JSON序列化）
crud.create("user", {"name": "李四", "hobbies": ["读书", "游泳"]})
```

### 3. 错误处理

```python
try:
    result = crud.create("key", "value")
    if result:
        print("创建成功")
    else:
        print("创建失败")
except Exception as e:
    print(f"操作失败: {e}")
```

### 4. 连接管理

```python
from redis_client import RedisClient

# 测试连接
client = RedisClient()
if client.test_connection():
    print("Redis连接正常")
else:
    print("Redis连接失败")
```

## 常见问题

### Q: 如何确保Redis服务正在运行？

A: 运行以下命令检查：

```bash
# 检查Redis进程
ps aux | grep redis

# 测试连接
redis-cli ping
```

### Q: 如何处理连接失败？

A: 检查以下几点：

1. Redis服务是否启动
2. 端口是否正确（默认6379）
3. 防火墙设置
4. 密码配置

### Q: 如何优化性能？

A: 建议：

1. 使用连接池（已内置）
2. 合理设置过期时间
3. 使用批量操作
4. 避免大对象存储

## 扩展功能

### 自定义序列化

```python
import pickle

# 自定义序列化函数
def custom_serialize(obj):
    return pickle.dumps(obj)

def custom_deserialize(data):
    return pickle.loads(data)
```

### 事务支持

```python
# 使用Redis事务
pipe = crud.redis.pipeline()
pipe.multi()
pipe.set("key1", "value1")
pipe.set("key2", "value2")
pipe.execute()
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 其他

这里暂时没有东西
