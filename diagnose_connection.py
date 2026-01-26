#!/usr/bin/env python3
"""
设备连接诊断工具
检查 ADB、Scrcpy 和设备连接状态
"""
import sys
import subprocess
import shutil
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.config import load_config


def check_command(command: str) -> bool:
    """检查命令是否存在"""
    return shutil.which(command) is not None


def run_command(command: str) -> tuple:
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        return True, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "命令超时"
    except Exception as e:
        return False, "", str(e)


def main():
    print("=" * 70)
    print("设备连接诊断工具")
    print("=" * 70)
    
    # 1. 检查 ADB
    print("\n[1/5] 检查 ADB 安装...")
    if check_command("adb"):
        print("  ✅ ADB 已安装")
        success, stdout, _ = run_command("adb version")
        if success:
            version_line = stdout.split('\n')[0]
            print(f"  ℹ️  {version_line}")
    else:
        print("  ❌ ADB 未安装")
        print("  💡 安装方法:")
        print("     macOS: brew install android-platform-tools")
        print("     Linux: sudo apt install android-tools-adb")
        return
    
    # 2. 检查 Scrcpy
    print("\n[2/5] 检查 Scrcpy 安装...")
    if check_command("scrcpy"):
        print("  ✅ Scrcpy 已安装")
        success, stdout, _ = run_command("scrcpy --version")
        if success:
            print(f"  ℹ️  {stdout.strip()}")
    else:
        print("  ❌ Scrcpy 未安装")
        print("  💡 安装方法:")
        print("     macOS: brew install scrcpy")
        print("     Linux: sudo apt install scrcpy")
        print("  ⚠️  注意: 即使没有 scrcpy 命令，Python 库也可能工作")
    
    # 3. 检查 Python scrcpy 库
    print("\n[3/5] 检查 Python scrcpy 库...")
    try:
        import scrcpy
        print("  ✅ scrcpy Python 库已安装")
    except ImportError:
        print("  ❌ scrcpy Python 库未安装")
        print("  💡 安装方法:")
        print("     pip install scrcpy-client")
        print("     或")
        print("     pip install git+https://github.com/leng-yue/py-scrcpy-client.git")
    
    # 4. 加载配置并测试连接
    print("\n[4/5] 测试设备连接...")
    try:
        config = load_config()
        device_ip = config['device']['ip']
        adb_port = config['device']['adb_port']
        
        print(f"  📱 目标设备: {device_ip}:{adb_port}")
        
        # 测试 ADB 连接
        print(f"  🔌 尝试 ADB 连接...")
        success, stdout, stderr = run_command(f"adb connect {device_ip}:{adb_port}")
        
        if success and "connected" in stdout.lower():
            print(f"  ✅ ADB 连接成功")
            print(f"     {stdout.strip()}")
        else:
            print(f"  ❌ ADB 连接失败")
            print(f"     输出: {stdout.strip()}")
            if stderr:
                print(f"     错误: {stderr.strip()}")
            print("\n  💡 可能的原因:")
            print("     1. 设备未开启无线调试")
            print("     2. IP 地址或端口不正确")
            print("     3. 设备和电脑不在同一网络")
            print("     4. 防火墙阻止连接")
            return
        
    except Exception as e:
        print(f"  ❌ 配置加载失败: {e}")
        return
    
    # 5. 获取设备信息
    print("\n[5/5] 获取设备信息...")
    success, stdout, _ = run_command("adb devices -l")
    if success:
        print("  连接的设备列表:")
        for line in stdout.strip().split('\n')[1:]:  # 跳过标题行
            if line.strip():
                print(f"    {line}")
    
    # 获取设备详细信息
    print("\n  设备详细信息:")
    commands = {
        "型号": "adb -s {device} shell getprop ro.product.model",
        "制造商": "adb -s {device} shell getprop ro.product.manufacturer",
        "Android版本": "adb -s {device} shell getprop ro.build.version.release",
        "SDK版本": "adb -s {device} shell getprop ro.build.version.sdk",
        "分辨率": "adb -s {device} shell wm size"
    }
    
    device_name = f"{device_ip}:{adb_port}"
    for label, cmd_template in commands.items():
        cmd = cmd_template.replace("{device}", device_name)
        success, stdout, _ = run_command(cmd)
        if success:
            value = stdout.strip()
            if "Physical size:" in value:
                value = value.split("Physical size:")[1].strip()
            print(f"    {label}: {value}")
    
    print("\n" + "=" * 70)
    print("诊断完成")
    print("=" * 70)
    print("\n✅ 如果所有检查都通过，现在可以运行: python main.py")
    print("❌ 如果有失败项，请按照提示修复后再试\n")


if __name__ == "__main__":
    main()
