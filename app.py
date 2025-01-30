import tkinter as tk
import random
import datetime

# Imports from your modules folder
from Ram import RamObject
from modules import Storage
from modules.Streaks import update_teeth_streak, display_teeth_streak
from modules.WaterTracker import WaterTracker

root_window = tk.Tk()
root_window.title("Ram Ranch")
root_window.geometry("800x800")

# Create a menu frame at the top
menu_frame = tk.Frame(root_window, bg="gray", height=50)
menu_frame.pack(fill=tk.X, side=tk.TOP)

# Create a canvas for rams
canvas = tk.Canvas(root_window, width=1200, height=900, bg="green")
canvas.pack()

# Initialize some RamObjects (5 rams in random positions),
# passing in the image path for each.
rams = [
    RamObject(canvas, random.randint(50, 750), random.randint(50, 550), "ram.gif")
    for _ in range(5)
]

# ================== WATER TROUGH VARIABLES ==================
TROUGH_X1, TROUGH_Y1 = 50, 700   # Top-left corner of trough outline
TROUGH_X2, TROUGH_Y2 = 250, 750  # Bottom-right corner
trough_outline = None
trough_fill = None

def create_trough():

    global trough_outline, trough_fill

    # Outline of the trough
    trough_outline = canvas.create_rectangle(
        TROUGH_X1, TROUGH_Y1,
        TROUGH_X2, TROUGH_Y2,
        outline="black", width=2, fill=""
    )

    # Water fill rectangle (initially zero width—i.e., empty).
    trough_fill = canvas.create_rectangle(
        TROUGH_X1, TROUGH_Y1,
        TROUGH_X1, TROUGH_Y2,  # same left X as outline, zero width
        outline="", fill="blue"
    )

def update_trough_fill():

    if trough_fill is None:
        return

    data = Storage.load_data()
    today_str = datetime.date.today().isoformat()
    current_amt = data["water_intake"].get(today_str, 0.0)

    # If < 100, make the fill rectangle zero width (empty)
    if current_amt < 100:
        canvas.coords(trough_fill, TROUGH_X1, TROUGH_Y1, TROUGH_X1, TROUGH_Y2)
    else:
        # If >= 100, fill the entire rectangle
        canvas.coords(trough_fill, TROUGH_X1, TROUGH_Y1, TROUGH_X2, TROUGH_Y2)

# ========== HEART ON CLICK ==========

def on_ram_click(event, ram):

    heart_x = ram.x + 25  # horizontally center over the ram
    heart_y = ram.y - 10  # place it slightly above the ram

    heart_id = canvas.create_text(heart_x, heart_y,
                                  text="♥", fill="red", font=("Arial", 16))

    root_window.after(1000, lambda: canvas.delete(heart_id))

def animate():

    for ram in rams:
        ram.move_random()
    root_window.after(200, animate)

def show_stats():

    stats_window = tk.Toplevel(root_window)
    stats_window.title("Rams' Stats")
    stats_window.geometry("300x300")

    for i, _ in enumerate(rams):
        tk.Label(stats_window, text=f"Ram #{i+1} is alive and well!").pack()

# ========== TASK HANDLERS ==========

def handle_brushed_teeth():

    popup = tk.Toplevel(root_window)
    popup.title("Teeth Brushing")
    popup.geometry("250x120")

    tk.Label(popup, text="How many times?").pack(pady=5)
    entry = tk.Entry(popup)
    entry.pack()

    def submit():
        times_brushed = int(entry.get() or 0)

        data = Storage.load_data()
        today_str = datetime.date.today().isoformat()
        data["teeth_brushing"][today_str] = times_brushed
        Storage.save_data(data)

        update_teeth_streak()
        display_teeth_streak()

        popup.destroy()

    tk.Button(popup, text="Submit", command=submit).pack(pady=5)

def handle_showered():

    popup = tk.Toplevel(root_window)
    popup.title("Shower Status")
    popup.geometry("200x120")

    tk.Label(popup, text="Did you shower? (yes/no)").pack(pady=5)
    entry = tk.Entry(popup)
    entry.pack()

    def submit():
        shower_status = entry.get().lower().strip()

        data = Storage.load_data()
        today_str = datetime.date.today().isoformat()
        data["showers"][today_str] = (shower_status == "yes")
        Storage.save_data(data)

        popup.destroy()

    tk.Button(popup, text="Submit", command=submit).pack(pady=5)

def handle_drank_water():

    popup = tk.Toplevel(root_window)
    popup.title("Water Intake")
    popup.geometry("250x120")

    tk.Label(popup, text="How many ounces?").pack(pady=5)
    entry = tk.Entry(popup)
    entry.pack()

    def submit():
        water_ounces = float(entry.get() or 0)

        data = Storage.load_data()
        today_str = datetime.date.today().isoformat()
        current_amt = data["water_intake"].get(today_str, 0.0)
        data["water_intake"][today_str] = current_amt + water_ounces
        Storage.save_data(data)


        tracker = WaterTracker(capacity_ounces=100)
        tracker.add_water(data["water_intake"][today_str])
        tracker.print_status()

        update_trough_fill()

        popup.destroy()

    tk.Button(popup, text="Submit", command=submit).pack(pady=5)

def handle_steps():

    popup = tk.Toplevel(root_window)
    popup.title("Steps/Strava")
    popup.geometry("250x120")

    tk.Label(popup, text="Did you meet your step goal? (yes/no)").pack(pady=5)
    entry = tk.Entry(popup)
    entry.pack()

    def submit():

        _ = entry.get().lower().strip()
        popup.destroy()

    tk.Button(popup, text="Submit", command=submit).pack(pady=5)


TASK_HANDLERS = {
    "Brushed Teeth?": handle_brushed_teeth,
    "Showered?": handle_showered,
    "Drank water goal?": handle_drank_water,
    "Met required steps?": handle_steps
}

def select_task(task_label):
    handler_func = TASK_HANDLERS.get(task_label)
    if handler_func:
        handler_func()
    else:
        print(f"No handler found for {task_label}")

# ========== DROPDOWN AND BUTTONS ==========

tasks = [
    "Brushed Teeth?",
    "Showered?",
    "Drank water goal?",
    "Met required steps?"
]
selected_task = tk.StringVar(root_window)
selected_task.set(tasks[0])

task_menu = tk.OptionMenu(menu_frame, selected_task, *tasks, command=select_task)
task_menu.pack(side=tk.LEFT, padx=10, pady=5)

stats_button = tk.Button(menu_frame, text="Stats", command=show_stats)
stats_button.pack(side=tk.LEFT, padx=10, pady=5)


create_trough()
update_trough_fill()
for ram in rams:
    canvas.tag_bind(ram.image_id, "<Button-1>", lambda e, r=ram: on_ram_click(e, r))


animate()

root_window.mainloop()
