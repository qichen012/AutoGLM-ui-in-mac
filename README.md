# AutoGLM Cockpit - 手机智能控制系统

一个基于AutoGLM的Mac手机控制系统，支持对话模式和智能控制模式。

## 🌟 功能特性

- **双模式操作**
  - 💬 **A模式（对话模式）**：与AI自由对话，就像ChatGPT
  - 🤖 **B模式（控制模式）**：通过自然语言控制手机（基于AutoGLM）

- **实时投屏**
  - 基于Scrcpy的低延迟手机投屏
  - 支持鼠标点击、滑动等交互

- **模块化架构**
  - 清晰的四层架构设计
  - 易于扩展和维护

## 📋 系统要求

- macOS
- Python 3.9（必须，因为scrcpy限制）
- 手机和Mac在同一局域网
- 手机已开启无线调试

## 🚀 快速开始

### 1. 安装Python 3.9

```bash
# 使用系统自带的Python 3.9
/usr/bin/python3 --version  # 应显示Python 3.9.6

# 或使用brew安装
brew install python@3.9
```

### 2. 创建虚拟环境

```bash
# 使用系统Python 3.9创建虚拟环境
/usr/bin/python3 -m venv .venv39

# 激活虚拟环境
source .venv39/bin/activate
```

### 3. 安装依赖

```bash
# 升级pip
python -m pip install --upgrade pip

# 安装依赖（可使用国内镜像）
python -m pip install -r requirements.txt 
```

### 4. 配置设备

编辑 `config.yaml` 或 `~/.autoglm-ui/config.yaml`：

```yaml
device:
  ip: "你的手机IP"      # 修改为你的手机IP
  adb_port: 40661       # 无线调试端口
```

### 5. 运行程序

```bash
python -m main
```

## 📂 项目结构

```
autoglm-ui/
├── main.py                    # 主入口
├── config.yaml                # 配置文件
├── requirements.txt           # 依赖列表
├── ui/                        # 界面层
│   ├── main_window.py        # 主窗口
│   ├── phone_viewer.py       # 投屏区
│   └── chat_panel.py         # 对话区
├── core/                      # 业务逻辑层
│   ├── mode_manager.py       # 模式管理
│   ├── chat_manager.py       # 对话管理
│   └── phone_controller.py   # 手机控制
├── ai/                        # AI服务层
│   ├── normal_chat.py        # 对话AI
│   └── autoglm_agent.py      # 控制Agent
├── device/                    # 设备层
│   ├── scrcpy_client.py      # Scrcpy
│   └── adb_manager.py        # ADB
└── utils/                     # 工具模块
    ├── logger.py             # 日志
    └── config.py             # 配置
```

## 🔧 配置说明

### AI API密钥

如果要使用真实的AI对话功能，需要在配置文件中设置API密钥：

```yaml
ai:
  api_key: "your-api-key-here"
```

### 集成AutoGLM

确保 `AutoGLM-phone/Open-AutoGLM` 目录存在于项目中，然后在 `ai/autoglm_agent.py` 中取消注释实际的调用代码。

## 💡 使用方法

1. **启动程序**：运行 `python -m main`
2. **等待连接**：左侧会显示手机投屏画面
3. **选择模式**：
   - 默认为对话模式，可以与AI自由对话
   - 点击"切换到控制模式"使用手机控制功能
4. **输入指令**：
   - 对话模式：输入任何问题
   - 控制模式：输入控制指令（如"打开微信"）

## 🐛 故障排除

### 问题：scrcpy Python包安装失败

**原因**：Python的scrcpy包依赖较老的av库，在macOS ARM上编译失败

**解决**：使用命令行scrcpy工具代替
```bash
# 安装命令行scrcpy
brew install scrcpy

# 在单独终端启动投屏
scrcpy --serial <设备IP>:<端口> --max-size 800 --max-fps 30
```

详见 [SCRCPY_NOTES.md](SCRCPY_NOTES.md)

### 问题：手机连接失败

**检查**：
1. 手机和Mac在同一WiFi
2. 手机已开启无线调试
3. IP和端口配置正确

### 问题：依赖安装超时

**解决**：使用国内镜像源

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 📝 开发说明

### 集成真实AI API

编辑 `ai/normal_chat.py`，参考文件中的集成示例代码。

### 集成AutoGLM

编辑 `ai/autoglm_agent.py`，取消注释实际调用代码。

## 📄 许可证

MIT License

## 🙏 致谢

- [AutoGLM](https://github.com/your-autoglm-repo) - 手机智能控制
- [Scrcpy](https://github.com/Genymobile/scrcpy) - 手机投屏
- [PySide6](https://www.qt.io/qt-for-python) - GUI框架
