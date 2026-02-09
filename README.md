# AutoGLM Cockpit

一个基于 Web 的智能手机控制系统，集成了 scrcpy 投屏和 AutoGLM AI 控制。

## ✨ 功能特性

- **💬 A模式（聊天）**：使用 GLM-4 进行自然对话
- **🤖 B模式（控制）**：通过 AutoGLM 智能控制手机
- **📱 实时投屏**：基于 scrcpy 的低延迟手机投屏
- **🌐 Web 界面**：浏览器访问，跨平台兼容

## 📋 系统要求

- macOS / Linux / Windows
- Python 3.11+
- ADB (Android Debug Bridge)
- scrcpy
- 现代浏览器

## 🚀 快速开始

### 1. 安装依赖

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 AutoGLM
cd AutoGLM-phone/Open-AutoGLM
pip install -e .
cd ../..
```

### 2. 配置

编辑 `config.yaml`：

```yaml
device:
  ip: "192.168.2.13"      # 手机 IP
  adb_port: 34333         # ADB 端口

ai:
  api_key: "your-glm-api-key"   # GLM-4 API 密钥
```

### 3. 连接手机

```bash
# 无线调试配对（Android 11+）
adb pair <IP>:<配对端口>
adb connect <IP>:<调试端口>

# 或通过 USB 启用无线
adb tcpip 5555
adb connect <IP>:5555
```

### 4. 启动服务

```bash
python web_server.py
```

浏览器访问：**http://localhost:5000**

## 📁 项目结构

```
autoglm-ui/
├── web_server.py          # Web 服务器入口
├── templates/             # HTML 模板
├── static/               # CSS & JS
├── ai/                   # AI 模块
├── core/                 # 核心逻辑
├── device/               # 设备控制
└── utils/                # 工具函数
```

详见 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 📖 使用说明

1. **左侧投屏区**
   - 点击"启动投屏"查看手机屏幕
   - 实时显示约 10 FPS

2. **右侧对话区**
   - 切换 A/B 模式
   - 输入消息发送

3. **模式说明**
   - A模式：普通 AI 对话
   - B模式：手机控制指令

## 🛠 技术栈

- **后端**: Flask + SocketIO + Eventlet
- **前端**: HTML5 + CSS3 + JavaScript
- **投屏**: scrcpy + OpenCV
- **AI**: GLM-4 + AutoGLM

## 📄 许可证

MIT License

---

更多详细信息请查看 [WEB_README.md](WEB_README.md)
