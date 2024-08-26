import json
import logging
import os

from dotenv import load_dotenv

load_dotenv()

LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Create log directories if they do not exist
LOG_DIR_GENERAL = os.getenv("LOG_DIR_GENERAL", f"{LOG_DIR}/general")
LOG_DIR_ERRORS = os.getenv("LOG_DIR_ERRORS", f"{LOG_DIR}/errors")

os.makedirs(LOG_DIR_GENERAL, exist_ok=True)
os.makedirs(LOG_DIR_ERRORS, exist_ok=True)


def init_logger(file_path):
    # Derive module name from the file path
    module_name = os.path.splitext(os.path.relpath(file_path, start=os.getcwd()))[
        0
    ].replace(os.sep, ".")

    # Load logging configuration from JSON file
    with open("logging_config.json", "r") as f:
        config = json.load(f)

    # Update the log file paths to include the module name and full path from the 'app' directory
    relative_file_path = os.path.relpath(file_path, start="app")
    general_log_path = os.path.join(LOG_DIR_GENERAL, f"{relative_file_path}.log")
    error_log_path = os.path.join(LOG_DIR_ERRORS, f"{relative_file_path}_error.log")

    # Ensure the log directories exist
    os.makedirs(os.path.dirname(general_log_path), exist_ok=True)
    os.makedirs(os.path.dirname(error_log_path), exist_ok=True)

    # Create file handlers for the module
    general_handler = logging.FileHandler(general_log_path)
    general_handler.setLevel(logging.DEBUG)  # Capture all levels of logs
    general_handler.setFormatter(
        logging.Formatter(config["formatters"]["standard"]["format"])
    )

    error_handler = logging.FileHandler(error_log_path)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(
        logging.Formatter(config["formatters"]["detailed"]["format"])
    )

    # Create console handler for the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(
        logging.INFO
    )  # Capture INFO level and above for the console
    console_handler.setFormatter(
        logging.Formatter(config["formatters"]["standard"]["format"])
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


# Example usage in different files
if __name__ == "__main__":
    logger = init_logger(__file__)
    logger.info("This is an info message")
    logger.error("This is an error message")
