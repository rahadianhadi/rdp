import os
import subprocess

from rdp.debug.logging import logger

def run(command, is_debug=False):
  """Run a command and output its process in real-time."""

  is_success = False
  if is_debug:
    try:
      os.system(" ".join(command))
      is_success = True
    except Exception as e:
        print(f"Command '{command}' failed: {e}")
  else:
    try:
      # Menjalankan perintah menggunakan subprocess.run
      result = subprocess.run(command, capture_output=True, text=True, check=True)
      # Jika perintah berhasil, log output stdout
      logger.debug(f"Command '{' '.join(command)}' is working succesfully.")
      logger.debug(f"Output: {result.stdout}")
      is_success = True
    except subprocess.CalledProcessError as e:
      # Jika perintah mengembalikan kode kesalahan, tangani error-nya
      logger.error(f"Command '{' '.join(command)}' fail with code status: {e.returncode}.")
      logger.error(f"stderr: {e.stderr}")

    except Exception as e:
      # Tangani exception lain yang mungkin terjadi
      logger.exception(f"Error when running: '{' '.join(command)}': {e}")

  return is_success