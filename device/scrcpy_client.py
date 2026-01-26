"""Scrcpy客户端 - 手机投屏与控制"""
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage
import numpy as np
from PIL import Image


class ScrcpyMonitorThread(QThread):
    """Scrcpy监控线程"""
    
    # 信号定义
    frame_signal = Signal(QImage)  # 画面帧信号
    status_signal = Signal(str)    # 状态信号
    error_signal = Signal(str)     # 错误信号
    
    def __init__(self, device_ip: str, adb_port: int = 40661):
        super().__init__()
        self.device_ip = device_ip
        self.adb_port = adb_port
        self.client = None
        self._running = False
        self.device_name = f"{device_ip}:{adb_port}"
    
    def run(self):
        """启动投屏监控"""
        self._running = True
        self.status_signal.emit(f"正在连接设备: {self.device_name}...")
        
        try:
            from scrcpy import Client
            
            self.status_signal.emit("正在初始化Scrcpy...")
            
            # 启动Scrcpy客户端
            self.client = Client(
                device=self.device_name,
                max_width=800,
                max_fps=30,
                bitrate=2000000
            )
            
            self.status_signal.emit("✅ Scrcpy客户端已创建")
            
            # 注册帧回调
            self.client.add_listener('frame', self.on_frame)
            
            self.status_signal.emit("✅ 正在启动投屏...")
            
            # 启动客户端（阻塞）
            self.client.start(threaded=True)
            
            self.status_signal.emit("✅ Scrcpy投屏已启动")
            
        except ImportError as e:
            error_msg = f"导入scrcpy失败: {str(e)}\n请运行: pip install git+https://github.com/leng-yue/py-scrcpy-client.git"
            self.error_signal.emit(error_msg)
            self.status_signal.emit("❌ 导入失败")
            
        except Exception as e:
            error_msg = f"Scrcpy启动失败: {str(e)}"
            self.error_signal.emit(error_msg)
            self.status_signal.emit("❌ 连接失败")
    
    def on_frame(self, frame):
        """处理接收到的帧"""
        if frame is not None and self._running:
            try:
                # frame是numpy数组，格式为BGR
                if isinstance(frame, np.ndarray):
                    # BGR -> RGB（使用numpy操作，并确保内存连续）
                    img_rgb = np.ascontiguousarray(frame[:, :, ::-1])  # BGR转RGB并确保连续
                    h, w, ch = img_rgb.shape
                    
                    # 转换为QImage
                    qt_img = QImage(img_rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
                    self.frame_signal.emit(qt_img.copy())  # 使用copy避免内存问题
                
            except Exception as e:
                print(f"[Scrcpy] 帧处理错误: {e}")
    
    def send_touch(self, x: int, y: int, action: int) -> bool:
        """发送触摸事件"""
        if self.client:
            try:
                # action: 0=DOWN, 1=UP, 2=MOVE
                if action == 0:  # DOWN
                    self.client.control.touch(x, y, 'down')
                elif action == 1:  # UP
                    self.client.control.touch(x, y, 'up')
                elif action == 2:  # MOVE
                    self.client.control.touch(x, y, 'move')
                return True
            except Exception as e:
                print(f"[Scrcpy] 触摸事件发送失败: {e}")
                return False
        return False
    
    def send_text(self, text: str) -> bool:
        """发送文本输入"""
        if self.client:
            try:
                self.client.control.text(text)
                return True
            except Exception as e:
                print(f"[Scrcpy] 文本输入失败: {e}")
                return False
        return False
    
    def send_keycode(self, keycode: int) -> bool:
        """发送按键事件"""
        if self.client:
            try:
                self.client.control.keycode(keycode)
                return True
            except Exception as e:
                print(f"[Scrcpy] 按键发送失败: {e}")
                return False
        return False
    
    def stop(self):
        """停止监控"""
        self._running = False
        if self.client:
            try:
                self.client.stop()
                self.status_signal.emit("Scrcpy已停止")
            except Exception as e:
                print(f"[Scrcpy] 停止时出错: {e}")
    
    @property
    def resolution(self):
        """获取分辨率"""
        if self.client and hasattr(self.client, 'resolution'):
            return self.client.resolution
        return None
    
    @property
    def is_running(self) -> bool:
        """是否正在运行"""
        return self._running and self.client is not None
