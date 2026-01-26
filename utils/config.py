"""配置管理"""
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_CONFIG = {
    'device': {
        'ip': '192.168.1.100',  # 默认设备IP
        'adb_port': 40661,       # 无线调试端口
    },
    'scrcpy': {
        'max_width': 800,
        'max_fps': 30,
        'bitrate': 2000000,
    },
    'ai': {
        'chat_model': 'glm-4',
        'api_key': '',  # 需要用户配置
        'max_history': 100,
    },
    'ui': {
        'window_width': 1200,
        'window_height': 800,
        'theme': 'dark',
    }
}


def get_config_path() -> Path:
    """获取配置文件路径（优先使用项目目录的config.yaml）"""
    # 优先使用项目根目录的config.yaml
    project_config = Path(__file__).parent.parent / "config.yaml"
    if project_config.exists():
        return project_config
    
    # 否则使用用户目录的配置
    config_dir = Path.home() / ".autoglm-ui"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.yaml"


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    config_path = get_config_path()
    
    if not config_path.exists():
        # 首次运行，创建默认配置
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        # 合并默认配置（补充缺失的键）
        merged_config = DEFAULT_CONFIG.copy()
        if config:  # 确保config不为None
            merged_config.update(config)
        
        return merged_config
        
    except Exception as e:
        print(f"[Config] 加载配置失败: {e}，使用默认配置")
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> bool:
    """保存配置文件"""
    config_path = get_config_path()
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(config, f, allow_unicode=True, default_flow_style=False)
        
        print(f"[Config] 配置已保存到: {config_path}")
        return True
        
    except Exception as e:
        print(f"[Config] 保存配置失败: {e}")
        return False


def get_config_value(key_path: str, default: Any = None) -> Any:
    """获取配置值（支持点号分隔的路径）"""
    config = load_config()
    
    keys = key_path.split('.')
    value = config
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    return value


def set_config_value(key_path: str, value: Any) -> bool:
    """设置配置值"""
    config = load_config()
    
    keys = key_path.split('.')
    target = config
    
    # 导航到目标字典
    for key in keys[:-1]:
        if key not in target:
            target[key] = {}
        target = target[key]
    
    # 设置值
    target[keys[-1]] = value
    
    return save_config(config)
