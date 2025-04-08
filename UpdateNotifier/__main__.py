from asyncio import run
from json import JSONDecodeError, load

from UpdateNotifier.config import (
    check_env,
    check_files,
    logger,
    ping_all_releases,
    services_file,
    versions_file,
)
from UpdateNotifier.data_io import write_versions
from UpdateNotifier.discord_notifier import send_discord_notification
from UpdateNotifier.services import determine_if_major_update, fetch_all_versions

# Initialize the application
logger.info("Initializing the application.")
try:
    check_env()
    check_files()
except Exception as e:
    logger.error(f"Initialization error: {e}")
    exit(1)

# Read services from file
logger.debug("Reading services from file.")
try:
    with open(services_file) as file:
        services_list = [line.strip() for line in file.readlines()]
except OSError as e:
    logger.error(f"Error reading {services_file}: {e}")
    exit(1)

# Read versions from file
logger.debug("Reading versions from file.")
try:
    with open(versions_file) as file:
        versions_list = load(file)
except (OSError, JSONDecodeError) as e:
    logger.error(f"Error reading {versions_file}: {e}")
    versions_list = {}


# Main function
async def main() -> tuple[list[dict[str, str]], bool]:
    """
    Main function to fetch the latest versions of the services and compare with the stored versions."

    :return new_versions: List of dictionaries with the service name, version and url.
    :return ping_user: Boolean indicating if the user should be pinged.
    """
    # Define the ping_user variable with the value of ping_all_releases (defined in .env file)
    ping_user = ping_all_releases
    logger.info("Starting to fetch latest versions.")
    # Fetch the latest versions of the services (formatted)
    results = await fetch_all_versions(services_list)
    # New versions found
    new_versions = []
    # Compare the versions
    for service in results:
        # Check if the service is new
        if service["name"] not in versions_list:
            logger.info(
                f"New service found: {service['name']}, writing the latest version: {service['version']}"
            )
            # Write the new version to the file
            write_versions(f"{service['name']}", f"{service['version']}")
            # Add the new service to the list
            versions_list[service["name"]] = service["version"]
            new_versions.append(service)
            # Set ping_user to True if a new service is found, even if ping_all_releases is False
            logger.debug("As a new service was found, all releases will be pinged.")
            ping_user = True

        if service["version"] != versions_list[service["name"]]:
            # Compare the versions, determine if this is a major update or not
            is_major = await determine_if_major_update(service, versions_list)
            if is_major:
                logger.debug(
                    f"Major update found for {service['name']}: {versions_list[service['name']]} -> {service['version']}"
                )
                # Set ping_user to True if a major update is found
                ping_user = True
            else:
                logger.debug(
                    f"Minor update found for {service['name']}: {versions_list[service['name']]} -> {service['version']}"
                )
            # Update the version in the file
            write_versions(f"{service['name']}", f"{service['version']}")
            # Add the new version to the list
            new_versions.append(service)
    # Return the new versions
    return new_versions, ping_user


# Run the main function and send notifications if new updates are found
try:
    results, ping_user = run(main())
    # Send notifications if new updates are found
    if results:
        send_discord_notification(results, ping_user)
        logger.info("New updates found and notifications sent.")
    else:
        logger.info("No new updates found.")
except Exception as e:
    logger.error(f"Error during execution: {e}")
    exit(1)
