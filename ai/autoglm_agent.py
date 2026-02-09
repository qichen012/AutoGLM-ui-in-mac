"""AutoGLM Agent - B模式（手机智能控制）"""
import sys
import os
from typing import Optional, List, Dict, Any, Callable
from pathlib import Path


class AutoGLMAgent:
    """AutoGLM智能手机控制Agent（B模式）"""
    
    def __init__(self, device_ip: str, adb_port: int = 40661):
        self.device_ip = device_ip
        self.adb_port = adb_port
        self._phone_agent = None
        self._initialized = False
        self._execution_log: List[Dict[str, Any]] = []
        self._step_callback: Optional[Callable[[str], None]] = None
        
        # 设置环境变量（与 run.sh 保持一致）
        os.environ["PHONE_AGENT_BASE_URL"] = "https://open.bigmodel.cn/api/paas/v4"
        os.environ["PHONE_AGENT_MODEL"] = "autoglm-phone"
        os.environ["PHONE_AGENT_API_KEY"] = "69cee8e59f2a4e44af21c06c0ee57871.fJjJ5mye1L3WFmmh"
    
    def initialize(self) -> bool:
        """初始化AutoGLM Agent"""
        try:
            # 动态导入AutoGLM模块
            autoglm_path = Path(__file__).parent.parent / "AutoGLM-phone" / "Open-AutoGLM"
            if not autoglm_path.exists():
                print(f"[AutoGLMAgent] AutoGLM路径不存在: {autoglm_path}")
                return False
            
            sys.path.insert(0, str(autoglm_path))
            
            # 导入必要的模块
            from phone_agent import PhoneAgent
            from phone_agent.model import ModelConfig
            from phone_agent.agent import AgentConfig
            
            # 配置模型（从环境变量读取）
            model_config = ModelConfig(
                base_url=os.getenv("PHONE_AGENT_BASE_URL", "https://open.bigmodel.cn/api/paas/v4"),
                model_name=os.getenv("PHONE_AGENT_MODEL", "autoglm-phone"),
                api_key=os.getenv("PHONE_AGENT_API_KEY", "")
            )
            
            # 配置Agent（device_id 格式: "ip:port"）
            device_id = f"{self.device_ip}:{self.adb_port}"
            agent_config = AgentConfig(
                max_steps=int(os.getenv("PHONE_AGENT_MAX_STEPS", "100")),
                device_id=device_id,
                lang="cn",
                verbose=True
            )
            
            # 初始化PhoneAgent
            self._phone_agent = PhoneAgent(
                model_config=model_config,
                agent_config=agent_config
            )
            
            print(f"[AutoGLMAgent] 初始化成功，设备: {self.device_ip}:{self.adb_port}")
            print(f"[AutoGLMAgent] 模型: {model_config.model_name}")
            self._initialized = True
            return True
                
        except Exception as e:
            print(f"[AutoGLMAgent] 初始化失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def set_step_callback(self, callback: Callable[[str], None]):
        """设置步骤回调函数，用于实时显示执行进度"""
        self._step_callback = callback
    
    def execute_task(self, instruction: str) -> Dict[str, Any]:
        """执行手机控制任务"""
        if not self._initialized:
            return {
                'success': False,
                'error': 'Agent未初始化',
                'steps': []
            }
        
        try:
            print(f"[AutoGLMAgent] 执行任务: {instruction}")
            
            if self._step_callback:
                self._step_callback(f"📱 正在获取手机屏幕状态...")
            
            if self._step_callback:
                self._step_callback(f"🤖 调用AI模型分析任务: {instruction}")
            
            # 调用实际的AutoGLM执行逻辑
            message = self._phone_agent.run(instruction)
            
            if self._step_callback:
                self._step_callback(f"✅ 任务执行完成")
            
            result = {
                'success': True,
                'instruction': instruction,
                'message': message,
                'steps': []  # AutoGLM 内部处理步骤
            }
            
            # 记录执行日志
            self._execution_log.append(result)
            
            return result
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            traceback.print_exc()
            
            if self._step_callback:
                self._step_callback(f"❌ 错误: {error_msg}")
            
            error_result = {
                'success': False,
                'error': error_msg,
                'instruction': instruction,
                'steps': []
            }
            self._execution_log.append(error_result)
            return error_result
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """获取执行日志"""
        return self._execution_log.copy()
    
    def clear_log(self) -> None:
        """清空执行日志"""
        self._execution_log.clear()
    
    def stop_task(self) -> None:
        """停止当前任务"""
        if self._phone_agent and hasattr(self._phone_agent, 'stop'):
            self._phone_agent.stop()
            print("[AutoGLMAgent] 任务已停止")
    
    def is_ready(self) -> bool:
        """检查是否就绪"""
        return self._initialized
    
    def get_status(self) -> Dict[str, Any]:
        """获取Agent状态"""
        return {
            'initialized': self._initialized,
            'device': f"{self.device_ip}:{self.adb_port}",
            'task_count': len(self._execution_log)
        }


# ==================== 使用说明 ====================
# 环境变量配置（已在 __init__ 中自动设置）：
# - PHONE_AGENT_BASE_URL: API 基础 URL
# - PHONE_AGENT_MODEL: 模型名称
# - PHONE_AGENT_API_KEY: API 密钥
#
# 使用示例：
# agent = AutoGLMAgent(device_ip="10.29.8.38", adb_port=40661)
# agent.initialize()
# result = agent.execute_task("打开微信")
