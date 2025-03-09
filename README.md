# UpdateNotifier

UpdateNotifier is a Python application that checks for the latest releases of specified GitHub repositories and sends notifications to a Discord channel if new updates are found.

## Features

- Fetches the latest release versions of specified GitHub repositories.
- Sends notifications to a Discord channel using a webhook.
- Logs activities and errors for easy debugging.

## Requirements

- Python 3.9 or higher
- `aiohttp`
- `asyncio`
- `discord-webhook`
- `python-dotenv`

You better have a virtual environment for your python installation. See [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) in order to setup it.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/gylfirst/UpdateNotifier.git
    cd UpdateNotifier
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Rename the `.env.example` file in the root directory to `.env` and add your Discord webhook URL and role ID:

    ```properties
    DISCORD_WEBHOOK_URL = "your discord webhook url"
    DISCORD_ROLE_ID = "discord id (int)"
    LOG_LEVEL = "INFO"  # Optional, default is INFO
    ```

    You can change the log level if needed.

## Usage

1. Add the GitHub repositories you want to monitor to the `data/services.txt` file. Each line should contain a repository in the format `owner/repo`.

2. Run the application:

    ```bash
    python -m UpdateNotifier
    ```

## Configuration

- **Environment Variables**:
  - `DISCORD_WEBHOOK_URL`: The URL of the Discord webhook.
  - `DISCORD_ROLE_ID`: The ID of the Discord role to ping.
  - `LOG_LEVEL`: The logging level (optional, default is `INFO`).

- **Files**:
  - `data/services.txt`: List of GitHub repositories to monitor.
  - `data/versions.json`: Stores the latest known versions of the repositories.
  - `logs/app.log`: Log file for the application.

## Logging

The application uses a rotating file handler to manage logs. Logs are stored in `logs/app.log` with a maximum size of 5 MB per file and up to 3 backup files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

[Gylfirst](https://github.com/gylfirst)
