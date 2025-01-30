class WaterTracker:
    def __init__(self, capacity_ounces):

        self.capacity_ounces = capacity_ounces
        self.current_ounces = 0

    def add_water(self, ounces):
        """
        Adds water to the trough. Caps at max capacity.
        """
        self.current_ounces += ounces
        if self.current_ounces > self.capacity_ounces:
            self.current_ounces = self.capacity_ounces

    def get_water_level(self):
        """
        Returns an integer from 0 to 4 representing how many quarters full the trough is:
          0 = empty
          1 = 1/4 full
          2 = 1/2 full
          3 = 3/4 full
          4 = full
        """
        if self.capacity_ounces <= 0:
            return 0
        quarter_capacity = self.capacity_ounces / 4
        level = int(self.current_ounces / quarter_capacity)
        return min(level, 4)

    def print_status(self):
        """
        Prints a status message about the trough’s water level.
        """
        level = self.get_water_level()
        if level == 0:
            print("The trough is empty.")
        elif level == 1:
            print("The trough is 1/4 full.")
        elif level == 2:
            print("The trough is 1/2 full.")
        elif level == 3:
            print("The trough is 3/4 full.")
        else:
            print("The trough is full.")
