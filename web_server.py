"""
AutoGLM Cockpit - Web 服务器
基于 Flask + SocketIO 的 Web 界面
"""
import os
import sys
import base64
import threading
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
    adb_connected = adb_manager.is_connected() if adb_manager else False
    return jsonify({
        'adb_connected': adb_connected,
        'mode': current_mode,
        'device': f"{config.get('device', {}).get('ip')}:{config.get('device', {}).get('port')}"
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
    
    try:
        if current_mode == 'normal':
            # A 模式：普通聊天
            response = ""
            for chunk in normal_chat.chat_stream(message):
                response += chunk
                emit('ai_message_chunk', {'chunk': chunk})
            emit('ai_message_complete', {'message': response})
            
        else:
            # B 模式：AutoGLM 控制
            emit('ai_message_chunk', {'chunk': f'🤖 开始执行任务: {message}\n'})
            
            result = autoglm_agent.execute_task(message)
            
            if result.get('success'):
                final_msg = f"✅ 任务完成: {result.get('message', '')}"
            else:
                final_msg = f"❌ 任务失败: {result.get('error', '')}"
            
            emit('ai_message_chunk', {'chunk': final_msg})
            emit('ai_message_complete', {'message': final_msg})
            
    except Exception as e:
        logger.error(f"处理消息时出错: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': f'处理失败: {str(e)}'})


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
    """scrcpy 推流工作线程"""
    try:
        import subprocess
        import cv2
        import numpy as np
        
        device = f"{config.get('device', {}).get('ip')}:{config.get('device', {}).get('port')}"
        
        # 启动 scrcpy 输出到 stdout
        cmd = [
            'scrcpy',
            '--serial', device,
            '--max-size', '800',
            '--video-codec', 'h264',
            '--no-audio',
            '--video-encoder', 'c2.android.avc.encoder',
            '--record', '-',  # 输出到 stdout
            '--no-window'
        ]
        
        logger.info(f"启动 scrcpy: {' '.join(cmd)}")
        
        # 这里简化处理：使用截图方式
        # 完整的视频流需要解析 H264，较复杂
        import time
        while True:
            try:
                # 使用 scrcpy-client 截图
                from scrcpy import Client
                client = Client(device=device, max_width=800)
                client.start()
                
                while client.alive:
                    frame = client.last_frame
                    if frame is not None:
                        # 转换为 JPEG base64
                        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                        jpg_base64 = base64.b64encode(buffer).decode('utf-8')
                        
                        socketio.emit('screen_frame', {'frame': jpg_base64})
                    
                    time.sleep(0.1)  # 10 FPS
                    
            except Exception as e:
                logger.error(f"scrcpy 推流错误: {e}")
                time.sleep(2)
                
    except Exception as e:
        logger.error(f"scrcpy 工作线程错误: {e}")
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
    logger.info(f"设备: {config.get('device', {}).get('ip')}:{config.get('device', {}).get('port')}")
    logger.info("=" * 60)
    
    socketio.run(app, host=host, port=port, debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
