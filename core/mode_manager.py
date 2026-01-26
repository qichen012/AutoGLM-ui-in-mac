"""模式管理器 - 负责A/B模式的切换和状态管理"""
from enum import Enum
from typing import Callable, Optional


class Mode(Enum):
    """运行模式枚举"""
    CHAT = "chat"      # A模式：普通对话
    CONTROL = "control"  # B模式：手机控制


class ModeManager:
    """模式管理器"""
    
    def __init__(self):
        self._current_mode: Mode = Mode.CHAT
        self._on_mode_changed: Optional[Callable[[Mode], None]] = None
    
    @property
    def current_mode(self) -> Mode:
        """获取当前模式"""
        return self._current_mode
    
    def switch_mode(self, mode: Mode) -> None:
        """切换模式"""
        if self._current_mode != mode:
            old_mode = self._current_mode
            self._current_mode = mode
            print(f"[ModeManager] 模式切换: {old_mode.value} -> {mode.value}")
            
            # 触发回调
            if self._on_mode_changed:
                self._on_mode_changed(mode)
    
    def is_control_mode(self) -> bool:
        """是否为控制模式"""
        return self._current_mode == Mode.CONTROL
    
    def is_chat_mode(self) -> bool:
        """是否为对话模式"""
        return self._current_mode == Mode.CHAT
    
    def set_mode_changed_callback(self, callback: Callable[[Mode], None]) -> None:
        """设置模式切换回调"""
        self._on_mode_changed = callback
    
    def get_mode_display_name(self) -> str:
        """获取当前模式的显示名称"""
        return "🤖 手机控制模式" if self.is_control_mode() else "💬 普通对话模式"
