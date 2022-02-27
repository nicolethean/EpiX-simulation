import numpy as np
import matplotlib.image as mpimg
import sys

FRAME_CONST = 60


# converts rgb tuples into luminance value
def rgb2luminance(rgbTup):
    # print(rgbTup)
    luminance = (0.2126*255*rgbTup[0] + 0.7152 * 255 * rgbTup[1] +
                 0.0722 * 255 * rgbTup[2])  # NTSC formula
    val = 413.435*pow((0.002746*luminance+0.0189623), 22)

    # print("RGB LUM")
    # print(val)
    return val


# converts 2x2 array of rgb tuples into 2x2 array of luminance. nx is number of pixels in x direction and
# ny is number of pixels in y direction
def rgb2luminanceArr(rgbArr):
    # print("IN RGB2 ARR")
    # print(rgbArr.shape[0])
    lum_arr = np.zeros((rgbArr.shape[0], rgbArr.shape[1]))
    for i in range(rgbArr.shape[0]):
        for j in range(rgbArr.shape[1]):
            lum_arr[i][j] = rgb2luminance(rgbArr[i][j])
    # print(lum_arr)
    return lum_arr


# l2 is pixel's current luminosity and l1 is pixel's previous luminosity in previous fram
# returns 1 if change is very bright, -1 if change is too dark and 0 if no significant change
def flagChange(l1, l2):
    if ((l2-l1 > 0) and (l1 < 160)):
        return 1
    elif (l1 - l2 > 0) and (l2 < 160):
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


def sift(flag_history, most_recent_flag, curr_flag, img, data0):
    img2 = img
    for i in range(most_recent_flag.shape[0]):
        for j in range(most_recent_flag.shape[1]):
            # either 1 and -1 or -1 and 1
            if (curr_flag[i][j] * most_recent_flag[i][j] == -1):
                # need to filter
                # print("SIFT: FIRST IF")
                # print(data0)
                most_recent_flag[i][j] = curr_flag[i][j]
                img2[i][j] = filter(img[i][j])
                # print("SIFT: FIRST IF, SECOND ")
                # print(data0)
                flag_history[i][j] = 0
                # print("SIFT: FIRST IF, THIRD ")
                # print(data0)
            # either 1 and 1 or -1 and -1
            elif (curr_flag[i][j] == most_recent_flag[i][j]):

                # current change equal to most recent change
                flag_history[i][j] = 0
            # either 0 and 1 or 0 and -1
            elif (curr_flag[i][i] == 1 or curr_flag[i][i] == -1):
                flag_history[i][j] = 0
                most_recent_flag[i][j] = curr_flag[i][j]
            # either 1 and 0 or -1 and 0
            elif (flag_history[i][j] < FRAME_CONST):
                # increment most recent change
                flag_history[i][j] = flag_history[i][j] + 1
            else:
                # most recent change was > 1 second ago
                most_recent_flag[i][j] = 0
                flag_history[i][j] = 0

    return (flag_history, most_recent_flag, img2)


def filter(pix):
    return (120, 120, 120)


def mini_data():
    # b_strip = [get_pixels("color-black.png")] * 10
    # alternate = [get_pixels("color-black.png"),
    #              get_pixels("color-white.png")] * 2
    # b_strip = [get_pixels("color-black.png")] * 10
    # set = b_strip + alternate + b_strip

    # data = [mpimg.imread("color-black.png"), mpimg.imread("color-white.png"), mpimg.imread("color-black.png")]
    i1 = np.full((3, 3, 3), (0., 0., 0.))
    i2 = [np.full((3, 3, 3), (0., 0., 0.)), np.full((3, 3, 3), (0., 0., 0.))]
    i3 = np.full((3, 3, 3), (1., 1., 1.))
    black_img2 = np.full((3, 3, 3), (0., 0., 0.))

    b_strip = i1.copy() * 3
    alternate = i2.copy() * 2
    b_strip2 = i1.copy() * 3

    return [b_strip, alternate, b_strip2]


def execute():
    data = mini_data()
    # print(data)
    # sys.exit()
    filtered_imgs = [data[0], data[1]]
    flag_hist = np.zeros(data[0].shape)
    lum_arr1 = rgb2luminanceArr(data[0])
    lum_arr2 = rgb2luminanceArr(data[1])
    flag12 = flagPixels(lum_arr1, lum_arr2)
    recent = flag12
    # print("DATA 0:")
    # print(data[0])
    # print(data[1])

    for img_data in data[2:]:
        lum_arr1 = lum_arr2
        lum_arr2 = rgb2luminanceArr(img_data)
        flag12 = flagPixels(lum_arr1, lum_arr2)
        (flag_hist, recent, imgOut) = sift(
            flag_hist, recent, flag12, img_data, data[0])
        # print("DATA 0:")
        # print(data[0])
        # print(data[1])
        filtered_imgs.append(imgOut)
        # print("IMG OUT:")
        # print(imgOut)

    for fi in filtered_imgs:
        print(fi)


execute()
