"""Generic controller Class for Project Screens

Copyright (c) 2023 Maximilian Stephan <stephan.maxi@icloud.com>
"""

import sys

from abc import abstractmethod
from sense_hat import SenseHat
from typing import final, Any, Tuple, List
import signal


class SenseController:
    """The Sense Controller is an abstraction for the RPI SenseHat.
    It comes with functions, such as signal handling, drawing, erasing and simple animations.

    # Arguments

    * `sense` - SenseHat object the actions shall be performed on.

    * `rotation` - The screen rotation (between 0 and 360 degrees)

    * `low_light_mode` - boolean value on whether the screen shall be dimmed or used normally.
    """
    def __init__(self, sense: SenseHat, rotation: int = 0, low_light_mode: bool = True,) -> None:
        self.sense: SenseHat = sense
        # Adjust Display Rotation
        self.sense.rotation = rotation
        self.sense.low_light = low_light_mode
        self.__running = False

    def handle_signal(self, signum: int, frame: Any):
        """Handle SIGTERM and SIGINT. Stop the Snowflakes and clear the Sense Hat Display

        # Arguments

        Arguments are defined in the
        [Python Signal Docs](https://docs.python.org/3/library/signal.html).

        """
        print(f"Running default cleanup method after signal {signum} ({signal.strsignal(signum)})")
        self.__running = False
        print("Clearing Display...")
        self.sense.clear()
        print("Finishing up.. Goodbye!")
        sys.exit(0)

    def draw(self, position: Tuple[int], color: List[int]):
        """Draw a color at a position on the RPI Sense Hat

        # Arguments

        * `position` - The Position on the RaspberryPi Sense Hat as a tuple
                    with two elements, where the first one is x and the
                    second one is y.
        * `color` - The desired color of the pixel as a list of three elements
                    with the first one being the red, the second one the green
                    and third element being the blue factor of the color.
                    Color Values are Integers between 0 and 255.
        """
        if 0 <= position[0] and position[0] < 8 and 0 <= position[1] and position[1] < 8:
            self.sense.set_pixel(
                *position,
                *color
            )
        else:
            print(f"WARNING: Tried to draw out of display ({position})!")


    def clear_at(self, position: Tuple[int]):
        """Clear a snowflake at certain position

        # Arguments

        * `position` - The Position on the RaspberryPi Sense Hat as a list
                    with two elements, where the first one is x and the
                    second one is y.
        """
        self.sense.set_pixel(
            *position,
            [0, 0, 0]
        )

    @final
    def init_scene(self, clear: bool = True):
        """Initialize the scene

        # Arguments

        * `clear` - Clear the screen before initializing. Defaults to True.
        """
        if clear:
            print("Clearing SenseHat Display ...")
            self.sense.clear()
        self.__running: bool = True
        print("Initializing Scene ...")
        self._init_scene()

    @abstractmethod
    def _init_scene(self):
        """Draw the scene's background. Here"""
        return

    @final
    def start_scene(self):
        """Start the scene loop here"""
        print("Starting Scene Loop ...")
        while self.__running:
            self._next_frame()

    @abstractmethod
    def _next_frame(self):
        """Draw the scene's background. Here"""
        return
