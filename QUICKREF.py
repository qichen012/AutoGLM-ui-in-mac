"""
AutoGLM 集成 - 快速参考
====================================

集成方式
--------
将 run.sh 的 AutoGLM 运行逻辑集成到 UI 的控制模式中

关键文件
--------
1. ai/autoglm_agent.py - AutoGLM Agent 封装
2. ui/main_window.py - UI 集成入口
3. test_autoglm_integration.py - 集成测试脚本

使用方法
--------
1. 启动主程序: python main.py
2. 切换到控制模式（右上角按钮）
3. 输入自然语言指令，例如 "打开微信"
4. AutoGLM 自动执行并实时显示进度

核心特性
--------
✅ 自动设置环境变量（与 run.sh 一致）
✅ 使用 BigModel API (autoglm-phone)
✅ 实时步骤回调显示
✅ 完整错误处理

环境变量（自动设置）
--------------------
PHONE_AGENT_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
PHONE_AGENT_MODEL = "autoglm-phone"
PHONE_AGENT_API_KEY = "69cee8e59f2a4e44af21c06c0ee57871.fJjJ5mye1L3WFmmh"

测试命令
--------
python test_autoglm_integration.py

详细说明
--------
见 INTEGRATION.md
"""
print(__doc__)
