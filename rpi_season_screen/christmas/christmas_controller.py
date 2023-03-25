""" Sense Controller to wrap up the RPI Sense Hat Display functions.

Copyright (c) 2022 Maximilian Stephan <stephan.maxi@icloud.com>
"""

import random
import sys

from sense_hat import SenseHat
from typing import List

from rpi_season_screen.christmas.christmastree import O, TREE, TREE_DPT
from rpi_season_screen.christmas.snowflake import SnowFlake
from rpi_season_screen.sense.sense_controller import SenseController


class ChristmasController(SenseController):
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
        super().__init__(sense, rotation, low_light_mode)
        self.snowflakes: list[SnowFlake] = []
        self.parallel_flakes: int = num_flakes
        self.available_indices = [i for i in range(8)]
        self.running = False

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

    def _draw_tree(self):
        """Draw the initial Christmas Tree"""
        self.sense.set_pixels(TREE)

    def _init_scene(self):
        """Initialize the scene"""
        self._draw_tree()
        self.__generate_snowflakes()

    def merry_christmas(self):
        """Display 'Merry Christmas!' message on SenseHat"""
        self.sense.show_message("Merry Christmas!")

    def tree_depth_at(self, position: List[int]) -> int:
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

    def clear_at(self, position: List[int]):
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

    def __generate_snowflakes(self):
        """Generate Snowflakes that can then be used to rain down"""
        for _ in range(self.parallel_flakes):
            index = random.choice(self.available_indices)
            self.available_indices.remove(index)
            self.snowflakes.append(SnowFlake(index, 0))

    def _next_frame(self):
        """Rain Snowflakes down from the top on the Sense Hat"""
        for flake in self.snowflakes:
            flake.move(self)
