import numpy as np

FRAME_CONST = 60


# converts rgb tuples into luminance value


def rgb2luminance(rgbTup):
    greyscale = (0.2126*rgbTup[0] + 0.7152 * rgbTup[1] +
                 0.0722 * rgbTup[2])  # NTSC formula
    return 413.435*pow((0.002746*greyscale+0.0189623), 22)


# converts 2x2 array of rgb tuples into 2x2 array of luminance. nx is number of pixels in x direction and
# ny is number of pixels in y direction
def rgb2luminanceArr(rgbArr):
    return [[rgb2luminance(j) for j in i] for i in rgbArr]


# returns l2 if luminosity difference between l1 and l2 is harmful and 0 otherwise where l1 and l2 are pixel luminosity
def filterHarmful(l1, l2):
    if ((abs(l2-l1) > 20) and min((l1, l2)) < 160):
        return l2
    return 0


# l2 is pixel's current luminosity and l1 is pixel's previous luminosity in previous fram
# returns 1 if change is very bright, -1 if change is too dark and 0 if no significant change
def flagChange(l1, l2):
    if (l2-l1 > 0) and (l1 < 160):
        return 1
    elif (l1 - l2 > 0) and (l2 < 160):
        return -1
    return 0


# returns array representing changes between two frames
def flagPixels(lum_old, lum_curr):
    flagged = np.zeros(lum_old.shape())
    for i in range(lum_old.length):
        for j in range(lum_old[0].length):
            # if (filterHarmful(lum_old[i][j], lum_curr[i][j]) != 0):
            flagged[i][j] = flagChange(lum_old[i][j], lum_curr[i][j])
    return flagged

# updates values of flag history and recent flag:
# recent flag is a matrix that represents the most recent change
# flag_history stores the


def sift(flag_history, most_recent_flag, curr_flag, img):
    rf = most_recent_flag
    fh = flag_history
    for i in range(most_recent_flag.shape):
        for j in range(most_recent_flag[0].length):
            if curr_flag[i][j] * most_recent_flag[i][j] == -1:  # either 1 and -1 or -1 and 1
                # need to filter
                rf[i][j] = curr_flag[i][j]
                img[i][j] = filter(img[i][j])
                flag_history[i][j] = 0
            elif curr_flag[i][j] == most_recent_flag[i][j]:  # either 1 and 1 or -1 and -1
                # current change equal to most recent change
                flag_history[i][j] = 0
            # either 0 and 1 or 0 and -1
            elif curr_flag[i][i] == 1 or curr_flag[i][i] == -1:
                flag_history[i][j] = 0
                rf[i][j] = curr_flag[i][j]
            elif flag_history[i][j] < FRAME_CONST:  # either 1 and 0 or -1 and 0
                # increment most recent change
                flag_history[i][j] = flag_history[i][j] + 1
            else:  # most recent change was > 1 second ago
                most_recent_flag[i][j] = 0
                flag_history[i][j] = 0

    return (fh, rf, img)


def filter(pix):
    return (0, 0, 0)
