"""
Configuration file for Distributed Emergency Alert & Response System (DEARS)

This file contains all configuration settings for the system components:
- Database connection settings (PostgreSQL/Neon)
- RPC service endpoints and ports
- REST API configurations
- Service-specific settings

Author: DEARS Team
Date: 2025-11-16
"""

import os
from typing import Dict, Any


# =============================================================================
# ENVIRONMENT SETTINGS
# =============================================================================

# Current environment: 'development', 'staging', or 'production'
ENVIRONMENT = os.getenv('DEARS_ENVIRONMENT', 'development')

# Debug mode (should be False in production)
DEBUG = os.getenv('DEARS_DEBUG', 'True').lower() == 'true'


# =============================================================================
# DATABASE CONFIGURATION (PostgreSQL/Neon)
# =============================================================================

DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv('DB_NAME', 'dears_db'),
    'USER': os.getenv('DB_USER', 'dears_user'),
    'PASSWORD': os.getenv('DB_PASSWORD', ''),
    'HOST': os.getenv('DB_HOST', 'localhost'),
    'PORT': os.getenv('DB_PORT', '5432'),
    'OPTIONS': {
        'sslmode': os.getenv('DB_SSLMODE', 'require'),
    }
}

# Neon-specific connection string format (alternative)
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}?sslmode={SSLMODE}'.format(
        USER=DATABASE_CONFIG['USER'],
        PASSWORD=DATABASE_CONFIG['PASSWORD'],
        HOST=DATABASE_CONFIG['HOST'],
        PORT=DATABASE_CONFIG['PORT'],
        NAME=DATABASE_CONFIG['NAME'],
        SSLMODE=DATABASE_CONFIG['OPTIONS']['sslmode']
    )
)


# =============================================================================
# RPC SERVICE CONFIGURATION
# =============================================================================

# Base RPC configuration
RPC_CONFIG = {
    'timeout': int(os.getenv('RPC_TIMEOUT', '30')),  # seconds
    'allow_none': True,  # Allow None values in RPC calls
    'encoding': 'utf-8',
}

# Police Service RPC Endpoint
POLICE_SERVICE_RPC = {
    'host': os.getenv('POLICE_SERVICE_HOST', 'localhost'),
    'port': int(os.getenv('POLICE_SERVICE_PORT', '8001')),
    'path': '/RPC2',
}

# Fire Service RPC Endpoint
FIRE_SERVICE_RPC = {
    'host': os.getenv('FIRE_SERVICE_HOST', 'localhost'),
    'port': int(os.getenv('FIRE_SERVICE_PORT', '8002')),
    'path': '/RPC2',
}

# Medical Service RPC Endpoint
MEDICAL_SERVICE_RPC = {
    'host': os.getenv('MEDICAL_SERVICE_HOST', 'localhost'),
    'port': int(os.getenv('MEDICAL_SERVICE_PORT', '8003')),
    'path': '/RPC2',
}

# RPC Service URLs (computed)
POLICE_SERVICE_URL = f"http://{POLICE_SERVICE_RPC['host']}:{POLICE_SERVICE_RPC['port']}{POLICE_SERVICE_RPC['path']}"
FIRE_SERVICE_URL = f"http://{FIRE_SERVICE_RPC['host']}:{FIRE_SERVICE_RPC['port']}{FIRE_SERVICE_RPC['path']}"
MEDICAL_SERVICE_URL = f"http://{MEDICAL_SERVICE_RPC['host']}:{MEDICAL_SERVICE_RPC['port']}{MEDICAL_SERVICE_RPC['path']}"


# =============================================================================
# DISPATCHER SERVICE CONFIGURATION
# =============================================================================

DISPATCHER_CONFIG = {
    'host': os.getenv('DISPATCHER_HOST', 'localhost'),
    'port': int(os.getenv('DISPATCHER_PORT', '8000')),
    'api_prefix': '/api',
    'alert_endpoint': '/alerts',
}

DISPATCHER_URL = f"http://{DISPATCHER_CONFIG['host']}:{DISPATCHER_CONFIG['port']}"
DISPATCHER_ALERT_URL = f"{DISPATCHER_URL}{DISPATCHER_CONFIG['api_prefix']}{DISPATCHER_CONFIG['alert_endpoint']}"


# =============================================================================
# DJANGO WEB APP CONFIGURATION
# =============================================================================

DJANGO_CONFIG = {
    'host': os.getenv('DJANGO_HOST', 'localhost'),
    'port': int(os.getenv('DJANGO_PORT', '8080')),
    'secret_key': os.getenv('DJANGO_SECRET_KEY', 'dev-secret-key-change-in-production'),
    'allowed_hosts': os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(','),
}


# =============================================================================
# EMERGENCY TYPES AND CONSTANTS
# =============================================================================

# Emergency type mappings
EMERGENCY_TYPES = {
    'POLICE': 'police',
    'FIRE': 'fire',
    'MEDICAL': 'medical',
}

# Alert status values
ALERT_STATUS = {
    'PENDING': 'pending',
    'DISPATCHED': 'dispatched',
    'EN_ROUTE': 'en_route',
    'ARRIVED': 'arrived',
    'RESOLVED': 'resolved',
    'CANCELLED': 'cancelled',
}

# Response unit status values
UNIT_STATUS = {
    'AVAILABLE': 'available',
    'EN_ROUTE': 'en_route',
    'ON_SCENE': 'on_scene',
    'UNAVAILABLE': 'unavailable',
}

# User roles
USER_ROLES = {
    'CITIZEN': 'citizen',
    'ADMIN': 'admin',
}


# =============================================================================
# LOCATION AND GEOSPATIAL SETTINGS
# =============================================================================

# Default location settings (for testing/development)
DEFAULT_LOCATION = {
    'latitude': 33.5731,  # Casablanca, Morocco (example)
    'longitude': -7.5898,
}

# Maximum distance for unit search (in kilometers)
MAX_SEARCH_RADIUS_KM = float(os.getenv('MAX_SEARCH_RADIUS_KM', '50'))


# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '[{levelname}] {asctime} {name} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.getenv('LOG_FILE', 'dears.log'),
            'formatter': 'detailed',
            'level': 'INFO',
        },
    },
    'loggers': {
        'dears': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}


# =============================================================================
# SECURITY SETTINGS
# =============================================================================

SECURITY_CONFIG = {
    'rpc_auth_enabled': os.getenv('RPC_AUTH_ENABLED', 'False').lower() == 'true',
    'rpc_auth_token': os.getenv('RPC_AUTH_TOKEN', ''),
    'api_rate_limit': int(os.getenv('API_RATE_LIMIT', '100')),  # requests per minute
    'use_https': os.getenv('USE_HTTPS', 'False').lower() == 'true',
}


# =============================================================================
# SERVICE HEALTH CHECK CONFIGURATION
# =============================================================================

HEALTH_CHECK_CONFIG = {
    'enabled': True,
    'interval_seconds': int(os.getenv('HEALTH_CHECK_INTERVAL', '60')),
    'timeout_seconds': int(os.getenv('HEALTH_CHECK_TIMEOUT', '5')),
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_service_url(service_type: str) -> str:
    """
    Get the RPC service URL for a given emergency type.
    
    Args:
        service_type: Emergency type ('POLICE', 'FIRE', or 'MEDICAL')
        
    Returns:
        The RPC service URL for the specified service type
        
    Raises:
        ValueError: If the service type is invalid
    """
    service_urls = {
        'POLICE': POLICE_SERVICE_URL,
        'FIRE': FIRE_SERVICE_URL,
        'MEDICAL': MEDICAL_SERVICE_URL,
    }
    
    service_type = service_type.upper()
    if service_type not in service_urls:
        raise ValueError(f"Invalid service type: {service_type}. Must be one of {list(service_urls.keys())}")
    
    return service_urls[service_type]


def get_database_config() -> Dict[str, Any]:
    """
    Get the complete database configuration dictionary.
    
    Returns:
        Database configuration suitable for Django settings
    """
    return DATABASE_CONFIG.copy()


def is_production() -> bool:
    """
    Check if the current environment is production.
    
    Returns:
        True if running in production mode, False otherwise
    """
    return ENVIRONMENT.lower() == 'production'


def validate_config() -> bool:
    """
    Validate that all required configuration values are set.
    
    Returns:
        True if configuration is valid, raises ValueError otherwise
    """
    if is_production():
        # Check critical production settings
        if DJANGO_CONFIG['secret_key'] == 'dev-secret-key-change-in-production':
            raise ValueError("DJANGO_SECRET_KEY must be set in production")
        
        if not DATABASE_CONFIG['PASSWORD']:
            raise ValueError("DB_PASSWORD must be set in production")
        
        if not SECURITY_CONFIG['use_https']:
            print("WARNING: HTTPS is not enabled in production")
    
    return True


# =============================================================================
# MODULE INITIALIZATION
# =============================================================================

# Validate configuration on import (can be disabled if needed)
if os.getenv('DEARS_VALIDATE_CONFIG', 'True').lower() == 'true':
    try:
        validate_config()
    except ValueError as e:
        print(f"Configuration validation failed: {e}")
        if is_production():
            raise
