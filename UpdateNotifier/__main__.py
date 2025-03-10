from asyncio import run
from json import JSONDecodeError, load

from UpdateNotifier.config import check_env, check_files, logger, services_file, versions_file
from UpdateNotifier.data_io import write_versions
from UpdateNotifier.discord_notifier import send_discord_notification
from UpdateNotifier.services import fetch_all_versions

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
async def main() -> list[dict[str, str]]:
    """
    Main function to fetch the latest versions of the services and compare with the stored versions."

    :return new_versions: List of dictionaries with the service name, version and url.
    """
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
        # Check if the version is different
        if service["version"] != versions_list[service["name"]]:
            logger.info(
                f"New version found for {service['name']}: {versions_list[service['name']]} -> {service['version']}"
            )
            # Update the version in the file
            write_versions(f"{service['name']}", f"{service['version']}")
            # Add the new version to the list
            new_versions.append(service)
    # Return the new versions
    return new_versions


# Run the main function and send notifications if new updates are found
try:
    results = run(main())
    # Send notifications if new updates are found
    if results:
        send_discord_notification(results)
        logger.info("New updates found and notifications sent.")
    else:
        logger.info("No new updates found.")
except Exception as e:
    logger.error(f"Error during execution: {e}")
    exit(1)
