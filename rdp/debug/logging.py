import importlib.util
from pathlib import Path

import logging
import logging.config
import yaml

from rdp import __name__

class LoggerSetup:
    def __init__(self, package_name: str, config_file: str = 'logging.yaml'):
        self.package_name = package_name
        self.config_file = config_file
        
        self.logger = self._setup_logging()

    def _setup_logging(self):
        """
        Sets up logging configuration from a YAML file found in the 'debug' directory of the given package.

        :return: A logger object if successful, None otherwise.
        """
        spec = importlib.util.find_spec(self.package_name)

        if spec is None:
            print(f"Library '{self.package_name}' not found.")
            return None
        else:
            package_dir = Path(spec.origin).parent
            config_path = package_dir / 'debug' / self.config_file

            if config_path.exists():
                with open(config_path, 'r') as file:
                    config = yaml.safe_load(file.read())
                    logging.config.dictConfig(config)
                    return logging.getLogger(self.package_name)
            else:
                print(f"Configuration file '{config_path}' not found!")
                return None
            
    def get_logger(self):
        # Ensure the logger is properly initialized before use
        if self.logger is None:
            raise ValueError("Logger has not been set up correctly.")
        return self.logger
    
    def __call__(self):
        # Ketika objek LoggerSetup dipanggil, akan mengembalikan logger
        return self.logger

logger = LoggerSetup(__name__)()