from json import JSONDecodeError, dump, load

from UpdateNotifier.config import logger, versions_file


def write_versions(service: str, version: str) -> None:
    """
    Writes the service and version to the versions JSON file.

    :param service: Name of the service.
    :type service: str
    :param version: Latest version of the service.
    :type version: str
    """
    try:
        # Read the existing data from the JSON file
        with open(versions_file) as file:
            data = load(file)
    except FileNotFoundError:
        data = {}
    except JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {versions_file}: {e}")
        data = {}

    # Update the data with the new service and version
    data[service] = version

    try:
        # Write the updated data back to the JSON file
        with open(versions_file, "w") as file:
            dump(data, file, indent=4)
    except OSError as e:
        logger.error(f"Error writing to {versions_file}: {e}")
