from PIL import Image

def is_png(input_path):
  try:
    with Image.open(input_path) as img:
      return img.format == 'PNG'
  except IOError:
    return False
