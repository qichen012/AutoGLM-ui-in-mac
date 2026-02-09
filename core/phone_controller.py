"""手机控制协调器 - 协调投屏显示和AI控制"""
from typing import Optional, Dict, Any
from PyQt5.QtCore import QObject, pyqtSignal as Signal


class PhoneController(QObject):
    """手机控制协调器"""
    
    # 信号定义
    screen_updated = Signal(object)  # 屏幕画面更新
    status_changed = Signal(str)     # 状态变化
    command_executed = Signal(str, bool)  # 命令执行结果 (命令, 是否成功)
    
    def __init__(self):
        super().__init__()
        self._scrcpy_client = None
        self._adb_manager = None
        self._is_connected = False
        self._device_info: Dict[str, Any] = {}
    
    def set_scrcpy_client(self, client) -> None:
        """设置Scrcpy客户端"""
        self._scrcpy_client = client
    
    def set_adb_manager(self, manager) -> None:
        """设置ADB管理器"""
        self._adb_manager = manager
    
    @property
    def is_connected(self) -> bool:
        """是否已连接手机"""
        return self._is_connected
    
    def update_connection_status(self, connected: bool) -> None:
        """更新连接状态"""
        if self._is_connected != connected:
            self._is_connected = connected
            status = "已连接" if connected else "已断开"
            self.status_changed.emit(f"手机 {status}")
    
    def update_screen(self, frame) -> None:
        """更新屏幕画面"""
        self.screen_updated.emit(frame)
    
    def execute_command(self, command: str) -> bool:
        """执行手机控制命令"""
        try:
            if not self._is_connected:
                self.status_changed.emit("⚠️ 手机未连接，无法执行命令")
                return False
            
            # 这里可以添加具体的命令执行逻辑
            # 例如：adb shell命令、点击坐标等
            print(f"[PhoneController] 执行命令: {command}")
            self.command_executed.emit(command, True)
            return True
            
        except Exception as e:
            error_msg = f"命令执行失败: {str(e)}"
            self.status_changed.emit(f"❌ {error_msg}")
            self.command_executed.emit(command, False)
            return False
    
    def get_screen_state(self) -> Dict[str, Any]:
        """获取当前屏幕状态"""
        state = {
            'connected': self._is_connected,
            'device_info': self._device_info,
            'resolution': None
        }
        
        if self._scrcpy_client and hasattr(self._scrcpy_client, 'resolution'):
            state['resolution'] = self._scrcpy_client.resolution
        
        return state
    
    def send_touch(self, x: int, y: int, action: int) -> None:
        """发送触摸事件"""
        if self._scrcpy_client:
            try:
                self._scrcpy_client.control.touch(x, y, action)
            except Exception as e:
                print(f"[PhoneController] 触摸事件发送失败: {e}")
    
    def get_device_info(self) -> Dict[str, Any]:
        """获取设备信息"""
        return self._device_info.copy()
    
    def set_device_info(self, info: Dict[str, Any]) -> None:
        """设置设备信息"""
        self._device_info = info
