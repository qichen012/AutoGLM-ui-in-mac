# AutoGLM 集成说明

## 功能概述

AutoGLM Cockpit 现已集成 AutoGLM-phone 的独立虚拟环境调用功能。在 UI 的**控制模式**下，你可以直接通过对话框下达自然语言指令来控制手机。

## 工作原理

### 1. 独立虚拟环境调用
- UI 使用 `subprocess` 调用 `AutoGLM-phone` 文件夹中的独立虚拟环境
- 通过 `run_accessibility.sh` 脚本启动 AutoGLM
- 实时捕获 AutoGLM 的输出并显示在 UI 中

### 2. 调用流程
```
用户输入指令 
    ↓
UI (控制模式)
    ↓
AutoGLMExecutor
    ↓
run_accessibility.sh (独立虚拟环境)
    ↓
accessibility_main.py
    ↓
AutoGLM Agent 执行
    ↓
实时输出返回 UI
```

## 使用方法

### 1. 启动 UI
```bash
cd /Users/xwj/Desktop/autoglm-ui
python main.py
```

### 2. 切换到控制模式
点击右侧对话面板右上角的 **"切换到控制模式"** 按钮

### 3. 下达指令
在输入框输入自然语言指令，例如：
- "打开微信"
- "发送消息给张三说你好"
- "打开抖音并刷视频"

### 4. 查看执行过程
- AutoGLM 的执行输出会实时显示在对话历史中
- 带灰色背景的是系统日志
- 执行完成后会显示最终结果

## 文件说明

### 核心文件

#### `/core/autoglm_executor.py`
AutoGLM 执行器，负责：
- 调用独立虚拟环境中的脚本
- 捕获和转发输出
- 管理进程生命周期

#### `/AutoGLM-phone/run_accessibility.sh`
AutoGLM 启动脚本，包含：
- 环境变量配置（API Key、模型等）
- 虚拟环境激活
- 脚本调用

#### `/AutoGLM-phone/.env`
设备配置文件：
```env
device_ip = "10.29.8.38"
```

## 配置说明

### 1. 修改手机 IP
编辑 `/AutoGLM-phone/.env`：
```env
device_ip = "你的手机IP"
```

### 2. 修改 API 配置
编辑 `/AutoGLM-phone/run_accessibility.sh`：
```bash
export PHONE_AGENT_BASE_URL="API地址"
export PHONE_AGENT_MODEL="模型名称"
export PHONE_AGENT_API_KEY="你的API密钥"
```

### 3. 检查虚拟环境
确保 AutoGLM-phone 的虚拟环境已正确配置：
```bash
cd /Users/xwj/Desktop/autoglm-ui/AutoGLM-phone
# 如果使用虚拟环境，确保在脚本中正确激活
# source venv/bin/activate  # 在 run_accessibility.sh 中取消注释这行
```

## 环境检查

UI 启动时会自动检查：
1. ✅ `run_accessibility.sh` 脚本是否存在
2. ✅ `.env` 配置文件是否存在
3. ✅ `accessibility_main.py` 主程序是否存在

如果检查失败，会在对话框中显示错误信息。

## 故障排查

### 问题：点击发送后无反应
**解决方案：**
1. 检查 `run_accessibility.sh` 是否有执行权限：
   ```bash
   chmod +x /Users/xwj/Desktop/autoglm-ui/AutoGLM-phone/run_accessibility.sh
   ```

2. 查看 UI 日志输出（对话框中的灰色日志）

### 问题：提示脚本不存在
**解决方案：**
确认文件路径正确：
```bash
ls -la /Users/xwj/Desktop/autoglm-ui/AutoGLM-phone/run_accessibility.sh
```

### 问题：AutoGLM 执行失败
**解决方案：**
1. 手动测试脚本：
   ```bash
   cd /Users/xwj/Desktop/autoglm-ui/AutoGLM-phone
   bash run_accessibility.sh --task "打开微信"
   ```

2. 检查 `.env` 文件中的 `device_ip` 是否正确

3. 确认手机和电脑在同一 WiFi

4. 确认手机上的无障碍 App 已启动

### 问题：虚拟环境找不到包
**解决方案：**
1. 激活虚拟环境并安装依赖：
   ```bash
   cd /Users/xwj/Desktop/autoglm-ui/AutoGLM-phone
   source venv/bin/activate  # 如果使用 venv
   pip install -r Open-AutoGLM/requirements.txt
   pip install python-dotenv
   ```

2. 在 `run_accessibility.sh` 中取消注释虚拟环境激活行

## 高级功能

### 停止正在执行的任务
```python
# 在代码中可以调用
autoglm_executor.stop_current_task()
```

### 查看执行状态
UI 会实时显示 AutoGLM 的状态：
- 🚀 正在启动
- 📡 正在执行
- ✅ 执行完成
- ❌ 执行失败

## 架构优势

1. **环境隔离**：UI 和 AutoGLM 使用独立的虚拟环境，避免依赖冲突
2. **实时反馈**：所有输出实时显示在 UI 中
3. **进程管理**：可以停止正在执行的任务
4. **错误处理**：完善的错误捕获和提示

## 下一步

- [ ] 添加任务队列支持（连续执行多个任务）
- [ ] 添加任务历史记录
- [ ] 支持任务暂停/恢复
- [ ] 添加执行进度条

## 技术细节

### 信号机制
```python
# AutoGLMExecutor 发出的信号
output_received = Signal(str)  # 实时输出
task_completed = Signal(bool, str)  # 完成状态
```

### UI 连接
```python
# 在 MainWindow 中连接
self.autoglm_executor.output_received.connect(self.on_autoglm_output)
self.autoglm_executor.task_completed.connect(self.on_autoglm_completed)
```
