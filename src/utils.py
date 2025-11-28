import logging
import os
from pathlib import Path
from assets.file_formats import FILE_FORMAT_FOLDERS

def clear_console() -> None:
    """Clears the console based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def invalid_path(path: Path) -> bool:
    """Checks if the path is invalid."""
    return not path.exists() or not path.is_dir()

def not_a_file(file: Path) -> bool:
    """Checks if the file is not a file. Returns True if not a file, False otherwise."""
    return not file.is_file()
  
def print_file(file: Path) -> None:
  """Prints the file name, file format, and file size."""
  file_info = f"File: {file.name} | File format: {file.suffix} | File size: {round(file.stat().st_size/1000000,2)} Megabytes"
  hLine = len(file_info) * "-"
  print(f"\n{hLine}\n{file_info}\n{hLine}")


def sort_file(file: Path, mode: str) -> None:
    """ Sorts a file into the appropriate folder based on its file format.
        
        Args:        
            file (Path): The file to be sorted.    
            mode: "auto" for automatic sorting, "manual" for manual sorting. 
    """
    
    if not_a_file(file):
        logging.error(f"{file} is not a valid file.")
        return

    file_type = file.suffix.lower()
    target_folder : str = FILE_FORMAT_FOLDERS.get(file_type, "Other")
    target_path : Path = Path.joinpath(file.parent, target_folder)

    if invalid_path(target_path):
        logging.info(f"Creating folder: {target_folder}")
        target_path.mkdir(parents=True, exist_ok=True)

    if mode == "auto":
        try:
            logging.info(f"Moving {file.name} to {target_folder} folder")
            file.rename(Path.joinpath(target_path, file.name))
        except FileExistsError:
            logging.error(f"File {file.name} already exists in {target_folder} folder")
        except Exception as e:
            logging.error(f"Error moving file {file.name}: {e}")
    elif mode == "manual":
        print_file(file)

        action = input(
    """
    Choose an action for the file:
        (1) Auto Sort file based on file type
        (2) Delete file
        (3) Skip file
        (4) Add Custom Path

    Enter your choice:""")

        print("")  # For better readability in the console
        
        match action:
            case "1":
                sort_file(file, mode="auto") # Recursive call to sort automatically
            case "2":
                logging.info(f"Deleted {file.name} from {file.parent} folder")
                os.remove(file)
            case "3":
                logging.info(f"Skipped {file.name} from {file.parent} folder")
            case "4":
                customPath = input("Enter the custom path > ")
                if invalid_path(Path(customPath)):
                    logging.error(f"Path {customPath} does not exist")
                else:
                    logging.info(f"Moving {file.name} to {customPath} folder")
                    file.rename(Path.joinpath(Path(customPath), file.name))
            case _:
                logging.error(f"Invalid Input: {action}")



