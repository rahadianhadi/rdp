import os
import shutil

from pathlib import Path
from tempfile import TemporaryDirectory

class Directory:
    def __init__(self, dir_path=''):
        self.dir_path = dir_path
    
    def is_exist(self, create_if_missing=False):
        """
        Check if a directory exists. Optionally create it if it doesn't exist.

        :param dir_path: Path to the directory.
        :param create_if_missing: If True, create the directory if it doesn't exist.
        :return: True if the directory exists (or was created), False otherwise.
        """
        path = Path(self.dir_path)
        if path.is_dir():
            return True
        elif create_if_missing:
            # path.mkdir(parents=True, exist_ok=True)  # Create directory with all necessary parent directories
            self.create()
            return True
        return False

    def is_empty(self):
        """Check if a directory is empty."""
        dir_path = Path(self.dir_path)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"{dir_path} is not a directory.")
        return not any(dir_path.iterdir())

    def create(self, parents=True, exist_ok=True):
        """Create a directory.
        parents    if parent directory not exist, will be create
        exist_ok   no error occure if directory exsist
        """
        Path(self.dir_path).mkdir(parents=parents, exist_ok=exist_ok)

    def create_temp(self):
        """Create a temporary directory."""
        return TemporaryDirectory()

    def lists(self):
        """List all contents in a directory."""
        return [str(p) for p in Path(self.dir_path).iterdir()]

    def list_subdirectories(self):
        """List all subdirectories in a directory."""
        return [str(p) for p in Path(self.dir_path).iterdir() if p.is_dir()]

    def delete(self):
        """Delete a directory and its contents."""
        shutil.rmtree(self.dir_path)


    def rename(self, new_name):
        """Rename a directory."""
        dir_path = Path(self.dir_path)
        new_dir = dir_path.parent / new_name
        dir_path.rename(new_dir)

    def get_size(self):
        """Get the size of a directory."""
        dir_path = Path(self.dir_path)
        return sum(f.stat().st_size for f in dir_path.glob('**/*') if f.is_file())
    
    def get_creation_date(self):
        """Get the creation date of a directory."""
        return Path(self.dir_path).stat().st_ctime
    
    def join(self, sub_dir):
        """Join a directory."""
        return Path(self.dir_path) / sub_dir
    
    def str(self, subdir=''):
        return str(Path(self.dir_path) / subdir)
    
    @staticmethod
    def move(src, dest):
        """Move a directory."""
        shutil.move(src, dest)
        
    @staticmethod
    def copy(src, dest, copy_subdirs=True, replace_existing=False):
        """
        Copies files and directories from src to dest with options to:
        - Copy entire directory (with subdirectories) or only files.
        - Replace existing files in the destination or not.
        
        :param src: Source directory path
        :param dest: Destination directory path
        :param copy_subdirs: Whether to copy subdirectories (default is True)
        :param replace_existing: Whether to replace existing files (default is False)
        """
        try:
            # Ensure the source directory exists
            if not os.path.exists(src):
                raise FileNotFoundError(f"Source directory does not exist: {src}")
            
            # Ensure the destination directory exists
            if not os.path.exists(dest):
                os.makedirs(dest, exist_ok=True)

            # If copying subdirectories and files
            if copy_subdirs:
                # Walk through the source directory and copy subdirectories and files
                for root, dirs, files in os.walk(src):
                    # Calculate the relative path for subdirectories
                    relative_path = os.path.relpath(root, src)
                    dest_dir = os.path.join(dest, relative_path)

                    # Create subdirectories in the destination if they don't exist
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)

                    # Copy each file
                    for file in files:
                        src_file = os.path.join(root, file)
                        dest_file = os.path.join(dest_dir, file)

                        # If file exists and replace_existing is True, overwrite the file
                        if os.path.exists(dest_file):
                            if replace_existing:
                                shutil.copy2(src_file, dest_file)  # Copy with metadata
                        else:
                            shutil.copy2(src_file, dest_file)

            else:
                # If only copying files (not subdirectories)
                for item in os.listdir(src):
                    src_path = os.path.join(src, item)
                    dest_path = os.path.join(dest, item)

                    # Copy only files, skip directories
                    if os.path.isfile(src_path):
                        if os.path.exists(dest_path):
                            if replace_existing:
                                shutil.copy2(src_path, dest_path)
                        else:
                            shutil.copy2(src_path, dest_path)

            # print(f"Files copied from {src} to {dest}")
        except Exception as e:
            print(f"An error occurred: {e}")

    
    @staticmethod
    def get_cwd() -> Path:
        """Get the current work of directory."""
        return Path.cwd()
    
    @staticmethod
    def contains_directory(path: str) -> bool:
        return Path(path).parent != Path('.')
