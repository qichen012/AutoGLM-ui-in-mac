"""对话管理器 - 管理对话历史和消息路由"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Message:
    """消息数据类"""
    role: str  # 'user', 'assistant', 'system', 'log'
    content: str
    timestamp: datetime
    mode: str  # 'chat' or 'control'
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'mode': self.mode
        }


class ChatManager:
    """对话管理器"""
    
    def __init__(self, max_history: int = 100):
        self._history: List[Message] = []
        self._max_history = max_history
    
    def add_message(self, role: str, content: str, mode: str = 'chat') -> Message:
        """添加消息到历史记录"""
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            mode=mode
        )
        self._history.append(message)
        
        # 限制历史记录长度
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]
        
        return message
    
    def get_history(self, limit: Optional[int] = None) -> List[Message]:
        """获取对话历史"""
        if limit:
            return self._history[-limit:]
        return self._history.copy()
    
    def get_context_for_ai(self, limit: int = 10) -> List[dict]:
        """获取用于AI的上下文（只包含用户和助手消息）"""
        messages = []
        for msg in self._history[-limit:]:
            if msg.role in ['user', 'assistant']:
                messages.append({
                    'role': msg.role,
                    'content': msg.content
                })
        return messages
    
    def clear_history(self) -> None:
        """清空对话历史"""
        self._history.clear()
    
    def add_user_message(self, content: str, mode: str = 'chat') -> Message:
        """添加用户消息"""
        return self.add_message('user', content, mode)
    
    def add_assistant_message(self, content: str, mode: str = 'chat') -> Message:
        """添加助手消息"""
        return self.add_message('assistant', content, mode)
    
    def add_system_message(self, content: str, mode: str = 'chat') -> Message:
        """添加系统消息"""
        return self.add_message('system', content, mode)
    
    def add_log_message(self, content: str, mode: str = 'chat') -> Message:
        """添加日志消息"""
        return self.add_message('log', content, mode)
