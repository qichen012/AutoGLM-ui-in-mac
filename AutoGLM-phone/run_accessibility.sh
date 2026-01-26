#!/bin/bash


cd AutoGLM-phone/

# 1. 自动激活虚拟环境 (防止你忘)
source .venv/bin/activate

# 2. 设置环境变量 (项目会自动读取这些变量，不需要传参了)
export PHONE_AGENT_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
export PHONE_AGENT_MODEL="autoglm-phone"
export PHONE_AGENT_API_KEY="69cee8e59f2a4e44af21c06c0ee57871.fJjJ5mye1L3WFmmh"

# 3. 运行主程序，"$@" 表示把你输入的后续指令传进去

cd Open-AutoGLM

python accessibility_main.py "$@"