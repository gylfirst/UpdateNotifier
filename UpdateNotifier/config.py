import logging
from logging.handlers import RotatingFileHandler
from os import getenv, path

from dotenv import find_dotenv, load_dotenv

# Load environment variables from .env file
if not find_dotenv():
    raise FileNotFoundError("The .env file is missing.")
load_dotenv()


# Get the directory of the current script
base_dir = path.dirname(path.abspath(__file__))

# Define file paths for services, versions and logs
services_file = path.join(base_dir, "../data/services.txt")
versions_file = path.join(base_dir, "../data/versions.json")
log_file = path.join(base_dir, "../logs/app.log")

# Retrieve environment variables
webhook_url = getenv("DISCORD_WEBHOOK_URL")
discord_role_id = getenv("DISCORD_ROLE_ID")
log_level = getenv("LOG_LEVEL", "INFO")


def check_env() -> None:
    """
    Check if the required environment variables are set.

    :raises OSError: If the environment variables are not set.
    """
    # Check if environment variables are set
    if webhook_url is None or discord_role_id is None:
        logging.error(
            "Please set the `DISCORD_WEBHOOK_URL` and `DISCORD_ROLE_ID` environment variables."
        )
        raise OSError(
            "Please set the `DISCORD_WEBHOOK_URL` and `DISCORD_ROLE_ID` environment variables."
        )


def check_files() -> None:
    """
    Check if the required files exist and are not empty.

    :raises FileNotFoundError: If the files do not exist or are empty (only for services.txt).
    """
    # Check if services file exists or empty, if not create it and notify the user by exception
    if not path.isfile(services_file) or path.getsize(services_file) == 0:
        with open(services_file, "w") as file:
            file.write("")
        logging.error("Please add services to the `/data/services.txt` file.")
        raise FileNotFoundError("Please add services to the `/data/services.txt` file.")

    # Check if versions file exists or empty, if not create it and notify the user by exception
    if not path.isfile(versions_file) or path.getsize(versions_file) == 0:
        with open(versions_file, "w") as file:
            file.write("{}")
        logging.warning("No current versions found in `/data/versions.json` file...")
        logging.info("Adding an empty JSON object for you...")
        logging.info("This will deploy notifications for all services.")


# Configure logging
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# File handler
file_handler = RotatingFileHandler(
    log_file, maxBytes=5 * 1024 * 1024, backupCount=3
)  # 5 MB per file, keep 3 backups
file_handler.setFormatter(log_formatter)

# Stream handler (console)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)

# Basic configuration
logging.basicConfig(level=log_level, handlers=[file_handler, stream_handler])

# Create logger
logger = logging.getLogger("UpdateNotifier")
