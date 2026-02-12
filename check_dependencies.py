#!/usr/bin/env python3
"""
检查ADB无线配对所需的依赖和环境
"""

import sys
import subprocess


def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print(f"   需要Python 3.8+")
        return False


def check_module(module_name, package_name=None):
    """检查Python模块是否已安装"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"   ✅ {package_name}")
        return True
    except ImportError:
        print(f"   ❌ {package_name} - 未安装")
        return False


def check_python_modules():
    """检查Python依赖模块"""
    print("\n📦 检查Python依赖...")
    
    modules = [
        ('qrcode', 'qrcode[pil]'),
        ('PIL', 'Pillow'),
        ('flask', 'Flask'),
        ('flask_socketio', 'flask-socketio'),
    ]
    
    all_ok = True
    for module, package in modules:
        if not check_module(module, package):
            all_ok = False
    
    return all_ok


def check_adb():
    """检查ADB是否已安装"""
    print("\n🔧 检查ADB工具...")
    
    try:
        result = subprocess.run(
            ['adb', 'version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"   ✅ {version_line}")
            return True
        else:
            print(f"   ❌ ADB未正常工作")
            return False
            
    except FileNotFoundError:
        print(f"   ❌ ADB未安装")
        print(f"   💡 安装方法 (macOS): brew install android-platform-tools")
        return False
    except Exception as e:
        print(f"   ❌ 检查ADB时出错: {e}")
        return False


def check_network():
    """检查网络连接"""
    print("\n🌐 检查网络...")
    
    try:
        import socket
        
        # 尝试获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        
        print(f"   ✅ 本机IP: {ip}")
        
        if ip.startswith("127."):
            print(f"   ⚠️  警告: IP为本地地址，可能无法连接手机")
            print(f"   请确保连接到WiFi网络")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ 网络检查失败: {e}")
        print(f"   请确保已连接到网络")
        return False


def check_project_files():
    """检查项目文件"""
    print("\n📁 检查项目文件...")
    
    import os
    
    files = [
        'adb/qrcode.py',
        'adb/qrcode_api.py',
        'test_adb_pairing.py',
        'requirements.txt',
    ]
    
    all_ok = True
    for file in files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - 文件不存在")
            all_ok = False
    
    return all_ok


def print_installation_guide():
    """打印安装指南"""
    print("\n" + "="*70)
    print("📚 安装指南")
    print("="*70)
    
    print("\n1️⃣ 安装Python依赖:")
    print("   pip install qrcode[pil] Pillow Flask flask-socketio")
    print("   或")
    print("   pip install -r requirements.txt")
    
    print("\n2️⃣ 安装ADB (macOS):")
    print("   brew install android-platform-tools")
    
    print("\n3️⃣ 验证安装:")
    print("   python check_dependencies.py")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("🔍 ADB无线配对 - 环境检查")
    print("="*70)
    
    checks = [
        ("Python版本", check_python_version()),
        ("Python依赖", check_python_modules()),
        ("ADB工具", check_adb()),
        ("网络连接", check_network()),
        ("项目文件", check_project_files()),
    ]
    
    print("\n" + "="*70)
    print("📊 检查结果")
    print("="*70)
    
    all_passed = all(result for _, result in checks)
    
    for name, result in checks:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:20s} {status}")
    
    print("\n" + "="*70)
    
    if all_passed:
        print("✅ 所有检查通过！环境配置完成")
        print("\n🚀 你可以开始使用ADB无线配对功能了:")
        print("   python test_adb_pairing.py --mode auto")
        print("   或")
        print("   python examples/simple_adb_pairing.py")
    else:
        print("❌ 部分检查未通过，请根据上述信息修复问题")
        print_installation_guide()
    
    print("="*70 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
