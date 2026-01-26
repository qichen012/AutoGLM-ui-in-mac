"""HTTP connection management for accessibility service devices."""

import time
import requests
import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from dotenv import load_dotenv

# 从 .env 文件加载配置
load_dotenv()
DEFAULT_PHONE_IP = os.getenv("device_ip", "10.29.8.38")
DEFAULT_PORT = 8080

class ConnectionType(Enum):
    """Type of connection (kept for compatibility)."""
    USB = "usb"
    WIFI = "wifi"
    REMOTE = "remote"

@dataclass
class DeviceInfo:
    """Information about a connected device."""
    device_id: str          # 这里存 IP 地址
    status: str             # "device" or "offline"
    connection_type: ConnectionType
    model: str | None = "OPPO Assistant" # 伪造一个型号
    android_version: str | None = "14"   # 伪造一个版本

class ADBConnection:
    """
    Manages HTTP connections to the Accessibility App.
    (Named ADBConnection to maintain interface compatibility)
    """

    def __init__(self, adb_path: str = "adb"):
        # adb_path 参数在这里没用，但为了兼容必须留着
        self.current_ip = DEFAULT_PHONE_IP
        self.port = DEFAULT_PORT

    def _get_base_url(self, ip: str = None):
        target = ip if ip else self.current_ip
        return f"http://{target}:{self.port}"

    def connect(self, address: str, timeout: int = 5) -> tuple[bool, str]:
        """
        Check connectivity to the HTTP server.
        Args:
            address: IP address of the phone (e.g., "192.168.1.101")
        """
        # 移除端口号 (如果有的话)，我们固定用 8080
        ip = address.split(":")[0]
        self.current_ip = ip
        
        try:
            # 假设你的 Android App 有一个 /ping 接口用于检测存活
            # 如果没有，用 /info/current_package 也可以
            url = f"{self._get_base_url(ip)}/ping"
            resp = requests.get(url, timeout=timeout)
            
            if resp.status_code == 200:
                return True, f"Connected to {ip}"
            else:
                return False, f"Device responded with status {resp.status_code}"
                
        except requests.exceptions.Timeout:
            return False, f"Connection timeout to {ip}"
        except Exception as e:
            return False, f"Connection error: {e}"

    def disconnect(self, address: str | None = None) -> tuple[bool, str]:
        """
        HTTP 不需要断开连接，为了兼容，直接返回成功。
        """
        return True, "Disconnected (Logical)"

    def list_devices(self) -> list[DeviceInfo]:
        """
        List reachable devices.
        既然不能扫描网络，我们就检查当前的 DEFAULT_PHONE_IP 是否在线。
        """
        devices = []
        
        # 尝试 Ping 一下当前设备
        is_connected, _ = self.connect(self.current_ip, timeout=1)
        
        if is_connected:
            devices.append(
                DeviceInfo(
                    device_id=self.current_ip,  # 用 IP 作为 ID
                    status="device",
                    connection_type=ConnectionType.WIFI,
                    model="OPPO Find X7",       # 可以写死，或者从 HTTP 接口获取
                    android_version="Android 14"
                )
            )
            
        return devices

    def get_device_info(self, device_id: str | None = None) -> DeviceInfo | None:
        """Get detailed information about a device."""
        devices = self.list_devices()
        if not devices:
            return None
        
        # 如果指定了 ID (IP)，找匹配的；否则返回第一个
        if device_id:
            for d in devices:
                if d.device_id == device_id:
                    return d
            return None
            
        return devices[0]

    def is_connected(self, device_id: str | None = None) -> bool:
        """Check if device is reachable."""
        target_ip = device_id if device_id else self.current_ip
        success, _ = self.connect(target_ip, timeout=1)
        return success

    def enable_tcpip(self, port: int = 5555, device_id: str | None = None) -> tuple[bool, str]:
        """
        Compat method. Returns success because we are already wireless.
        """
        return True, "TCP/IP mode handled by App Server"

    def get_device_ip(self, device_id: str | None = None) -> str | None:
        """
        In our case, the device_id IS the IP.
        """
        return device_id if device_id else self.current_ip

    def restart_server(self) -> tuple[bool, str]:
        """No ADB server to restart."""
        return True, "Server check OK"


# --- Helper Functions ---

def quick_connect(address: str) -> tuple[bool, str]:
    conn = ADBConnection()
    return conn.connect(address)

def list_devices() -> list[DeviceInfo]:
    conn = ADBConnection()
    return conn.list_devices()

