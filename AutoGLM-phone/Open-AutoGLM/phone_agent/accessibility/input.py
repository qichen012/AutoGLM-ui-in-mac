import requests
import time
import os
from typing import Optional
from dotenv import load_dotenv

# 从 .env 文件加载配置
load_dotenv()
DEVICE_IP = os.getenv("device_ip", "192.168.2.10")

PORT = 8080

def _parse_device_ip(device_id: str | None) -> str:
    """从 device_id 中提取 IP 地址（去除端口号）。"""
    if not device_id:
        return DEVICE_IP
    # 如果 device_id 包含端口（格式: ip:port），只取 IP 部分
    if ':' in device_id:
        return device_id.split(':')[0]
    return device_id

def type_text(text: str, device_ip: str = DEVICE_IP, timeout: int = 5) -> bool:
    """
    发送文本输入指令到 Android 设备。
    
    Args:
        text: 要输入的文本内容（支持中文、英文、符号）。
        device_ip: 手机的 IP 地址。
        timeout: 请求超时时间。

    Returns:
        bool: 输入是否成功。
    """
    if not text:
        print("❌ Error: Input text cannot be empty.")
        return False

    # 构造请求 URL
    url = f"http://{device_ip}:{PORT}/action"
    
    # 构造参数
    # requests 库非常智能，它会自动把中文转成 URL 编码
    # 例如："你好" -> "%E4%BD%A0%E5%A5%BD"
    params = {
        "type": "input",
        "text": text
    }

    try:
        print(f"⌨️ Sending input command: '{text}' to {device_ip}...")
        
        # 发送 GET 请求
        response = requests.get(url, params=params, timeout=timeout)
        
        # 检查响应
        if response.status_code == 200:
            print(f"✅ Input Success: Device responded '{response.text}'")
            return True
        elif response.status_code == 500:
            # 这是我们在 Android 端定义的错误（找不到焦点）
            print("❌ Input Failed: Device returned 500.")
            print("👉 Possible Reason: No input field is focused. (Did you TAP the input box first?)")
            return False
        else:
            print(f"❌ Input Failed: Unknown status {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Refused: Is the App running on {device_ip}?")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout: Device took too long to respond.")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

# --- 单元测试代码 (直接运行这个文件时会执行) ---
if __name__ == "__main__":
    # 这里的 IP 记得换成你手机的
    target_ip = "10.29.227.28" 
    
    print("🚀 Testing Input Module...")
    print("⚠️ 请确保手机屏幕是亮着的，并且你已经【点击】了一个输入框（光标在闪烁）！")
    print("等待 3 秒给你时间准备...")
    time.sleep(3)
    
    # 测试输入中文
    type_text("你好AutoGLM", device_ip=target_ip)