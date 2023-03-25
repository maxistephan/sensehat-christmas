""" Firework Rockets on the RPI Sense Hat Display.

A Rocket flies from the bottom to somewhere in the top middle of the screen and
explodes there.
The height, speed and size of an exploding Rocket are based off of their depth
in the scene.

Copyright (c) 2022 Maximilian Stephan <stephan.maxi@icloud.com>
"""

import random
import time
import math

from rpi_season_screen.sense.sense_controller import SenseController
from enum import Enum, auto
from typing import Tuple, List


MAX_RAD = 4
X_MAX = 7
Y_MAX = 7
X_MIN = 0
Y_MIN = 0


class RocketState(Enum):
    """Enum Representation of Firework Rockets states"""
    FLYING = auto()
    EXPLODING = auto()
    DESTROYED = auto()
    WAITING = auto()


class RocketError(Exception):
    """Errors related to firework rockets"""


class ExplosionParticle:
    """Explosion class of the Firework Rocket representing a single particle in the Explosion"""
    def __init__(self, position: Tuple[int], direction: Tuple[int], lifetime: int):
        self.position: Tuple[int] = position
        self.direction: Tuple[int] = direction
        self.lifetime: int = lifetime
        self.waiting = False

    def move(self):
        if math.fabs(self.direction[0]) + math.fabs(self.direction[1]) > 1:
            if self.waiting:
                self.waiting = False
            else:
                self.waiting = True
                return
        self.position = (
            self.position[0] + self.direction[0],
            self.position[1] + self.direction[1]
        )
        self.lifetime -= 1

    def check_out_of_bounds(self) -> bool:
        return (self.position[0] < X_MIN or X_MAX < self.position[0] or
                self.position[1] < Y_MIN or Y_MAX < self.position[1])


class Rocket:
    """Representation of a Firework Rocket on the RPI Sense Hat

    # Arguments

    * `x` - x position of the Rocket
    """
    def __init__(self, x: int, color: List[int] = None):
        self.x = x
        self.y = Y_MAX
        self.color_is_custom: bool = color is not None
        self.color = color if color else [round(random.random() * 255) for _ in range(3)]
        self.depth = random.randint(1, 10)
        self.time = self._time_by_depth()
        self.last_time = time.time()
        self.state = RocketState.FLYING
        self.explosion_particles: List[ExplosionParticle] = []

    def move(self, controller: SenseController):
        """Move this rocket's Particels the way they should

        # Arguments

        * `controller` - NewYearController Object the move shall be performed on
        """
        if self.state == RocketState.FLYING:
            self._fly(controller)
        elif self.state == RocketState.EXPLODING:
            self._explode(controller)
        elif self.state == RocketState.WAITING:
            self._stop_waiting()
        elif self.state == RocketState.DESTROYED:
            for particle in self.explosion_particles:
                if particle.check_out_of_bounds(): continue
                controller.clear_at(particle.position)
            controller.available_indices.append(self.x)
            self.depth = random.randint(1, 10)
            self.time = self._time_by_depth()
            self.y = Y_MAX
            self.x = random.choice(controller.available_indices)
            if not self.color_is_custom:
                self.color = [round(random.random() * 255) for _ in range(3)]
            controller.available_indices.remove(self.x)
            self.explosion_particles: List[ExplosionParticle] = []
            self.state = RocketState.FLYING
        else: raise RocketError(f"Unknown State: {self.state}")

    def _fly(self, controller: SenseController):
        """Move this rocket one field up if the timing is correct.

        # Arguments

        * `controller` - NewYearController Object the move shall be performed on
        """
        if self.last_time + self.time <= time.time():
            self.last_time = time.time()
            self.time = self.time * 1.2
            controller.clear_at([self.x, self.y])
            self.y -= 1
            if self.y <= self._height_by_depth():
                self.state = RocketState.WAITING
                controller.clear_at((self.x, self.y))

        controller.draw((self.x, self.y), [255, 255, 255])

    def _explode(self, controller: SenseController):
        """Animate the explosion of the Rocket if the timing is right.

        # Arguments

        * `controller` - NewYeaController Object the explosion shall be performed on
        """
        if not self.explosion_particles or 0 == len(self.explosion_particles):
            self._generate_particles()
        if self.last_time + self.time <= time.time():
            self.last_time = time.time()
            self.time = self.time * 0.8
            for particle in self.explosion_particles:
                if particle.check_out_of_bounds(): continue
                controller.clear_at(particle.position)
                if 0 < particle.lifetime:
                    particle.move()
                    if particle.check_out_of_bounds(): continue
                    controller.draw(particle.position, self.color)
                else:
                    controller.clear_at(particle.position)
                    self.state = RocketState.DESTROYED

    def _stop_waiting(self):
        if self.last_time + self.time <= time.time():
            self.time = self._time_by_depth()
            self.state = RocketState.EXPLODING

    def _generate_particles(self):
        particles: List[ExplosionParticle] = []
        fields: List[Tuple[int]] = self._get_surrounding_fields()
        for field in fields:
            direction: Tuple[int] = (field[0] - self.x, field[1] - self.y)
            particles.append(ExplosionParticle(
                position=(self.x, self.y),
                direction=direction,
                lifetime=self._lifetime_by_depth()
            ))
        self.explosion_particles = particles

    def _get_surrounding_fields(self) -> List[Tuple[int]]:
        fields = []
        for i in (-1, 0, 1):
            x = i + self.x
            if x < X_MIN or x > X_MAX: continue
            for j in (-1, 0, 1):
                y = j + self.y
                if y < Y_MIN or y > Y_MAX: continue
                if x == self.x and y == self.y: continue
                fields.append((x, y))
        return fields

    def _lifetime_by_depth(self) -> int:
        """Returns the lifetime (radius) of a fireworks explosion,
        depending on its depth in the scene.
        """
        return MAX_RAD - self.depth // 3

    def _time_by_depth(self) -> float:
        """Return a time between 0.1 and 1 seconds based off of the depth.

        A Depth of 10 is far away, so the time between updates is longer.
        This results in 10 being 1 second, 5 being 0.5 seconds and 1 being 0.1 seconds, and so on.
        """
        assert 0 < self.depth and self.depth <= 10
        return self.depth / 10

    def _height_by_depth(self) -> int:
        """Return a y value between 1 and 5 based off of the depth.

        A Depth of 10 is far away, so the time between updates is longer.
        This results in 10 being 1 second, 5 being 0.5 seconds and 1 being 0.1 seconds, and so on.
        """
        assert 0 < self.depth and self.depth <= 10
        return self.depth // 2
