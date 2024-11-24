import os
import requests
import subprocess

from rdp.system.directory import Directory
from rdp.system.file import File

class Web:
    """
    Class untuk utilitas berhubungan dengan internet seperti download file, 
    fetch data, check URL, dan lainnya.
    """
    
    @staticmethod
    def download_file_with_curl(url: str, path_name: str) -> None:
        """
        Mengunduh file menggunakan curl.
        Args:
            url (str): URL file yang akan diunduh.
            name (str): Nama file untuk disimpan.
            save_dir (str): Direktori tempat file disimpan.
        Raises:
            SystemExit: Jika download gagal.
        """
        # Validasi input
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL. Must start with http:// or https://")
        
        # extract path component
        path = File.extract_path_components(path_name)
        # Check contain directory
        if Directory.contains_directory(path['directory']):
          os.makedirs(path_name, exist_ok=True)
          
        # save_path = os.path.join(save_dir, name)

        print(f"Downloading {path['filename']}...")
        proc = subprocess.run(
            [
                "curl",
                "--fail",
                "--location",
                url,
                "-o",
                path_name,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode != 0:
            print(f"Error downloading {path['filename']}: {proc.stderr.decode().strip()}")
            raise SystemExit(1)
        print(f"Downloaded {path['filename']} to {path['directory']}")
        
    @staticmethod
    def download_file(url: str, save_path: str) -> str:
        """Mengunduh file dari URL dan menyimpannya ke lokasi tertentu."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return f"File downloaded successfully: {save_path}"
        except requests.RequestException as e:
            return f"Download failed: {e}"
    
    @staticmethod
    def fetch_data(url: str) -> str:
        """Mendapatkan data dari URL sebagai string."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return f"Fetch failed: {e}"
    
    @staticmethod
    def post_data(url: str, data: dict) -> str:
        """Mengirimkan data ke URL melalui POST."""
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return f"POST failed: {e}"
    
    @staticmethod
    def check_url(url: str) -> bool:
        """Memeriksa apakah URL dapat diakses."""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    @staticmethod
    def upload_file(url: str, file_path: str, field_name: str = "file") -> str:
        """Mengunggah file ke server."""
        if not os.path.exists(file_path):
            return "File not found."
        try:
            with open(file_path, "rb") as file:
                files = {field_name: file}
                response = requests.post(url, files=files)
                response.raise_for_status()
                return f"File uploaded successfully: {response.json()}"
        except requests.RequestException as e:
            return f"Upload failed: {e}"

# # Contoh penggunaan:
# if __name__ == "__main__":
#     utils = InternetUtils()
    
#     # Contoh download file
#     print(utils.download_file("https://example.com/file.zip", "file.zip"))
    
#     # Contoh fetch data
#     print(utils.fetch_data("https://api.github.com"))
    
#     # Contoh post data
#     print(utils.post_data("https://httpbin.org/post", {"key": "value"}))
    
#     # Contoh cek URL
#     print(utils.check_url("https://www.google.com"))
    
#     # Contoh upload file
#     print(utils.upload_file("https://example.com/upload", "file.zip"))
