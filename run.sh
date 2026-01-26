#!/bin/bash

# AutoGLM Cockpit 快速启动脚本

echo "================================"
echo "  AutoGLM Cockpit 启动中..."
echo "================================"

# 检查虚拟环境
if [ ! -d ".venv39" ]; then
    echo "❌ 虚拟环境不存在，请先运行："
    echo "   /usr/bin/python3 -m venv .venv39"
    echo "   source .venv39/bin/activate"
    echo "   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple"
    exit 1
fi

# 激活虚拟环境
echo "✓ 激活虚拟环境..."
source .venv39/bin/activate

# 检查配置文件
if [ ! -f "config.yaml" ] && [ ! -f "$HOME/.autoglm-ui/config.yaml" ]; then
    echo "⚠️  首次运行，将创建默认配置文件"
    echo "   请编辑 ~/.autoglm-ui/config.yaml 配置你的设备IP"
fi

# 设置编码和 Qt 环境变量
export LANG=en_US.UTF-8
export DYLD_LIBRARY_PATH=$PWD/.venv39/lib/python3.9/site-packages/PySide6/Qt/lib:$DYLD_LIBRARY_PATH
export QT_PLUGIN_PATH=$PWD/.venv39/lib/python3.9/site-packages/PySide6/Qt/plugins

# 运行程序（直接调用，不使用 -m）
echo "✓ 启动程序..."
python main.py

echo ""
echo "程序已退出"
