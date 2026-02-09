"""配置管理 - Web 版简化版本"""
import yaml
from pathlib import Path
from typing import Any, Dict


DEFAULT_CONFIG = {
    'device': {
        'ip': '192.168.2.13',
        'adb_port': 34333,
    },
    'ai': {
        'api_key': '',  # 需要在 config.yaml 中配置
        'model': 'glm-4',
    }
}


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    # 项目根目录的 config.yaml
    config_path = Path(__file__).parent.parent / "config.yaml"
    
    if not config_path.exists():
        print(f"[Config] 警告: 配置文件不存在，使用默认配置")
        print(f"[Config] 请创建 config.yaml 并配置您的设备和 API 密钥")
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        # 合并默认配置
        merged = DEFAULT_CONFIG.copy()
        if config:
            # 深度合并
            for key, value in config.items():
                if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                    merged[key].update(value)
                else:
                    merged[key] = value
        
        return merged
        
    except Exception as e:
        print(f"[Config] 加载配置失败: {e}，使用默认配置")
        return DEFAULT_CONFIG.copy()

