# AutoGLM Cockpit Web 版本

## 快速开始

### 1. 安装依赖

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装 Web 依赖
pip install flask flask-socketio flask-cors python-socketio eventlet

# 安装其他依赖
pip install -r requirements.txt
```

### 2. 配置设备

编辑 `config.yaml` 设置手机 IP 和端口：

```yaml
device:
  ip: "192.168.2.13"
  port: 34333
```

### 3. 连接手机

```bash
# 方式 1：USB 配对后无线连接
adb tcpip 5555
adb connect <手机IP>:5555

# 方式 2：无线调试（Android 11+）
# 手机：设置 → 开发者选项 → 无线调试 → 配对
adb pair <IP>:<配对端口>
adb connect <IP>:<调试端口>
```

### 4. 启动服务器

```bash
python web_server.py
```

然后在浏览器访问：**http://localhost:5000**

## 功能说明

### 左侧：手机投屏
- 点击"启动投屏"按钮开始 scrcpy 投屏
- 实时显示手机屏幕（约 10 FPS）

### 右侧：AI 对话
- **A 模式（聊天）**：使用 GLM-4 进行普通对话
- **B 模式（控制）**：使用 AutoGLM 控制手机

## 技术栈

- 后端：Flask + SocketIO
- 前端：原生 HTML/CSS/JavaScript
- 通信：WebSocket 实时双向通信
- 投屏：scrcpy + base64 图像流

## 优点

✅ 无 Qt 依赖，避免 macOS 兼容性问题  
✅ 跨平台，手机/平板浏览器也能访问  
✅ 调试方便（浏览器 F12）  
✅ 部署灵活（可做成远程服务）

## 故障排除

### Flask 安装超时
如果网络超时，可以使用镜像源：
```bash
pip install flask flask-socketio -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### scrcpy 未找到
确保已安装 scrcpy：
```bash
brew install scrcpy
```

### ADB 连接失败
检查手机和电脑在同一网络，并确认：
```bash
adb devices  # 应该能看到你的设备
```
