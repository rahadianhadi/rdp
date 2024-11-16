import os
import click
import subprocess

from rdp import django

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
  
  if len(args) < 1:
    raise click.UsageError("You must provide a project name")
  
  name = args[0]
  if not name.isidentifier():
     raise click.UsageError(f"Invalid name '{name}': Must be a valid Python identifier.")

  command = ['django-admin', 'startproject', name]

  # Validate DIRECTORY (second argument)
  if len(args) > 1:  
    command .append(args[1]) # Args 1 = Directory
   
  subprocess.run(command)


@main.command()
@click.argument('args', nargs=-1)
def app(args):
  """
  Creates a Django app directory structure for the given app name in the current directory or optionally in the given directory.\n
  
  name        Name of application or project.\n
  directory   Optional destination directory.\n
  
  """
  if len(args) < 1:
    raise click.UsageError("You must provide an application name")
  
  name = args[0]
  if not name.isidentifier():
     raise click.UsageError(f"Invalid name '{name}': Must be a valid Python identifier.")

  # Check if current directory in root of Django project
  pwd = os.getcwd()
  if not django.utils.is_django_project_root(directory=pwd):
    raise click.UsageError(f"Current directory '{pwd} not in Django root project!'")
  
  command = ['django-admin', 'startapp', name]

  # Validate DIRECTORY (second argument)
  if len(args) > 1:  
    command .append(args[1]) # Args 1 = Directory
   
  subprocess.run(command)
  
if __name__ == '__main__':
    main()