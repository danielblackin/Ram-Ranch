import tkinter as tk
import random

class RamObject:
    def __init__(self, canvas, x, y, image_path="ram.gif"):
        """
        Represents a Ram on a Tkinter canvas using an image instead of a rectangle.

        :param canvas: The Tkinter Canvas where the ram is drawn.
        :param x: Initial X-position (top-left corner).
        :param y: Initial Y-position (top-left corner).
        :param image_path: File path to the ram image (default is 'ram.png').
        """
        self.canvas = canvas
        self.x = x
        self.y = y

        # Load the image.
        # IMPORTANT: We must store the resulting PhotoImage in an instance variable
        # so it isn't garbage-collected. If we don't, the image won't display.
        self.image_obj = tk.PhotoImage(file=image_path)

        # Create the image on the canvas.
        # anchor=tk.NW means the (x, y) is the top-left corner of the image.
        self.image_id = canvas.create_image(
            self.x,
            self.y,
            image=self.image_obj,
            anchor=tk.NW
        )

    def move(self, dx, dy):
        """
        Moves the ram image by (dx, dy) on the canvas.
        """
        self.canvas.move(self.image_id, dx, dy)
        self.x += dx
        self.y += dy

    def move_random(self):
        """
        Moves the ram randomly by -5 to +5 in both x and y directions.
        """
        dx = random.randint(-5, 5)
        dy = random.randint(-5, 5)
        self.move(dx, dy)
