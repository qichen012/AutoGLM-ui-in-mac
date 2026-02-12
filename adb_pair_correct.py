#!/usr/bin/env python3
"""
ADB 无线配对 - 正确的交互式版本
用户在手机上获取配对信息，然后输入到这个脚本
"""

import subprocess
import sys


def print_banner():
    print("\n" + "="*70)
    print("🔗 ADB 无线配对助手 (正确版本)")
    print("="*70 + "\n")


def pair_device():
    """交互式配对"""
    print_banner()
    
    print("📱 第一步：在手机上操作")
    print("-" * 70)
    print("1. 打开 '设置' > '开发者选项' > '无线调试'")
    print("2. 点击 '使用配对码配对设备'")
    print("3. 手机会显示：")
    print("   - IP地址（例如：192.168.2.100）")
    print("   - 端口（例如：37273）")
    print("   - 配对码（6位数字，例如：123456）")
    print()
    
    input("⏸️  准备好后按回车继续...")
    
    print("\n💻 第二步：输入手机上显示的信息")
    print("-" * 70)
    
    # 获取用户输入
    try:
        pairing_ip = input("请输入手机显示的IP地址: ").strip()
        pairing_port = input("请输入手机显示的端口: ").strip()
        pairing_code = input("请输入手机显示的配对码（6位数字）: ").strip()
        
        if not all([pairing_ip, pairing_port, pairing_code]):
            print("\n❌ 输入信息不完整")
            return False
        
        print(f"\n🔄 正在配对...")
        print(f"   目标: {pairing_ip}:{pairing_port}")
        print(f"   配对码: {pairing_code}")
        print()
        
        # 执行配对命令
        pair_address = f"{pairing_ip}:{pairing_port}"
        cmd = ["adb", "pair", pair_address]
        
        # 使用 Popen 来交互式输入配对码
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # 发送配对码
        output, _ = process.communicate(input=pairing_code + "\n", timeout=30)
        
        print("配对输出:")
        print(output)
        
        if "Successfully paired" in output or "成功" in output:
            print("\n✅ 配对成功！")
            
            # 尝试连接
            print("\n🔌 正在连接设备...")
            
            # 使用默认端口5555或用户提供的端口
            connection_port = input(f"\n请输入连接端口（直接回车使用5555）: ").strip() or "5555"
            connect_address = f"{pairing_ip}:{connection_port}"
            
            result = subprocess.run(
                ["adb", "connect", connect_address],
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            
            if "connected" in result.stdout.lower():
                print("\n✅ 连接成功！")
                
                # 显示已连接设备
                print("\n📋 已连接设备:")
                subprocess.run(["adb", "devices", "-l"])
                
                return True
            else:
                print("\n⚠️ 配对成功但连接失败")
                print(f"💡 提示: 请在手机的'无线调试'页面查看实际端口")
                print(f"   然后手动执行: adb connect {pairing_ip}:端口号")
                return False
        else:
            print("\n❌ 配对失败")
            return False
            
    except subprocess.TimeoutExpired:
        print("\n⏱️ 配对超时")
        return False
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消操作")
        return False
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def quick_connect():
    """快速连接（如果之前已配对）"""
    print_banner()
    print("🔌 快速连接模式（适用于已配对过的设备）\n")
    
    ip = input("请输入设备IP地址: ").strip()
    port = input("请输入端口（直接回车使用5555）: ").strip() or "5555"
    
    address = f"{ip}:{port}"
    print(f"\n连接到 {address}...")
    
    result = subprocess.run(
        ["adb", "connect", address],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if "connected" in result.stdout.lower():
        print("✅ 连接成功！")
        subprocess.run(["adb", "devices", "-l"])
        return True
    else:
        print("❌ 连接失败")
        return False


def main():
    """主函数"""
    print_banner()
    
    print("请选择模式:")
    print("1. 配对新设备（需要在手机上输入配对码）")
    print("2. 连接已配对设备（快速连接）")
    print()
    
    choice = input("请输入选项 (1 或 2): ").strip()
    
    if choice == "1":
        pair_device()
    elif choice == "2":
        quick_connect()
    else:
        print("无效选项")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 程序已退出")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)
