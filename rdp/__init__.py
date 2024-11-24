import importlib.util
from pathlib import Path

from . import django, image, debug, system, text, data, net

__all__ = [
  django, image, debug, system, text, data, net,
]

# Define the metadata | from rdp import __name__, __version__, __description__
__name__ = 'rdp'
__version__ = '0.1.0'
__description__ = 'Utility tools for Python and Django framework.'

__basedir__ = Path(importlib.util.find_spec(__name__).origin).parent
