import json
import logging
import os
from app.configs.general import GeneralSettings


class LoggerSettings(GeneralSettings):
    LOG_DIR: str

    @property
    def LOG_DIR_GENERAL(self):
        return f"{self.LOG_DIR_GENERAL}/general"

    @property
    def LOG_DIR_ERRORS(self):
        return f"{self.LOG_DIR_GENERAL}/errors"

    @classmethod
    def create_log_dirs(cls, values: dict[str, str]):
        try:
            os.makedirs(values.get("LOG_DIR_GENERAL"), exist_ok=True)
            os.makedirs(values.get("LOG_DIR_ERRORS"), exist_ok=True)
        except OSError as e:
            logging.error(f"Error creating log directories: {e}")
            raise


def init_logger(file_path: str, settings: LoggerSettings) -> logging.Logger:
    # Derive module name from the file path
    module_name = os.path.splitext(os.path.relpath(file_path, start=os.getcwd()))[
        0
    ].replace(os.sep, ".")

    # Load logging configuration from JSON file
    try:
        with open("logging_config.json") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise RuntimeError("Logging configuration file not found.")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error parsing logging configuration: {e}")

    # Update the log file paths to include the module name and full path from the 'app' directory
    relative_file_path = os.path.relpath(file_path, start="app")
    general_log_path = os.path.join(
        settings.LOG_DIR_GENERAL,
        f"{relative_file_path}.log",
    )
    error_log_path = os.path.join(
        settings.LOG_DIR_ERRORS,
        f"{relative_file_path}_error.log",
    )

    # Ensure the log directories exist
    try:
        os.makedirs(os.path.dirname(general_log_path), exist_ok=True)
        os.makedirs(os.path.dirname(error_log_path), exist_ok=True)
    except OSError as e:
        raise RuntimeError(f"Error creating log directories: {e}")

    # Create file handlers for the module
    general_handler = logging.FileHandler(general_log_path)
    general_handler.setLevel(logging.INFO)  # Capture all levels of logs
    general_handler.setFormatter(
        logging.Formatter(config["formatters"]["standard"]["format"]),
    )

    error_handler = logging.FileHandler(error_log_path)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(
        logging.Formatter(config["formatters"]["detailed"]["format"]),
    )

    # Create console handler for the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Capture DEBUG level for the console
    console_handler.setFormatter(
        logging.Formatter(config["formatters"]["standard"]["format"]),
    )

    # Configure logger
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # Set logger to capture all levels
    logger.addHandler(general_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    # Remove propagate to avoid duplicate logging to root logger
    logger.propagate = False

    logger.debug(f"{module_name} logger was initialized")

    return logger
