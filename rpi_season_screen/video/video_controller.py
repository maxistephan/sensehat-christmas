""" Sense Controller Derivative to display a video (in 8x8).

Copyright (c) 2023 Maximilian Stephan <stephan.maxi@icloud.com>
"""
import json
import time
from pathlib import Path

import cv2
from sense_hat import SenseHat
from rpi_season_screen.sense.sense_controller import SenseController

X_MAX = 7
Y_MAX = 7


class VideoController(SenseController):
    """Wrapper for the RPI Sense hat to display video content.

    # Arguments

    * `video_path` - Path to the video
    * `sense` - The RPI Sense Hat the Controller is based on
    * `rotation` - Rotation of the tree, value between 0 and 306.
    * `low_light_mode` - True if the Sense Hat should use the Low Light mode.
    """
    def __init__(
        self, video_path: str, sense: SenseHat, rotation: int = 0, low_light_mode: bool = True
    ):
        super().__init__(sense, rotation, low_light_mode)
        if not Path(video_path).exists():
            raise FileNotFoundError(f"Path to video ({video_path}) does not exist.")
        self.video = cv2.VideoCapture(video_path)
        self.fps: int = self.video.get(cv2.CAP_PROP_FPS)
        self.last_time: float = time.time()
        self.video_length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame: int = 0
        self.images = []

    def _init_scene(self):
        """Draw the scene's background. Here nothing happens."""
        buffer_size = 50 if self.video_length >= 50 else self.video_length
        print(f"Buffering the first {buffer_size} images ...")
        for _ in range(buffer_size):
            self._fill_next_image()
        print("Done!")

    def _next_frame(self):
        """Start the scene loop here"""
        if len(self.images) < self.video_length:
            self._fill_next_image()
        if self.last_time + (1 / self.fps) > time.time():
            return
        self.last_time = time.time()
        self.sense.set_pixels(self.images[self.current_frame])
        self.current_frame += 1
        if self.current_frame >= len(self.images):
            self.current_frame = 0

    def _fill_next_image(self):
        success, image = self.video.read()
        if not success:
            print("ERROR: Could not read video frame!")
            return
        resized_img = cv2.resize(image, (X_MAX + 1, Y_MAX + 1))
        img_arr = []
        for img in resized_img:
            for i in img:
                img_arr.append(i)
        self.images.append(img_arr)
