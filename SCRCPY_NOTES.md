# Scrcpy 集成说明

由于Python的`scrcpy`包依赖较老的`av`库（需要8.x版本），而PyPI上已不再提供该版本的预编译包，导致在macOS ARM上安装失败。

## 当前状态

✅ **项目架构已完成** - 所有核心模块已实现  
✅ **依赖已安装** - 除scrcpy外的所有包已安装成功  
⚠️ **Scrcpy暂时禁用** - 投屏功能需要额外配置

## 解决方案

### 方案1：使用命令行scrcpy（推荐）

1. **安装scrcpy命令行工具**：
   ```bash
   brew install scrcpy
   ```

2. **手动启动投屏**（在单独终端中）：
   ```bash
   scrcpy --serial <设备IP>:<端口> --max-size 800 --max-fps 30
   ```

3. **使用本项目的AI控制功能**：
   - 项目仍可正常运行，提供AI对话和AutoGLM控制
   - 投屏由scrcpy命令行工具独立提供

### 方案2：使用Python子进程调用scrcpy

修改 `device/scrcpy_client.py`，使用 `subprocess` 调用命令行scrcpy：

```python
import subprocess

class ScrcpyMonitorThread(QThread):
    def run(self):
        cmd = [
            'scrcpy',
            '--serial', f"{self.device_ip}:{self.adb_port}",
            '--max-size', '800',
            '--max-fps', '30'
        ]
        subprocess.Popen(cmd)
```

### 方案3：使用其他投屏方案

- **QtScrcpy**: 基于Qt的scrcpy GUI版本
- **AirPlay**: 如果是iOS设备
- **USB投屏**: 通过USB连接减少延迟

## 暂时禁用投屏运行

当前代码中已注释掉scrcpy的import，项目可以在没有投屏的情况下运行，专注于AI控制功能。

要启用scrcpy功能，请选择上述任一方案实施。

## 推荐工作流程

1. 使用brew安装命令行scrcpy
2. 在单独终端运行scrcpy查看手机画面
3. 在另一个终端运行本项目进行AI控制
4. 两者配合使用，达到可视化控制效果
