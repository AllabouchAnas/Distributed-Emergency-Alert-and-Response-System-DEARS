import logging
import os
from typing import Optional, Union

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_DATEFMT = os.getenv("LOG_DATEFMT", "%Y-%m-%d %H:%M:%S")
_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFMT)


def _resolve_level(level: Optional[Union[int, str]]) -> int:
    if level is None:
        level = LOG_LEVEL
    if isinstance(level, int):
        return level
    if isinstance(level, str):
        lvl = getattr(logging, level.upper(), None)
        if isinstance(lvl, int):
            return lvl
    return logging.INFO


def get_logger(name: Optional[str] = None, level: Optional[Union[int, str]] = None) -> logging.Logger:
 
    logger = logging.getLogger(name or "police_service")
    eff_level = _resolve_level(level)

    # Always update level/formatter if called again
    logger.setLevel(eff_level)

    if logger.handlers:
        for h in logger.handlers:
            h.setLevel(eff_level)
            try:
                h.setFormatter(_formatter)
            except Exception:
                pass
        logger.propagate = False
        return logger

    handler = logging.StreamHandler()
    handler.setLevel(eff_level)
    handler.setFormatter(_formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger

logger = get_logger()
