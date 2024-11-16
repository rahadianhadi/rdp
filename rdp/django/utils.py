import os

def is_django_project_root(directory):
  """Check if the given directory is in the root of a Django project.

  Args:
      directory (str): Input directory
  """
  return os.path.isfile(os.path.join(directory, 'manage.py'))