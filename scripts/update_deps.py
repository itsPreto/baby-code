import re
import requests


def get_latest_version(package_name: str) -> str:
    """
    Retrieves the latest version of a package from PyPI.

    Args:
        package_name (str): The name of the package to retrieve the latest version for.

    Returns:
        str: The latest version of the specified package.

    Raises:
        Exception: If there is an error retrieving the package information from PyPI.
    """
    pypi_api_url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(pypi_api_url)

    if response.status_code == 200:
        latest_version = response.json()["info"]["version"]
        return latest_version
    else:
        raise Exception(f"Error retrieving {package_name} information. Status code: {response.status_code}")


def update_requirements_txt(file_path: str) -> None:
    """
    Updates the requirements.txt file with the latest versions of packages.

    Args:
        file_path (str): The path to the requirements.txt file.

    Returns:
        None: This function does not return anything.
    """
    with open(file_path, "r") as file:
        requirements = file.readlines()

    updated_requirements = []

    for line in requirements:
        match = re.match(r"^([a-zA-Z0-9-_.]+)==(.+)$", line.strip())
        if match:
            package_name, current_version = match.groups()
            latest_version = get_latest_version(package_name)

            if current_version != latest_version:
                print(f"Updating {package_name} from {current_version} to {latest_version}")
                updated_requirements.append(f"{package_name}=={latest_version}\n")
            else:
                print(f"{package_name} is up to date ({current_version})")
                updated_requirements.append(line)
        else:
            print(f"Skipping unrecognized line: {line.strip()}")
            updated_requirements.append(line)

    with open(file_path, "w") as file:
        file.writelines(updated_requirements)
    print("Requirements file updated.")


requirements_file_path = "/Users/marconeves/Desktop/desktop/projects/baby-llama.pycpp/baby-code/requirements.txt"
update_requirements_txt(requirements_file_path)