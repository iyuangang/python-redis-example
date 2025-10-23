"""
Redis CRUD使用示例
演示基本的增删改查操作
"""
import time
from redis_crud import RedisCRUD
from redis_client import RedisClient

def main():
    """主函数 - 演示Redis CRUD操作"""
    
    print("修改测试\n")
    print("=== Redis CRUD 操作示例 ===\n")
    
    # 创建CRUD实例
    crud = RedisCRUD(key_prefix="demo")
    
    # 1. 创建操作
    print("1. 创建操作 (Create)")
    print("-" * 30)
    
    # 创建简单字符串
    crud.create("user:name", "张三")
    crud.create("user:age", 25)
    # 创建JSON对象
    user_info = {
        "name": "李四",
        "age": 30,
        "email": "lisi@example.com",
        "hobbies": ["读书", "游泳", "编程"]
    }
    crud.create("user:info", user_info)
    
    # 创建带过期时间的键
    crud.create("session:token", "abc123xyz", expire=60)  # 60秒后过期
    
    print("✅ 创建了多个键值对\n")
    
    # 2. 读取操作
    print("2. 读取操作 (Read)")
    print("-" * 30)
    
    # 读取简单值
    name = crud.read("user:name")
    age = crud.read("user:age")
    print(f"用户名: {name}")
    print(f"年龄: {age}")
    
    # 读取JSON对象
    user_info = crud.read("user:info")
    print(f"用户信息: {user_info}")
    
    # 检查键是否存在
    exists = crud.exists("user:name")
    print(f"user:name 是否存在: {exists}")
    
    # 获取TTL
    ttl = crud.get_ttl("session:token")
    print(f"session:token 剩余时间: {ttl}秒")
    
    print()
    
    # 3. 更新操作
    print("3. 更新操作 (Update)")
    print("-" * 30)
    
    # 更新用户年龄
    crud.update("user:age", 26)
    new_age = crud.read("user:age")
    print(f"更新后的年龄: {new_age}")
    
    # 更新用户信息
    updated_info = {
        "name": "李四",
        "age": 31,
        "email": "lisi@newemail.com",
        "hobbies": ["读书", "游泳", "编程", "旅行"],
        "city": "北京"
    }
    crud.update("user:info", updated_info)
    print(f"更新后的用户信息: {crud.read('user:info')}")
    
    print()
    
    # 4. 批量操作
    print("4. 批量操作")
    print("-" * 30)
    
    # 批量创建
    batch_data = {
        "product:1": {"name": "iPhone", "price": 9999},
        "product:2": {"name": "MacBook", "price": 12999},
        "product:3": {"name": "iPad", "price": 3999}
    }
    crud.batch_create(batch_data)
    print("✅ 批量创建了产品信息")
    
    # 获取所有键
    all_keys = crud.get_all_keys()
    print(f"所有键: {all_keys}")
    
    # 获取特定模式的键
    user_keys = crud.get_all_keys("user:*")
    print(f"用户相关键: {user_keys}")
    
    print()
    
    # 5. 删除操作
    print("5. 删除操作 (Delete)")
    print("-" * 30)
    
    # 删除单个键
    deleted = crud.delete("user:age")
    print(f"删除 user:age: {'成功' if deleted else '失败'}")
    
    # 检查删除结果
    age_after_delete = crud.read("user:age")
    print(f"删除后 user:age 的值: {age_after_delete}")
    
    # 批量删除
    deleted_count = crud.batch_delete(["product:1", "product:2"])
    print(f"批量删除了 {deleted_count} 个产品")
    
    print()
    
    # 6. 高级操作
    print("6. 高级操作")
    print("-" * 30)
    
    # 设置过期时间
    crud.create("temp:data", "临时数据")
    crud.set_expire("temp:data", 10)  # 10秒后过期
    print("设置了临时数据的过期时间")
    
    # 监控过期
    for i in range(12):
        ttl = crud.get_ttl("temp:data")
        exists = crud.exists("temp:data")
        print(f"第{i+1}秒: TTL={ttl}, 存在={exists}")
        if not exists:
            break
        time.sleep(1)
    
    print()
    
    # 7. 清理演示数据
    print("7. 清理演示数据")
    print("-" * 30)
    
    # 获取所有演示键并删除
    demo_keys = crud.get_all_keys()
    if demo_keys:
        deleted_count = crud.batch_delete(demo_keys)
        print(f"清理了 {deleted_count} 个演示键")
    else:
        print("没有需要清理的键")
    
    print("\n=== 演示完成 ===")

if __name__ == "__main__":
    main()
