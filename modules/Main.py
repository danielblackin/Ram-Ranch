import datetime
from modules import Storage
from modules.WaterTracker import WaterTracker
from modules.Streaks import update_teeth_streak, display_teeth_streak

def main():
    while True:
        print("\n-- RAM RANCH CLI --")
        print("1. Enter daily water intake")
        print("2. Enter daily calorie intake")
        print("3. Enter if you took a shower today")
        print("4. Upload steps to Strava? (Placeholder)")
        print("5. Enter how many times you brushed your teeth")
        print("0. Quit")

        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Exiting... Have a good day!")
            break

        data = Storage.load_data()
        today_str = datetime.date.today().isoformat()

        if choice == "1":
            amount = float(input("Enter the amount of water you drank (in ounces): "))
            current_water = data["water_intake"].get(today_str, 0)
            data["water_intake"][today_str] = current_water + amount
            Storage.save_data(data)
            print(f"Total water intake for today: {data['water_intake'][today_str]} ounces")

            tracker = WaterTracker(capacity_ounces=100)
            tracker.add_water(data["water_intake"][today_str])
            tracker.print_status()

        elif choice == "2":
            calories = float(input("Enter the amount of calories you ate today: "))
            print(f"Total calories eaten: {calories} calories")

        elif choice == "3":
            shower_status = input("Did you shower today? (yes/no): ").strip().lower()
            data["showers"][today_str] = (shower_status == "yes")
            Storage.save_data(data)
            if shower_status == "yes":
                print("Your rams are showered too!")
            else:
                print("Your rams smell like you do!")

        elif choice == "4":
            upload_strava = input("Do you want to upload steps to Strava? (yes/no): ").strip().lower()
            if upload_strava == "yes":
                print("Uploading steps to Strava...")
            else:
                print("Strava steps upload canceled.")

        elif choice == "5":
            times_brushed = int(input("How many times did you brush your teeth today? "))
            data["teeth_brushing"][today_str] = times_brushed
            Storage.save_data(data)
            update_teeth_streak()
            display_teeth_streak()
            print(f"You brushed your teeth {times_brushed} times today. Happy rams!")

        else:
            print("Invalid option, please select a valid number.")

if __name__ == "__main__":
    main()
