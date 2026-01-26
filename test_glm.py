#!/usr/bin/env python
"""GLM-4 API 测试脚本"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ai.normal_chat import NormalChatAI
from utils.config import load_config

def main():
    print("=" * 50)
    print("GLM-4 API 测试")
    print("=" * 50)
    
    # 加载配置
    config = load_config()
    api_key = config['ai'].get('api_key')
    
    if not api_key:
        print("❌ 未找到API密钥，请在config.yaml中配置")
        return
    
    print(f"✓ 已加载API密钥: {api_key[:10]}...")
    
    # 初始化AI
    ai = NormalChatAI(model="glm-4", api_key=api_key)
    
    print("\n正在初始化GLM-4...")
    if not ai.initialize():
        print("❌ 初始化失败")
        return
    
    print("✅ 初始化成功！")
    
    # 测试对话
    print("\n" + "=" * 50)
    print("开始测试对话...")
    print("=" * 50)
    
    test_message = "你好，请简单介绍一下你自己"
    print(f"\n用户: {test_message}")
    print("AI: ", end="", flush=True)
    
    # 使用流式输出
    for chunk in ai.stream_chat(test_message):
        print(chunk, end="", flush=True)
    
    print("\n\n" + "=" * 50)
    print("✅ 测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
