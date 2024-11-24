import os
from rdp.image import resize, convert
from rdp.image.enum import ImageFormat

real_image_path = "tests/test_image.png"  # Replace with your image file name

def test_resize_image():
  '''
  Test: 
    - Resize
    - PNG to JPG
    - PNG to SVG
  '''
  
  # Resize - Call the resize function
  output_path="tests/test_image_output.png"
  
  resize.size(input_path=real_image_path, output_path=output_path, scale_factor=0.5)
  assert os.path.isfile(output_path), "Resized image does not exist."

  # Optionally, check the size is roughly as expected
  original_size = os.path.getsize(real_image_path)
  resized_size = os.path.getsize(output_path)
  assert resized_size < original_size, "Resized image should be smaller than the original."
  
  # Clean up the output image file after the test
  if os.path.isfile(output_path):
    os.remove(output_path)
  
  # PNG to JPEG
  output_path="tests/test_image_output.jpeg"
  convert.format(input_path=real_image_path, output_path=output_path, format=ImageFormat.JPEG)
  assert os.path.isfile(output_path), "Convert image does not exist."
  if os.path.isfile(output_path):
    os.remove(output_path)
  
  # PNG to SVG
  output_path="tests/test_image_output.svg"
  convert.svg(input_path=real_image_path, output_path=output_path)
  assert os.path.isfile(output_path), "Convert SVG image does not exist."
  if os.path.isfile(output_path):
    os.remove(output_path)
