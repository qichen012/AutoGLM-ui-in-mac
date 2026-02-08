import sys
import os
import importlib.util
import glob

def print_header(title):
    print(f"\n{'='*20} {title} {'='*20}")

def check_package_location(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec and spec.origin:
        print(f"[已安装] {package_name}:")
        print(f"  -> 路径: {os.path.dirname(spec.origin)}")
        return os.path.dirname(spec.origin)
    else:
        print(f"[未安装] {package_name}")
        return None

def check_opencv_conflict(cv2_path):
    if not cv2_path:
        return
    
    # 检查 OpenCV 文件夹里有没有 Qt 相关的文件
    print(f"\n正在检查 OpenCV 内部是否夹带了私货 (Qt库)...")
    qt_files = glob.glob(os.path.join(cv2_path, "**", "*Qt*"), recursive=True)
    libqcocoa = glob.glob(os.path.join(cv2_path, "**", "libqcocoa.dylib"), recursive=True)
    
    if qt_files or libqcocoa:
        print("⚠️  发现潜在冲突！OpenCV 自带了 Qt 库，这会和 PySide6 打架：")
        if libqcocoa:
            print(f"  -> 发现平台插件: {libqcocoa[0]}")
        for f in qt_files[:5]: # 只列出前5个
            print(f"  -> 发现文件: {os.path.basename(f)}")
        if len(qt_files) > 5:
            print(f"  -> ... 以及其他 {len(qt_files)-5} 个 Qt 文件")
    else:
        print("✅ OpenCV 看起来是干净的 (headless 版本)，没有自带 Qt。")

def check_env_vars():
    keys = ['QT_PLUGIN_PATH', 'QT_QPA_PLATFORM_PLUGIN_PATH', 'DYLD_LIBRARY_PATH', 'PYTHONPATH']
    for key in keys:
        val = os.environ.get(key)
        if val:
            print(f"⚠️  环境变量 {key} 被设置了: {val}")
        else:
            print(f"OK: 环境变量 {key} 未设置 (干净)")

if __name__ == "__main__":
    print_header("环境诊断报告")
    print(f"Python 解释器: {sys.executable}")
    print(f"Python 版本: {sys.version.split()[0]}")
    
    # 1. 检查 PySide6
    print_header("1. PySide6 状态")
    pyside_path = check_package_location("PySide6")
    
    # 2. 检查 OpenCV (这是最可能的嫌疑人)
    print_header("2. OpenCV 状态")
    cv2_path = check_package_location("cv2") # cv2 是 opencv-python 的导入名
    check_opencv_conflict(cv2_path)
    
    # 3. 检查 OpenAI (虽然不太可能是它，但为了确认你的疑虑)
    print_header("3. OpenAI 状态")
    check_package_location("openai")

    # 4. 检查环境变量
    print_header("4. 环境变量检查")
    check_env_vars()
    
    print_header("诊断结束")