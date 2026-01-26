"""ADB管理器 - 设备连接和命令执行"""
from typing import Optional, List
import subprocess


class ADBManager:
    """ADB管理器"""
    
    def __init__(self, device_id: Optional[str] = None):
        self.device_id = device_id
        self._connected = False
    
    def connect(self, ip: str, port: int = 5555) -> bool:
        """连接到设备"""
        try:
            cmd = f"adb connect {ip}:{port}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if "connected" in result.stdout.lower():
                self.device_id = f"{ip}:{port}"
                self._connected = True
                print(f"[ADB] 连接成功: {self.device_id}")
                return True
            else:
                print(f"[ADB] 连接失败: {result.stdout}")
                return False
                
        except Exception as e:
            print(f"[ADB] 连接异常: {e}")
            return False
    
    def disconnect(self) -> bool:
        """断开连接"""
        if not self.device_id:
            return False
        
        try:
            cmd = f"adb disconnect {self.device_id}"
            subprocess.run(cmd, shell=True, capture_output=True)
            self._connected = False
            print(f"[ADB] 已断开: {self.device_id}")
            return True
        except Exception as e:
            print(f"[ADB] 断开失败: {e}")
            return False
    
    def execute_shell(self, command: str) -> Optional[str]:
        """执行shell命令"""
        if not self._connected:
            print("[ADB] 未连接设备")
            return None
        
        try:
            device_arg = f"-s {self.device_id}" if self.device_id else ""
            cmd = f"adb {device_arg} shell {command}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            print(f"[ADB] 命令执行失败: {e}")
            return None
    
    def get_device_info(self) -> dict:
        """获取设备信息"""
        if not self._connected:
            return {}
        
        info = {}
        try:
            # 获取设备型号
            model = self.execute_shell("getprop ro.product.model")
            if model:
                info['model'] = model
            
            # 获取Android版本
            version = self.execute_shell("getprop ro.build.version.release")
            if version:
                info['android_version'] = version
            
            # 获取SDK版本
            sdk = self.execute_shell("getprop ro.build.version.sdk")
            if sdk:
                info['sdk_version'] = sdk
            
            # 获取分辨率
            size = self.execute_shell("wm size")
            if size and "Physical size:" in size:
                resolution = size.split("Physical size:")[1].strip()
                info['resolution'] = resolution
            
        except Exception as e:
            print(f"[ADB] 获取设备信息失败: {e}")
        
        return info
    
    def list_devices(self) -> List[str]:
        """列出所有连接的设备"""
        try:
            cmd = "adb devices"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            devices = []
            for line in result.stdout.split('\n')[1:]:  # 跳过第一行标题
                if '\tdevice' in line:
                    device_id = line.split('\t')[0].strip()
                    devices.append(device_id)
            
            return devices
        except Exception as e:
            print(f"[ADB] 列出设备失败: {e}")
            return []
    
    def install_apk(self, apk_path: str) -> bool:
        """安装APK"""
        if not self._connected:
            return False
        
        try:
            device_arg = f"-s {self.device_id}" if self.device_id else ""
            cmd = f"adb {device_arg} install -r {apk_path}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            return "Success" in result.stdout
        except Exception as e:
            print(f"[ADB] 安装APK失败: {e}")
            return False
    
    def push_file(self, local_path: str, remote_path: str) -> bool:
        """推送文件到设备"""
        if not self._connected:
            return False
        
        try:
            device_arg = f"-s {self.device_id}" if self.device_id else ""
            cmd = f"adb {device_arg} push {local_path} {remote_path}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            return result.returncode == 0
        except Exception as e:
            print(f"[ADB] 推送文件失败: {e}")
            return False
    
    def pull_file(self, remote_path: str, local_path: str) -> bool:
        """从设备拉取文件"""
        if not self._connected:
            return False
        
        try:
            device_arg = f"-s {self.device_id}" if self.device_id else ""
            cmd = f"adb {device_arg} pull {remote_path} {local_path}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            return result.returncode == 0
        except Exception as e:
            print(f"[ADB] 拉取文件失败: {e}")
            return False
    
    @property
    def is_connected(self) -> bool:
        """是否已连接"""
        return self._connected
