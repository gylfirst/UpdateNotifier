from asyncio import gather

from aiohttp import ClientError, ClientSession

from UpdateNotifier.config import github_token, logger

api_github = "https://api.github.com/repos"


def get_service_info(service: dict) -> dict[str, str]:
    """
    Extracts the service name, version and url from the service data.

    :param service: Dictionary with the service data.
    :type service: dict

    :return dict: Dictionary with the service name, version and url.
    """
    logger.debug(f"Processing service: {service['repo_name']}")
    # Keep only the relevant information.
    return {
        "name": service["repo_name"],
        "version": service["tag_name"],
        "url": service["html_url"],
    }


async def get_latest_version(session: ClientSession, service: str) -> dict[str, str]:
    """
    Fetches the latest version of a service using the GitHub API.

    :param session: aiohttp ClientSession object.
    :type session: ClientSession
    :param service: Name of the service to fetch the latest version.
    :type service: str

    :return dict: Dictionary with the service name, version and url.
    """
    logger.info(f"Fetching latest version for {service}.")
    try:
        async with session.get(f"{api_github}/{service}/releases/latest") as response:
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = await response.json()
            data["repo_name"] = service  # Add the repository name to the response
            return get_service_info(data)
    except ClientError as e:
        logger.error(f"Failed to fetch latest version for {service}: {e}")
        return None


async def fetch_all_versions(services_list: list[str]) -> list[dict[str, str]]:
    """
    Fetches the latest version of all services in the list.

    :param services_list: List of services to fetch the latest version.
    :type services_list: list[str]

    :return results: List of dictionaries with the service name, version and url.
    """
    if not github_token:
        logger.info(
            "GITHUB_TOKEN is not set. Requests will be made without authentication and may be rate limited."
        )
        auth_headers = {}
    else:
        auth_headers = {"Authorization": f"token {github_token}"}

    async with ClientSession(headers=auth_headers) as session:
        results = await gather(
            *[get_latest_version(session, service) for service in services_list],
            return_exceptions=True,
        )
    return [result for result in results if result is not None]
