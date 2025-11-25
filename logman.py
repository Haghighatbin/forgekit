import os
import logging
import platform
import subprocess
import socket
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
from src.configs.config import Config


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    if not logger.handlers:  
        logger.setLevel(Config.LOG_LEVEL)

        # Ensure logs folder exists
        log_folder = os.path.join(os.getcwd(), 'logs')
        os.makedirs(log_folder, exist_ok=True)
        log_filename = os.path.join(log_folder, f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

        # File handler with rotation
        file_handler = RotatingFileHandler(log_filename, maxBytes=5 * 1024 * 1024, backupCount=5)
        file_handler.setLevel(Config.LOG_LEVEL)
        file_formatter = logging.Formatter(
            '[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(module)s] - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        # Rich console handler
        rich_handler = RichHandler(rich_tracebacks=True, markup=True)
        rich_handler.setLevel(Config.LOG_LEVEL)
        rich_handler.setFormatter(logging.Formatter("%(message)s"))

        # Add handlers to logger
        logger.addHandler(file_handler)
        # logger.addHandler(rich_handler)

    return logger


def collect_run_metadata(seed: int) -> dict:
    """Gather host, git SHA and versions for run.json and first log line."""
    try:
        git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        git_sha = "unknown"
    try:
        import tensorflow as tf
        tf_ver = tf.__version__
    except Exception:
        tf_ver = "not-imported"
    import numpy as np
    return {
        "seed": seed,
        "git_sha": git_sha,
        "host": socket.gethostname(),
        "python": platform.python_version(),
        "tensorflow": tf_ver,
        "numpy": np.__version__,
        "started_at": datetime.now(timezone.utc).isoformat()
    }