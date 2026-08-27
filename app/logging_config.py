import logging
import json


class JSONFormatter(logging.Formatter):
    """Custom JSON log formatter for structured application logging."""

    def format(self, record):
        log_obj = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)


def setup_logging(app=None):
    """Configure structured logging for the application."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if not root_logger.handlers:
        root_logger.addHandler(handler)

    if app:
        app.logger.setLevel(logging.INFO)
        if not app.logger.handlers:
            app.logger.addHandler(handler)
