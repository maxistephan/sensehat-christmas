""" Snowflakes on the RPI Sense Hat Display.

A Snowflake falls down every 0-1 seconds. The time intervall is based on its depth.
A higher depth means that the snowflake is further away and falls slower than one that is nearer.
Snowflakes that have a higher depth than the tree will not be rendered in front
of it, for they are too far away.

Copyright (c) 2022 Maximilian Stephan <stephan.maxi@icloud.com>
"""

import random
import time

from christmaspi.christmastree import time_by_depth


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
