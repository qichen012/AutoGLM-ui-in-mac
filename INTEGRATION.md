# AutoGLM 集成说明

## 集成方式

已将 `run.sh` 中的 AutoGLM 运行方式集成到主程序的**控制模式**中。

## 核心修改

### 1. **AutoGLMAgent** (`ai/autoglm_agent.py`)

- ✅ 自动设置环境变量（与 `run.sh` 一致）
- ✅ 使用真实的 `PhoneAgent` API
- ✅ 支持步骤回调，实时显示执行进度
- ✅ 正确的模型配置（BigModel API）

```python
# 环境变量自动配置
os.environ["PHONE_AGENT_BASE_URL"] = "https://open.bigmodel.cn/api/paas/v4"
os.environ["PHONE_AGENT_MODEL"] = "autoglm-phone"
os.environ["PHONE_AGENT_API_KEY"] = "69cee8e59f2a4e44af21c06c0ee57871.fJjJ5mye1L3WFmmh"
```

### 2. **MainWindow** (`ui/main_window.py`)

- ✅ 控制模式下自动初始化 AutoGLM
- ✅ 实时显示执行进度
- ✅ 处理成功/失败状态

## 使用流程

### 启动主程序

```bash
cd /Users/xwj/Desktop/autoglm-ui
python main.py
```

### 在 UI 中使用

1. **启动应用** - 主窗口打开，左侧显示手机投屏，右侧是对话面板
2. **切换到控制模式** - 点击右上角切换按钮，选择 "🤖 控制模式"
3. **输入指令** - 在输入框输入自然语言指令，例如：
   - "打开微信"
   - "打开设置"
   - "发送消息给张三"
4. **查看执行** - AutoGLM 会：
   - 自动初始化（首次使用）
   - 实时显示执行步骤
   - 返回执行结果

## 执行流程

```
用户输入指令
    ↓
[控制模式路由]
    ↓
MainWindow.handle_control_mode()
    ↓
检查 AutoGLM 是否初始化
    ↓
AutoGLMAgent.initialize()  (首次)
    ├─ 加载 AutoGLM-phone/Open-AutoGLM
    ├─ 配置 ModelConfig (BigModel API)
    ├─ 创建 PhoneAgent
    └─ 设置回调函数
    ↓
AutoGLMAgent.execute_task(instruction)
    ├─ 调用 self._phone_agent.run(instruction)
    ├─ 实时回调显示进度
    └─ 返回执行结果
    ↓
在对话面板显示结果
```

## 关键特性

### 环境变量

所有环境变量在 `AutoGLMAgent.__init__()` 中自动设置：
- `PHONE_AGENT_BASE_URL`: BigModel API 地址
- `PHONE_AGENT_MODEL`: 模型名称 (autoglm-phone)
- `PHONE_AGENT_API_KEY`: API 密钥

### 实时回调

```python
# 设置回调函数
agent.set_step_callback(lambda msg: print(msg))

# 执行任务时会触发回调
# 🤖 开始执行: 打开微信
# ✅ 完成: 已打开微信
```

### 错误处理

- 初始化失败 → 提示用户检查 AutoGLM-phone 目录
- 执行失败 → 显示详细错误信息
- 异常捕获 → 记录日志并返回友好提示

## 测试

运行测试脚本验证集成：

```bash
python test_autoglm_integration.py
```

预期输出：
```
============================================================
测试 AutoGLM 集成
============================================================

1. 创建 AutoGLM Agent
   设备: 10.29.8.38:40661

2. 初始化 Agent
   ✅ 初始化成功

3. 设置回调函数

4. 执行测试任务
   指令: 打开设置
   [回调] 🤖 开始执行: 打开设置
   [回调] ✅ 完成: 已打开设置

5. 结果分析
   成功: True
   消息: 已打开设置

6. 获取状态
   initialized: True
   device: 10.29.8.38:40661
   task_count: 1

============================================================
测试完成
============================================================
```

## 与 run.sh 的对比

| 项目 | run.sh | 集成后 |
|-----|--------|--------|
| 环境变量 | export 手动设置 | 代码自动设置 |
| 运行方式 | 命令行 python main.py | UI 控制模式 |
| 交互方式 | CLI 文本 | GUI 对话面板 |
| 进度显示 | 终端打印 | UI 实时回调 |
| 结果展示 | 终端输出 | 对话面板消息 |

## 依赖检查

确保以下目录存在：
```
autoglm-ui/
├── AutoGLM-phone/
│   └── Open-AutoGLM/
│       ├── phone_agent/
│       │   ├── __init__.py
│       │   ├── agent.py
│       │   └── model/
│       └── ...
```

## 常见问题

### Q: 提示 "Agent未初始化"
A: 检查 `AutoGLM-phone/Open-AutoGLM` 目录是否存在

### Q: API 调用失败
A: 检查 API_KEY 是否有效，网络是否正常

### Q: ADB 连接问题
A: 确保设备已连接，IP 和端口配置正确

## 后续优化

- [ ] 支持多设备切换
- [ ] 添加任务队列
- [ ] 任务执行历史记录
- [ ] 支持任务中断/恢复
- [ ] 配置文件化 API 密钥

---

**集成完成时间**: 2026-01-25  
**测试状态**: ✅ 已验证核心功能
