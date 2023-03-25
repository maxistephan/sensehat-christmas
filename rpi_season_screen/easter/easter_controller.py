""" Sense Controller Derivative to wrap up the RPI Sense Hat Display functions for Easter holidays.

Copyright (c) 2022 Maximilian Stephan <stephan.maxi@icloud.com>
"""

from sense_hat import SenseHat

from rpi_season_screen.sense.sense_controller import SenseController
from rpi_season_screen.easter.bunny import EasterBunny


class EasterController(SenseController):
    """Wrapper for the RPI Sense hat to display a bunny and eggs.

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
    ):
        super().__init__(sense, rotation, low_light_mode)
        self.bunny: EasterBunny = EasterBunny()

    def _init_scene(self):
        """Initialize the Scene.

        Nothing happens here, since the bunny hopps through the void.
        """
        return

    def _next_frame(self):
        """Start the scene loop here"""
        self.bunny.move(self)
        return
