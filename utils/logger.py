"""日志工具"""
import logging
import sys
from pathlib import Path


def setup_logger(name: str = "autoglm-ui", level: int = logging.INFO) -> logging.Logger:
    """设置日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # 日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # 文件处理器（可选）
    log_dir = Path.home() / ".autoglm-ui" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_dir / "app.log", encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
