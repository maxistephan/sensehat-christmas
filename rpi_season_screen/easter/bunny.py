""" Bunny hopping on the RPI Sense Hat Display.

A bunny comes in from the left side of the screen and jumps until in the middle.
Once in the middle, the bunny blinks and resumes hopping out of the right.

Copyright (c) 2022 Maximilian Stephan <stephan.maxi@icloud.com>
"""

import time

from enum import Enum, auto
from typing import List

from rpi_season_screen.sense.sense_controller import SenseController

MAX_RAD = 4
X_MAX = 7
Y_MAX = 7
X_MIN = 0
Y_MIN = 0

W = [255, 255, 255] # White
O = [0, 0, 0]       # Dark / Black
B = [53, 22, 6]     # Brown
b = [137, 98, 71]   # light Brown
P = [214, 149, 184] # Pink

BUNNY: List[List[int]] = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, B, b, O, O,
    O, O, O, O, B, b, O, O,
    O, O, O, O, B, O, B, O,
    O, B, B, B, B, B, P, O,
    W, b, b, B, B, B, O, O,
    W, b, b, B, B, B, O, O,
    O, b, b, b, O, B, B, O,
]


class BunnyState(Enum):
    """Enum Representation of Bunny states"""
    ENTERING = auto()
    BLINKING = auto()
    EXITING = auto()


class BunnyDirection(Enum):
    """Enum Representation of current Direction
    """
    UP = auto()
    DOWN = auto()
    RIGHT = auto()


class EasterBunny:
    """Representation of the easter bunny coming in from the left.
    """
    def __init__(self):
        self.state: BunnyState = BunnyState.ENTERING
        self.matrix: List[List[int]] = BUNNY.copy()
        self.prev_matrix: List[List[int]] = []
        self.timedelta: float = 0.1
        self.last_time: float = time.time()
        self.motion_cycle: List[BunnyDirection] = [
            BunnyDirection.UP,
            BunnyDirection.RIGHT,
            BunnyDirection.DOWN,
        ]
        self.current_motion = 0

    def move(self, controller: SenseController):
        """Move the bunny.

        # Arguments

        * `controller` - NewYearController Object the move shall be performed on
        """
        extra_wait = 0.8 if self.current_motion == 0 else 0
        if self.last_time + self.timedelta + extra_wait > time.time():
            return

        self.last_time = time.time()
        new_matrix: List[List[int]] = []
        for y_pos in range(Y_MAX + 1):
            for x_pos in range(X_MAX + 1):
                new_color = self._get_new_color_at(x_pos=x_pos, y_pos=y_pos)
                new_matrix.append(
                    new_color
                )
                controller.draw(
                    position=(x_pos, y_pos),
                    color=new_color,
                )
        self.matrix = new_matrix
        self._change_motion()

    def _change_motion(self):
        self.current_motion += 1
        if self.current_motion >= len(self.motion_cycle):
            self.current_motion = 0

    def _get_new_color_at(self, x_pos: int, y_pos: int) -> List[int]:
        """Get the new color of a point for the next frame at a certain position

        # Arguments

        * `x_pos` - x position

        * `y_pos` - y position

        # Returns

        `List[int]` - Color
        """
        # WARNING! this only works if the bunny does not leave the screen!
        matrix_index: int = (Y_MAX + 1) * y_pos + x_pos

        if self.motion_cycle[self.current_motion] == BunnyDirection.UP:
            if y_pos >= Y_MAX:
                return O
            matrix_index = matrix_index + (Y_MAX + 1)
        elif self.motion_cycle[self.current_motion] == BunnyDirection.DOWN:
            if y_pos == 0:
                return O
            matrix_index = matrix_index - (Y_MAX + 1)
        elif self.motion_cycle[self.current_motion] == BunnyDirection.RIGHT:
            matrix_index = matrix_index - 1 if x_pos > 0 else X_MAX + (1 + Y_MAX) * y_pos

        return self.matrix[matrix_index].copy()
