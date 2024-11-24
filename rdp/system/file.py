import os
import shutil
from pathlib import Path
from typing import Dict
from rdp.text import string 

class File:
    def __init__(self, file_path=''):
        self.file_path = file_path
        

    def create(self, content=None):
        """Create a new file with optional content."""
        file_path = Path(self.file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Create parent directories if needed
        with file_path.open('w') as f:
            if content:
                f.write(content)

    def touch(self):
        """Open the file in append mode, which creates it if it doesn't exist"""
        with open(self.file_path, 'a'):
            pass  # No need to write anything, it just touches the file

    def read(self):
        """Read the content of a file."""
        file_path = Path(self.file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")
        with file_path.open('r') as f:
            return f.read()

    def write(self, content):
        """Write content to a file (overwrite existing content)."""
        with Path(self.file_path).open('w') as f:
            f.write(content)

    def append(self, content):
        """Append content to a file."""
        with Path(self.file_path).open('a') as f:
            f.write(content)

    def delete(self):
        """Delete a file."""
        file_path = Path(self.file_path)
        if file_path.exists():
            file_path.unlink()

    def get_size(self):
        """Get the size of a file in bytes."""
        return Path(self.file_path).stat().st_size

    def find_replace(self, find, replace, case_sensitive=True):
        content = self.read()
        if isinstance(find, list):
            for item_find, item_replace in zip(find, replace):
                # content = content.replace(item_find, item_replace)
                content = string.replace(item_find, item_replace, content, case_sensitive)
        else:
            content = string.replace(find, replace, content, case_sensitive)
                
        self.write(content)
    
    @staticmethod
    def copy_find_replace(src, dest, find, replace, case_sensitive=True, replace_file=True):
        File.copy(src, dest)
        file = File(dest)
        file.find_replace(find, replace, case_sensitive=case_sensitive)
        
    @staticmethod
    def exist(path):
        """Check if a file or directory exists."""
        return Path(path).exists()

    @staticmethod
    def move(src, dest):
        """Move a file to a new location."""
        shutil.move(src, dest)
    
    @staticmethod
    def copy(src, dest, replace=True, create_dest_folder=False):
        """Copy a file to a new location."""
        if create_dest_folder:
            # Ensure the target directory exists
            dest_folder = os.path.dirname(dest)
            if not os.path.exists(dest_folder):
                # Create all necessary subdirectories if they don't exist
                os.makedirs(dest_folder, exist_ok=True)
                
        if File.exist(dest):
            if replace:
                shutil.copy(src, dest)
        else:
            shutil.copy(src, dest)

    @staticmethod
    def extract_path_components(path: str) -> Dict[str, str]:
        """Extract file or directory path

        Args:
            path (str): Full path information

        Returns:
            Dict[str, str]: Return information Dict key: directory, filename, extension, filename_with_ext
        """
        path_obj = Path(path)
                     # Extract extension
        return {
            "directory": str(path_obj.parent),
            "filename": path_obj.stem,
            "extension": path_obj.suffix,
            "filename_with_ext": path_obj.name,
        }
