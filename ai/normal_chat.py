"""普通对话AI - A模式"""
from typing import Iterator, List, Dict, Optional


class NormalChatAI:
    """普通对话AI（A模式）- 集成智谱AI GLM-4"""
    
    def __init__(self, model: str = "glm-4", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key
        self._initialized = False
        self._client = None
    
    def initialize(self) -> bool:
        """初始化AI服务"""
        try:
            if not self.api_key:
                print(f"[NormalChatAI] 警告：未配置API密钥，请在config.yaml中设置")
                return False
            
            # 导入并初始化智谱AI客户端
            from zhipuai import ZhipuAI
            
            self._client = ZhipuAI(api_key=self.api_key)
            self._initialized = True
            print(f"[NormalChatAI] 初始化成功，模型: {self.model}")
            return True
            
        except ImportError as e:
            print(f"[NormalChatAI] 缺少zhipuai库，请运行: pip install zhipuai")
            return False
        except Exception as e:
            print(f"[NormalChatAI] 初始化失败: {e}")
            return False
    
    def chat(self, message: str, context: Optional[List[Dict]] = None) -> str:
        """同步对话"""
        if not self._initialized or not self._client:
            return "❌ AI服务未初始化，请检查API密钥配置"
        
        try:
            # 构建消息列表
            messages = context or []
            messages.append({"role": "user", "content": message})
            
            # 调用GLM-4 API
            print(f"[NormalChatAI] 调用API，消息: {message}")
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            # 提取响应内容
            result = response.choices[0].message.content
            return result
            
        except Exception as e:
            error_msg = f"❌ 对话出错: {str(e)}"
            print(f"[NormalChatAI] {error_msg}")
            return error_msg
    
    def stream_chat(self, message: str, context: Optional[List[Dict]] = None) -> Iterator[str]:
        """流式对话（逐字输出）"""
        if not self._initialized or not self._client:
            yield "❌ AI服务未初始化，请检查API密钥配置"
            return
        
        try:
            # 构建消息列表
            messages = context or []
            messages.append({"role": "user", "content": message})
            
            # 调用GLM-4 流式API
            print(f"[NormalChatAI] 调用流式API，消息: {message}")
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
            
            # 逐字输出
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            error_msg = f"\n\n❌ 对话出错: {str(e)}"
            print(f"[NormalChatAI] {error_msg}")
            yield error_msg
    
    def set_api_key(self, api_key: str) -> None:
        """设置API密钥"""
        self.api_key = api_key
        self._initialized = False  # 需要重新初始化
    
    def is_ready(self) -> bool:
        """检查是否就绪"""
        return self._initialized and self._client is not None


# ==================== 集成示例 ====================
# 如果你想集成真实的GLM-4 API，可以参考以下代码：
#
# from zhipuai import ZhipuAI
#
# class NormalChatAI:
#     def __init__(self, api_key: str):
#         self.client = ZhipuAI(api_key=api_key)
#         self.model = "glm-4"
#     
#     def chat(self, message: str, context: List[Dict] = None) -> str:
#         messages = context or []
#         messages.append({"role": "user", "content": message})
#         
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=messages
#         )
#         return response.choices[0].message.content
#     
#     def stream_chat(self, message: str, context: List[Dict] = None) -> Iterator[str]:
#         messages = context or []
#         messages.append({"role": "user", "content": message})
#         
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=messages,
#             stream=True
#         )
#         
#         for chunk in response:
#             if chunk.choices[0].delta.content:
#                 yield chunk.choices[0].delta.content
