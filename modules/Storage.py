import json
import os

DATA_FILE = "data.json"

# Default structure for data.json
DEFAULT_DATA = {
    "water_intake": {},
    "teeth_brushing": {},
    "showers": {},
    "strava": {},
    "streaks": {
        "current": 0,
        "best": 0,
        "teeth_current": 0,
        "teeth_best": 0
    }
}

def load_data():
    """
    Loads user data from data.json or creates a new file if it doesn't exist.
    Also merges any missing keys from DEFAULT_DATA into existing data.
    """
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    # Merge missing keys from DEFAULT_DATA into data
    updated = False
    for key, default_value in DEFAULT_DATA.items():
        if key not in data:
            data[key] = default_value
            updated = True
        else:
            # If it's a dict, check sub-keys
            if isinstance(default_value, dict):
                for sub_key, sub_default_value in default_value.items():
                    if sub_key not in data[key]:
                        data[key][sub_key] = sub_default_value
                        updated = True

    if updated:
        save_data(data)

    return data

def save_data(data):
    """
    Saves the user data to data.json in pretty-printed JSON.
    """
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
