import logging
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler

console_handler = RichHandler(
    rich_tracebacks=True,
    show_time=True,
    show_level=True,
    show_path=False,
)

file_handler = RotatingFileHandler(
    "app.log",
    maxBytes=5_000_000,
    backupCount=3,
    encoding="utf-8",
)

file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
)

logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler],
    force=True,
)

logger = logging.getLogger("app")