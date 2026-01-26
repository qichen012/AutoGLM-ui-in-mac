"""测试 AutoGLM 集成"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ai.autoglm_agent import AutoGLMAgent
from utils.config import load_config


def test_autoglm():
    """测试AutoGLM集成"""
    print("=" * 60)
    print("测试 AutoGLM 集成")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    device_ip = config['device']['ip']
    adb_port = config['device']['adb_port']
    
    print(f"\n1. 创建 AutoGLM Agent")
    print(f"   设备: {device_ip}:{adb_port}")
    
    agent = AutoGLMAgent(device_ip=device_ip, adb_port=adb_port)
    
    print(f"\n2. 初始化 Agent")
    if agent.initialize():
        print("   ✅ 初始化成功")
    else:
        print("   ❌ 初始化失败")
        return
    
    print(f"\n3. 设置回调函数")
    def log_callback(message: str):
        print(f"   [回调] {message}")
    
    agent.set_step_callback(log_callback)
    
    print(f"\n4. 执行测试任务")
    test_instruction = "打开设置"
    print(f"   指令: {test_instruction}")
    
    result = agent.execute_task(test_instruction)
    
    print(f"\n5. 结果分析")
    print(f"   成功: {result['success']}")
    if result['success']:
        print(f"   消息: {result.get('message')}")
    else:
        print(f"   错误: {result.get('error')}")
    
    print(f"\n6. 获取状态")
    status = agent.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_autoglm()
