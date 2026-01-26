#!/bin/bash

# 1. 自动激活虚拟环境 (防止你忘)
#source venv/bin/activate

# 2. 设置环境变量 (项目会自动读取这些变量，不需要传参了)
export PHONE_AGENT_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
export PHONE_AGENT_MODEL="autoglm-phone"
export PHONE_AGENT_API_KEY="your api key"

# 3. 运行主程序，"$@" 表示把你输入的后续指令传进去
cd help_the_old
cd AutoGLM-phone
cd Open-AutoGLM

python main.py "$@"