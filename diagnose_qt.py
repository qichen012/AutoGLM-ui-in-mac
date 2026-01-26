#!/usr/bin/env python3
"""诊断 Qt 插件问题"""
import sys
import os
from pathlib import Path

# 设置插件路径
venv_path = Path(__file__).parent / ".venv39"
plugins_path = venv_path / "lib/python3.9/site-packages/PySide6/Qt/plugins"
lib_path = venv_path / "lib/python3.9/site-packages/PySide6/Qt/lib"

os.environ["QT_PLUGIN_PATH"] = str(plugins_path)
os.environ["DYLD_LIBRARY_PATH"] = f"{lib_path}:{os.environ.get('DYLD_LIBRARY_PATH', '')}"

print(f"QT_PLUGIN_PATH: {os.environ['QT_PLUGIN_PATH']}")
print(f"DYLD_LIBRARY_PATH: {os.environ['DYLD_LIBRARY_PATH']}")
print()

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication

# 手动加载插件
plugin_loader = QtCore.QPluginLoader()
cocoa_path = plugins_path / "platforms/libqcocoa.dylib"

print(f"尝试加载: {cocoa_path}")
print(f"文件存在: {cocoa_path.exists()}")

plugin_loader.setFileName(str(cocoa_path))
if plugin_loader.load():
    print("✅ 插件加载成功")
else:
    print(f"❌ 插件加载失败: {plugin_loader.errorString()}")

# 尝试创建应用
try:
    app = QApplication(sys.argv)
    print("✅ QApplication 创建成功")
except Exception as e:
    print(f"❌ QApplication 创建失败: {e}")
    import traceback
    traceback.print_exc()
