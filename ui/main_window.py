"""主窗口"""
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

from ui.phone_viewer import PhoneViewer
from ui.chat_panel import ChatPanel
from core.mode_manager import ModeManager, Mode
from core.chat_manager import ChatManager
from core.phone_controller import PhoneController
from core.autoglm_executor import AutoGLMExecutor
from device.scrcpy_client import ScrcpyMonitorThread
from device.adb_manager import ADBManager
from ai.normal_chat import NormalChatAI
from ai.autoglm_agent import AutoGLMAgent


class AIWorkerThread(QThread):
    """AI工作线程（避免阻塞UI）"""
    
    reply_signal = Signal(str)  # 回复信号
    log_signal = Signal(str)    # 日志信号
    
    def __init__(self, ai_service, message: str, context=None):
        super().__init__()
        self.ai_service = ai_service
        self.message = message
        self.context = context
    
    def run(self):
        """执行AI任务"""
        try:
            response = self.ai_service.chat(self.message, self.context)
            self.reply_signal.emit(response)
        except Exception as e:
            self.reply_signal.emit(f"❌ AI服务错误: {str(e)}")


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        
        # 核心组件
        self.mode_manager = ModeManager()
        self.chat_manager = ChatManager(max_history=config['ai']['max_history'])
        self.phone_controller = PhoneController()
        
        # AI服务
        self.normal_ai = NormalChatAI(
            model=config['ai']['chat_model'],
            api_key=config['ai'].get('api_key')
        )
        # 使用新的 AutoGLM 执行器（独立虚拟环境）
        self.autoglm_executor = AutoGLMExecutor()
        # 连接信号
        self.autoglm_executor.output_received.connect(self.on_autoglm_output)
        self.autoglm_executor.task_completed.connect(self.on_autoglm_completed)
        
        # 设备组件
        self.scrcpy_thread = None
        self.adb_manager = ADBManager()
        
        # AI工作线程
        self.ai_worker = None
        
        self.setup_ui()
        self.setup_connections()
        self.initialize_services()
    
    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("AutoGLM Cockpit - 手机智能控制系统")
        self.resize(
            self.config['ui']['window_width'],
            self.config['ui']['window_height']
        )
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QWidget {
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                color: #e0e0e0;
            }
        """)
        
        # 中心部件
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QHBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 左侧：手机投屏区
        self.phone_viewer = PhoneViewer()
        self.phone_viewer.set_phone_controller(self.phone_controller)
        
        # 右侧：AI对话区
        self.chat_panel = ChatPanel()
        
        layout.addWidget(self.phone_viewer, 4)
        layout.addWidget(self.chat_panel, 6)
    
    def setup_connections(self):
        """设置信号连接"""
        # 对话面板信号
        self.chat_panel.message_sent.connect(self.on_message_sent)
        self.chat_panel.mode_switched.connect(self.on_mode_switched)
        
        # 手机控制器信号
        self.phone_controller.status_changed.connect(self.phone_viewer.update_status)
        
        # 模式管理器回调
        self.mode_manager.set_mode_changed_callback(self.on_mode_changed)
    
    def initialize_services(self):
        """初始化服务"""
        # 初始化AI服务
        if not self.normal_ai.initialize():
            self.chat_panel.append_message("log", "⚠️ 普通对话AI初始化失败")
        
        # 先连接ADB设备
        self.connect_adb_device()
        
        # 启动Scrcpy投屏
        self.start_scrcpy()
        
        # 显示欢迎消息
        self.chat_panel.append_message(
            "assistant",
            "你好！我是AutoGLM助手。\n\n"
            "💬 对话模式：与我自由对话\n"
            "🤖 控制模式：通过自然语言控制你的手机\n\n"
            "点击右上角按钮切换模式。"
        )
    
    def connect_adb_device(self):
        """连接ADB设备"""
        device_ip = self.config['device']['ip']
        adb_port = self.config['device']['adb_port']
        
        self.chat_panel.append_message("log", f"📱 正在通过ADB连接设备: {device_ip}:{adb_port}...")
        
        if self.adb_manager.connect(device_ip, adb_port):
            self.chat_panel.append_message("log", "✅ ADB连接成功")
            
            # 获取设备信息
            device_info = self.adb_manager.get_device_info()
            if device_info:
                info_text = f"📱 设备: {device_info.get('model', 'Unknown')}"
                if 'android_version' in device_info:
                    info_text += f" | Android {device_info['android_version']}"
                if 'resolution' in device_info:
                    info_text += f" | {device_info['resolution']}"
                self.chat_panel.append_message("log", info_text)
        else:
            self.chat_panel.append_message("log", "⚠️ ADB连接失败，投屏可能无法正常工作")
    
    def start_scrcpy(self):
        """启动Scrcpy投屏"""
        device_ip = self.config['device']['ip']
        adb_port = self.config['device']['adb_port']
        
        self.scrcpy_thread = ScrcpyMonitorThread(device_ip, adb_port)
        
        # 连接信号
        self.scrcpy_thread.frame_signal.connect(self.phone_viewer.update_screen)
        self.scrcpy_thread.status_signal.connect(self.phone_viewer.update_status)
        self.scrcpy_thread.error_signal.connect(lambda msg: self.chat_panel.append_message("log", msg))
        
        # 设置到组件
        self.phone_viewer.set_scrcpy_client(self.scrcpy_thread)
        self.phone_controller.set_scrcpy_client(self.scrcpy_thread)
        
        # 启动线程
        self.scrcpy_thread.start()
        self.chat_panel.append_message("log", f"🖥️ 正在启动投屏: {device_ip}:{adb_port}...")
    
    def on_message_sent(self, message: str):
        """处理发送的消息"""
        # 添加到聊天历史
        self.chat_manager.add_user_message(message, self.mode_manager.current_mode.value)
        self.chat_panel.append_message("user", message, is_user=True)
        
        # 根据模式路由到不同的AI服务
        if self.mode_manager.is_chat_mode():
            self.handle_chat_mode(message)
        else:
            self.handle_control_mode(message)
    
    def handle_chat_mode(self, message: str):
        """处理对话模式"""
        self.chat_panel.append_message("log", "AI正在思考...")
        
        # 获取上下文
        context = self.chat_manager.get_context_for_ai(limit=10)
        
        # 启动AI工作线程
        self.ai_worker = AIWorkerThread(self.normal_ai, message, context)
        self.ai_worker.reply_signal.connect(self.on_ai_reply)
        self.ai_worker.start()
    
    def handle_control_mode(self, message: str):
        """处理控制模式 - 使用独立虚拟环境中的 AutoGLM"""
        # 检查环境
        env_ok, env_msg = self.autoglm_executor.check_environment()
        if not env_ok:
            self.chat_panel.append_message("assistant", f"❌ AutoGLM 环境检查失败: {env_msg}")
            return
        
        # 执行任务（后台运行）
        success = self.autoglm_executor.execute_task(message, background=True)
        if not success:
            self.chat_panel.append_message("assistant", "❌ 无法启动 AutoGLM 任务")
    
    def on_autoglm_output(self, output: str):
        """处理 AutoGLM 输出"""
        # 将 AutoGLM 的输出显示为日志
        self.chat_panel.append_message("log", output)
    
    def on_autoglm_completed(self, success: bool, result: str):
        """处理 AutoGLM 任务完成"""
        if success:
            msg = f"✅ 任务完成: {result}"
            self.chat_panel.append_message("assistant", msg)
            self.chat_manager.add_assistant_message(msg, 'control')
        else:
            msg = f"❌ 任务失败: {result}"
            self.chat_panel.append_message("assistant", msg)
            self.chat_manager.add_assistant_message(msg, 'control')
    
    def on_ai_reply(self, reply: str):
        """处理AI回复"""
        self.chat_panel.append_message("assistant", reply)
        self.chat_manager.add_assistant_message(reply, 'chat')
    
    def on_mode_switched(self, mode: str):
        """处理模式切换"""
        new_mode = Mode.CONTROL if mode == "control" else Mode.CHAT
        self.mode_manager.switch_mode(new_mode)
    
    def on_mode_changed(self, mode: Mode):
        """模式改变回调"""
        mode_name = self.mode_manager.get_mode_display_name()
        self.chat_panel.append_message("log", f"已切换到: {mode_name}")
    
    def closeEvent(self, event):
        """关闭事件"""
        # 停止Scrcpy
        if self.scrcpy_thread:
            self.scrcpy_thread.stop()
            self.scrcpy_thread.wait()
        
        # 断开ADB
        if self.adb_manager.is_connected:
            self.adb_manager.disconnect()
        
        event.accept()
