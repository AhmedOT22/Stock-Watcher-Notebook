import json
import os
from config import WATCHLIST_FILE  


def load_json(filename, default_data=None):
    """
    Load data from a JSON file.

    Parameters:
        filename (str): The JSON file to load.
        default_data (any): The default data if the file doesn't exist.

    Returns:
        dict or list: The loaded data.
    """
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding {filename}. Resetting to default.")
    return default_data if default_data is not None else {}

def save_json(filename, data):
    """
    Save data to a JSON file.

    Parameters:
        filename (str): The JSON file to save to.
        data (dict or list): The data to save.
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
