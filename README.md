# 🚀 AutoGLM Cockpit Web

<div align="center">

**基于 Web 的智能手机 AI 控制平台**

集成实时投屏 • AI 对话 • 手机智能控制

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[功能特性](#✨-功能特性) • [快速开始](#🚀-快速开始) • [使用指南](#📖-使用指南) • [架构设计](#🏗️-架构设计)

</div>

---

## 📸 产品预览

### 主界面 - 双模式操作
![主界面截图](data/01.png)

**左侧：** 实时手机投屏 (1080p@60fps)  
**右侧：** AI 智能助手（双模式切换）

### B模式 - 智能控制执行
![B模式执行过程](data/02.png)

**上半部分：** 任务对话输入区  
**下半部分：** AutoGLM 实时执行过程可视化

---

## ✨ 功能特性

### 🎯 核心功能

| 功能模块 | 说明 | 技术亮点 |
|---------|------|---------|
| 💬 **A模式 - AI对话** | 基于GLM-4的智能对话系统 | 支持流式输出，实时响应 |
| 🤖 **B模式 - 智能控制** | AutoGLM驱动的手机自动化 | 视觉理解+操作执行，自然语言控制 |
| 📱 **实时投屏** | scrcpy超低延迟视频流 | 1080p分辨率，60fps流畅度 |
| 🔄 **执行可视化** | 实时显示AI思考与操作 | 分步骤展示，过程透明 |

### 🌟 技术亮点

- **🚄 高性能投屏**
  - 基于 scrcpy 原生视频流，延迟 < 100ms
  - 支持 1080p/60fps 高清流畅显示
  - JPEG 高质量编码 + CSS 渲染优化

- **🧠 双模式 AI 引擎**
  - **A模式**：GLM-4 流式对话，支持多轮交互
  - **B模式**：AutoGLM 视觉智能体，自主手机控制

- **🎨 现代化 Web UI**
  - 响应式布局，自适应屏幕尺寸
  - WebSocket 实时通信，无刷新交互
  - 动画流畅，用户体验优秀

- **🔌 灵活架构**
  - 前后端分离，易于扩展
  - 模块化设计，清晰的代码组织
  - 支持多设备并发（未来扩展）

---

## 🏗️ 架构设计

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     浏览器客户端                              │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  左侧：手机投屏   │         │  右侧：AI 控制台  │          │
│  │  • scrcpy 视频   │         │  • 模式切换       │          │
│  │  • 实时显示      │         │  • 对话输入       │          │
│  │                  │         │  • 执行过程       │          │
│  └──────────────────┘         └──────────────────┘          │
└────────────┬─────────────────────────┬─────────────────────┘
             │    WebSocket (Socket.IO) │
             │                          │
┌────────────▼──────────────────────────▼─────────────────────┐
│                 Flask Web Server                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ 投屏服务      │  │ A模式 GLM-4  │  │ B模式 AutoGLM│      │
│  │ scrcpy Client│  │ Normal Chat  │  │ Phone Agent  │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                  │               │
│         │                 │                  │               │
│  ┌──────▼─────────────────▼──────────────────▼──────┐       │
│  │          ADB Manager (设备控制层)                 │       │
│  └──────────────────────┬───────────────────────────┘       │
└─────────────────────────┼─────────────────────────────────────┘
                          │ ADB over TCP
                          │
              ┌───────────▼───────────┐
              │   Android 手机设备     │
              │   192.168.2.13:34333  │
              └───────────────────────┘
```

### 数据流详解

1. **投屏流程**（左侧显示）
   ```
   手机屏幕 → scrcpy Server (手机端) 
           → scrcpy Client (服务器) 
           → JPEG 编码 
           → WebSocket 推送 
           → 浏览器显示
   ```

2. **A模式对话流程**
   ```
   用户输入 → Flask 后端 
           → GLM-4 API (流式) 
           → 逐字返回 
           → 浏览器显示
   ```

3. **B模式控制流程**
   ```
   用户指令 → AutoGLM Agent 
           → ADB 截图 
           → GLM 视觉分析 
           → 生成操作 
           → ADB 执行 
           → 反馈结果
   ```

---

## 📋 系统要求

### 必备环境

- **操作系统**: macOS / Linux / Windows
- **Python**: 3.11 或更高版本
- **ADB**: Android Debug Bridge（用于手机通信）
- **scrcpy**: 手机投屏工具
- **浏览器**: Chrome / Firefox / Safari / Edge（现代浏览器）

### Android 手机要求

- Android 5.0+ (推荐 Android 11+)
- 开启开发者选项 + USB 调试
- 支持无线调试（Android 11+ 推荐）

---

## 🚀 快速开始

### 1️⃣ 克隆项目

```bash
git clone <repository-url>
cd autoglm-ui
```

### 2️⃣ 安装系统依赖

**macOS:**
```bash
brew install android-platform-tools scrcpy
```

**Ubuntu/Debian:**
```bash
sudo apt install android-tools-adb scrcpy
```

**Windows:**
- 下载 [ADB Platform Tools](https://developer.android.com/studio/releases/platform-tools)
- 下载 [scrcpy](https://github.com/Genymobile/scrcpy/releases)

### 3️⃣ 安装 Python 依赖

```bash
# 创建并激活虚拟环境
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装 AutoGLM（B模式必需）
cd AutoGLM-phone/Open-AutoGLM
pip install -e .
cd ../..
```

### 4️⃣ 配置文件

编辑 `config.yaml`：

```yaml
device:
  ip: "192.168.2.13"          # 手机的 IP 地址
  adb_port: 34333             # ADB 无线调试端口

ai:
  api_key: "your-api-key"     # 智谱 GLM API 密钥
  model: "glm-4"              # 模型名称
```

**获取 API 密钥**: [智谱开放平台](https://open.bigmodel.cn/)

### 5️⃣ 连接手机

**方法1：无线调试（Android 11+ 推荐）**

1. 手机进入：设置 → 开发者选项 → 无线调试
2. 点击"使用配对码配对设备"
3. 在电脑执行：
   ```bash
   adb pair <IP>:<配对端口>
   # 输入配对码
   
   adb connect <IP>:<调试端口>
   ```

**方法2：USB 转无线**

```bash
# USB 连接手机后
adb tcpip 5555
adb connect <手机IP>:5555
```

**验证连接：**
```bash
adb devices
# 应该显示: <IP>:<端口>  device
```

### 6️⃣ 启动服务

```bash
python web_server.py
```

看到以下输出表示启动成功：
```
[autoglm-ui] [INFO] ======================================
[autoglm-ui] [INFO] AutoGLM Cockpit Web 服务器启动
[autoglm-ui] [INFO] 访问地址: http://localhost:5000
[autoglm-ui] [INFO] 设备: 192.168.2.13:34333
[autoglm-ui] [INFO] ======================================
```

### 7️⃣ 打开浏览器

访问：**http://localhost:5000**

---

## 📖 使用指南

### 界面布局

```
┌─────────────────────────────────────────────────────────┐
│                    AutoGLM Cockpit                      │
├─────────────────────┬───────────────────────────────────┤
│  📱 手机投屏         │  🤖 AI 助手                       │
│                    │  ┌───────┬───────┐                │
│                    │  │ A模式  │ B模式  │                │
│                    │  └───────┴───────┘                │
│                    │                                   │
│  [手机屏幕实时画面]  │  [对话消息区域]                   │
│                    │                                   │
│                    │  ┌─────────────────────┐          │
│  [启动投屏]         │  │ 输入消息...          │          │
│                    │  └─────────────────────┘          │
│                    │  [发送]                           │
└─────────────────────┴───────────────────────────────────┘
```

### 操作步骤

#### 🎬 启动投屏

1. 点击左侧"启动投屏"按钮
2. 等待连接（约2-3秒）
3. 手机屏幕实时显示在左侧面板

**投屏参数**：
- 分辨率：1080p
- 帧率：60 FPS
- 编码：JPEG (质量100)
- 延迟：< 100ms

#### 💬 A模式 - AI对话

1. 点击右侧"A模式: 聊天"
2. 在输入框输入消息
3. 按 Enter 发送（Shift+Enter 换行）
4. AI 实时流式回复

**使用场景**：
- 日常对话交流
- 问题咨询
- 创意写作
- 代码辅助

#### 🤖 B模式 - 智能控制

1. 点击右侧"B模式: 控制"
2. 界面自动分为上下两部分：
   - **上半部分**：输入任务指令
   - **下半部分**：执行过程可视化
3. 输入手机控制指令，例如：
   - "打开微信"
   - "发送消息给张三"
   - "打开设置并调整音量"
4. 观察下半部分的执行过程：
   - 🤔 **思考步骤**：AI 分析任务
   - ⚡ **执行操作**：实际操作手机
   - ✅ **执行结果**：任务完成反馈

**执行流程可视化**：
```
🤔 思考中: 分析用户指令
📱 正在获取手机屏幕状态...
🤖 调用AI模型分析任务
⚡ 执行操作: 点击微信图标
⚡ 执行操作: 输入搜索内容
✅ 执行结果: 任务完成
```

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Enter` | 发送消息 |
| `Shift + Enter` | 输入换行 |
| `Ctrl + /` | 清空输入框 |

---

## 📁 项目结构

```
autoglm-ui/
├── web_server.py              # Flask 应用入口
├── config.yaml                # 配置文件
├── requirements.txt           # Python 依赖
├── README.md                  # 本文档
├── PROJECT_STRUCTURE.md       # 详细结构文档
│
├── templates/                 # HTML 模板
│   └── index.html            # 主页面
│
├── static/                   # 静态资源
│   ├── css/
│   │   └── style.css        # 样式表
│   └── js/
│       └── main.js          # 前端逻辑
│
├── ai/                       # AI 模块
│   ├── normal_chat.py       # GLM-4 对话
│   └── autoglm_agent.py     # AutoGLM 智能体
│
├── device/                   # 设备控制
│   └── adb_manager.py       # ADB 管理器
│
├── utils/                    # 工具函数
│   ├── config.py            # 配置加载
│   └── logger.py            # 日志系统
│
├── data/                     # 数据文件
│   ├── 01.png               # 截图1
│   └── 02.png               # 截图2
│
└── AutoGLM-phone/           # AutoGLM 子模块
    └── Open-AutoGLM/        # 开源 AutoGLM
```

---

## 🛠 技术栈

### 后端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| **Flask** | 3.0+ | Web 框架 |
| **Flask-SocketIO** | 5.3+ | WebSocket 通信 |
| **Eventlet** | 0.33+ | 异步 I/O |
| **zhipuai** | 2.0+ | 智谱 AI SDK |
| **OpenCV** | 4.8+ | 图像处理 |
| **scrcpy-client** | - | 投屏客户端 |

### 前端技术

| 技术 | 用途 |
|------|------|
| **HTML5** | 页面结构 |
| **CSS3** | 样式设计 |
| **JavaScript (ES6+)** | 交互逻辑 |
| **Socket.IO Client** | 实时通信 |

### AI 技术

| 模型 | 用途 | 提供商 |
|------|------|--------|
| **GLM-4** | A模式对话 | 智谱AI |
| **AutoGLM-Phone** | B模式控制 | 智谱AI |

---

## ⚙️ 高级配置

### 投屏参数调整

编辑 `web_server.py` 中的 scrcpy 参数：

```python
client = Client(
    device=device, 
    max_width=1080,      # 分辨率：720/1080/1920
    bitrate=8000000,     # 比特率：8Mbps
    max_fps=60           # 帧率：15/30/60
)
```

### 网络代理配置

如果 GLM API 连接超时，配置代理：

编辑 `ai/autoglm_agent.py`：
```python
os.environ["HTTP_PROXY"] = "http://proxy:port"
os.environ["HTTPS_PROXY"] = "http://proxy:port"
```

### 日志级别

编辑 `utils/logger.py` 调整日志详细程度。

---

## 🐛 常见问题

### Q1: 投屏黑屏或无画面？

**解决方案**：
1. 检查 ADB 连接：`adb devices`
2. 手机屏幕保持唤醒
3. 重启投屏服务
4. 检查防火墙设置

### Q2: AutoGLM 响应很慢？

**原因**：网络访问 GLM API 超时

**解决方案**：
1. 配置网络代理
2. 检查 API 密钥有效性
3. 使用本地模型（高级）

### Q3: ADB 连接不稳定？

**解决方案**：
1. 确保手机和电脑在同一局域网
2. 关闭手机省电模式
3. 使用 USB 连接代替无线
4. 重启 ADB 服务：`adb kill-server && adb start-server`

### Q4: WebSocket 连接失败？

**解决方案**：
1. 检查端口 5000 是否被占用
2. 清除浏览器缓存
3. 使用 Chrome/Firefox 浏览器
4. 检查防火墙/代理设置

---

## 🔄 更新日志

### v1.0.0 (2026-02-09)

**初始版本发布**

✨ **新功能**
- 实现基于 scrcpy 的实时投屏系统
- 集成 GLM-4 AI 对话功能（A模式）
- 集成 AutoGLM 智能手机控制（B模式）
- 开发现代化 Web UI 界面
- B模式上下分屏执行过程可视化

🎨 **优化**
- 投屏优化至 1080p@60fps
- JPEG 高质量编码
- WebSocket 实时通信
- 响应式布局设计

🐛 **修复**
- 修复 Qt 框架兼容性问题
- 解决 eventlet 与 HTTP 客户端冲突
- 优化 AutoGLM ModelConfig 参数
- 修复设备 ID 传递问题

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本项目
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [scrcpy](https://github.com/Genymobile/scrcpy) - 优秀的安卓投屏工具
- [AutoGLM](https://github.com/THUDM/AutoGLM) - 智能手机控制框架
- [智谱AI](https://open.bigmodel.cn/) - GLM 系列模型
- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [Socket.IO](https://socket.io/) - 实时通信库

---

## 📞 联系方式

- **问题反馈**: [GitHub Issues](../../issues)
- **功能建议**: [GitHub Discussions](../../discussions)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！⭐**

Made with ❤️ by AutoGLM Cockpit Team

</div>
