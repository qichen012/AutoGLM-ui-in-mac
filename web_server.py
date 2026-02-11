"""
AutoGLM Cockpit - Web 服务器
基于 Flask + SocketIO 的 Web 界面
"""
# Eventlet monkey patch（必须在最前面）
import eventlet
eventlet.monkey_patch()

import os
import sys
import base64
import threading
import io
from contextlib import redirect_stdout
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# 导入项目模块
from utils.config import load_config
from utils.logger import setup_logger
from ai.normal_chat import NormalChatAI
from ai.autoglm_agent import AutoGLMAgent
from device.adb_manager import ADBManager

# 初始化日志
logger = setup_logger()

# 创建 Flask 应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'autoglm-secret-key-2026'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# 全局变量
config = load_config()
adb_manager = None
normal_chat = None
autoglm_agent = None
scrcpy_thread = None
current_mode = "normal"  # normal 或 autoglm


class RealTimeOutputStream:
    """实时输出流捕获器，用于捕获 AutoGLM 的终端输出"""
    def __init__(self, socketio_instance, original_stdout):
        self.socketio = socketio_instance
        self.original_stdout = original_stdout
        
    def write(self, text):
        """写入数据时同时输出到原始 stdout 并通过 socket 发送"""
        # 写入原始 stdout（保持终端输出）
        self.original_stdout.write(text)
        self.original_stdout.flush()
        
        # 实时发送每个 token，前端负责追加
        if text:
            self.socketio.emit('autoglm_realtime_log', {'content': text})
    
    def flush(self):
        """刷新缓冲区"""
        self.original_stdout.flush()


def init_services():
    """初始化服务"""
    global adb_manager, normal_chat, autoglm_agent
    
    logger.info("初始化服务...")
    
    # 初始化 ADB
    device_ip = config.get('device', {}).get('ip', '192.168.2.13')
    device_port = config.get('device', {}).get('adb_port', 34333)
    device_id = f"{device_ip}:{device_port}"
    adb_manager = ADBManager(device_id=device_id)
    
    # 初始化 GLM 聊天
    api_key = config.get('ai', {}).get('api_key', '')
    normal_chat = NormalChatAI(api_key=api_key)
    normal_chat.initialize()
    
    # 初始化 AutoGLM（延迟初始化）
    autoglm_agent = AutoGLMAgent(device_ip, device_port)
    
    logger.info("服务初始化完成")


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """获取系统状态"""
    adb_connected = adb_manager.is_connected if adb_manager else False
    return jsonify({
        'adb_connected': adb_connected,
        'mode': current_mode,
        'device': f"{config.get('device', {}).get('ip')}:{config.get('device', {}).get('adb_port')}"
    })


@socketio.on('connect')
def handle_connect():
    """客户端连接"""
    logger.info(f"客户端已连接: {request.sid}")
    emit('status', {'message': '已连接到服务器'})


@socketio.on('disconnect')
def handle_disconnect():
    """客户端断开"""
    logger.info(f"客户端已断开: {request.sid}")


@socketio.on('switch_mode')
def handle_switch_mode(data):
    """切换模式"""
    global current_mode
    mode = data.get('mode', 'normal')
    current_mode = mode
    
    logger.info(f"切换到模式: {mode}")
    
    # 如果切换到 autoglm 模式，初始化 agent
    if mode == 'autoglm' and autoglm_agent and not autoglm_agent.is_ready():
        success = autoglm_agent.initialize()
        if not success:
            emit('error', {'message': 'AutoGLM 初始化失败'})
            return
    
    emit('mode_switched', {'mode': mode})


@socketio.on('send_message')
def handle_message(data):
    """处理用户消息"""
    message = data.get('message', '')
    
    if not message:
        return
    
    logger.info(f"收到消息 [{current_mode}]: {message}")
    
    # 先回显用户消息
    emit('user_message', {'message': message})
    
    def process_message():
        """在独立线程中处理消息（避免 eventlet 冲突）"""
        try:
            if current_mode == 'normal':
                # A 模式：普通聊天
                response = ""
                for chunk in normal_chat.stream_chat(message):
                    response += chunk
                    socketio.emit('ai_message_chunk', {'chunk': chunk})
                socketio.emit('ai_message_complete', {'message': response})
                
            else:
                # B 模式：AutoGLM 控制
                socketio.emit('ai_message_chunk', {'chunk': f'🤖 开始执行任务: {message}\n'})
                socketio.emit('autoglm_step', {'type': 'thinking', 'content': f'收到任务指令: {message}'})
                
                # 保存原始 stdout
                original_stdout = sys.stdout
                
                try:
                    # 创建实时输出捕获器
                    realtime_stream = RealTimeOutputStream(socketio, original_stdout)
                    
                    # 重定向 stdout 到我们的捕获器
                    sys.stdout = realtime_stream
                    
                    # 设置步骤回调，实时显示执行过程
                    def step_callback(step_info):
                        # 判断步骤类型
                        if '思考' in step_info or '🤔' in step_info:
                            step_type = 'thinking'
                        elif '执行' in step_info or '⚡' in step_info:
                            step_type = 'action'
                        elif '错误' in step_info or '❌' in step_info:
                            step_type = 'error'
                        else:
                            step_type = 'result'
                        
                        socketio.emit('autoglm_step', {'type': step_type, 'content': step_info})
                    
                    autoglm_agent.set_step_callback(step_callback)
                    
                    # 执行任务（这里的所有 print 输出都会被捕获并实时发送）
                    result = autoglm_agent.execute_task(message)
                    
                finally:
                    # 恢复原始 stdout
                    sys.stdout = original_stdout
                
                if result.get('success'):
                    final_msg = f"✅ 任务完成: {result.get('message', '')}"
                    socketio.emit('autoglm_step', {'type': 'finish', 'content': result.get('message', '')})
                else:
                    final_msg = f"❌ 任务失败: {result.get('error', '')}"
                    socketio.emit('autoglm_step', {'type': 'error', 'content': result.get('error', '')})
                
                socketio.emit('ai_message_chunk', {'chunk': final_msg})
                socketio.emit('ai_message_complete', {'message': final_msg})
                
        except Exception as e:
            logger.error(f"处理消息时出错: {e}")
            import traceback
            traceback.print_exc()
            socketio.emit('error', {'message': f'处理失败: {str(e)}'})
    
    # 在后台线程中处理（避免阻塞 eventlet）
    import threading
    thread = threading.Thread(target=process_message, daemon=True)
    thread.start()


@socketio.on('start_scrcpy')
def handle_start_scrcpy():
    """启动投屏"""
    global scrcpy_thread
    
    if scrcpy_thread and scrcpy_thread.is_alive():
        emit('error', {'message': '投屏已在运行'})
        return
    
    logger.info("启动 scrcpy 投屏...")
    
    # 在新线程中启动 scrcpy 并推流
    scrcpy_thread = threading.Thread(target=scrcpy_stream_worker, daemon=True)
    scrcpy_thread.start()
    
    emit('scrcpy_started', {'message': '投屏已启动'})


def scrcpy_stream_worker():
    """scrcpy 推流工作线程（使用 scrcpy 客户端实时视频流）"""
    import time
    import cv2
    import numpy as np
    
    try:
        from scrcpy import Client
        
        device = f"{config.get('device', {}).get('ip')}:{config.get('device', {}).get('adb_port')}"
        logger.info(f"启动 scrcpy 实时推流，设备: {device}")
        
        # 创建 scrcpy 客户端（1080p分辨率 + 60fps + 高比特率）
        client = Client(device=device, max_width=1080, bitrate=8000000, max_fps=60)
        
        # 启动客户端
        logger.info("正在连接 scrcpy server...")
        client.start(threaded=True)
        
        # 等待连接
        time.sleep(2)
        
        if not client.alive:
            logger.error("scrcpy 客户端启动失败")
            return
        
        logger.info("scrcpy 连接成功，开始推流")
        frame_count = 0
        
        while client.alive:
            try:
                frame = client.last_frame
                
                if frame is not None:
                    # JPEG 最高质量（质量100 + 无色度子采样）
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100,
                                    int(cv2.IMWRITE_JPEG_OPTIMIZE), 1,
                                    int(cv2.IMWRITE_JPEG_PROGRESSIVE), 1]
                    _, buffer = cv2.imencode('.jpg', frame, encode_param)
                    img_base64 = base64.b64encode(buffer).decode('utf-8')
                    
                    # 通过 WebSocket 推送
                    socketio.emit('screen_frame', {'frame': img_base64})
                    
                    frame_count += 1
                    if frame_count % 100 == 0:
                        logger.info(f"已推送 {frame_count} 帧")
                
                # 60 FPS（尽可能流畅）
                time.sleep(1.0 / 60)
                
            except Exception as e:
                logger.error(f"帧处理错误: {e}")
                time.sleep(0.5)
        
        logger.info("scrcpy 客户端已停止")
        
    except ImportError:
        logger.error("未安装 scrcpy 客户端库，请运行: pip install git+https://github.com/leng-yue/py-scrcpy-client.git")
    except Exception as e:
        logger.error(f"scrcpy 推流错误: {e}")
        import traceback
        traceback.print_exc()


@socketio.on('adb_connect')
def handle_adb_connect():
    """连接 ADB"""
    if adb_manager:
        success = adb_manager.connect()
        if success:
            emit('adb_status', {'connected': True, 'message': 'ADB 已连接'})
        else:
            emit('adb_status', {'connected': False, 'message': 'ADB 连接失败'})


def main():
    """启动服务器"""
    init_services()
    
    host = '0.0.0.0'
    port = 5000
    
    logger.info("=" * 60)
    logger.info("AutoGLM Cockpit Web 服务器启动")
    logger.info(f"访问地址: http://localhost:{port}")
    logger.info(f"设备: {config.get('device', {}).get('ip')}:{config.get('device', {}).get('adb_port')}")
    logger.info("=" * 60)
    
    socketio.run(app, host=host, port=port, debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
