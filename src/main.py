import glob
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.image as mpimg
from PIL import Image

# import imageio
# images = []
# for filename in filenames:
#     images.append(imageio.imread(filename))
# imageio.mimsave('/path/to/movie.gif', images)


file = False

IMG_W = 4096
IMG_H = 2160


def data_set1():
    b_strip = [get_pixels("color-black.png")] * 10
    alternate = [get_pixels("color-black.png"),
                 get_pixels("color-white.png")] * 1
    b_strip = [get_pixels("color-black.png")] * 10
    set = b_strip + alternate + b_strip
    return set


def start(self):
    self._stop = False
    # self._fps = 25


def update(file):
    return False


def get_pixels(image_str):
    # returns image data as matplotlib img data array
    # im = Image.open(image_str)
    # im = im.crop((0, 0, IMG_W, IMG_H))
    # pixellated = mpimg.imread(im)
    pixellated = mpimg.imread(image_str)
    return pixellated


def make_gif():
    pix_frames = data_set1()
    img_frames = []
    for f in pix_frames:
        frame_to_img(f)
    frame_one = img_frames[0]
    frame_one.save("my_awesome.gif", format="GIF", append_images=img_frames,
                   save_all=True, duration=100, loop=0)


def frame_to_img(arr):
    im = Image.fromarray(arr)


def execute():
    make_gif()

    # print(get_pixels("color-black.png"))


execute()
