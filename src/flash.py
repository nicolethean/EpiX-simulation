import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
import sys
from PIL import Image
import matplotlib.cm as cm
import os


FRAME_CONST = 60
HOLD_CONST = 5
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FILTER_COLOR = (0.5, 0.5, 0.5)


# converts rgb tuples into luminance value
def rgb2luminance(rgbTup):
    luminance = (0.2126*255*rgbTup[0] + 0.7152 * 255 * rgbTup[1] +
                 0.0722 * 255 * rgbTup[2])  # NTSC formula
    val = 413.435*pow((0.002746*luminance+0.0189623), 2.2)
    return val


# converts 2x2 array of rgb tuples into 2x2 array of luminance. nx is number of pixels in x direction and
# ny is number of pixels in y direction
def rgb2luminanceArr(rgbArr):
    lum_arr = np.zeros((rgbArr.shape[0], rgbArr.shape[1]))
    for i in range(rgbArr.shape[0]):
        for j in range(rgbArr.shape[1]):
            lum_arr[i][j] = rgb2luminance(rgbArr[i][j])
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


def sift(flag_history, most_recent_flag, curr_flag, img, filtered_pixels):
    for i in range(most_recent_flag.shape[0]):
        for j in range(most_recent_flag.shape[1]):
            # either 1 and -1 or -1 and 1
            if filtered_pixels[i][j] > 0:
                if (filtered_pixels[i][j] > HOLD_CONST):
                    filtered_pixels[i][j] = 0
                    most_recent_flag[i][j] = curr_flag[i][j]
                else:
                    img[i][j] = filter(img[i][j])
                    filtered_pixels[i][j] = filtered_pixels[i][j]+1
            else:
                if (curr_flag[i][j] * most_recent_flag[i][j] == -1):
                    # need to filter
                    img[i][j] = filter(img[i][j])
                    flag_history[i][j] = 0
                    filtered_pixels[i][j] = 1
                # either 1 and 1 or -1 and -1
                elif (curr_flag[i][j] == most_recent_flag[i][j]):
                    filtered_pixels[i][j] = 0
                    # current change equal to most recent change
                    flag_history[i][j] = 0
                # either 0 and 1 or 0 and -1
                elif (curr_flag[i][j] == 1 or curr_flag[i][j] == -1):
                    filtered_pixels[i][j] = 0
                    flag_history[i][j] = 0
                    most_recent_flag[i][j] = curr_flag[i][j]
                # either 1 and 0 or -1 and 0
                elif (flag_history[i][j] < FRAME_CONST):
                    filtered_pixels[i][j] = 0
                    # increment most recent change
                    flag_history[i][j] = flag_history[i][j] + 1
                else:
                    # most recent change was > 1 second ago
                    filtered_pixels[i][j] = 0
                    most_recent_flag[i][j] = 0
                    flag_history[i][j] = 0
    return (flag_history, most_recent_flag, img, filtered_pixels)


def filter(pix):
    return FILTER_COLOR


def mini_data():

    n = 3

    colors = [BLACK, BLACK, BLACK, BLACK, WHITE, WHITE,
              BLACK, BLACK, WHITE, WHITE, WHITE, WHITE,
              BLACK, BLACK, BLACK, BLACK, WHITE, WHITE,
              BLACK, BLACK, BLACK, BLACK, WHITE, WHITE,
              BLACK, BLACK, BLACK, BLACK, WHITE, WHITE,
              BLACK, BLACK, BLACK, BLACK, WHITE, WHITE, ]

    data = []

    for i in range(len(colors)):
        data.append(np.full((n, n, 3), colors[i]))

    return data


def getData1():
    data = []
    directory = '/Users/nicole/hack-22/src'
    for filename in os.listdir(directory):
        if (filename.endswith(".png")):
            data.append(mpimg.imread(filename))

    return data


def execute():
    data = getData1()
    animate_non(data)
    filtered_imgs = [data[0], data[1]]
    filtered_pixels = np.zeros((data[0].shape[0], data[0].shape[1]))
    flag_hist = np.zeros((data[0].shape[0], data[0].shape[1]))
    lum_arr1 = rgb2luminanceArr(data[0])
    lum_arr2 = rgb2luminanceArr(data[1])
    flag12 = flagPixels(lum_arr1, lum_arr2)
    recent = flag12

    for img_data in data[2:]:
        print("loading. . .")
        lum_arr1 = getPrevLum(lum_arr1, lum_arr2, filtered_pixels)
        lum_arr2 = rgb2luminanceArr(img_data)
        flag12 = flagPixels(lum_arr1, lum_arr2)
        (flag_hist, recent, imgOut, filtered_pixels) = sift(
            flag_hist, recent, flag12, img_data, filtered_pixels)
        filtered_imgs.append(imgOut)

    for f in filtered_imgs:
        f = (f * 255).astype(np.uint8)

    print("done!")
    animate_filtered(filtered_imgs)


def animate_non(imgs):
    frames = []
    fig = plt.figure()
    for i in imgs:
        frames.append(
            [plt.imshow(i, cmap=cm.Greys_r, animated=True)])

    ani = animation.ArtistAnimation(fig, frames, interval=1, blit=True,
                                    repeat_delay=1000)

    ani.save('testnon.gif', fps=60)
    plt.axis('off')
    plt.show()


def animate_filtered(filtered_imgs):
    frames = []
    fig = plt.figure()
    for i in filtered_imgs:
        frames.append(
            [plt.imshow(i, cmap=cm.Greys_r, animated=True)])

    ani = animation.ArtistAnimation(fig, frames, interval=1, blit=True,
                                    repeat_delay=1000)

    ani.save('testfilter.gif', fps=60)
    plt.axis('off')
    plt.show()


execute()
