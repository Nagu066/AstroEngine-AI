"""
Structured logging and latency measurement utilities.
"""
import time
import logging
import sys
from contextlib import contextmanager
from typing import Generator, Dict, Any, Optional

# Configure standard logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("mynaksh.context_engine")


@contextmanager
def log_latency(operation_name: str, extra_meta: Optional[Dict[str, Any]] = None) -> Generator[None, None, None]:
    """
    Context manager to measure and log execution latency of blocks.
    """
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        meta_str = f" | meta={extra_meta}" if extra_meta else ""
        logger.info(f"LATENCY | {operation_name} completed in {elapsed_ms} ms{meta_str}")
