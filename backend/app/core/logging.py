import logging
import sys
from app.config import get_settings


class LoggingConfigurator:
    """
    Configures application-wide logging so that logs are consistently
    formatted and written to stdout.
    """

    def __init__(self) -> None:
        """Load settings needed for log level."""
        self._settings = get_settings()

    def configure(self) -> None:
        """Set up stdout logging with the configured level and format."""
        logging.basicConfig(
            level=getattr(logging, self._settings.log_level.upper(), logging.INFO),
            format=("%(asctime)s " "level=%(levelname)s " "logger=%(name)s " "%(message)s"),
            stream=sys.stdout,
            force=True,
        )


def configure_logging() -> None:
    """Shortcut for setting up logging without building the configurator yourself."""
    LoggingConfigurator().configure()
