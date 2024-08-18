import os
import json
import joblib
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from pathlib import Path
from typing import Any
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a YAML file and returns a ConfigBox object.

    Args:
        path_to_yaml (Path): Path to the YAML file.

    Raises:
        ValueError: If the YAML file is empty or cannot be loaded.
        FileNotFoundError: If the YAML file is not found.
        yaml.YAMLError: If there is a syntax error in the YAML file.
        Exception: For any other errors encountered.

    Returns:
        ConfigBox: A ConfigBox object containing the parsed YAML data.
    """
    try:
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            if content is None:
                raise ValueError(f"YAML file {path_to_yaml} is empty.")
            validate_yaml_content(content)  # Optional: validate YAML structure
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"YAML file {path_to_yaml} has an invalid structure.")
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file {path_to_yaml} not found.")
    except yaml.YAMLError as e:
        logger.error(f"YAML syntax error in file {path_to_yaml}: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error loading YAML file {path_to_yaml}: {e}")
        raise e


def validate_yaml_content(content):
    """Validates the content of the YAML file.

    Args:
        content (dict): The content of the YAML file.

    Raises:
        ValueError: If the content is invalid.
    """
    # Example validation, customize based on your needs
    if 'required_key' not in content:
        raise ValueError("YAML content is missing 'required_key'.")
    # Add more validations as needed


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Create directories if they don't exist.

    Args:
        path_to_directories (list): List of directory paths to create.
        verbose (bool, optional): Whether to log the creation. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """Save data to a JSON file.

    Args:
        path (Path): Path to the JSON file.
        data (dict): Data to be saved.
    """
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"JSON file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load data from a JSON file.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        ConfigBox: A ConfigBox object with the loaded data.
    """
    with open(path, "r") as f:
        content = json.load(f)
    logger.info(f"JSON file loaded successfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """Save data to a binary file using joblib.

    Args:
        data (Any): Data to be saved.
        path (Path): Path to the binary file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Load data from a binary file using joblib.

    Args:
        path (Path): Path to the binary file.

    Returns:
        Any: The loaded data.
    """
    data = joblib.load(path)
    logger.info(f"Binary file loaded from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """Get the size of a file in KB.

    Args:
        path (Path): Path of the file.

    Returns:
        str: Size of the file in KB.
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"
