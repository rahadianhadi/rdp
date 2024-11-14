# setup.py
from setuptools import setup, find_packages

setup(
  name="rdp",
  version="0.1.0",
  packages=find_packages(),
  install_requires=[
      "Pillow", 
      "requests",
      "beautifulsoup4",
    ],
  description="A utility library for RDP projects",
  author="Rahadian Hadi",
  author_email="rahadianhadi@gmail.com",
  url="https://github.com/rahadianhadi/rdp",
)