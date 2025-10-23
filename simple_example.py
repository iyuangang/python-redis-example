"""
最简单的Redis CRUD使用示例
适合快速上手
"""
from redis_crud import RedisCRUD

def simple_demo():
    """最简单的使用示例"""
    
    # 创建CRUD实例
    crud = RedisCRUD()
    
    print("=== 最简单的Redis CRUD示例 ===\n")
    
    # 1. 创建数据
    print("1. 创建数据")
    crud.create("name", "张三")
    crud.create("age", 25)
    crud.create("user", {"name": "李四", "age": 30})
    crud.create("rootname", "Bob")
    print("✅ 数据创建完成\n")
    
    # 2. 读取数据
    print("2. 读取数据")
    name = crud.read("name")
    age = crud.read("age")
    user = crud.read("user")
    rootname = crud.read("rootname")
    
    print(f"姓名: {name}")
    print(f"年龄: {age}")
    print(f"用户信息: {user}\n")
    print(f"根用户名: {rootname}\n")
    
    # 3. 更新数据
    print("3. 更新数据")
    crud.update("age", 26)
    new_age = crud.read("age")
    crud.update("rootname", "Thirty")
    print(f"更新后的年龄: {new_age}\n")
    print(f"更新后的根用户名: {crud.read('rootname')}\n")

    # 4. 删除数据
    print("4. 删除数据")
    crud.delete("name")
    name_after_delete = crud.read("name")
    print(f"删除后姓名的值: {name_after_delete}")
    crud.delete("rootname")
    print(f"删除后根用户名的值: {crud.read('rootname')}")
    
    # 5. 检查键是否存在
    print(f"age键是否存在: {crud.exists('age')}")
    print(f"name键是否存在: {crud.exists('name')}")
    print(f"rootname键是否存在: {crud.exists('rootname')}")
    
    print("\n=== 示例完成 ===")

if __name__ == "__main__":
    simple_demo()
