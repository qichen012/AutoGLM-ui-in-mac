"""Accessibility Service implementation for Android device interaction."""

# 1. 从 connection.py 导入
# 注意：我们导入了那个"别名" ADBConnection，骗过上层代码
from .connection import (
    ADBConnection,       # 这是其实是 AccessibilityConnection
    ConnectionType,
    DeviceInfo,
    list_devices,
    quick_connect,
)

# 2. 从 device.py 导入
from .device import (
    back,
    double_tap,
    get_current_app,
    home,
    launch_app,
    long_press,
    swipe,
    tap,
)

# 3. 从 screenshot.py 导入
from .screenshot import get_screenshot

# =========================================================
# 4. 兼容性处理 (Input 模块)
# 因为我们删掉了复杂的 input.py (ADB键盘)，但上层代码可能还会调用
# 所以在这里定义一些"空函数"或者"简单转发"，防止报错
# =========================================================

from .device import _send_cmd  # 复用 device.py 里的发送函数

def type_text(text: str, device_id: str | None = None) -> None:
    """
    HTTP version of type_text.
    Sends text directly to the Accessibility Service.
    """
    # 📢 1. 抓嫌疑人：看看代码有没有跑到这里
    print(f"\n[Debug] 正在执行 accessibility.type_text...")
    print(f"[Debug] 目标IP: {device_id}, 内容: {text}")

    # 发送指令
    # 这里的 "type": "input" 必须和你 Android 代码里的 if (type == "input") 完美匹配
    _send_cmd("action", {"type": "input", "text": text}, device_id=device_id)
    
    # 📢 2. 确认开火：表示请求已通过 requests 发出
    print(f"[Debug] 指令已发送给 _send_cmd\n")

def clear_text(device_id: str | None = None) -> None:
    """HTTP version of clear_text."""
    _send_cmd("action", {"type": "clear"}, device_id=device_id)

def detect_and_set_adb_keyboard(device_id: str | None = None) -> str:
    """
    Dummy function for compatibility.
    Accessibility service doesn't need to switch keyboards.
    """
    return "dummy.ime"

def restore_keyboard(ime: str, device_id: str | None = None) -> None:
    """Dummy function for compatibility."""
    pass


# =========================================================
# 5. 定义导出列表 (保持与官方完全一致)
# =========================================================
__all__ = [
    # Screenshot
    "get_screenshot",
    # Input (我们在上面重新实现了简化版)
    "type_text",
    "clear_text",
    "detect_and_set_adb_keyboard",
    "restore_keyboard",
    # Device control
    "get_current_app",
    "tap",
    "swipe",
    "back",
    "home",
    "double_tap",
    "long_press",
    "launch_app",
    # Connection management
    "ADBConnection",
    "DeviceInfo",
    "ConnectionType",
    "quick_connect",
    "list_devices",
]