import os
import click

from rdp.system import command
from rdp.data.yaml import Yaml
from rdp import __basedir__
from rdp.system.file import File
from rdp.system.directory import Directory
# from rdp.system.library import is_library_installed
from rdp.system.environment import (append_to_env_file, get_value_from_file)
 
''''
# Usage
base_dir = Path.cwd()  # Current working directory
    
manager = DjangoProjectManager(base_dir)
manager.run(args)
'''
class DjangoProjectManager:
    """
    A class to create and configure a Django project directory structure.

    This class provides methods to:
    1. Validate project inputs.
    2. Create a Django project structure.
    3. Setup configurations and assets.
    4. Modify specific project files and settings.
    """
    
    BASE_DIR = os.getcwd()
    BASE_RDP = __basedir__
    
    def __init__(self):
        self.project_name = ''
        self.project_root = ''
        self.directory = ''
        self.env = ''
        self.apps = ''
    
    def run(self, args):
        """
        Execute the process of creating and configuring a Django project.

        Parameters:
            args (list): Arguments for the project name and optional directory.
        """
        self.validate_project_inputs(args)
        if self.create_project():
            self.setup_project_config()
            self.setup_project_assets()
            self.install_dependencies()
            self.modify_project_settings()

    def validate_project_inputs(self, args):
        """
        Validate the input arguments for creating a Django project.

        Parameters:
            args (list): List of arguments containing the project name and optional directory.

        Returns:
            tuple: A tuple containing the validated project name and directory.
        """
        if len(args) < 1:
            raise click.UsageError("You must provide a project name.")

        project_name = args[0]
        if not project_name.isidentifier():
            raise click.UsageError(f"Invalid project name '{project_name}': Must be a valid Python identifier.")

        directory = args[1] if len(args) > 1 else ''
        
        self.project_name = project_name
        self.directory = directory

    def create_project(self):
        """
        Create the Django project structure using `django-admin`.

        Parameters:
            project_name (str): The name of the project.
            directory (str): Optional target directory for the project.

        Returns:
            bool: True if the project was successfully created, False otherwise.
        """
        command_list = ['django-admin', 'startproject', self.project_name]
        if self.directory:
            command_list.append(self.directory)

        return command.run(command=command_list, is_debug=True)

    def setup_project_config(self):
        """
        Setup initial project configurations.

        Parameters:
            project_name (str): The name of the project.
            custom_config (bool): Whether to allow custom configurations.
        """
        self.project_root = os.path.join(DjangoProjectManager.BASE_DIR, self.project_name)
        if self.directory == ".":
            self.project_root = DjangoProjectManager.BASE_DIR 
        
        custom_config = input("Do you want custom config for this project (Yes)") or "Yes"
        if custom_config == "Yes":
            apps = input("Directory for new Django application (apps)?") or "apps"
            table_prefix = input("Table prefix (app)?") or "app"
            env = input("Default environment 'dev' or 'prod' (dev)?") or "dev"
        else:
            apps, table_prefix, env = "apps", "app", "dev"

        data = {
            'project': {
                'name': self.project_name,
                'root': self.project_root,
                'apps': apps,
                'table_prefix': table_prefix,
                'environment': env,
            }
        }

        self.env = env
        self.apps = apps
        
        config_path = os.path.join(self.project_root, 'rdp.yaml')
        config = Yaml(config_path)
        config.save_config(data=data)

    def setup_project_assets(self):
        """
        Copy and organize project assets and configurations.

        Parameters:
            project_name (str): The name of the project.
        """
        # project_root = os.path.join(DjangoProjectManager.BASE_DIR, project_name)
        src = DjangoProjectManager.BASE_RDP / 'django/assets/settings'
        dest = os.path.join(self.project_root, self.project_name, 'settings')
        Directory.copy(src, dest)

        # Rename settings.py to settings/base.py
        settings = os.path.join(self.project_root, self.project_name)
        src = os.path.join(settings, 'settings.py')
        dest = os.path.join(dest, 'base.py')
        File.move(src, dest)
        
        # Modify <app>/settings.py
        find = "'DIRS': [],"
        replace = "'DIRS': ['templates', ],"
        File(dest).find_replace(find=find, replace=replace)

        # Copy environment files and requirements
        src = DjangoProjectManager.BASE_RDP / 'django/assets'
        Directory.copy(src, self.project_root, copy_subdirs=False)
        
        ## APPS
        apps_dir = Directory(dir_path=f'{self.project_root}/{self.apps}')
        apps_dir.create()
        # copy from django/assets/core to apps/core
        src = DjangoProjectManager.BASE_RDP / "django/assets/core"
        Directory.copy(src, apps_dir.str('core'))
        
        # UPDATE .env APPS =
        src = f'{self.project_root}/.env'
        value = f'{self.apps}.core, '
        append_to_env_file(env_file=src, key='APPS', value_to_append=f'{value}')
        
        # Copy templates
        src = DjangoProjectManager.BASE_RDP / "django/assets/templates"
        dest = f'{self.project_root}/templates'
        Directory.copy(src, dest, copy_subdirs=True, replace_existing=False)

        # Copy static
        src = DjangoProjectManager.BASE_RDP / "django/assets/static"
        dest = f'{self.project_root}/static'
        Directory.copy(src, dest, copy_subdirs=True, replace_existing=False)
        
        # Change directory
        if self.directory != ".":
            main_dir = os.getcwd()
            try:
                os.chdir(self.project_root)
                command.run(command=[f'{self.project_root}/tailwind-install'], is_debug=False)
            finally:
                os.chdir(main_dir)
        else:
            command.run(command=[f'{self.project_root}/tailwind-install'], is_debug=True)
        

    def modify_project_settings(self):
        """
        Modify Django project settings and related files.

        Parameters:
            project_name (str): The name of the project.
            env (str): The environment ('dev' or 'prod').
        """
        # project_root = os.path.join(DjangoProjectManager.BASE_DIR, project_name)
        
        # Update .env file with settings
        env_path = os.path.join(self.project_root, '.env')
        append_to_env_file(env_path, 'DJANGO_SETTINGS_MODULE', f"{self.project_name}.settings.{self.env}")
        
        # Get SECRET_KEY from settings
        src = f'{self.project_root}/{self.project_name}/settings/base.py'  # Path to the file
        key = 'SECRET_KEY'
        value = get_value_from_file(src, key)
        # Replace in .env
        src = f'{self.project_root}/.env'
        append_to_env_file(env_file=src, key=key, value_to_append=f'"{value}"')
        
        # Replace BASE_DIR parent
        src = f'{self.project_root}/{self.project_name}/settings/base.py'  # Path to the file
        find = 'BASE_DIR = Path(__file__).resolve().parent.parent'
        replace = 'BASE_DIR = Path(__file__).resolve().parent.parent.parent'
        File(src).find_replace(find, replace)

        # Modify manage.py to load environment variables
        manage_path = os.path.join(self.project_root, 'manage.py')
        find = ['import sys', 'def main():']
        replace = ["import sys\nfrom dotenv import load_dotenv\n", "def main():\n    load_dotenv()\n"]
        File(manage_path).find_replace(find, replace)
        
        src = f'{self.project_root}/{self.project_name}/urls.py'
        find = 'from django.urls import path'
        replace = 'from django.urls import path, include\n\napi_path = os.getenv("API_PATH", "v1")\n'
        File(src).find_replace(find, replace)
        
        # Modify asgi.py
        manage_path = os.path.join(self.project_root, self.project_name, 'asgi.py')
        find = ['from django.core.asgi import get_asgi_application']
        replace = ["from django.core.asgi import get_asgi_application\nfrom dotenv import load_dotenv\n\nload_dotenv()"]
        File(manage_path).find_replace(find, replace)
        
        # Modify asgi.py
        manage_path = os.path.join(self.project_root, self.project_name, 'wsgi.py')
        find = ['from django.core.wsgi import get_wsgi_application']
        replace = ["from django.core.wsgi import get_wsgi_application\nfrom dotenv import load_dotenv\n\nload_dotenv()"]
        File(manage_path).find_replace(find, replace)

    def install_dependencies(self):
        """
        Install required dependencies for the project.
        """
        # if not is_library_installed('import_export'):
        command.run(['pip', 'install', '-r', f'{self.project_root}/requirements.txt'], is_debug=False)

    
