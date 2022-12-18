#!/usr/bin/python3

""" Python Implementation to display a Christmas Tree on the RaspberyPi Sense Hat.

This Project is setup considering the Sense Hat version 1.0 is used and the
Display has a total of 8x8 pixels.
"""

import click
import random
import signal
import sys
import time

from sense_hat import SenseHat


R = [255, 0, 0]     # Red
G = [0, 255, 0]     # Green
B = [0, 0, 255]     # Blue
W = [255, 255, 255] # White
O = [0, 0, 0]       # Dark
b = [139, 69, 19]   # Brown
Y = [255, 255, 0]  # Yellow


TREE = [
    O, O, O, O, O, O, O, O,
    O, O, Y, O, O, O, O, O,
    O, O, G, O, O, O, O, O,
    O, G, Y, G, O, O, O, O,
    O, Y, R, G, O, O, O, O,
    Y, G, G, Y, G, O, O, O,
    B, O, b, O, R, O, O, O,
    O, O, b, O, O, O, O, O
]


TREE_DPT = 7


def time_by_depth(depth: int) -> float:
    """Return a time between 0.1 and 1 seconds based off of the depth.

    A Depth of 10 is far away, so the time between updates is longer.
    This results in 10 being 1 second, 5 being 0.5 seconds and 1 being 0.1 seconds, and so on.
    """
    assert 0 < depth and depth <= 10
    return depth / 10


class SnowFlake:
    """Representation of a single Snowflake on the RPI Sense Hat
    
    # Arguments

    * `x` - x position of the Snowflake
    * `y` - initial y position of the Snowflake, 0 being top and 7 being bottom
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.depth = random.randint(1, 10)
        self.time = time_by_depth(self.depth)
        self.last_time = time.time()

    def move(self, controller):
        """Move this snowflake one field down if the timing is correct.

        # Arguments

        * `controller` - SenseController Object the move shall be performed on

        """
        if self.last_time + self.time <= time.time():
            self.last_time = time.time()
            controller.clear_at([self.x, self.y])
            self.y += 1
            if self.y > 7:
                controller.available_indices.append(self.x)
                self.depth = random.randint(1, 10)
                self.time = time_by_depth(self.depth)
                self.y = 0
                self.x = random.choice(controller.available_indices)
                controller.available_indices.remove(self.x)

            if controller.tree_depth_at([self.x, self.y]) > self.depth:
                controller.draw([self.x, self.y], [255, 255, 255])
    

class SenseController:
    """Wrapper for the RPI Sense hat to display a Christmas Tree and Snowflakes.

    # Arguments

    * `sense` - The RPI Sense Hat the Controller is based on
    * `num_flakes` - Number of snowflakes, default and max being 8 (Sense hat is 8 px wide)
    * `rotation` - Rotation of the tree, value between 0 and 360.
    * `low_light_mode` - True if the Sense Hat should use the Low Light mode.
    """
    def __init__(self, sense: SenseHat, num_flakes: int = 8, rotation: int = 0, low_light_mode: bool = True):
        self.sense = sense
        self.snowflakes = []
        self.parallel_flakes = num_flakes
        self.available_indices = [i for i in range(8)]
        # Adjust Rotation
        self.sense.rotation = rotation
        self.sense.low_light = low_light_mode

    def handle_signal(self, signum, frame):
        """Handle SIGTERM and SIGINT. Stop the Snowflakes and clear the Sense Hat Display

        # Arguments

        Arguments are defined in the [Python Signal Docs](https://docs.python.org/3/library/signal.html).

        """
        print("\nStopping Snowflakes...")
        self.running = False
        print("Clearing Display...")
        self.sense.clear()
        print("Finishing up.. Goodbye!")
        sys.exit(0)

    def draw_tree(self):
        """Draw the initial Christmas Tree"""
        self.sense.set_pixels(TREE)

    def merry_christmas(self):
        """Display 'Merry Christmas!' message on SenseHat"""
        self.sense.show_message("Merry Christmas!")

    def tree_depth_at(self, position: list[int]) -> int:
        """Return TREE_DPT if there is a value at TREE position and 11 (far back) if there is none.

        # Arguments

        * `position` - The Position on the RaspberryPi Sense Hat as a list
                    with two elements, where the first one is x and the
                    second one is y.
        """
        index = position[0] + 8 * position[1]
        if O == TREE[index]:
            return 11
        else:
            return TREE_DPT

    def clear_at(self, position: list[int]):
        """Clear a snowflake at certain position

        # Arguments

        * `position` - The Position on the RaspberryPi Sense Hat as a list
                    with two elements, where the first one is x and the
                    second one is y.

        """
        index = position[0] + 8 * position[1]
        self.sense.set_pixel(
            *position,
            *TREE[index]
        )

    def draw(self, position: list[int], color: list[float]):
        """Draw a color at a position on the RPI Sense Hat

        # Arguments

        * `position` - The Position on the RaspberryPi Sense Hat as a list
                    with two elements, where the first one is x and the
                    second one is y.
        * `color` - The desired color of the pixel as a list of three elements
                    with the first one being the red, the second one the green
                    and third element being the blue factor of the color.
                    Color Values are between 0 and 255.

        """
        self.sense.set_pixel(
            *position,
            *color
        )

    def __generate_snowflakes(self):
        """Generate Snowflakes that can then be used to rain down"""
        for i in range(self.parallel_flakes):
            index = random.choice(self.available_indices)
            self.available_indices.remove(index)
            self.snowflakes.append(SnowFlake(index, 0))

    def let_it_snow(self):
        """Rain Snowflakes down from the top on the Sense Hat"""
        self.running = True
        self.__generate_snowflakes()
        start = time.time()
        while self.running:
            [flake.move(self) for flake in self.snowflakes]


@click.command()
@click.option("--snowflakes", default=8, type=int, help="Number of Snowflakes on the Sense Hat.")
@click.option("--rotation", default=0, type=int, help="Rotation of the Chrismas Tree in degrees.")
@click.option("--low-light-mode", is_flag=True, help="Sets the Low Light Mode on the Sense Hat")
def main(snowflakes: int, rotation: int, low_light_mode: bool):
    sense = SenseHat()
    controller = SenseController(
        sense, num_flakes=snowflakes, rotation=rotation, low_light_mode=low_light_mode
    )
    signal.signal(signal.SIGTERM, controller.handle_signal)
    signal.signal(signal.SIGINT, controller.handle_signal)
    controller.merry_christmas()
    controller.draw_tree()
    controller.let_it_snow()


if __name__ == '__main__':
    main()
