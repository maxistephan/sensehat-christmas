""" Sense Controller Derivative to wrap up the RPI Sense Hat Display functions for NewYears.

Copyright (c) 2022 Maximilian Stephan <stephan.maxi@icloud.com>
"""

from sense_hat import SenseHat
from typing import List

import random

from rpi_season_screen.sense.sense_controller import SenseController
from rpi_season_screen.new_year.rocket import Rocket


class NewYearController(SenseController):
    """Wrapper for the RPI Sense hat to display Firework.

    # Arguments

    * `sense` - The RPI Sense Hat the Controller is based on
    * `rotation` - Rotation of the tree, value between 0 and 360.
    * `low_light_mode` - True if the Sense Hat should use the Low Light mode.
    """
    def __init__(
        self,
        sense: SenseHat,
        rotation: int = 0,
        low_light_mode: bool = True,
        parallel_rockets: int = 5,
    ):
        super().__init__(sense, rotation, low_light_mode)
        self.rockets: List[Rocket] = []
        self.available_indices: List[int] = [i for i in range(8)]
        self.parallel_rockets: int = parallel_rockets

    def _init_scene(self):
        """Initialize the Scene.
        Here the background is just black/empty.
        """
        self.__generate_rockets()
        return

    def _next_frame(self):
        """Start the scene loop here"""
        for rocket in self.rockets:
            rocket.move(self)
        return

    def __generate_rockets(self):
        """Generate Rockets that can then be used to fly up"""
        for _ in range(self.parallel_rockets):
            index = random.choice(self.available_indices)
            self.available_indices.remove(index)
            self.rockets.append(Rocket(x=index))
