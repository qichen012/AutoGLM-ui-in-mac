"""
AutoGLM Cockpit - 手机智能控制系统
主入口文件
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置 Qt 插件环境变量（必须在导入 Qt 之前）
venv_path = project_root / ".venv39"
if venv_path.exists():
    qt_plugins = venv_path / "lib/python3.9/site-packages/PySide6/Qt/plugins"
    qt_lib = venv_path / "lib/python3.9/site-packages/PySide6/Qt/lib"
    os.environ["QT_PLUGIN_PATH"] = str(qt_plugins)
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = str(qt_plugins / "platforms")
    # 设置动态库路径
    dyld_path = os.environ.get("DYLD_LIBRARY_PATH", "")
    os.environ["DYLD_LIBRARY_PATH"] = f"{qt_lib}:{dyld_path}"

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.config import load_config
from utils.logger import setup_logger


def main():
    """主函数"""
    # 设置日志
    logger = setup_logger()
    logger.info("=" * 50)
    logger.info("AutoGLM Cockpit 启动中...")
    logger.info("=" * 50)
    
    # 加载配置
    config = load_config()
    logger.info(f"配置已加载: 设备 {config['device']['ip']}:{config['device']['adb_port']}")
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("AutoGLM Cockpit")
    app.setOrganizationName("AutoGLM")
    
    # 创建主窗口
    window = MainWindow(config)
    window.show()
    
    logger.info("主窗口已显示")
    
    # 运行事件循环
    exit_code = app.exec()
    logger.info("应用程序退出")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
