"""
Logging setup for legal-ai project.
Provides consistent logging across all modules.
"""

import logging
from pathlib import Path
from datetime import datetime

def setup_logging(
    log_dir: Path = Path("logs"),
    debug: bool = False
) -> logging.Logger:
    """
    Setup logging for the application.
    
    Args:
        log_dir: Directory to store log files
        debug: Enable debug-level logging
    
    Returns:
        Root logger instance
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Log file naming
    timestamp = datetime.now().strftime('%Y%m%d')
    log_file = log_dir / f"legal_ai_{timestamp}.log"
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # Clear any existing handlers
    root_logger.handlers = []
    
    # Format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler (always DEBUG level)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # Log initialization
    root_logger.info(f"Logging initialized. Log file: {log_file}")
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module."""
    return logging.getLogger(name)
