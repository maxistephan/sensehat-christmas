""" Colours and Tree as a represenation on the rpi Sense Hat.

Copyright (c) 2022 Maximilian Stephan <stephan.maxi@icloud.com>
"""

R = [255, 0, 0]     # Red
G = [0, 255, 0]     # Green
B = [0, 0, 255]     # Blue
W = [255, 255, 255] # White
O = [0, 0, 0]       # Dark
b = [139, 69, 19]   # Brown
Y = [255, 255, 0]  # Yellow


TREE = [
    O, O, O, O, O, O, O, O,
    O, O, Y, O, O, O, O, O,
    O, O, G, O, O, O, O, O,
    O, G, Y, G, O, O, O, O,
    O, Y, R, G, O, O, O, O,
    Y, G, G, Y, G, O, O, O,
    B, O, b, O, R, O, O, O,
    O, O, b, O, O, O, O, O
]


TREE_DPT = 7
