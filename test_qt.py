#!/usr/bin/env python3
"""测试 Qt 是否能正常工作"""
import sys
import os

print("=" * 60)
print("Qt 环境测试")
print("=" * 60)

print(f"\n1. Python 可执行文件: {sys.executable}")
print(f"2. Python 版本: {sys.version}")

try:
    from PySide6 import QtCore
    print(f"\n3. ✅ PySide6 导入成功")
    print(f"   Qt 版本: {QtCore.qVersion()}")
    print(f"   插件路径: {QtCore.QLibraryInfo.path(QtCore.QLibraryInfo.LibraryPath.PluginsPath)}")
except Exception as e:
    print(f"\n3. ❌ PySide6 导入失败: {e}")
    sys.exit(1)

try:
    from PySide6.QtWidgets import QApplication
    print(f"\n4. ✅ QtWidgets 导入成功")
    
    # 创建应用
    app = QApplication(sys.argv)
    print(f"\n5. ✅ QApplication 创建成功")
    print(f"   平台名称: {app.platformName()}")
    
    # 不显示窗口，直接退出
    print(f"\n6. ✅ 测试完成，Qt 工作正常！")
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ Qt 初始化失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
