import os
import click

from rdp import __basedir__, django
from rdp.system import command
from rdp.data.yaml import Yaml
from rdp.system.file import File
from rdp.system.directory import Directory
from rdp.system.environment import (
    append_to_env_file, append_to_urls
)


class DjangoAppManager:
  
  def __init__(self):
      self.base_dir = Directory.get_cwd()
      self.base_rdp = __basedir__
      
      self.app_name = None
      self.directory = None
      
      self.project_name = None
      self.project_root = None
      self.apps = None
      self.table_prefix = None
      
      self.apps_root = None
      self.app_dir = None  
      self.app_setting_dir = None# After move to project/apps
      
      self.register_api = False
      self.register_views = False
  
  def run(self, args):
      """
      Execute the process of creating and configuring a Django project.

      Parameters:
          args (list): Arguments for the project name and optional directory.
      """
      self.validate_app_inputs(args)
      self.setup_app_config()
      if self.create_app():
          self.modify_app_assets()
          self.setup_models()
          self.setup_admin()
          self.setup_views()
          self.setup_urls()
          self.create_api()
          
          self.register_to_env()
          
  def validate_app_inputs(self, args):
      """
      Validate the input arguments for creating a Django project.

      Parameters:
          args (list): List of arguments containing the project name and optional directory.

      Returns:
          tuple: A tuple containing the validated project name and directory.
      """
      if len(args) < 1:
          raise click.UsageError("You must provide a application name.")

      app_name = args[0]
      if not app_name.isidentifier():
          raise click.UsageError(f"Invalid application name '{app_name}': Must be a valid Python identifier.")

      # Check if current directory in root of Django project
      pwd = os.getcwd()
      if not django.utils.is_django_project_root(directory=pwd):
        raise click.UsageError(f"Current directory '{pwd} not in Django root project!'")
      
      if app_name == 'core':
        raise click.UsageError("App name 'core' required by RDP Library.")
      
      
      
      directory = args[1] if len(args) > 1 else ''
      
      self.app_name = app_name
      self.directory = directory

  def setup_app_config(self):
      # Read rdp.cfg if exist
    config_path = 'rdp.yaml'
    if File.exist(config_path):
      config = Yaml(config_path)
      
      self.project_name = config.get('project.name', '')
      self.project_root = config.get('project.root', self.base_dir) 
      self.apps = config.get('project.apps', 'apps')
      self.table_prefix = config.get('project.table_prefix', 'app')
    else:
      self.project_name, self.project_root, self.apps, self.table_prefix = '', self.base_dir, 'apps', 'app'
    
    # Check if app_name == project_name
    if self.app_name == self.project_name:
      raise click.UsageError(f"App name '{self.app_name}' is equal with project name '{self.project_name}'.")

    self.apps_root = os.path.join(self.project_root, self.apps)
    self.app_setting_dir = f'{self.project_root}/{self.project_name}'
  
  def create_app(self):
            
      command_list = ['django-admin', 'startapp', self.app_name]
      if self.directory:
          command_list.append(self.directory)
          
      if not command.run(command_list):
          raise click.ClickException("Failed to create Django app.")
      
      # Move to project/apps/
      app = f'{self.project_root}/{self.app_name}'
      Directory.move(app, self.apps_root)
      
      self.app_dir = f'{self.apps_root}/{self.app_name}'
      
      return True
    
  def modify_app_assets(self):
    # Replace apps.py from name = 'product' to name = 'apps.product'
    apps = File(f'{self.app_dir}/apps.py')
    apps.find_replace(find=self.app_name, replace=f'{self.apps}.{self.app_name}')
    
    
    
  def setup_models(self):
      models_dir = Directory(f'{self.app_dir}/models')
      models_dir.create()
      
      File(f'{models_dir.str()}/__init__.py').touch()
      src = self.base_rdp / "django/assets/app/models.py"
      dest = f'{models_dir.str()}/{self.app_name}.py'
      find = ['Xmodel', 'x_model', 'x_apps']
      replace = [f'{self.app_name.capitalize()}', f'{self.table_prefix}_{self.app_name}', self.apps]
      File.copy_find_replace(src, dest, find, replace)
      File(f'{self.app_dir}/models.py').delete()

  def setup_admin(self):
      src = self.base_rdp / "django/assets/app/admin.py"
      dest = f'{self.app_dir}/admin.py'
      find = ['XModel', 'xapps', 'xname']
      replace = [f'{self.app_name.capitalize()}', self.apps, self.app_name]
      File.copy_find_replace(src, dest, find, replace, replace_file=True)

  def setup_views(self):
    create = input("Append views (Yes)? ") or "Yes"
    if create == "Yes":
      self.register_views = True
      views_dir = Directory(f'{self.app_dir}/views')
      views_dir.create()
      
      File(f'{views_dir.str()}/__init__.py').touch()
      src = self.base_rdp / "django/assets/app/views.py"
      dest = f'{views_dir.str()}/{self.app_name}.py'
      find = ['XModel', 'x_apps', 'x_name']
      replace = [f'{self.app_name.capitalize()}', self.apps, self.app_name]
      File.copy_find_replace(src, dest, find, replace)
      File(f'{self.app_dir}/views.py').delete()
      
      src = self.base_rdp / "django/assets/templates/components/Layouts/templates/blank.html"
      dest = f'templates/{self.apps}/{self.app_name}/{self.app_name}.html'
      File.copy(src, dest, create_dest_folder=True)
      
      # Forms
      forms_dir = Directory(f'{self.app_dir}/forms')
      forms_dir.create()
      
      File(f'{views_dir.str()}/__init__.py').touch()
      src = self.base_rdp / "django/assets/app/forms.py"
      dest = f'{forms_dir.str()}/{self.app_name}.py'
      find = ['XModel', 'xname', 'xapps' ]
      replace = [f'{self.app_name.capitalize()}', self.app_name, self.apps]
      File.copy_find_replace(src, dest, find, replace)
      
      

  def setup_urls(self):
      src = self.base_rdp / "django/assets/app/urls.py"
      dest = f'{self.app_dir}/urls.py'
      find = ['XModel', 'x_name']
      replace = [f'{self.app_name.capitalize()}', self.app_name]
      File.copy_find_replace(src, dest, find, replace, replace_file=True)


   
  def create_api(self):
    create = input("Append RestFull/API? (Yes)? ") or "Yes"
    if create == "Yes":
      self.register_api = True
      # Copy from 
      src = self.base_rdp / "django/assets/api"
      dest = f'{self.app_dir}/api'
      Directory.copy(src, dest, copy_subdirs=True, replace_existing=False)
      
      # Update urls
      find = ['xmodel', 'XModel']
      replace = [self.app_name, self.app_name.capitalize()]
      files = ['/api/urls.py', '/api/serializers.py', '/api/views/views.py']
      for file in files:
        urls = File(f'{self.app_dir}{file}')
        urls.find_replace(find=find, replace=replace)
      
      # rename /api/views/views.py -> app_name.py
      File.move(f'{self.app_dir}/api/views/views.py', f'{self.app_dir}/api/views/{self.app_name}.py')
      
   
  def register_to_env(self):
    register_to_env = input("Register to .env (Yes)? ") or "Yes"
    if register_to_env == "Yes":
      env_file = self.base_dir / '.env'
      append_to_env_file(env_file=env_file, key='APPS', value_to_append=f'{self.apps}.{self.app_name}, ')
      
      # Views
      if self.register_views:
        urls = self.base_dir / f'{self.project_name}/urls.py'
        new_path = f"    path('{self.app_name}/', include('{self.apps}.{self.app_name}.urls'), name='{self.app_name}'),\n"
        append_to_urls(file_path=urls, new_path=new_path)
      
      # API URLs
      if self.register_api:
        urls = self.base_dir / f'{self.project_name}/urls.py'
        # new_path = f"    path('{self.app_name}/', include('{self.apps}.{self.app_name}.urls'), name='{self.app_name}'),\n"
        new_path = f"    path(f'{{api_path}}/{self.app_name}/', include('apps.{self.app_name}.api.urls'), name='{self.app_name}_api'),"
        append_to_urls(file_path=urls, new_path=new_path)
        

