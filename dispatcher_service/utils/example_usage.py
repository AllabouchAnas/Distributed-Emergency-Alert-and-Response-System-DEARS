#!/usr/bin/env python3
"""
Example usage of the dispatcher service logger.

This script demonstrates various ways to use the logging utility.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dispatcher_service.utils.logger import setup_logger, setup_module_logger
from dispatcher_service.utils import logger as logger_utils


def example_basic_usage():
    """Example 1: Basic logger usage."""
    print("\n" + "="*60)
    print("Example 1: Basic Logger Usage")
    print("="*60)
    
    logger = setup_logger('example_basic', log_to_file=False, log_to_console=True)
    logger.info('Starting dispatcher service')
    logger.debug('Configuration loaded')
    logger.warning('High memory usage detected')
    logger.error('Failed to connect to database')


def example_module_logger():
    """Example 2: Module-specific logger."""
    print("\n" + "="*60)
    print("Example 2: Module-Specific Logger")
    print("="*60)
    
    logger = setup_module_logger(__name__)
    logger.info('Module logger initialized')
    logger.debug('Processing alert data')


def example_convenience_functions():
    """Example 3: Using convenience functions."""
    print("\n" + "="*60)
    print("Example 3: Convenience Functions")
    print("="*60)
    
    logger_utils.info('Alert received from client')
    logger_utils.warning('Response service not available')
    logger_utils.error('Failed to route alert')


def example_exception_logging():
    """Example 4: Exception logging with traceback."""
    print("\n" + "="*60)
    print("Example 4: Exception Logging")
    print("="*60)
    
    logger = setup_logger('example_exception', log_to_file=False, log_to_console=True)
    
    try:
        # Simulate an error
        result = 1 / 0
    except ZeroDivisionError:
        logger.exception('An error occurred while processing')


def example_different_log_levels():
    """Example 5: Different log levels."""
    print("\n" + "="*60)
    print("Example 5: Different Log Levels")
    print("="*60)
    
    # Create logger with DEBUG level
    logger = setup_logger(
        'example_levels',
        log_level='DEBUG',
        log_to_file=False,
        log_to_console=True
    )
    
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')


def example_file_logging():
    """Example 6: File logging."""
    print("\n" + "="*60)
    print("Example 6: File Logging")
    print("="*60)
    
    logger = setup_logger(
        'example_file',
        log_to_file=True,
        log_to_console=True
    )
    
    logger.info('This message will be logged to both console and file')
    logger.warning('Check the logs directory for the log file')
    
    print("\nLog file location: logs/dispatcher_service.log")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("DISPATCHER SERVICE LOGGER EXAMPLES")
    print("="*60)
    
    example_basic_usage()
    example_module_logger()
    example_convenience_functions()
    example_exception_logging()
    example_different_log_levels()
    example_file_logging()
    
    print("\n" + "="*60)
    print("Examples completed successfully!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
