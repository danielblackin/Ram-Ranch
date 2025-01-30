import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from .env
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

def get_access_token():
    """
    Fetches a new access token using the refresh token.
    """
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=payload)
    data = response.json()

    if "access_token" in data:
        return data["access_token"]
    else:
        raise Exception(f"Failed to get access token: {data}")

def get_strava_activities():
    """
    Fetches recent Strava activities.
    """
    access_token = get_access_token()
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch activities: {response.json()}")

# Example usage:
if __name__ == "__main__":
    try:
        print("Fetching latest Strava activities...\n")
        activities = get_strava_activities()
        # Display the first 3 activities
        for activity in activities[:3]:
            print(f"- {activity['name']} | {activity['distance']} meters")
    except Exception as e:
        print(f"Error: {e}")
