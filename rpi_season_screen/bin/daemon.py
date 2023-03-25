#!/usr/bin/python3

""" Python Implementation to display a Christmas Tree on the RaspberyPi Sense Hat.

This Project is setup considering the Sense Hat version 1.0 is used and the
Display has a total of 8x8 pixels.

Copyright (c) 2022 Maximilian Stephan <stephan.maxi@icloud.com>
"""

from datetime import datetime
from signal import signal, SIGTERM, SIGINT

import click

from sense_hat import SenseHat

from rpi_season_screen.christmas.christmas_controller import ChristmasController
from rpi_season_screen.new_year.new_year_controller import NewYearController
from rpi_season_screen.easter.easter_controller import EasterController
from rpi_season_screen.sense.sense_controller import SenseController
from rpi_season_screen.fill.fill_controller import FillController
from rpi_season_screen.video.video_controller import VideoController


def start_scene(controller: SenseController):
    """Starts the Scene"""
    signal(SIGTERM, controller.handle_signal)
    signal(SIGINT, controller.handle_signal)
    controller.init_scene()
    controller.start_scene()


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


@main.command(name="auto")
@click.pass_context
def start_automatically(ctx):
    rotation = ctx.obj["rotation"]
    low_light_mode = ctx.obj["low_light_mode"]
    sense = SenseHat()
    controller = FillController(
        sense, rotation=rotation, low_light_mode=low_light_mode
    )
    current_month = datetime.now().month
    if current_month == 1:
        controller = NewYearController(
            sense, rotation=rotation, low_light_mode=low_light_mode
        )
    elif current_month == 12:
        controller = ChristmasController(
            sense, rotation=rotation, low_light_mode=low_light_mode
        )
    start_scene(controller)


@main.command(name="christmas")
@click.option("--snowflakes", default=8, type=int, help="Number of Snowflakes on the Sense Hat.")
@click.pass_context
def start_christmas(ctx, snowflakes: int):
    rotation = ctx.obj["rotation"]
    low_light_mode = ctx.obj["low_light_mode"]
    sense = SenseHat()
    controller = ChristmasController(
        sense, num_flakes=snowflakes, rotation=rotation, low_light_mode=low_light_mode
    )
    start_scene(controller)


@main.command(name="new-year")
@click.pass_context
def start_new_year(ctx):
    rotation = ctx.obj["rotation"]
    low_light_mode = ctx.obj["low_light_mode"]
    sense = SenseHat()
    controller = NewYearController(
        sense, rotation=rotation, low_light_mode=low_light_mode
    )
    start_scene(controller)


@main.command(name="easter")
@click.pass_context
def start_easter(ctx):
    rotation = ctx.obj["rotation"]
    low_light_mode = ctx.obj["low_light_mode"]
    sense = SenseHat()
    controller = EasterController(
        sense, rotation=rotation, low_light_mode=low_light_mode
    )
    start_scene(controller)


@main.command(name="fill")
@click.pass_context
def start_fill(ctx):
    rotation = ctx.obj["rotation"]
    low_light_mode = ctx.obj["low_light_mode"]
    sense = SenseHat()
    controller = FillController(
        sense, rotation=rotation, low_light_mode=low_light_mode
    )
    start_scene(controller)


@main.command(name="video")
@click.option("--video-path", "-f", type=str, help="Path to the video source.")
@click.pass_context
def start_video(ctx, video_path):
    rotation = ctx.obj["rotation"]
    low_light_mode = ctx.obj["low_light_mode"]
    sense = SenseHat()
    controller = VideoController(
        video_path, sense, rotation=rotation, low_light_mode=low_light_mode
    )
    start_scene(controller)


if __name__ == '__main__':
    main()
