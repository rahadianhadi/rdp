@main.command()
@click.argument('args', nargs=-1)  # Collect all extra arguments
def project(args):
  """
  Creates a Django project directory structure for the given project name in the current directory or optionally in the given directory.\n

  name        Name of the application or project.\n
  directory   Optional destination directory.\n
  """
  
  # Validation
  if len(args) < 1:
    raise click.UsageError("You must provide a project name")
  
  project_name = args[0]
  if not project_name.isidentifier():
     raise click.UsageError(f"Invalid project name '{project_name}': Must be a valid Python identifier.")

  command_list = ['django-admin', 'startproject', project_name]

  # Validate directory (second argument)
  directory = ''
  if len(args) > 1:
    directory = args[1]
    command_list .append(directory) # Args 1 = Directory
   
  if command.run(command=command_list, is_debug=True):
    
    # Create rdp.conf
    apps_dir_value = 'apps'
    table_prefix = 'app'
    env = 'dev'
    
    custom = input("Do you want custom config for this project (Yes)") or "Yes"
    if custom == "Yes":
      apps_dir_value = input(f"Custom directory for new Django application ({apps_dir_value})?") or apps_dir_value
      table_prefix = input(f"Table prefix ({table_prefix})?") or table_prefix
      env = input(f"Default environment 'dev' or 'prod' ({env})?") or env
    
    project_root = os.path.join(os.getcwd(), project_name)
    if directory == ".":
      project_root = os.path.join(os.getcwd()) 
    
    data = {
      'project': {
        'name': project_name,                  # Eg. config
        'root': project_root,  # /mnt/data/project
        'apps_dir': apps_dir_value,    # apps
        'table_prefix': table_prefix,  # app
        'environment': env,            # dev
      }
    }
    
    # Menulis ke file YAML
    config_path = f"{project_root}/rdp.yaml"
    config = Yaml(config_path)
    config.save_config(data=data)

    # Setup
    ## SETTINGS
    # Copy django/assets/settings -> config/settings
    src = BASE_RDP / 'django/assets/settings'
    dest = f'{project_root}/{project_name}/settings'
    Directory.copy(src=src, dest=dest)
    
    # Rename and move config/settings.py -> config/settings
    src = BASE_DIR / f'{project_root}/{project_name}/settings.py'
    dest = f'{project_root}/{project_name}/settings/base.py'
    File.move(src=src, dest=dest)
    
    # Copy .env, requirements.txt
    src = BASE_RDP / "django/assets"
    Directory.copy(src, project_root, copy_subdirs=False)
    
    ## APPS
    apps_dir = Directory(dir_path=f'{project_root}/{apps_dir_value}')
    apps_dir.create()
    # copy from django/assets/core to apps/core
    src = BASE_RDP / "django/assets/core"
    Directory.copy(src, apps_dir.str('core'))
    
    # UPDATE .env APPS =
    src = f'{project_root}/.env'
    value = f'{apps_dir_value}.core, '
    append_to_env_file(env_file=src, key='APPS', value_to_append=f'{value}')
    

    
    # Check if library is installed?
    if not is_library_installed('import_export'):
      # run pip install
      cmd = ['pip', 'install', '-r',  'requirements.txt']
      command.run(command=cmd, is_debug=True)
    
    # replace .env DJANGO_SETTINGS_MODULE = 
    src = f'{project_root}/.env'
    find = 'DJANGO_SETTINGS_MODULE = '
    replace = f'DJANGO_SETTINGS_MODULE = {project_name}.settings.{env}'
    File(src).find_replace(find, replace)
    
    # Get SECRET_KEY from settings
    src = f'{project_root}/{project_name}/settings/base.py'  # Path to the file
    key = 'SECRET_KEY'
    value = get_value_from_file(src, key)
    # Replace in .env
    src = f'{project_root}/.env'
    append_to_env_file(env_file=src, key=key, value_to_append=f'"{value}"')
    
    # Replace BASE_DIR parent
    src = f'{project_root}/{project_name}/settings/base.py'  # Path to the file
    find = 'BASE_DIR = Path(__file__).resolve().parent.parent'
    replace = 'BASE_DIR = Path(__file__).resolve().parent.parent.parent'
    File(src).find_replace(find, replace)
    
    # replace 'config.settings' in manage.py
    src = f'{project_root}/manage.py'
    find = ['import sys', 'def main():']
    replace = ["import sys\nfrom dotenv import load_dotenv\n", "def main():\n    load_dotenv()\n"]
    File(src).find_replace(find, replace)
    
    src = f'{project_root}/{project_name}/urls.py'
    find = 'from django.urls import path'
    replace = 'from django.urls import path, include'
    File(src).find_replace(find, replace)
    
@main.command()
@click.argument('args', nargs=-1)
def xapp(args):
  """
  Creates a Django app directory structure for the given app name in the current directory or optionally in the given directory.\n
  
  name        Name of application or project.\n
  directory   Optional destination directory.\n
  
  """
  if len(args) < 1:
    raise click.UsageError("You must provide an application name")
  
  app_name = args[0].lower()
  if not app_name.isidentifier():
     raise click.UsageError(f"Invalid application name '{app_name}': Must be a valid Python identifier.")
  
  # Check name is core (required)
  if app_name == 'core':
    raise click.UsageError("App name 'core' required by RDP Library.")
  
  # Check if current directory in root of Django project
  pwd = os.getcwd()
  if not django.utils.is_django_project_root(directory=pwd):
    raise click.UsageError(f"Current directory '{pwd} not in Django root project!'")
  
  command_list = ['django-admin', 'startapp', app_name]

  # Validate DIRECTORY (second argument)
  if len(args) > 1:  
    command_list .append(args[1]) # Args 1 = Directory
   
  if command.run(command_list):
    
    # Default 
    apps_dir_value = "apps"
    apps_dir = Directory(dir_path=BASE_DIR / apps_dir_value)
    table_prefix = "app"
    project_name = ""
    
    # Read rdp.cfg if exist
    config_path = 'rdp.yaml'
    if File.exist(config_path):
      config = Yaml(config_path)
      apps_dir_value = config.get('project.apps_dir', 'apps') # apps
      apps_dir = Directory(dir_path=BASE_DIR / apps_dir_value)
      table_prefix = config.get('project.table_prefix', 'app')
      project_name = config.get('project.name', '')
    
    #============================================================
    # Setup
    
    # Move new app to apps directory | product => apps/product
    apps_dir.move(app_name, apps_dir_value)
    
    # New app location (apps.name)
    app_dir = apps_dir.join(app_name)
    
    # Replace apps.py from name = 'product' to name = 'apps.product'
    file_path = File(f'{app_dir}/apps.py')
    file_path.find_replace(find=app_name, replace=f'{apps_dir_value}.{app_name}')
    
    # Copy templates
    src = BASE_RDP / "django/assets/templates"
    dest = BASE_DIR / "templates" 
    Directory.copy(src, dest, copy_subdirs=True, replace_existing=False)
    
    # Modify <app>/settings.py
    settings_path = BASE_DIR / f'{project_name}/settings/base.py'  # Replace with the path to your settings.py
    find = "'DIRS': [],"
    replace = "'DIRS': ['templates', ],"
    File(settings_path).find_replace(find=find, replace=replace)
    
    #============================================================
    # Models
    models_dir = Directory(f'{app_dir}/models')
    # Directory name/models
    models_dir.create()
    File(f'{app_dir}/models/__init__.py').touch()
             
    # Create name/models/name.py
    src = BASE_RDP / "django/assets/app/models.py"
    dest = f'{models_dir.str()}/{app_name}.py'
    find = ['Xmodel', 'x_model', 'x_apps']
    replace = [f'{app_name.capitalize()}', f'{table_prefix}_{app_name}', apps_dir_value]
    File.copy_find_replace(src, dest, find, replace)
    
    # remove original name/models.py
    File(f'{app_dir}/models.py').delete()
    
    #============================================================
    # Admin
    src = BASE_RDP / "django/assets/app/admin.py"
    dest = f'{app_dir}/admin.py'
    find = ['XModel', 'xapps', 'xname' ]
    replace = [f'{app_name.capitalize()}', apps_dir_value, app_name]
    File.copy_find_replace(src, dest, find, replace, replace_file=True)
    
    #============================================================
    # Views
    views_dir = Directory(f'{app_dir}/views')
    # Directory name/views
    views_dir.create()
    File(f'{app_dir}/views/__init__.py').touch()
    
    # Create name/views/name.py
    src = BASE_RDP / "django/assets/app/views.py"
    dest = f'{views_dir.str()}/{app_name}.py'
    find = ['XModel', 'x_apps', 'x_name', ]
    replace = [f'{app_name.capitalize()}', apps_dir_value,  app_name]
    File.copy_find_replace(src, dest, find, replace)
    
    # remove original name/views.py
    File(f'{app_dir}/views.py').delete()
    
    # Copy template
    src = BASE_RDP / "django/assets/templates/components/Layouts/templates/blank.html"
    dest = f'templates/{apps_dir_value}/{app_name}/{app_name}.html' # templates/apps/user/user.html
    File.copy(src, dest, create_dest_folder=True)
    
    #============================================================
    # URLs
    src = BASE_RDP / "django/assets/app/urls.py"
    dest = f'{app_dir}/urls.py'
    find = ['XModel', 'x_name' ]
    replace = [f'{app_name.capitalize()}', app_name]
    File.copy_find_replace(src, dest, find, replace, replace_file=True)
    
    # Ask user
    register_to_env = input("Register to .env (default: Yes)?") or "Yes"
    if register_to_env == "Yes":
      # Update .env, config/urls.py
      env_file = BASE_DIR / '.env'
      append_to_env_file(env_file=env_file, key='APPS', 
                         value_to_append=f'{apps_dir_value}.{app_name}, ')
      if not string.is_empty(project_name):
        # Add current apps/product/urls.py to config/urls.py
        file_path = BASE_DIR / f'{project_name}/urls.py'
        new_path = f"    path('{app_name}/', include('{apps_dir_value}.{app_name}.urls'), name='{app_name}'),\n"
        append_to_urls(file_path=file_path, new_path=new_path)
      else:
        print('Cannot find config in rdp.yaml [project] name. Append urls.py cancel.')

