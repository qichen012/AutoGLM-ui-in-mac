"""Screenshot utilities via Accessibility Service (HTTP)."""

import base64
import requests
import os
from dataclasses import dataclass
from io import BytesIO
from typing import Tuple
from dotenv import load_dotenv

from PIL import Image

# 从 .env 文件加载配置
load_dotenv()
PHONE_IP = os.getenv("device_ip", "10.29.227.28")
BASE_URL = f"http://{PHONE_IP}:8080"

@dataclass
class Screenshot:
    """Represents a captured screenshot."""
    base64_data: str
    width: int
    height: int
    is_sensitive: bool = False

def get_screenshot(device_id: str | None = None, timeout: int = 10) -> Screenshot:
    """
    Capture a screenshot from the Accessibility Service App via HTTP.
    
    Args:
        device_id: In HTTP mode, this is treated as the IP address (optional).
                   If provided, it overrides the default PHONE_IP.
    """
    # 如果调用方传了 device_id (IP)，就用传进来的，否则用默认的
    target_ip = device_id if device_id else PHONE_IP
    target_url = f"http://{target_ip}:8080/screenshot"

    try:
        # 1. 发送请求给 Android App
        response = requests.get(target_url, timeout=timeout)
        
        # 2. 解析 Android 返回的 JSON 数据
        # 假设 Android 端返回格式: 
        # { "status": "success", "base64": "...", "width": 1080, "height": 2400 }
        # 或者 { "status": "sensitive" }
        if response.status_code == 200:
            data = response.json()
            
            # 处理敏感页面（Android 端截不到图的情况）
            if data.get("status") == "sensitive":
                return _create_fallback_screenshot(is_sensitive=True)
                
            if data.get("status") == "success":
                return Screenshot(
                    base64_data=data["base64"],
                    width=data["width"],
                    height=data["height"],
                    is_sensitive=False
                )
        
        # 如果状态码不对，或者 JSON 解析失败，返回黑屏兜底
        print(f"Screenshot failed, status code: {response.status_code}")
        try:
            print(f"Server Error Message: {response.text}") 
        except:
            pass
        return _create_fallback_screenshot(is_sensitive=False)

    except Exception as e:
        print(f"Screenshot connection error: {e}")
        return _create_fallback_screenshot(is_sensitive=False)

def _create_fallback_screenshot(is_sensitive: bool) -> Screenshot:
    """Create a black fallback image when screenshot fails."""
    default_width, default_height = 1080, 2400

    black_img = Image.new("RGB", (default_width, default_height), color="black")
    buffered = BytesIO()
    black_img.save(buffered, format="PNG")
    base64_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return Screenshot(
        base64_data=base64_data,
        width=default_width,
        height=default_height,
        is_sensitive=is_sensitive,
    )