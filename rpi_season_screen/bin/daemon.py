#!/usr/bin/python3

""" Python Implementation to display a Christmas Tree on the RaspberyPi Sense Hat.

This Project is setup considering the Sense Hat version 1.0 is used and the
Display has a total of 8x8 pixels.

Copyright (c) 2022 Maximilian Stephan <stephan.maxi@icloud.com>
"""

import click

from sense_hat import SenseHat
from signal import signal, SIGTERM, SIGINT

from rpi_season_screen.christmas.sense_controller import SenseController


@click.group()
@click.option("--rotation", default=0, type=int, help="Rotation of the Chrismas Tree in degrees.")
@click.option("--low-light-mode", is_flag=True, help="Sets the Low Light Mode on the Sense Hat")
@click.pass_context
def main(ctx, rotation: int, low_light_mode: bool):
    # Reserverd for generic implementations
    ctx.obj = {
        "rotation": rotation,
        "low_light_mode": low_light_mode,
    }


@main.command(name="christmas")
@click.option("--snowflakes", default=8, type=int, help="Number of Snowflakes on the Sense Hat.")
@click.pass_context
def start_christmas(ctx, snowflakes: int):
    rotation = ctx.obj["rotation"]
    low_light_mode = ctx.obj["low_light_mode"]
    sense = SenseHat()
    controller = SenseController(
        sense, num_flakes=snowflakes, rotation=rotation, low_light_mode=low_light_mode
    )
    signal(SIGTERM, controller.handle_signal)
    signal(SIGINT, controller.handle_signal)
    controller.merry_christmas()
    controller.draw_tree()
    controller.let_it_snow()


if __name__ == '__main__':
    main()
