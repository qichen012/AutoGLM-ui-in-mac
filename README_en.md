# 🚀 AutoGLM Cockpit Web

<div align="center">

**Web-based Smartphone AI Control Platform**

Real-time Screen Mirroring • AI Chat • Smartphone Intelligent Control

[English](README_en.md) | [中文](README.md)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#✨-features) • [Quick Start](#🚀-quick-start) • [User Guide](#📖-user-guide) • [Architecture](#🏗️-architecture-design)

</div>

---

## 📸 Product Preview

### Main Interface - Dual Mode Operation
![Main Interface](data/01.png)

**Left:** Real-time Phone Mirroring (1080p@60fps)  
**Right:** AI Intelligent Assistant (Dual Mode Switching)

### Mode B - Intelligent Control Execution
![Mode B Execution](data/02.png)

**Upper Part:** Task Conversation Input Area  
**Lower Part:** AutoGLM Real-time Execution Visualization

---

## ✨ Features

### 🎯 Core Features

| Module | Description | Technical Highlights |
|---------|------|---------|
| 💬 **Mode A - AI Chat** | GLM-4 based intelligent dialogue system | Supports streaming output, real-time response |
| 🤖 **Mode B - Intelligent Control** | AutoGLM driven phone automation | Visual understanding + operation execution, natural language control |
| 📱 **Real-time Mirroring** | scrcpy ultra-low latency video stream | 1080p resolution, 60fps smoothness |
| 🔗 **Wireless ADB Connection** | Built-in pairing and connection management | Pair directly on UI, no command line needed |
| 🔄 **Execution Visualization** | Real-time display of AI thinking and operations | Step-by-step display, transparent process |

### 🌟 Technical Highlights

- **🚄 High Performance Mirroring**
  - Based on scrcpy native video stream, latency < 100ms
  - Supports 1080p/60fps HD smooth display
  - JPEG high-quality encoding + CSS rendering optimization
  - Collapsible control panel, maximizing mirroring area

- **🔌 Wireless ADB Management**
  - **Graphical Pairing**: Enter pairing info directly in Web UI
  - **Quick Connect**: One-click connection for paired devices
  - **Smart Collapse**: Automatically hides control panel after connection/mirroring success
  - **Real-time Status**: Connection status and device info at a glance

- **🧠 Dual Mode AI Engine**
  - **Mode A**: GLM-4 streaming dialogue, supports multi-turn interaction
  - **Mode B**: AutoGLM visual agent, autonomous phone control

- **🎨 Modern Web UI**
  - Minimalist enterprise design style (SaaS-like)
  - Pure white floating cards + light gray grid background
  - Responsive layout, adapts to screen size
  - WebSocket real-time communication, no-refresh interaction
  - Delicate animation and interaction feedback

- **🔌 Flexible Architecture**
  - Front-end and back-end separation, easy to extend
  - Modular design, clear code organization
  - Supports multi-device concurrency (future extension)

---

## 🏗️ Architecture Design

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Browser Client                          │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  Left: Mirroring  │         │  Right: AI Console │       │
│  │  • scrcpy Video  │         │  • Mode Switch     │        │
│  │  • Real-time     │         │  • Chat Input     │         │
│  │                  │         │  • Execution Proc │         │
│  └──────────────────┘         └──────────────────┘          │
└────────────┬─────────────────────────┬─────────────────────┘
             │    WebSocket (Socket.IO) │
             │                          │
┌────────────▼──────────────────────────▼─────────────────────┐
│                 Flask Web Server                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Mirroring Svc │  │ Mode A GLM-4 │  │ Mode B AutoGLM│     │
│  │ scrcpy Client│  │ Normal Chat  │  │ Phone Agent  │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                  │               │
│         │ ADB             │ HTTPS            │ HTTP:8080     │
│         │                 │                  │               │
│  ┌──────▼─────────────────▼──────────────────▼──────┐       │
│  │      Device Control Layer - Accessibility Svc    │       │
│  └──────────────────────┬───────────────────────────┘       │
└─────────────────────────┼─────────────────────────────────────┘
                          │ ADB (Mirroring) + HTTP (Control)
                          │
              ┌───────────▼───────────┐
              │   Android Phone        │
              │  • ADB: Video Stream   │
              │  • HTTP:8080 Control  │
              │   192.168.2.10       │
              └───────────────────────┘
```

### Data Flow Details

1. **Mirroring Flow** (Left Side Display)
   ```
   Phone Screen → scrcpy Server (Phone) 
           → scrcpy Client (Server) 
           → JPEG Encoding 
           → WebSocket Push 
           → Browser Display
   ```

2. **Mode A Dialogue Flow**
   ```
   User Input → Flask Backend 
           → GLM-4 API (Streaming) 
           → Character-by-character Return 
           → Browser Display
   ```

3. **Mode B Control Flow** ⭐ Using Accessibility Service
   ```
   User Instruction → AutoGLM Agent 
           → HTTP Request Screenshot (port:8080)
           → GLM Visual Analysis 
           → Generate Operation Instruction
           → HTTP Send Operation (port:8080)
           → Accessibility Service Execution
           → Feedback Result
   ```

   **Accessibility Advantages**:
   - ✅ Supports text input (including Chinese)
   - ✅ More stable clicking and sliding
   - ✅ No need for ADB Keyboard
   - ✅ Native accessibility service support

---

## 📋 System Requirements

### Prerequisites

- **OS**: macOS / Linux / Windows
- **Python**: 3.11 or higher
- **ADB**: Android Debug Bridge (for phone communication)
- **scrcpy**:  Phone mirroring tool
- **Browser**: Chrome / Firefox / Safari / Edge (Modern browsers)

### Android Phone Requirements

- Android 5.0+ (Recommended Android 11+)
- Enable Developer Options + USB Debugging
- Support Wireless Debugging (for scrcpy mirroring)
- **Install Accessibility Service App** (Required for Mode B Control)
  - Used to receive control instructions (HTTP port 8080)
  - Execute click, slide, input and other operations

---

## 🚀 Quick Start

### 1️⃣ Clone Project

```bash
git clone <repository-url>
cd autoglm-ui
```

### 2️⃣ Install System Dependencies

**macOS:**
```bash
brew install android-platform-tools scrcpy
```

**Ubuntu/Debian:**
```bash
sudo apt install android-tools-adb scrcpy
```

**Windows:**
- Download [ADB Platform Tools](https://developer.android.com/studio/releases/platform-tools)
- Download [scrcpy](https://github.com/Genymobile/scrcpy/releases)

### 3️⃣ Install Python Dependencies

```bash
# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install AutoGLM (Required for Mode B)
cd AutoGLM-phone/Open-AutoGLM
pip install -e .
cd ../..
```

### 4️⃣ Configuration

#### Main Config `config.yaml`

```yaml
device:
  ip: "192.168.2.10"          # Phone IP Address (Auto-filled after Web UI pairing)
  adb_port: 35405             # ADB Wireless Debug Port (for scrcpy mirroring)

ai:
  api_key: "your-api-key"     # Zhipu GLM API Key
  model: "glm-4"              # Model Name
```

**Tip**:
- `device.ip` and `device.adb_port` can be automatically obtained after successful pairing in the Web interface.
- You can also manually view and fill in the "Wireless Debugging" page on your phone.
- For first-time use, it is recommended to automatically configure via the Web interface ADB pairing function.

#### Accessibility Config `.env` File

Create `.env` file in `AutoGLM-phone/Open-AutoGLM/` directory:

```bash
# Accessibility Service Config
device_ip="192.168.2.10"    # Keep consistent with IP in config.yaml
```

**Get API Key**: [Zhipu AI Open Platform](https://open.bigmodel.cn/)

### 5️⃣ Phone Setup

#### Step 1: Enable Wireless Debugging

**Android 11+ Recommended Way:**

1. Phone: Settings → Developer Options → Wireless Debugging
2. Turn on "Wireless Debugging" switch
3. **Pair and Connect in Web Interface** (See "User Guide" section)
   - No command line operation required
   - Complete pairing and connection directly on the interface

**Android 10 and below (USB to Wireless):**

```bash
# After connecting phone via USB
adb tcpip 5555
adb connect <Phone IP>:5555
```

**Verify Connection:**
```bash
adb devices
# Should show: <IP>:<Port>  device
```

#### Step 2: Install and Configure Accessibility Service

**Mode B Control relies on Accessibility Service App**, which provides HTTP interface (port 8080) for:
- Screenshot capture
- Click operations
- Slide operations
- Text input (Supports Chinese)
- App launch

**Installation Steps:**

1. **Install APK**
   
   The project includes a pre-built APK: `app_in_android/app-debug.apk`
   
   **Method 1: Install via ADB (Recommended)**
   ```bash
   # Ensure phone is connected via USB or wireless
   adb devices
   
   # Install the app
   adb install app_in_android/app-debug.apk
   
   # If already installed, use -r to reinstall
   adb install -r app_in_android/app-debug.apk
   ```
   
   **Method 2: Manual Installation**
   - Transfer `app_in_android/app-debug.apk` to your phone
   - Tap to install on phone (Enable "Install from Unknown Sources" if needed)

2. **Grant Accessibility Permission**:
   - Settings → Accessibility → Find "AutoGLM Accessibility Service" → Enable Service
   - Grant all requested permissions

3. **Start Service**:
   - Open the app (App Name: AutoGLM Service)
   - Tap "Start Service" button
   - Confirm service status shows "Running (Port 8080)"

4. **Verify Connection**:
   ```bash
   # Replace <Phone IP> with your actual IP address
   curl "http://<Phone IP>:8080/screenshot"
   # Should return screenshot data (base64 encoded image)
   
   # Or visit test page in browser
   # http://<Phone IP>:8080/status
   ```

**Configuration Points:**
- 📱 **App Name**: AutoGLM Service / AutoGLM Accessibility Service
- 📦 **APK Location**: `app_in_android/app-debug.apk` (Included in project)
- 🔌 **Service Port**: 8080 (HTTP Interface)
- 🌐 Ensure phone and computer are on the same LAN
- ⚡ Turn off phone battery saver mode (Prevent service from being killed)
- 🔋 Set app to "Don't optimize" in battery optimization settings
- 🔒 Grant all accessibility permissions and overlay permissions

### 6️⃣ Start Service

```bash
python web_server.py
```

See the following output indicating successful startup:
```
[autoglm-ui] [INFO] ======================================
[autoglm-ui] [INFO] AutoGLM Cockpit Web Server Started
[autoglm-ui] [INFO] Access URL: http://localhost:5000
[autoglm-ui] [INFO] Device: 192.168.2.10:35405
[autoglm-ui] [INFO] ======================================
[AutoGLMAgent] Using Accessibility method to connect device
[AutoGLMAgent] Initialization successful, device: 192.168.2.10:35405
```

### 7️⃣ Open Browser

Visit: **http://localhost:5000**

---

## 📖 User Guide

### Interface Layout

```
┌─────────────────────────────────────────────────────────┐
│                    AutoGLM Cockpit                      │
├─────────────────────┬───────────────────────────────────┤
│  📱 Phone Mirroring  │  🤖 AI Assistant                  │
│  [Connected] [Hide]  │  ┌───────┬───────┐                │
│                    │  │ Mode A │ Mode B │                │
│  ┌───────────────┐ │  └───────┴───────┘                │
│  │ ADB Pair/Conn  │ │                                   │
│  │ • Pair Device  │ │  [Chat Message Area]              │
│  │ • Quick Conn   │ │                                   │
│  └───────────────┘ │  ┌─────────────────────┐          │
│                    │  │ Input message...     │          │
│  [Phone Screen]      │  └─────────────────────┘          │
│                    │  [Send]                           │
│  [Start Mirroring]  │                                   │
└─────────────────────┴───────────────────────────────────┘
```

### Operating Steps

#### 🔗 Connect Phone (Wireless ADB)

**Method 1: Pair New Device (Android 11+)**

1. Phone Operation:
   - Go to: Settings → Developer Options → Wireless Debugging
   - Tap "Pair device with pairing code"
   - Note down: IP address, Pairing port, Pairing code

2. Web Interface Operation:
   - Click "Pair Device" tab on the left
   - Enter: Device IP, Pairing Port, Pairing Code (6 digits)
   - Click "🔗 Start Pairing"
   - Wait for pairing success prompt

3. Auto switch to "Quick Connect":
   - IP address automatically filled
   - Click "⚡ Quick Connect"
   - Connection success status shows "Connected"

**Method 2: Connect Paired Device**

1. Click "Quick Connect" tab
2. Enter Device IP (Default port 5555)
3. Click "⚡ Quick Connect"

**After Connection Success**:
- Status indicator turns green
- ADB control panel automatically collapses
- Mirroring area maximizes
- Can toggle panel visibility with "Hide Settings/Show Settings" button

**Other Functions**:
- "❌ Disconnect": Disconnect all ADB connections
- "📋 View Devices": View connected device list

#### 🎬 Start Mirroring

1. Ensure ADB connected (Status "Connected")
2. Click "Start Mirroring" button on the left
3. Wait for connection (about 2-3 seconds)
4. Phone screen displays in real-time on left panel
5. Control panel automatically collapses, mirroring screen maximizes

**Mirroring Parameters**:
- Resolution: 1080p
- Frame Rate: 60 FPS
- Encoding: JPEG (Quality 100)
- Latency: < 100ms

#### 💬 Mode A - AI Chat

1. Click right side "Mode A: Chat"
2. Input message in box
3. Press Enter to send (Shift+Enter for new line)
4. AI real-time streaming reply

**Usage Scenarios**:
- Daily conversation
- Question consulting
- Creative writing
- Code assistance

#### 🤖 Mode B - Intelligent Control

1. Click right side "Mode B: Control"
2. Interface automatically splits into upper/lower parts:
   - **Upper Part**: Input task instructions
   - **Lower Part**: Execution process visualization
3. Input phone control instructions, e.g.:
   - "Open WeChat"
   - "Send message to John Doe"
   - "Open Settings and adjust volume"
4. Observe execution process in lower part:
   - 🤔 **Thinking**: AI analyzes task
   - ⚡ **Execution**: Actually operating phone
   - ✅ **Result**: Task completion feedback

**Execution Process Visualization**:
```
🤔 Thinking: Analyzing user instruction
📱 Getting phone screen status...
🤖 Calling AI model to analyze task
⚡ Execution: Click WeChat icon
⚡ Execution: Input search content
✅ Result: Task completed
```

### Shortcuts

| Shortcut | Function |
|--------|------|
| `Enter` | Send message |
| `Shift + Enter` | New line |
| `Ctrl + /` | Clear input box |

---

## 📁 Project Structure

```
autoglm-ui/
├── web_server.py              # Flask App Entry
├── config.yaml                # Configuration File
├── requirements.txt           # Python Dependencies
├── README.md                  # This Document
│
├── scripts/                   # Script Tools
│   ├── adb_pair_correct.py   # ADB Pairing Script
│   └── check_dependencies.py # Dependency Check Script
│
├── docs/                      # Project Docs
│   ├── PROJECT_STRUCTURE.md  # Detailed Structure Doc
│   ├── ADB_PAIRING_GUIDE.md  # ADB Pairing Guide
│   └── WEB_README.md         # Web Version Guide
│
├── app_in_android/            # Android App
│   └── app-debug.apk         # AutoGLM Accessibility Service APK
│
├── templates/                 # HTML Templates
│   └── index.html            # Main Page
│
├── static/                   # Static Resources
│   ├── css/
│   │   └── style.css        # Stylesheet
│   └── js/
│       └── main.js          # Frontend Logic
│
├── ai/                       # AI Modules
│   ├── normal_chat.py       # GLM-4 Chat
│   └── autoglm_agent.py     # AutoGLM Agent
│
├── device/                   # Device Control
│   └── adb_manager.py       # ADB Manager
│
├── utils/                    # Utility Functions
│   ├── config.py            # Config Loading
│   └── logger.py            # Logger System
│
├── data/                     # Data Files
│   ├── 01.png               # Screenshot 1
│   └── 02.png               # Screenshot 2
│
└── AutoGLM-phone/           # AutoGLM Submodule
    └── Open-AutoGLM/        # Open Source AutoGLM
```

---

## 🛠 Tech Stack

### Backend Tech

| Tech | Version | Purpose |
|------|------|------|
| **Flask** | 3.0+ | Web Framework |
| **Flask-SocketIO** | 5.3+ | WebSocket Communication |
| **Eventlet** | 0.33+ | Async I/O |
| **zhipuai** | 2.0+ | Zhipu AI SDK |
| **OpenCV** | 4.8+ | Image Processing |
| **scrcpy-client** | - | Mirroring Client |

### Frontend Tech

| Tech | Purpose |
|------|------|
| **HTML5** | Page Structure |
| **CSS3** | Style Design |
| **JavaScript (ES6+)** | Interaction Logic |
| **Socket.IO Client** | Real-time Communication |

### AI Tech

| Model | Purpose | Provider |
|------|------|--------|
| **GLM-4** | Mode A Chat | Zhipu AI |
| **AutoGLM-Phone** | Mode B Control | Zhipu AI |

---

## ⚙️ Advanced Configuration

### Mirroring Parameter Adjustment

Edit scrcpy parameters in `web_server.py`:

```python
client = Client(
    device=device, 
    max_width=1080,      # Resolution: 720/1080/1920
    bitrate=8000000,     # Bitrate: 8Mbps
    max_fps=60           # Frame Rate: 15/30/60
)
```

### Network Proxy Configuration

If GLM API connection times out, configure proxy:

Edit `ai/autoglm_agent.py`:
```python
os.environ["HTTP_PROXY"] = "http://proxy:port"
os.environ["HTTPS_PROXY"] = "http://proxy:port"
```

### Log Level

Edit `utils/logger.py` to adjust log detail level.

---

## 🐛 FAQ

### Q0: Where to get the Accessibility Service APK?

**Answer**: The project includes the APK file!

**APK Location**:
```bash
app_in_android/app-debug.apk
```

**Quick Installation**:
```bash
# Method 1: Install via ADB (Easiest)
adb install app_in_android/app-debug.apk

# Method 2: Manual Installation
# 1. Transfer app-debug.apk to phone (e.g., via WeChat/Email)
# 2. Tap the apk file on phone to install
# 3. If prompted "Unknown sources", allow installation in settings
```

**App Information**:
- 📱 App Name: AutoGLM Service
- 🔌 Service Port: 8080
- 🔒 Required Permissions: Accessibility + Overlay
- ⚡ Function: Receive HTTP commands, control phone operations

**After Installation Remember**:
1. Enable service in Settings → Accessibility
2. Open app, tap "Start Service"
3. Confirm status shows "Running (Port 8080)"

### Q1: Accessibility Service connection failed?

**Error**: `Connection timeout to <IP>:8080`

**Solution**:
1. Confirm Accessibility Service app is started
2. Check if accessibility permission is enabled
3. Ensure phone and computer are on same LAN
4. Turn off phone firewall
5. Test connection: `curl "http://<IP>:8080/screenshot"`
6. Restart Accessibility Service app

### Q2: Text input failed or garbled?

**Solution**:
1. Confirm using Accessibility method (Not ADB Keyboard)
2. Check Accessibility Service version
3. Ensure input method supports Chinese
4. Restart Accessibility Service

### Q3: Mirroring black screen or no image?

**Solution**:
1. Check ADB connection: `adb devices`
2. Keep phone screen awake
3. Restart mirroring service
4. Check firewall settings

### Q4: AutoGLM response slow?

**Reason**: Network access to GLM API timeout

**Solution**:
1. Configure network proxy
2. Check API key validity
3. Use local model (Advanced)

### Q5: ADB connection unstable?

**Solution**:
1. **Prefer using Web Interface Connection** (Recommended)
   - Click "Show Settings" button on left
   - Use "Pair Device" or "Quick Connect" feature
   - No need for manual command line operations
2. Ensure phone and computer on same LAN
3. Turn off phone battery saver mode
4. Use USB connection instead of wireless
5. Restart ADB service: `adb kill-server && adb start-server`

### Q6: Web Interface pairing failed?

**Common Causes and Solutions**:

1. **Wrong Pairing Code**:
   - Pairing code is 6 digits
   - Note difference between number 0 and letter O
   - Pairing code valid for about 60 seconds, refresh if expired

2. **Wrong Pairing Port**:
   - Phone displayed pairing port is usually 5 digits (e.g., 37045)
   - Do not confuse with ADB port (Default 5555)
   - Port changes every time you tap "Pair device with pairing code"

3. **Wrong IP Address**:
   - Format: 192.168.x.x
   - Ensure phone and computer on same LAN
   - View full IP at top of "Wireless Debugging" page on phone

4. **Network Connection Issues**:
   - Phone and computer must be on same Wi-Fi network
   - Turning off VPN might help
   - Some enterprise networks might restrict device-to-device communication

5. **ADB Service Not Started**:
   - Ensure computer installed ADB (Android Platform Tools)
   - Verify command: `adb version`
   - If not installed, refer to "Quick Start" section

**After Successful Pairing**:
- System automatically switches to "Quick Connect" tab
- Next time just enter IP, no need to pair again
- Device info shows in "View Devices" list

### Q7: WebSocket connection failed?

**Solution**:
1. Check if port 5000 is occupied
2. Clear browser cache
3. Use Chrome/Firefox browser
4. Check Firewall/Proxy settings

---

## 🔄 Changelog

### v1.2.0 (2026-02-15)

**UI Overhaul + Wireless Connection Integration**

✨ **New Features**
- 🔗 Built-in Wireless ADB Pairing and Connection Management
  - Pair directly on Web UI, no command line needed
  - Support pairing new devices and quick connecting paired devices
  - Real-time status display and connection logs
  - Disconnect and device list view
- 📱 Collapsible ADB Control Panel
  - Auto-hide after connection/mirroring success
  - Maximize mirroring area
  - Manual toggle expand/collapse
- 🎨 New UI Design Style
  - Changed from dark tech style to modern minimalist white style
  - Pure white floating card design
  - Light gray grid background (SaaS-like product)
  - Black/White/Gray main color tone, removed blue-green gradient

🎨 **UI Optimization**
- Simplified button design, pure black primary button
- Delicate hover and click feedback animation
- Optimized title bar layout, integrated status indication
- Improved panel shadow and border effects
- Clearer text hierarchy and typography

📱 **Mirroring Optimization**
- Mirroring background changed to transparent/light gray
- Removed black border, more unified vision
- Auto-collapse control panel, larger screen area

🐛 **Fixes**
- Fixed mirroring area squeezed by settings panel
- Optimized connection status synchronization mechanism

### v1.1.0 (2026-02-11)

**Major Update**

✨ **New Features**
- 🔄 Switch to Accessibility Service method for phone control
- ⌨️ Support Chinese text input (No ADB Keyboard needed)
- 📊 Mode B execution process real-time streaming display
- 🎨 Right side lower part split layout: Summary + Detailed Log

🎨 **Optimization**
- Improved IP address parsing logic (Auto remove port number)
- Optimized log output format and highlighting
- More stable HTTP control interface
- Terminal style detailed log area

🐛 **Fixes**
- Fixed connection error caused by device_id format
- Fixed default IP address hardcoding issue
- Solved text input function unavailability
- Optimized streaming output buffering mechanism

### v1.0.0 (2026-02-09)

**Initial Release**

✨ **New Features**
- Implemented scrcpy based real-time mirroring system
- Integrated GLM-4 AI dialogue function (Mode A)
- Integrated AutoGLM smartphone intelligent control (Mode B)
- Developed modern Web UI interface
- Mode B split screen execution visualization

🎨 **Optimization**
- Mirroring optimized to 1080p@60fps
- JPEG high quality encoding
- WebSocket real-time communication
- Responsive layout design

🐛 **Fixes**
- Fixed Qt framework compatibility issues
- Solved eventlet and HTTP client conflict
- Optimized AutoGLM ModelConfig parameters
- Fixed Device ID passing issue

---

## 🤝 Contribution Guide

Welcome to contribute code, report issues or make suggestions!

1. Fork this project
2. Create Feature Branch: `git checkout -b feature/AmazingFeature`
3. Commit Changes: `git commit -m 'Add some AmazingFeature'`
4. Push Branch: `git push origin feature/AmazingFeature`
5. Submit Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgements

- [scrcpy](https://github.com/Genymobile/scrcpy) - Excellent Android mirroring tool
- [AutoGLM](https://github.com/THUDM/AutoGLM) - Smartphone control framework
- [Zhipu AI](https://open.bigmodel.cn/) - GLM series models
- [Flask](https://flask.palletsprojects.com/) - Web Framework
- [Socket.IO](https://socket.io/) - Real-time communication library

---

## 📞 Contact

- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)

---

<div align="center">

**⭐ If this project helps you, please give a Star! ⭐**

Made with ❤️ by AutoGLM Cockpit Team

</div>
