"""AutoGLM 执行器 - 调用独立虚拟环境中的 AutoGLM 脚本"""
import subprocess
import threading
import os
from pathlib import Path
from typing import Optional, Callable
from PyQt5.QtCore import QObject, pyqtSignal as Signal


class AutoGLMExecutor(QObject):
    """AutoGLM 执行器 - 通过独立虚拟环境运行 AutoGLM"""
    
    # 信号定义
    output_received = Signal(str)  # 接收到输出
    task_completed = Signal(bool, str)  # 任务完成 (成功?, 结果)
    
    def __init__(self, project_root: str = None):
        super().__init__()
        
        # 确定项目路径
        if project_root is None:
            project_root = str(Path(__file__).parent.parent)
        
        self.project_root = Path(project_root)
        self.autoglm_dir = self.project_root / "AutoGLM-phone"
        self.script_path = self.autoglm_dir / "run_accessibility.sh"
        
        # 当前运行的进程
        self.current_process: Optional[subprocess.Popen] = None
        self.is_running = False
    
    def execute_task(self, task: str, background: bool = False) -> bool:
        """
        执行 AutoGLM 任务
        
        Args:
            task: 任务描述（如："打开微信"）
            background: 是否在后台执行（不阻塞）
        
        Returns:
            是否成功启动
        """
        if self.is_running:
            self.output_received.emit("⚠️ AutoGLM 正在执行任务，请稍后...")
            return False
        
        if not self.script_path.exists():
            self.output_received.emit(f"❌ 脚本不存在: {self.script_path}")
            return False
        
        # 启动任务
        if background:
            thread = threading.Thread(target=self._run_task, args=(task,), daemon=True)
            thread.start()
        else:
            self._run_task(task)
        
        return True
    
    def _run_task(self, task: str):
        """内部：在独立线程中运行任务"""
        self.is_running = True
        self.output_received.emit(f"🚀 正在启动 AutoGLM 执行任务: {task}")
        
        try:
            # 构建命令
            # 使用 bash 执行 shell 脚本，并传递 --task 参数
            cmd = [
                "bash",
                str(self.script_path),
                "--task", task
            ]
            
            self.output_received.emit(f"📡 执行命令: {' '.join(cmd)}")
            
            # 启动进程
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=str(self.autoglm_dir),
                bufsize=1  # 行缓冲
            )
            
            # 实时读取输出
            for line in self.current_process.stdout:
                line = line.rstrip()
                if line:
                    self.output_received.emit(line)
            
            # 等待完成
            return_code = self.current_process.wait()
            
            if return_code == 0:
                self.output_received.emit("✅ 任务执行完成")
                self.task_completed.emit(True, "任务完成")
            else:
                self.output_received.emit(f"❌ 任务执行失败 (退出码: {return_code})")
                self.task_completed.emit(False, f"执行失败: {return_code}")
                
        except Exception as e:
            error_msg = f"❌ 执行出错: {str(e)}"
            self.output_received.emit(error_msg)
            self.task_completed.emit(False, str(e))
        
        finally:
            self.current_process = None
            self.is_running = False
    
    def stop_current_task(self):
        """停止当前任务"""
        if self.current_process:
            self.output_received.emit("🛑 正在停止任务...")
            self.current_process.terminate()
            self.current_process.wait(timeout=5)
            self.is_running = False
            self.output_received.emit("⏹️ 任务已停止")
    
    def check_environment(self) -> tuple[bool, str]:
        """检查 AutoGLM 环境是否正常"""
        # 检查脚本是否存在
        if not self.script_path.exists():
            return False, f"脚本不存在: {self.script_path}"
        
        # 检查 .env 文件
        env_file = self.autoglm_dir / ".env"
        if not env_file.exists():
            return False, f".env 配置文件不存在: {env_file}"
        
        # 检查 accessibility_main.py
        main_file = self.autoglm_dir / "Open-AutoGLM" / "accessibility_main.py"
        if not main_file.exists():
            return False, f"主程序不存在: {main_file}"
        
        return True, "环境检查通过"
    
    def get_status(self) -> str:
        """获取当前状态"""
        if self.is_running:
            return "执行中"
        else:
            return "空闲"
