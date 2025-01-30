import datetime
import Storage

def log_teeth_brushing():
    """Logs that the user brushed their teeth today."""
    today = datetime.date.today().isoformat()
    data = Storage.load_data()

    if today in data["teeth_brushing"]:
        print("🦷 You already logged brushing your teeth today!")
    else:
        data["teeth_brushing"][today] = True
        Storage.save_data(data)
        print("✅ Brushed teeth logged successfully!")


def check_teeth_brushing():

    """checks if user brushed their teeth today"""
    today = datetime.date.today().isoformat()
    data = Storage.load_data()

    if data["teeth_brushing"].get(today, False):
        print("🦷 You brushed your teeth today! Keep it up!")
    else:
        print("⚠️ You haven't logged brushing your teeth today! Go do it!")

if __name__ == "__main__":
    log_teeth_brushing()
    check_teeth_brushing()