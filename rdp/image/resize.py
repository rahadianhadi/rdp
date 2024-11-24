from PIL import Image
from rdp.debug.logging import logger

def size(input_path, output_path, scale_factor=0, height=0, width=0):
  """
  Resize image by scale factor, width, or height.

  Args:
      input_path (str):     The source of image file.
      output_path (str):    The output after image resize.
      scale_factor (float): Scale factor, sample: 0.5.
      height (int):         Change the height image.
      width (int):          Change the width image (if height and width > 0, change both).
      
  Returns:
      None: Resize image

  Raises:
      Exception: Image error handle.

  Example:
      resize_image(input_path='./image.jpg', output_path='./result.jpg', scale_factor=0.5)
  """
  try:
    with Image.open(input_path) as img:
      new_size = 0
      if scale_factor > 0:
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
      elif height > 0 and width == 0:
        new_size = (img.width, height)
      elif width > 0 and height == 0:
        new_size = (width, img.height)
      elif width > 0 and height > 0:
        new_size = (width, height)
      
      if new_size != 0:
        img = img.resize(new_size, Image.LANCZOS)
        
        img.save(output_path)
      
  except Exception as e:
    logger.error(f"Image: {e}", exc_info=True)


