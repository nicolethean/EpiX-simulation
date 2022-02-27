import os
import matplotlib.cm as cm
import sys
import matplotlib.animation as animation
import matplotlib.pyplot as plt
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


# def mini_data():
#     return [get_pixels("color-black.png"), get_pixels("color-white.png"), get_pixels("color-black.png")]


def data_set1():
    b_strip = [get_pixels("color-black.png")] * 10
    alternate = [get_pixels("color-black.png"),
                 get_pixels("color-white.png")] * 2
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
        print(f)
    frame_one = img_frames[0]
    frame_one.save("my_awesome.gif", format="GIF", append_images=img_frames,
                   save_all=True, duration=100, loop=0)


def frame_to_img(arr):
    im = Image.fromarray(arr)


# def execute():
#     for frame in mini_data():
#         f1 = rgb2luminanceArr(frame)

# execute()


######################################################################

######################################################################
# from videofig import videofig


FRAME_CONST = 60


# converts rgb tuples into luminance value
def rgb2luminance(rgbTup):
    # print(rgbTup)
    luminance = (0.2126*255*rgbTup[0] + 0.7152 * 255 * rgbTup[1] +
                 0.0722 * 255 * rgbTup[2])  # NTSC formula
    val = 413.435*pow((0.002746*luminance+0.0189623), 2.2)

    # print("RGB LUM")
    # print(val)
    return val


# converts 2x2 array of rgb tuples into 2x2 array of luminance. nx is number of pixels in x direction and
# ny is number of pixels in y direction
def rgb2luminanceArr(rgbArr):
    # print("IN RGB2 ARR")
    # print(rgbArr.shape[0])
    lum_arr = np.zeros((rgbArr.shape[0], rgbArr.shape[1]))
    for j in range(rgbArr.shape[1]):
        lum_arr[i][j] = rgb2luminance(rgbArr[i][j])
    # print(lum_arr)
    return lum_arr


def getPrevLum(lum_old, lum_curr, filtered_pixels):
    for i in range(lum_old.shape[0]):
        for j in range(lum_old.shape[1]):
            if filtered_pixels[i][j] == 0:
                lum_old[i][j] = lum_curr[i][j]
    return lum_old


# l2 is pixel's current luminosity and l1 is pixel's previous luminosity in previous fram
# returns 1 if change is very bright, -1 if change is too dark and 0 if no significant change


def flagChange(l1, l2):
    if ((l2-l1 > 20) and (l1 < 160)):
        return 1
    elif (l1 - l2 > 20) and (l2 < 160):
        return -1
    return 0


# returns array representing changes between two frames
def flagPixels(lum_old, lum_curr):
    flagged = np.zeros(lum_old.shape)
    for i in range(lum_old.shape[0]):
        for j in range(lum_old.shape[1]):

            flagged[i][j] = flagChange(lum_old[i][j], lum_curr[i][j])
    return flagged

# updates values of flag history, recent flag and filters img:
# recent flag is a matrix that represents the most recent change (bright, dark, neither) for each pixel
# flag_history stores how many frames it has been since the most recent change for each pixel
#  - if a change is recorded from bright to dark then filter out that pixel
#  - if the flag_history for a pixel is greater than the frame rate then the most recent change is no change

# d filtered_pixels is a matrix that is 0 if a pixel is filtered and 1 if a pixel is not filteredef sift(flag_history, most_recent_flag, curr_flag, img, filtered_pixels):
    for i in range(most_recent_flag.shape[0]):
        for j in range(most_recent_flag.shape[1]):
            # print("flag hist:")
            # print(flag_history[i][j])
            # either 1 and -1 or -1 and 1
            if (curr_flag[i][j] * most_recent_flag[i][j] == -1):
                # need to filter
                # print("SIFT: FIRST IF")
                # # print(data0)
                most_recent_flag[i][j] = curr_flag[i][j]
                img[i][j] = filter(img[i][j])
                # print("SIFT: FIRST IF, SECOND ")
                # print(data0)
                flag_history[i][j] = 0
                filtered_pixels[i][j] = 0
                # print("SIFT: FIRST IF, THIRD ")
                # print(data0)
            # either 1 and 1 or -1 and -1
            elif (curr_flag[i][j] == mos1_recent_flag[i][j]):

                # current change equal to most recent change
                flag_history[i][j] = 0
            # either 0 and 1 or 0 and -1
            elif (curr_flag[i][i] == 1 or curr_flag[i][i] == -1):
                flag_history[i][j] = 0
                most_recent_flag[i][j] = curr_flag[i][j]
                filtered_pixels[i][j] = 0
            # either 1 and 0 or -1 and 0
            elif (flag_history[i][j] < FRAME_CONST):
                # increment most recent change
                flag_history[i][j] = flag_history[i][j]
                filtered_pixels[i][j] = 0
            else:
                # most recent change was > 1 second ago
                most_recent_flag[i][j] = 0
                flag_history[i][j] = 0

                filtered_pixels[i][j] = 0
    return (flag_history, most_recent_flag, img)

    def execute():
        # data = mini_data()
    data = getData1()
    print(data)
    filtered_imgs = [data[0], data[1]]
    filtered_pixels = filtered_imgs
    flag_hist = np.zeros((data[0].shape[0], data[0].shape[1]))
    lum_arr1 = rgb2luminanceArr(data[0])
    lum_arr2 = rgb2luminanceArr(data[1])
    flag12 = flagPixels(lum_arr1, lum_arr2)
    recent = flag12
    # print("DATA 0:")
    # print(data[0])
    # print(data[1])

    for img_data in data[2:]:
        lum_arr1 = getNewLum(lum_arr1, st, rece, filtered_pixels)
        lum_arr2 = rgb2luminanceArr(img_data)
        flag12 = flagPixels(lum_arr1, lum_arr2)
        (flag_hist, recent, imgOut, filtered_pixels) = sift(
            flag_hist, flag12, img_data, filtered_pixels)
        # print("DATA 0:")
        # print(data[0])
        # print(data[1])
        filtered_imgs.append(imgOut)

       # print("IMG OUT:")
        # print(imgOut)
