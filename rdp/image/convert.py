import os
import subprocess
from PIL import Image

from rdp.debug.logging import logger

from .enum import ImageFormat
from .utils import is_png

def format(input_path, output_path, quality=85, format=ImageFormat.PNG):
  try:
    with Image.open(input_path) as img:
      if is_png(input_path):
        # Check if image has an alpha channel (transparency)
        if img.mode == 'RGBA':
            # Create a new background image with the specified color and the same size
            background = Image.new("RGB", img.size, (255, 255, 255))
            # Paste the original image onto the background
            background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
            img = background
        else:
            # Convert to RGB if not in RGBA mode (JPEG does not support other modes)
            img = img.convert("RGB")
    
      
      img.save(output_path, format=format, quality=quality)
  
  except Exception as e:
    logger.error(f"Image: {e}", exc_info=True)
    

''' Must install potrace: https://potrace.sourceforge.net/ '''
def svg(input_path, output_path):
  try:
    # Step 1: Convert image to black-and-white and save as PBM format
    with Image.open(input_path) as img:
      img = img.convert("L")  # Convert to grayscale
      img = img.point(lambda x: 0 if x < 128 else 1, '1')  # Threshold to black-and-white
      pbm_path = "temp_image.pbm"
      img.save(pbm_path) # format="PBM"

    # Step 2: Use potrace to convert PBM to SVG
    subprocess.run(["potrace", pbm_path, "-s", "-o", output_path])
  
  except Exception as e:
    logger.error(f"Image to SVG: {e}", exc_info=True)
    
  finally:
    # Clean up temporary PBM file
    if os.path.isfile(pbm_path):
      os.remove(pbm_path)
      
