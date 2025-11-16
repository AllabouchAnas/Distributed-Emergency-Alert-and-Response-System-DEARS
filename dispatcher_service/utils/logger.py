"""
Logger utility for the Dispatcher Service.

This module provides a centralized logging configuration for the dispatcher service,
supporting both console and file logging with configurable log levels and formats.
"""

import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Optional


class LoggerConfig:
    """Configuration class for logger settings."""
    
    # Default log directory
    LOG_DIR = os.environ.get('DISPATCHER_LOG_DIR', 'logs')
    
    # Default log file name
    LOG_FILE = os.environ.get('DISPATCHER_LOG_FILE', 'dispatcher_service.log')
    
    # Default log level
    LOG_LEVEL = os.environ.get('DISPATCHER_LOG_LEVEL', 'INFO')
    
    # Default log format
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    
    # Date format
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # Maximum log file size (10 MB)
    MAX_BYTES = 10 * 1024 * 1024
    
    # Number of backup files to keep
    BACKUP_COUNT = 5


def setup_logger(
    name: str = 'dispatcher_service',
    log_level: Optional[str] = None,
    log_to_file: bool = True,
    log_to_console: bool = True,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
    log_file_path: Optional[str] = None,
    use_rotating: bool = True
) -> logging.Logger:
    """
    Set up and configure a logger for the dispatcher service.
    
    Args:
        name: Logger name (default: 'dispatcher_service')
        log_level: Logging level (default: from config or 'INFO')
        log_to_file: Enable file logging (default: True)
        log_to_console: Enable console logging (default: True)
        log_format: Custom log format string (default: from config)
        date_format: Custom date format string (default: from config)
        log_file_path: Custom log file path (default: LOG_DIR/LOG_FILE)
        use_rotating: Use rotating file handler instead of basic file handler (default: True)
    
    Returns:
        Configured logger instance
    
    Example:
        >>> logger = setup_logger('dispatcher_service')
        >>> logger.info('Dispatcher service started')
        >>> logger.error('Failed to route alert', exc_info=True)
    """
    # Get or create logger
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Set log level
    level = log_level or LoggerConfig.LOG_LEVEL
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Create formatter
    fmt = log_format or LoggerConfig.LOG_FORMAT
    date_fmt = date_format or LoggerConfig.DATE_FORMAT
    formatter = logging.Formatter(fmt, datefmt=date_fmt)
    
    # Add console handler
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logger.level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Add file handler
    if log_to_file:
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file_path) if log_file_path else LoggerConfig.LOG_DIR
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # Determine full log file path
        if not log_file_path:
            log_file_path = os.path.join(LoggerConfig.LOG_DIR, LoggerConfig.LOG_FILE)
        
        # Create appropriate file handler
        if use_rotating:
            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=LoggerConfig.MAX_BYTES,
                backupCount=LoggerConfig.BACKUP_COUNT
            )
        else:
            file_handler = logging.FileHandler(log_file_path)
        
        file_handler.setLevel(logger.level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: str = 'dispatcher_service') -> logging.Logger:
    """
    Get an existing logger or create a new one with default configuration.
    
    Args:
        name: Logger name (default: 'dispatcher_service')
    
    Returns:
        Logger instance
    
    Example:
        >>> logger = get_logger()
        >>> logger.info('Processing alert')
    """
    logger = logging.getLogger(name)
    
    # If logger doesn't have handlers, set it up
    if not logger.handlers:
        logger = setup_logger(name)
    
    return logger


def setup_module_logger(module_name: str) -> logging.Logger:
    """
    Set up a logger for a specific module within the dispatcher service.
    
    Args:
        module_name: Name of the module (e.g., 'dispatcher_service.routing')
    
    Returns:
        Configured logger instance for the module
    
    Example:
        >>> logger = setup_module_logger(__name__)
        >>> logger.debug('Module initialized')
    """
    return setup_logger(
        name=module_name,
        log_to_file=True,
        log_to_console=True
    )


# Default logger instance for the dispatcher service
default_logger = get_logger('dispatcher_service')


# Convenience functions using the default logger
def debug(message: str, *args, **kwargs):
    """Log a debug message."""
    default_logger.debug(message, *args, **kwargs)


def info(message: str, *args, **kwargs):
    """Log an info message."""
    default_logger.info(message, *args, **kwargs)


def warning(message: str, *args, **kwargs):
    """Log a warning message."""
    default_logger.warning(message, *args, **kwargs)


def error(message: str, *args, **kwargs):
    """Log an error message."""
    default_logger.error(message, *args, **kwargs)


def critical(message: str, *args, **kwargs):
    """Log a critical message."""
    default_logger.critical(message, *args, **kwargs)


def exception(message: str, *args, **kwargs):
    """Log an exception with traceback."""
    default_logger.exception(message, *args, **kwargs)


__all__ = [
    'LoggerConfig',
    'setup_logger',
    'get_logger',
    'setup_module_logger',
    'default_logger',
    'debug',
    'info',
    'warning',
    'error',
    'critical',
    'exception',
]
