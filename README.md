# UpdateNotifier

[![Docker Image](https://github.com/gylfirst/UpdateNotifier/actions/workflows/docker-image.yaml/badge.svg?branch=main)](https://github.com/gylfirst/UpdateNotifier/actions/workflows/docker-image.yaml)
[![Docker Image Version](https://img.shields.io/docker/v/gylfirst/updatenotifier?style=flat)](https://hub.docker.com/r/gylfirst/updatenotifier)

UpdateNotifier is a Python application that checks for the latest releases of specified GitHub repositories and sends notifications to a Discord channel if new updates are found.

## Features

- Fetches the latest release versions of specified GitHub repositories.
- Sends notifications to a Discord channel using a webhook.
- Logs activities and errors for easy debugging.

## Requirements

- Python 3.11 or higher
- `aiohttp`
- `asyncio`
- `discord-webhook`
- `python-dotenv`

You better have a virtual environment for your python installation. See [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) in order to setup it.

You can need a GitHub Personal Token in order to increase the rate limit for your requests. <br>
Note that the rate without is 60 requests by hour, so if you have more services than this amount, you won't get all the version checks. <br>
For that, go to your token settings ([link](https://github.com/settings/tokens)) and create a token without any permissions. You can change the expiration date if needed.

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
    GITHUB_TOKEN = "your github token"  # Optional, but you will have a rate limit of 60 requests per hour
    ```

    You can change the log level if needed.

## Usage

### Python

1. Add the GitHub repositories you want to monitor to the `data/services.txt` file. Each line should contain a repository in the format `owner/repo`.

2. Run the application:

    ```bash
    python -m UpdateNotifier
    ```

### Docker

You can use the [docker image](https://hub.docker.com/r/gylfirst/updatenotifier) with the docker compose file. <br>
The app is designed to be launched once, so you can set up a cronjob or a script to execute it regularly.

## Configuration

- **Environment Variables**:
  - `DISCORD_WEBHOOK_URL`: The URL of the Discord webhook.
  - `DISCORD_ROLE_ID`: The ID of the Discord role to ping.
  - `LOG_LEVEL`: The logging level (optional, default is `INFO`).
  - `GITHUB_TOKEN`: Your personal token to authenticate your requests.

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
