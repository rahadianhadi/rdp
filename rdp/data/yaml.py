import yaml
from pathlib import Path


class Yaml:
  def __init__(self, file_path):
    """
    Initialize Yaml with a given file path.
    """
    self.file_path = Path(file_path)
    if not self.file_path.exists():
      # Create an empty file if it doesn't exist
      self.file_path.write_text("{}")

  def load_config(self):
    """
    Load the YAML configuration file.
    """
    with self.file_path.open('r') as file:
      return yaml.safe_load(file) or {}
    
  def save_config(self, data):
    """
    Save data to the YAML configuration file.
    """
    with self.file_path.open('w') as file:
      yaml.safe_dump(data, file)

  def get(self, key, default=None):
    """
    Get a value by key from the YAML configuration file. Supports nested keys using dot notation.

    :param key: Key to retrieve, with optional section specified (e.g., 'project.apps').
    :param default: Default value to return if the key is not found.
    :return: The value associated with the key or the default value.
    """
    config = self.load_config()
    
    keys = key.split(".")  # Split the key by dots (e.g., 'project.apps' -> ['project', 'apps'])
    for k in keys:
        try:
            config = config[k]  # Traverse the dictionary to the nested value
        except (KeyError, TypeError):
            return default  # Return default if any key is missing or if the value isn't a dictionary
    return config

  def update(self, key, value):
    """
    Update a key-value pair in the YAML configuration file.
    """
    config = self.load_config()
    config[key] = value
    self.save_config(config)

  def remove(self, key):
    """
    Remove a key from the YAML configuration file.
    """
    config = self.load_config()
    if key in config:
        del config[key]
        self.save_config(config)

  def get_all(self):
    """
    Get all items from the YAML configuration file.
    """
    return self.load_config()
  

