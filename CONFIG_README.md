# Configuration Guide for DEARS

This document explains how to use the `config.py` file for the Distributed Emergency Alert and Response System (DEARS).

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Configuration Sections](#configuration-sections)
- [Usage Examples](#usage-examples)
- [Production Deployment](#production-deployment)

## Overview

The `config.py` file provides a centralized configuration system for all DEARS components:
- Django Web Application
- Dispatcher Service
- Response Services (Police, Fire, Medical)
- Database connections
- Security settings

## Quick Start

### Basic Usage

```python
import config

# Get database configuration
db_config = config.get_database_config()

# Get service URLs
police_url = config.get_service_url('POLICE')
fire_url = config.get_service_url('FIRE')
medical_url = config.get_service_url('MEDICAL')

# Check environment
if config.is_production():
    print("Running in production mode")
```

### Development Mode (Default)

By default, the configuration runs in development mode with sensible defaults:

```bash
python3 your_app.py
```

## Environment Variables

All configuration values can be overridden using environment variables. This allows for flexible deployment without modifying the code.

### Core Environment Variables

| Variable | Description | Default | Required in Production |
|----------|-------------|---------|------------------------|
| `DEARS_ENVIRONMENT` | Environment mode | `development` | ✓ |
| `DEARS_DEBUG` | Debug mode | `True` | ✓ (set to False) |
| `DB_NAME` | Database name | `dears_db` | ✓ |
| `DB_USER` | Database user | `dears_user` | ✓ |
| `DB_PASSWORD` | Database password | _(empty)_ | ✓ |
| `DB_HOST` | Database host | `localhost` | ✓ |
| `DB_PORT` | Database port | `5432` | |
| `DATABASE_URL` | Complete DB connection string | _(computed)_ | |
| `DJANGO_SECRET_KEY` | Django secret key | _(dev key)_ | ✓ |
| `DJANGO_HOST` | Django server host | `localhost` | |
| `DJANGO_PORT` | Django server port | `8080` | |

### RPC Service Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POLICE_SERVICE_HOST` | Police service hostname | `localhost` |
| `POLICE_SERVICE_PORT` | Police service port | `8001` |
| `FIRE_SERVICE_HOST` | Fire service hostname | `localhost` |
| `FIRE_SERVICE_PORT` | Fire service port | `8002` |
| `MEDICAL_SERVICE_HOST` | Medical service hostname | `localhost` |
| `MEDICAL_SERVICE_PORT` | Medical service port | `8003` |
| `DISPATCHER_HOST` | Dispatcher service hostname | `localhost` |
| `DISPATCHER_PORT` | Dispatcher service port | `8000` |

### Security Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RPC_AUTH_ENABLED` | Enable RPC authentication | `False` |
| `RPC_AUTH_TOKEN` | RPC authentication token | _(empty)_ |
| `USE_HTTPS` | Use HTTPS for connections | `False` |
| `API_RATE_LIMIT` | API requests per minute | `100` |

## Configuration Sections

### 1. Database Configuration

```python
# Access database settings
db_config = config.DATABASE_CONFIG
# Returns:
# {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'dears_db',
#     'USER': 'dears_user',
#     'PASSWORD': '...',
#     'HOST': 'localhost',
#     'PORT': '5432',
#     'OPTIONS': {'sslmode': 'require'}
# }

# Or get the full connection URL
db_url = config.DATABASE_URL
```

### 2. RPC Services

```python
# Get service URLs
police_url = config.POLICE_SERVICE_URL
fire_url = config.FIRE_SERVICE_URL
medical_url = config.MEDICAL_SERVICE_URL

# Or use the helper function
service_url = config.get_service_url('POLICE')  # or 'FIRE' or 'MEDICAL'
```

### 3. Dispatcher Configuration

```python
# Access dispatcher settings
dispatcher_url = config.DISPATCHER_URL
alert_endpoint = config.DISPATCHER_ALERT_URL
```

### 4. Constants

```python
# Emergency types
emergency_types = config.EMERGENCY_TYPES
# Returns: {'POLICE': 'police', 'FIRE': 'fire', 'MEDICAL': 'medical'}

# Alert statuses
alert_statuses = config.ALERT_STATUS
# Returns: {'PENDING': 'pending', 'DISPATCHED': 'dispatched', ...}

# Unit statuses
unit_statuses = config.UNIT_STATUS
# Returns: {'AVAILABLE': 'available', 'EN_ROUTE': 'en_route', ...}
```

## Usage Examples

### Example 1: Django Settings Integration

```python
# In your Django settings.py
import config

# Database configuration
DATABASES = {
    'default': config.get_database_config()
}

# Secret key
SECRET_KEY = config.DJANGO_CONFIG['secret_key']

# Allowed hosts
ALLOWED_HOSTS = config.DJANGO_CONFIG['allowed_hosts']

# Debug mode
DEBUG = config.DEBUG
```

### Example 2: RPC Client (Dispatcher)

```python
# In your dispatcher service
import xmlrpc.client
import config

def dispatch_alert(alert_type, alert_data):
    """Dispatch an alert to the appropriate service."""
    try:
        # Get the service URL based on alert type
        service_url = config.get_service_url(alert_type)
        
        # Create RPC client
        client = xmlrpc.client.ServerProxy(
            service_url,
            allow_none=config.RPC_CONFIG['allow_none']
        )
        
        # Call the remote method
        response = client.receiveAlert_RPC(alert_data)
        return response
        
    except ValueError as e:
        print(f"Invalid alert type: {e}")
        return None
```

### Example 3: RPC Server (Response Service)

```python
# In your response service (e.g., police_service.py)
from xmlrpc.server import SimpleXMLRPCServer
import config

def receiveAlert_RPC(alert_data):
    """Handle incoming alert via RPC."""
    # Process the alert
    print(f"Received alert: {alert_data}")
    # ... business logic here ...
    return {"status": "success", "message": "Alert received"}

# Create RPC server
server = SimpleXMLRPCServer(
    (config.POLICE_SERVICE_RPC['host'], 
     config.POLICE_SERVICE_RPC['port']),
    allow_none=config.RPC_CONFIG['allow_none']
)

server.register_function(receiveAlert_RPC, 'receiveAlert_RPC')
print(f"Police Service listening on {config.POLICE_SERVICE_URL}")
server.serve_forever()
```

### Example 4: Using Environment Variables

```bash
# Development (using defaults)
python3 manage.py runserver

# Production deployment
export DEARS_ENVIRONMENT=production
export DB_HOST=your-neon-db.neon.tech
export DB_NAME=dears_production
export DB_USER=dears_admin
export DB_PASSWORD=your_secure_password
export DJANGO_SECRET_KEY=your_secret_key_here
export USE_HTTPS=True

python3 manage.py runserver
```

### Example 5: Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  django:
    build: ./django_web_app
    environment:
      - DEARS_ENVIRONMENT=production
      - DB_HOST=postgres
      - DB_NAME=dears_db
      - DB_USER=dears_user
      - DB_PASSWORD=${DB_PASSWORD}
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
    ports:
      - "8080:8080"

  dispatcher:
    build: ./dispatcher_service
    environment:
      - DISPATCHER_HOST=0.0.0.0
      - DISPATCHER_PORT=8000
      - POLICE_SERVICE_HOST=police_service
      - FIRE_SERVICE_HOST=fire_service
      - MEDICAL_SERVICE_HOST=medical_service
    ports:
      - "8000:8000"

  police_service:
    build: ./response_services/police_service
    environment:
      - POLICE_SERVICE_HOST=0.0.0.0
      - POLICE_SERVICE_PORT=8001
      - DB_HOST=postgres
    ports:
      - "8001:8001"

  # ... similar for fire_service and medical_service
```

## Production Deployment

### Required Steps for Production

1. **Set Environment Variables**
   ```bash
   export DEARS_ENVIRONMENT=production
   export DEARS_DEBUG=False
   export DJANGO_SECRET_KEY="your-strong-secret-key"
   export DB_PASSWORD="your-database-password"
   export USE_HTTPS=True
   ```

2. **Validate Configuration**
   ```python
   import config
   
   # This will raise an error if required production settings are missing
   config.validate_config()
   ```

3. **Security Checklist**
   - ✓ Set a strong `DJANGO_SECRET_KEY`
   - ✓ Set database password (`DB_PASSWORD`)
   - ✓ Enable HTTPS (`USE_HTTPS=True`)
   - ✓ Disable debug mode (`DEARS_DEBUG=False`)
   - ✓ Configure proper `ALLOWED_HOSTS`
   - ✓ Enable RPC authentication if needed
   - ✓ Set appropriate API rate limits

### Neon Database Configuration

For Neon PostgreSQL hosting:

```bash
# Option 1: Individual variables
export DB_HOST=your-project.neon.tech
export DB_NAME=dears_db
export DB_USER=your_username
export DB_PASSWORD=your_password
export DB_PORT=5432
export DB_SSLMODE=require

# Option 2: Connection string
export DATABASE_URL="postgresql://user:pass@host:5432/db?sslmode=require"
```

## Troubleshooting

### Issue: Configuration validation fails in production

**Solution**: Ensure all required production variables are set:
```bash
echo $DJANGO_SECRET_KEY  # Should not be empty
echo $DB_PASSWORD        # Should not be empty
echo $DEARS_ENVIRONMENT  # Should be 'production'
```

### Issue: Cannot connect to database

**Solution**: Verify database settings:
```python
import config
print(config.DATABASE_URL)  # Check the connection string
```

### Issue: RPC service connection refused

**Solution**: Check service hosts and ports:
```python
import config
print(config.POLICE_SERVICE_URL)
print(config.FIRE_SERVICE_URL)
print(config.MEDICAL_SERVICE_URL)
```

## Best Practices

1. **Never commit sensitive data**: Use environment variables for passwords and keys
2. **Use .env files**: Store environment variables in `.env` files (excluded from git)
3. **Validate early**: Call `config.validate_config()` during application startup
4. **Log configuration**: Log non-sensitive configuration on startup for debugging
5. **Keep production separate**: Use different databases and secrets for each environment

## Support

For questions or issues with configuration, please refer to:
- Main project README: [README.md](README.md)
- Architecture documentation: [docs/02_Conception/](docs/02_Conception/)
- Project team: Contact AllabouchAnas (Project Manager)

---

**Last Updated**: 2025-11-16  
**Version**: 1.0.0
