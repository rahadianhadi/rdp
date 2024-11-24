# RDP
Utility tools for Python and Django framework.

## Instal
Clone the library and install with pip.
```
git clone https://github.com/rahadianhadi/rdp.git
cd rdp
pip install -e . --config-settings editable_mode=compat
```
Or, directly install from repository.

```
pip install git+https://github.com/rahadianhadi/rdp.git
```

## Library

### Debug
- Logging

### Django
- Utils

### Image
- Convert
- Enum
- Resize
- Utils

### System
- Command

### Text
- String

### Data
- Yaml

## Tests
Running test: pytest

Folder: tests/
- test_image.py


## CLI
Command line interface for Django and other routine.

1. Create Django project 
   ```
   rdp project <name> [directory]
   ```

2. Create Django application
   ```
   cd <project>
   rdp app <name> [directory]
   ```

   What is app tasks do?
   ```
   - App run command: python manage.py startapp <name> [directory]
   - Check if rdp.yaml exist in current root project. Config will load from this file, if not, default config will apply.
   - Check if 'apps' directory exist, if not will create automaticly.
   - Move current 'app' to directory 'apps'.

   ``` 


