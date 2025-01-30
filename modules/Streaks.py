import datetime
from modules import Storage

def update_teeth_streak():
    """
    Updates the teeth brushing streak.
    If user brushed today, we check if they also brushed yesterday.
    Increments or resets the streak accordingly.
    """
    data = Storage.load_data()
    today_str = datetime.date.today().isoformat()
    yesterday_str = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

    brushed_today = data["teeth_brushing"].get(today_str, 0) > 0
    brushed_yesterday = data["teeth_brushing"].get(yesterday_str, 0) > 0

    if brushed_today:
        if brushed_yesterday:
            data["streaks"]["teeth_current"] += 1
        else:
            data["streaks"]["teeth_current"] = 1

        if data["streaks"]["teeth_current"] > data["streaks"]["teeth_best"]:
            data["streaks"]["teeth_best"] = data["streaks"]["teeth_current"]
    else:
        data["streaks"]["teeth_current"] = 0

    Storage.save_data(data)

def display_teeth_streak():
    """
    Displays the current and best streaks for brushing teeth.
    (Currently just prints to console; you can show in GUI if you want.)
    """
    data = Storage.load_data()
    print(f"🔥 Current Teeth Brushing Streak: {data['streaks']['teeth_current']} days")
    print(f"🏅 Best Teeth Brushing Streak: {data['streaks']['teeth_best']} days")
