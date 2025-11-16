"""
Utilities package for the Dispatcher Service.

This package provides utility modules including logging configuration
for the dispatcher service.
"""

from .logger import (
    LoggerConfig,
    setup_logger,
    get_logger,
    setup_module_logger,
    default_logger,
    debug,
    info,
    warning,
    error,
    critical,
    exception,
)

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
