from enum import Enum

class ImageFormat(str, Enum):
  JPEG = "JPEG"
  PNG = "PNG"
  GIF = "GIF"
  BMP = "BMP"
  TIFF = "TIFF"
  WEBP = "WEBP"
  ICO = "ICO"

  @classmethod
  def choices(cls):
    """Returns a list of format choices for easy access."""
    return [(format.value, format.name) for format in cls]

  def __str__(self):
    """String representation to directly get the value."""
    return self.value