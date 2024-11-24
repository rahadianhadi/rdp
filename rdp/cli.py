import click

from rdp import __basedir__
from rdp.system import command
from rdp.system.directory import Directory

from rdp.django.manage.project import DjangoProjectManager 
from rdp.django.manage.app import DjangoAppManager

BASE_DIR = Directory.get_cwd()
BASE_RDP = __basedir__

@click.group()
def main():
    pass

@main.command()
@click.argument('args', nargs=-1)  # Collect all extra arguments
def project(args):
  """
  Creates a Django project directory structure for the given project name in the current directory or optionally in the given directory.\n

  name        Name of the application or project.\n
  directory   Optional destination directory.\n
  """
  
  manager = DjangoProjectManager()
  manager.run(args)

@main.command()
@click.argument('args', nargs=-1)
def app(args):
  """
  Creates a Django app directory structure for the given app name in the current directory or optionally in the given directory.\n
  
  name        Name of application or project.\n
  directory   Optional destination directory.\n
  
  """
  manager = DjangoAppManager()
  manager.run(args)


@main.command()
@click.argument('cmd')
@click.argument('args', nargs=-1)
def m(cmd, args):
    """Dynamic command handler with alias support.
    
    r     runserver\n
    m     migrate\n
    cs    createsuperuser\n
    mm    makemigrations\n
    c     collectstatic
    t     test\n
    """
    
    COMMAND_MAPPING = {
        'r': 'runserver',
        'm': 'migrate',
        'cs': 'createsuperuser',
        'mm': 'makemigrations',
        'c': 'collectstatic',
        't': 'test',
    }
    
    if cmd in COMMAND_MAPPING:
      main_command = COMMAND_MAPPING.get(cmd, cmd)
      cmd_list = ['python', 'manage.py', main_command]
      cmd_list.extend(args)
      command.run(cmd_list, is_debug=True)
      
    else:
      raise click.UsageError(f"Unknown command or alias: {cmd}")
    
if __name__ == '__main__':
    main()