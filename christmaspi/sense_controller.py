""" Sense Controller to wrap up the RPI Sense Hat Display functions.

Copyright (c) 2022 Maximilian Stephan <stephan.maxi@icloud.com>
"""

import random
import sys
import time

from sense_hat import SenseHat

from christmaspi.christmastree import R, G, B, W, O, b, Y, TREE, TREE_DPT
from christmaspi.snowflake import SnowFlake


class SenseController:
    """Wrapper for the RPI Sense hat to display a Christmas Tree and Snowflakes.

    # Arguments

    * `sense` - The RPI Sense Hat the Controller is based on
    * `num_flakes` - Number of snowflakes, default and max being 8
    * `rotation` - Rotation of the tree, value between 0 and 360.
    * `low_light_mode` - True if the Sense Hat should use the Low Light mode.
    """
    def __init__(
        self, sense: SenseHat, num_flakes: int = 8, rotation: int = 0, low_light_mode: bool = True
    ):
        self.sense = sense
        self.snowflakes: list[SnowFlake] = []
        self.parallel_flakes: int = num_flakes
        self.available_indices = [i for i in range(8)]
        # Adjust Rotation
        self.sense.rotation = rotation
        self.sense.low_light = low_light_mode

    def handle_signal(self, signum, frame):
        """Handle SIGTERM and SIGINT. Stop the Snowflakes and clear the Sense Hat Display

        # Arguments

        Arguments are defined in the
        [Python Signal Docs](https://docs.python.org/3/library/signal.html).

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
