# Defines constants for important YAML files.
# Instead of hardcoding file paths in multiple scripts, they are stored in one place (constant/__init__.py).
# If the file location changes, you only need to update it once in constant/__init__.py.

from pathlib import Path

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")