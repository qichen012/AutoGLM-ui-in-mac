"""手机投屏显示组件"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap


class PhoneViewer(QWidget):
    """手机投屏显示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.phone_controller = None
        self.scrcpy_client = None
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # 状态标签
        self.status_label = QLabel("等待连接...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #888; font-size: 12px;")
        
        # 手机边框 - 不设置固定大小，让它自适应
        self.phone_frame = QFrame()
        self.phone_frame.setObjectName("PhoneBorder")
        # 移除固定大小，改为最小和最大尺寸约束
        self.phone_frame.setMinimumSize(300, 500)  # 最小尺寸
        self.phone_frame.setMaximumSize(600, 1200)  # 最大尺寸
        self.phone_frame.setStyleSheet("""
            QFrame#PhoneBorder {
                background-color: #000;
                border: 4px solid #333;
                border-radius: 15px;
            }
        """)
        
        # 屏幕显示标签
        frame_layout = QVBoxLayout(self.phone_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        
        self.screen_label = QLabel()
        self.screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 保持宽高比缩放
        self.screen_label.setScaledContents(False)  # 改为False，手动处理缩放
        self.screen_label.setStyleSheet("background-color: #000;")
        
        # 设置鼠标事件
        self.screen_label.mousePressEvent = self._handle_mouse_press
        self.screen_label.mouseReleaseEvent = self._handle_mouse_release
        self.screen_label.mouseMoveEvent = self._handle_mouse_move
        
        frame_layout.addWidget(self.screen_label)
        
        # 添加到主布局
        layout.addWidget(self.status_label)
        layout.addWidget(self.phone_frame, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
    
    def set_phone_controller(self, controller):
        """设置手机控制器"""
        self.phone_controller = controller
    
    def set_scrcpy_client(self, client):
        """设置Scrcpy客户端"""
        self.scrcpy_client = client
    
    def update_screen(self, image: QImage):
        """更新屏幕画面 - 保持宽高比缩放"""
        if image:
            # 获取phone_frame的可用尺寸
            available_width = self.phone_frame.width() - 8  # 减去边框
            available_height = self.phone_frame.height() - 8
            
            # 计算缩放后的尺寸（保持宽高比）
            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(
                available_width, 
                available_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            self.screen_label.setPixmap(scaled_pixmap)
            
            # 第一次收到画面时，调整frame大小以适应实际分辨率
            if not hasattr(self, '_size_adjusted'):
                self._size_adjusted = True
                # 根据实际图像尺寸调整frame
                img_width = image.width()
                img_height = image.height()
                
                # 计算合适的显示尺寸（限制在最大尺寸内）
                max_width = 600
                max_height = 1000
                
                if img_width > max_width or img_height > max_height:
                    scale = min(max_width / img_width, max_height / img_height)
                    display_width = int(img_width * scale)
                    display_height = int(img_height * scale)
                else:
                    display_width = img_width
                    display_height = img_height
                
                self.phone_frame.setFixedSize(display_width + 8, display_height + 8)
    
    def update_status(self, status: str):
        """更新状态文本"""
        self.status_label.setText(status)
    
    def _handle_mouse_press(self, event):
        """处理鼠标按下"""
        self._handle_mouse_event(event, action=0)  # ACTION_DOWN
    
    def _handle_mouse_release(self, event):
        """处理鼠标释放"""
        self._handle_mouse_event(event, action=1)  # ACTION_UP
    
    def _handle_mouse_move(self, event):
        """处理鼠标移动"""
        if event.buttons():  # 只在按下时响应移动
            self._handle_mouse_event(event, action=2)  # ACTION_MOVE
    
    def _handle_mouse_event(self, event, action: int):
        """处理鼠标事件并转换为触摸事件"""
        if not self.scrcpy_client:
            return
        
        # 获取分辨率
        resolution = self.scrcpy_client.resolution if hasattr(self.scrcpy_client, 'resolution') else None
        if not resolution:
            return
        
        w, h = resolution
        
        # 计算真实坐标
        real_x = int((event.position().x() / self.screen_label.width()) * w)
        real_y = int((event.position().y() / self.screen_label.height()) * h)
        
        # 发送触摸事件
        if self.phone_controller:
            self.phone_controller.send_touch(real_x, real_y, action)
