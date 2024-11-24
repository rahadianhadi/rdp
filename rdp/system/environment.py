import os

def append_to_env_file(env_file, key, value_to_append):
  '''
  # Usage: append_to_env_file(env_file='.env', key='LIBS', value_to_append='apps.product')
  '''
  try:
      with open(env_file, 'r') as file:
          lines = file.readlines()

      # Find the line that contains the key (e.g., LIBS=)
      for i, line in enumerate(lines):
          line = "".join(line.split()) # remove space
          if line.startswith(f"{key}="):
              # Append the value to the existing line
              current_value = line.strip().split('=')[1]
              new_value = f"{current_value}{value_to_append}"
              lines[i] = f"{key} = {new_value}\n"
              break
      else:
          # If the key is not found, add it at the end of the file
          lines.append(f"{key} = {value_to_append}\n")

      # Write the updated lines back to the file
      with open(env_file, 'w') as file:
          file.writelines(lines)

  except FileNotFoundError:
      print(f"{env_file} not found.")
  except Exception as e:
      print(f"An error occurred: {e}")

def append_to_urls(file_path, new_path):
    # Path to your file
    # file_path = 'path/to/your/file.py'

    # Read content of the file
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Define the new path line
    # new_path = "    path('new-path/', include('new_app.urls')),\n"

    # Find where 'urlpatterns' is defined and insert the new path before the closing bracket
    for index, line in enumerate(content):
        if line.strip() == "]" and content[index - 1].strip().startswith("path("):
            content.insert(index, new_path)
            break

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(content)
        
def getenv_list(key, default=""):
    return [v.strip() for v in os.getenv(key, default=default).split(',') if v.strip()]

'''
# Example usage
file_path = '.env'  # Path to the file
key = 'SECRET_KEY'
value = get_value_from_file(file_path, key)
'''
def get_value_from_file(file_path, key):
  try:
    with open(file_path, 'r') as file:
      for line in file:
        # Strip whitespace and check if the line starts with the key
        line = line.strip()
        if line.startswith(f"{key}"):
          # Extract the value after the '=' and remove quotes if present
          _, value = line.split("=", 1)
          return value.strip().strip("'").strip('"')
    return None  # Key not found
  except FileNotFoundError:
      print(f"Error: File '{file_path}' not found.")
      return None



