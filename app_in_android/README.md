# 📱 AutoGLM Accessibility Service

[English](#english) | [中文](#中文)

---

## 中文

### 📦 应用说明

这是 **AutoGLM 无障碍服务应用**，用于在 Android 手机上提供 HTTP 控制接口。

**应用名称**: AutoGLM Service  
**APK 文件**: `app-debug.apk`  
**服务端口**: 8080 (HTTP)

### ✨ 功能特性

- 📸 **截图获取**: 通过 HTTP 接口获取手机实时截图
- 👆 **触摸模拟**: 支持点击、长按、滑动等触摸操作
- ⌨️ **文本输入**: 支持中文输入（无需 ADB 键盘）
- 🚀 **应用启动**: 通过包名启动应用
- 🔍 **状态查询**: 查询服务运行状态和设备信息

### 📥 安装方法

#### 方式 1: 通过 ADB 安装（推荐）

```bash
# 确保手机已通过 USB 或无线连接
adb devices

# 安装应用
adb install app-debug.apk

# 如果提示已安装，使用 -r 参数重新安装
adb install -r app-debug.apk
```

#### 方式 2: 手动安装

1. 将 `app-debug.apk` 传输到手机（微信/QQ/邮件等）
2. 在手机文件管理器中找到 APK 文件
3. 点击安装
4. 如果提示"未知来源"，在设置中允许安装

### ⚙️ 配置步骤

1. **安装 APK** ✅

2. **授予无障碍权限** 🔓
   ```
   设置 → 无障碍 → AutoGLM Service → 开启服务
   ```
   - 需要授予所有请求的权限
   - 允许应用显示悬浮窗

3. **启动服务** 🚀
   - 打开 "AutoGLM Service" 应用
   - 点击 "启动服务" 按钮
   - 确认状态显示: "运行中 (端口 8080)"

4. **验证连接** ✅
   ```bash
   # 在电脑上测试连接（替换 <手机IP> 为实际 IP）
   curl "http://<手机IP>:8080/status"
   
   # 应该返回 JSON 格式的状态信息
   # {"status": "running", "port": 8080, ...}
   ```

### 🔗 API 接口

应用启动后，在局域网内提供以下 HTTP 接口：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/status` | GET | 查询服务状态 |
| `/screenshot` | GET | 获取屏幕截图 (Base64) |
| `/tap` | POST | 执行点击操作 |
| `/swipe` | POST | 执行滑动操作 |
| `/input` | POST | 输入文本 |
| `/start_app` | POST | 启动应用 |

**示例请求**:
```bash
# 获取截图
curl "http://192.168.1.100:8080/screenshot"

# 点击屏幕坐标 (500, 1000)
curl -X POST "http://192.168.1.100:8080/tap" \
  -H "Content-Type: application/json" \
  -d '{"x": 500, "y": 1000}'

# 输入文本
curl -X POST "http://192.168.1.100:8080/input" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello 你好"}'
```

### ⚠️ 注意事项

1. **网络要求**: 手机和电脑必须在同一局域网
2. **权限要求**: 必须授予无障碍权限，否则无法控制手机
3. **后台运行**: 
   - 关闭手机省电模式
   - 在电池优化中将应用设为"不优化"
   - 允许后台运行
4. **安全提示**: 
   - 仅在局域网环境使用
   - 不要暴露到公网（端口 8080）
   - 使用完毕后可关闭服务

### 🐛 常见问题

**Q: 服务启动后连接不上？**
- 检查手机和电脑是否在同一 Wi-Fi
- 确认手机防火墙未阻止端口 8080
- 使用 `curl` 测试连接

**Q: 无法点击或输入？**
- 确认已授予无障碍权限
- 在设置 → 无障碍中检查服务是否开启
- 重启应用和服务

**Q: 服务自动停止？**
- 将应用加入电池优化白名单
- 关闭手机省电模式
- 允许应用后台运行

**Q: 如何更新应用？**
```bash
# 直接安装新版本即可（会覆盖旧版本）
adb install -r app-debug.apk
```

### 📞 技术支持

如有问题，请参考主项目 [README.md](../README.md) 或提交 Issue。

---

## English

### 📦 App Description

This is the **AutoGLM Accessibility Service** app that provides HTTP control interface on Android phones.

**App Name**: AutoGLM Service  
**APK File**: `app-debug.apk`  
**Service Port**: 8080 (HTTP)

### ✨ Features

- 📸 **Screenshot Capture**: Get real-time phone screenshots via HTTP
- 👆 **Touch Simulation**: Support tap, long press, swipe operations
- ⌨️ **Text Input**: Support Chinese input (No ADB Keyboard needed)
- 🚀 **App Launch**: Launch apps by package name
- 🔍 **Status Query**: Query service status and device info

### 📥 Installation

#### Method 1: Install via ADB (Recommended)

```bash
# Ensure phone is connected via USB or wireless
adb devices

# Install app
adb install app-debug.apk

# If already installed, use -r to reinstall
adb install -r app-debug.apk
```

#### Method 2: Manual Installation

1. Transfer `app-debug.apk` to phone (WeChat/Email/etc.)
2. Find APK file in phone file manager
3. Tap to install
4. If prompted "Unknown sources", allow installation in settings

### ⚙️ Setup Steps

1. **Install APK** ✅

2. **Grant Accessibility Permission** 🔓
   ```
   Settings → Accessibility → AutoGLM Service → Enable Service
   ```
   - Grant all requested permissions
   - Allow app to display overlay

3. **Start Service** 🚀
   - Open "AutoGLM Service" app
   - Tap "Start Service" button
   - Confirm status shows: "Running (Port 8080)"

4. **Verify Connection** ✅
   ```bash
   # Test connection from computer (replace <Phone IP> with actual IP)
   curl "http://<Phone IP>:8080/status"
   
   # Should return JSON status info
   # {"status": "running", "port": 8080, ...}
   ```

### 🔗 API Endpoints

After service starts, provides following HTTP endpoints on LAN:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Query service status |
| `/screenshot` | GET | Get screenshot (Base64) |
| `/tap` | POST | Perform tap |
| `/swipe` | POST | Perform swipe |
| `/input` | POST | Input text |
| `/start_app` | POST | Start app |

**Example Requests**:
```bash
# Get screenshot
curl "http://192.168.1.100:8080/screenshot"

# Tap at coordinates (500, 1000)
curl -X POST "http://192.168.1.100:8080/tap" \
  -H "Content-Type: application/json" \
  -d '{"x": 500, "y": 1000}'

# Input text
curl -X POST "http://192.168.1.100:8080/input" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello 你好"}'
```

### ⚠️ Important Notes

1. **Network**: Phone and computer must be on same LAN
2. **Permissions**: Must grant accessibility permission
3. **Background Running**: 
   - Turn off battery saver mode
   - Set app to "Don't optimize" in battery settings
   - Allow background running
4. **Security**: 
   - Use only in LAN environment
   - Don't expose port 8080 to internet
   - Stop service when not in use

### 🐛 FAQ

**Q: Can't connect after starting service?**
- Check if phone and computer on same Wi-Fi
- Confirm phone firewall not blocking port 8080
- Test connection with `curl`

**Q: Can't tap or input?**
- Confirm accessibility permission granted
- Check if service enabled in Settings → Accessibility
- Restart app and service

**Q: Service auto stops?**
- Add app to battery optimization whitelist
- Turn off battery saver mode
- Allow background running

**Q: How to update app?**
```bash
# Install new version directly (will overwrite old version)
adb install -r app-debug.apk
```

### 📞 Support

For issues, refer to main project [README.md](../README.md) or submit an Issue.

---

<div align="center">

**Note**: This app is designed for AutoGLM project use only.  
本应用仅为 AutoGLM 项目配套使用。

</div>
