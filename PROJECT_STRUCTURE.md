# 项目结构说明

## 目录说明

### 顶层文件
- **web_server.py** - Flask Web 服务器主入口
- **config.yaml** - 项目配置（设备 IP、API 密钥等）
- **requirements.txt** - Python 依赖列表
- **README.md** - 项目说明
- **WEB_README.md** - Web 版详细使用说明

### templates/ - Web 前端模板
- **index.html** - 主界面HTML（左侧投屏 + 右侧对话）

### static/ - 静态资源
- **css/style.css** - 界面样式
- **js/main.js** - 前端逻辑和WebSocket通信

### ai/ - AI 模块
- **normal_chat.py** - A模式：GLM-4普通对话
- **autoglm_agent.py** - B模式：AutoGLM手机控制

### core/ - 核心业务逻辑
- **mode_manager.py** - 模式切换管理
- **chat_manager.py** - 对话历史管理
- **phone_controller.py** - 手机控制协调器
- **autoglm_executor.py** - AutoGLM任务执行器

### device/ - 设备交互
- **adb_manager.py** - ADB命令封装
- **scrcpy_client.py** - scrcpy投屏客户端

### utils/ - 工具模块
- **config.py** - 配置文件读写
- **logger.py** - 日志初始化

### AutoGLM-phone/ - 外部依赖
- **Open-AutoGLM/** - AutoGLM 手机控制框架

## 数据流

```
浏览器 ←→ WebSocket ←→ Flask Server
                           ↓
                    ┌──────┴──────┐
                    ↓             ↓
               Normal Chat    AutoGLM Agent
                  ↓                ↓
                GLM-4         Phone Agent
```

## 技术架构

### 后端
- Flask: Web 框架
- Flask-SocketIO: WebSocket 支持
- Eventlet: 异步 IO

### 前端
- 原生 HTML/CSS/JavaScript
- Socket.IO: 客户端 WebSocket

### 设备控制
- ADB: Android 调试桥
- scrcpy: 投屏工具
- OpenCV: 图像处理

### AI
- GLM-4: 智谱 AI 对话模型
- AutoGLM: 手机智能控制框架
