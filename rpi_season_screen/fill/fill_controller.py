""" Sense Controller Derivative to wrap up the RPI Sense Hat Display functions between Seasons.

Copyright (c) 2023 Maximilian Stephan <stephan.maxi@icloud.com>
"""
import json
import time

from sense_hat import SenseHat
from rpi_season_screen.sense.sense_controller import SenseController


class FillController(SenseController):
    """Wrapper for the RPI Sense hat to display "fill" content between events.

    # Arguments

    * `sense` - The RPI Sense Hat the Controller is based on
    * `rotation` - Rotation of the tree, value between 0 and 306.
    * `low_light_mode` - True if the Sense Hat should use the Low Light mode.
    """
    def __init__(
        self, sense: SenseHat, rotation: int = 0, low_light_mode: bool = True
    ):
        super().__init__(sense, rotation, low_light_mode)
        with open("/etc/rpi-season-screen/bad_apple.json", "r", encoding="utf-8") as jsonfile:
            self.frames = json.load(jsonfile)
        self.current_frame = 0
        self.framerate = 27 #fps
        self.last_time = time.time()

    def _init_scene(self):
        """Draw the scene's background. Here nothing happens."""
        return

    def _next_frame(self):
        """Start the scene loop here"""
        if self.last_time + (1 / self.framerate) > time.time():
            return
        self.last_time = time.time()
        self.sense.set_pixels(self.frames[f"{self.current_frame}"])
        self.current_frame += 1
