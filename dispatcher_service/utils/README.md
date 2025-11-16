# Dispatcher Service Utils

This directory contains utility modules for the Dispatcher Service.

## Logger Module

The logger module (`logger.py`) provides a centralized logging configuration for the dispatcher service with support for both console and file logging.

### Features

- **Console and File Logging**: Log to console, file, or both
- **Rotating File Handler**: Automatic log file rotation when size limit is reached
- **Configurable Log Levels**: Support for DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Environment Variable Support**: Configure via environment variables
- **Multiple Logger Instances**: Support for module-specific loggers
- **Production Ready**: Thread-safe with proper formatting and error handling

### Usage Examples

#### Basic Usage

```python
from dispatcher_service.utils.logger import setup_logger

# Create a logger with default configuration
logger = setup_logger('my_module')
logger.info('Service started')
logger.error('An error occurred', exc_info=True)
```

#### Using Module Logger

```python
from dispatcher_service.utils.logger import setup_module_logger

# Create a logger for a specific module
logger = setup_module_logger(__name__)
logger.debug('Debug information')
logger.info('Processing request')
```

#### Using Convenience Functions

```python
from dispatcher_service.utils import logger

# Use convenience functions for quick logging
logger.info('Alert received')
logger.warning('High load detected')
logger.error('Failed to connect to database')
logger.exception('Exception occurred')  # Includes traceback
```

#### Custom Configuration

```python
from dispatcher_service.utils.logger import setup_logger

# Custom logger configuration
logger = setup_logger(
    name='custom_logger',
    log_level='DEBUG',
    log_to_file=True,
    log_to_console=True,
    log_file_path='/var/log/dispatcher/custom.log',
    use_rotating=True
)
```

### Environment Variables

You can configure the logger using environment variables:

- `DISPATCHER_LOG_DIR`: Directory for log files (default: `logs`)
- `DISPATCHER_LOG_FILE`: Log file name (default: `dispatcher_service.log`)
- `DISPATCHER_LOG_LEVEL`: Logging level (default: `INFO`)

Example:

```bash
export DISPATCHER_LOG_DIR=/var/log/dispatcher
export DISPATCHER_LOG_FILE=dispatcher.log
export DISPATCHER_LOG_LEVEL=DEBUG
```

### Configuration Options

The `LoggerConfig` class provides default configuration:

- **LOG_DIR**: Directory where log files are stored
- **LOG_FILE**: Name of the log file
- **LOG_LEVEL**: Default logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
- **LOG_FORMAT**: Format string for log messages
- **DATE_FORMAT**: Format string for timestamps
- **MAX_BYTES**: Maximum log file size before rotation (10 MB)
- **BACKUP_COUNT**: Number of backup files to keep (5)

### Log Format

Default log format includes:

- Timestamp
- Logger name
- Log level
- Function name and line number
- Log message

Example output:

```
2025-11-16 15:11:01 - dispatcher_service - INFO - process_alert:42 - Alert received from client
2025-11-16 15:11:01 - dispatcher_service - WARNING - route_alert:67 - No available units found
2025-11-16 15:11:01 - dispatcher_service - ERROR - send_rpc:89 - RPC call failed: Connection timeout
```

### Best Practices

1. **Use Module-Specific Loggers**: Create a logger for each module using `setup_module_logger(__name__)`
2. **Use Appropriate Log Levels**: 
   - DEBUG: Detailed diagnostic information
   - INFO: General informational messages
   - WARNING: Warning messages for potentially harmful situations
   - ERROR: Error messages for problems that need attention
   - CRITICAL: Critical issues that may cause system failure
3. **Include Context**: Add relevant context to log messages
4. **Use `exc_info=True`**: When logging exceptions, include traceback with `exc_info=True`
5. **Avoid Sensitive Data**: Never log passwords, tokens, or other sensitive information

### Thread Safety

The logger is thread-safe and can be used safely in multi-threaded environments.

### Testing

The logger has been tested for:
- Basic console logging
- File logging with rotation
- Module-specific loggers
- Convenience functions
- Environment variable configuration
