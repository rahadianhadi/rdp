import re

def normalize_string(s):
  # Convert to lowercase
  s = s.lower()
  # Remove any non-alphanumeric characters and spaces
  s = re.sub(r'[^a-z0-9]', '', s)
  return s

def replace(find, replace, text, case_sensitive=True):
  if case_sensitive:
    text = text.replace(find, replace)
  else:
    text = re.sub(find, replace, text, flags=re.IGNORECASE)
  return text 

def is_empty(value):
    return not value or not value.strip()