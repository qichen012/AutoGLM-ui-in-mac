"""AI对话面板组件"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QTextEdit, QLineEdit, QPushButton, QLabel)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCursor


class ChatPanel(QWidget):
    """AI对话面板组件"""
    
    # 信号定义
    message_sent = Signal(str)  # 发送消息信号
    mode_switched = Signal(str)  # 模式切换信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_mode = "chat"  # 默认为对话模式
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 顶部：标题和模式切换
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("🤖 AI助手")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e0e0e0;")
        
        self.mode_indicator = QLabel("💬 对话模式")
        self.mode_indicator.setStyleSheet("font-size: 12px; color: #888;")
        
        self.mode_btn = QPushButton("切换到控制模式")
        self.mode_btn.setFixedWidth(140)
        self.mode_btn.clicked.connect(self._on_mode_toggle)
        
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.mode_indicator)
        header_layout.addStretch()
        header_layout.addWidget(self.mode_btn)
        
        # 中部：对话历史
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #e0e0e0;
            }
        """)
        
        # 底部：输入框和发送按钮
        input_layout = QHBoxLayout()
        
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("输入消息...")
        self.input_box.returnPressed.connect(self._on_send_message)
        self.input_box.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #333;
                border-radius: 20px;
                padding: 10px 15px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #007acc;
            }
        """)
        
        self.send_btn = QPushButton("发送")
        self.send_btn.setFixedWidth(80)
        self.send_btn.clicked.connect(self._on_send_message)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0098ff;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_btn)
        
        # 组装布局
        layout.addLayout(header_layout)
        layout.addWidget(self.chat_history)
        layout.addLayout(input_layout)
    
    def _on_send_message(self):
        """发送消息"""
        text = self.input_box.text().strip()
        if text:
            self.message_sent.emit(text)
            self.input_box.clear()
    
    def _on_mode_toggle(self):
        """切换模式"""
        new_mode = "control" if self.current_mode == "chat" else "chat"
        self.set_mode(new_mode)
        self.mode_switched.emit(new_mode)
    
    def set_mode(self, mode: str):
        """设置模式"""
        self.current_mode = mode
        
        if mode == "control":
            self.mode_indicator.setText("🤖 控制模式")
            self.mode_btn.setText("切换到对话模式")
            self.input_box.setPlaceholderText("输入控制指令（如：打开微信）...")
        else:
            self.mode_indicator.setText("💬 对话模式")
            self.mode_btn.setText("切换到控制模式")
            self.input_box.setPlaceholderText("输入消息...")
    
    def append_message(self, role: str, content: str, is_user: bool = False):
        """添加消息到历史"""
        if role == "user":
            color = "#007acc"
            align = "right"
            name = "我"
        elif role == "assistant":
            color = "#444444"
            align = "left"
            name = "AI"
        elif role == "log":
            # 日志消息
            self.chat_history.append(
                f"<div style='text-align:center; margin:5px;'>"
                f"<span style='color:#666; font-size:12px;'>{content}</span>"
                f"</div>"
            )
            self._scroll_to_bottom()
            return
        else:
            color = "#555555"
            align = "left"
            name = "系统"
        
        html = (
            f"<div style='text-align:{align}; margin:8px;'>"
            f"<span style='background:{color}; color:white; padding:10px 15px; "
            f"border-radius:12px; display:inline-block; max-width:70%;'>"
            f"<b>{name}:</b> {content}"
            f"</span>"
            f"</div>"
        )
        
        self.chat_history.append(html)
        self._scroll_to_bottom()
    
    def append_streaming_text(self, text: str):
        """追加流式文本（用于AI逐字输出）"""
        cursor = self.chat_history.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        self.chat_history.setTextCursor(cursor)
        self._scroll_to_bottom()
    
    def clear_history(self):
        """清空对话历史"""
        self.chat_history.clear()
    
    def _scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.chat_history.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
