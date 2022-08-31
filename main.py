from PIL import Image
import math
import numpy as np
import glob


def dom_colors(file):
    image = Image.open(file)
    image = image.resize((100, 100), resample=0)
    image = image.convert("RGB")
    pixels = image.getcolors(10000)
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    sorted_pixels = sorted_pixels[::-1]
    image.close()
    return sorted_pixels


def pick_three(pixel_count):
    """ Quick formula to get 3 most common dissimilar colors by comparing the distance of rgb tuples, can change the
        int conditional value for different results
        returns the three most common colors with a count of the number of times the color appears"""
    pixel_list = [list(pixel_count[0]), list(pixel_count[0]), list(pixel_count[0])]
    color_2 = False
    for i in pixel_count:
        if not color_2 and math.sqrt((i[1][0] - pixel_list[0][1][0]) ** 2 + (i[1][1] - pixel_list[0][1][1]) ** 2
                                     + (i[1][2] - pixel_list[0][1][2]) ** 2) > 40:
            pixel_list[1] = list(i)
            color_2 = True
            continue
        elif (math.sqrt((i[1][0] - pixel_list[0][1][0]) ** 2 + (i[1][1] - pixel_list[0][1][1]) ** 2 + (i[1][2] -
                                                                                                       pixel_list[0][1][
                                                                                                           1]) ** 2) > 40) \
                and (math.sqrt((i[1][0] - pixel_list[1][1][0]) ** 2 + (i[1][1] - pixel_list[1][1][1]) ** 2 +
                               (i[1][2] - pixel_list[1][1][2]) ** 2) > 40):
            pixel_list[2] = list(i)
            break

    return pixel_list


def pixel_list_to_lab(pixel_list):
    for i in range(3):
        pixel_list[i][1] = rgb_to_lab(pixel_list[i][1])

    # turns num of pixels into proportion out of 100
    total_pixels = pixel_list[0][0] + pixel_list[1][0] + pixel_list[2][0]
    for i in range(3):
        pixel_list[i][0] = round(pixel_list[i][0] / total_pixels, 5)

    return pixel_list


def rgb_to_lab(rgb_val):
    """ changes an rgb value to LAB value
        equations from http://www.brucelindbloom.com/index.html?
    """
    # rgb to xyz
    rgb = [0, 0, 0]
    for i in range(3):
        val = rgb_val[i]
        val = val / 255
        val = val / 12.92 if val <= 0.04045 else ((val + 0.055) / 1.055) ** 2.4
        rgb[i] = val
    rgb = np.array([[rgb[0]], [rgb[1]], [rgb[2]]])
    matrix = np.array(
        [[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = matrix @ rgb
    xyz = (xyz[0][0] * 100, xyz[1][0] * 100, xyz[2][0] * 100)
    # xyz to LAB
    xr = xyz[0] / 95.042
    xy = xyz[1] / 100
    xz = xyz[2] / 108.883
    fx = xr ** 0.333 if xr > 0.008856 else (903.3 * xr + 16) / 116
    fy = xy ** 0.333 if xy > 0.008856 else (903.3 * xr + 16) / 116
    fz = xz ** 0.333 if xz > 0.008856 else (903.3 * xr + 16) / 116
    LAB = (round(116 * fy - 16, 5), round(500 * (fx - fy), 5), round(200 * (fy - fz), 5))
    return LAB


def color_difference(col_1, col_2):
    """ Takes LAB value of two colors and calculates the Delta E value of a color to determine their similarity
    """
    delta = math.sqrt((col_2[0] - col_1[0]) ** 2 + (col_2[1] - col_1[1]) ** 2 + (col_2[2] - col_2[1]) ** 2)
    return delta


def picture_similarity(pixel_list1, pixel_list2):
    """ Comes up with a final number that determines how similar two pictures are """
    num = 0
    avg = [0, 0, 0]
    for i in range(3):
        for j in range(3):
            dif = color_difference(pixel_list1[i][1], pixel_list2[j][1])
            dif = 100 - dif
            dif = dif * pixel_list2[j][0]
            num += dif
        avg[i] = num * pixel_list1[i][0]
        num = 0

    total = sum(avg) / 3

    if total > 100:
        return 100
    else:
        return total


def generate_closest(pixel_list, album_stack):
    """ begins with a pixel list or color and returns the image in the list closest to it"""



stack = []


for file in glob.glob("albums/*.jpg"):
    e = dom_colors(file)
    f = pick_three(e)
    g = pixel_list_to_lab(f)
    stack.append([file, g])
    print(g)

print(stack)

h = picture_similarity([[0.98554, (87.39895, -6.61733, -2.27064)], [0.0099, (52.4075, 75.88192, 65.87016)], [0.00457, (94.7198, 3.20161, 10.90068)]], [[0.98137, (10.31327, -0.01793, -14.12088)], [0.00932, (12.06724, 15.04278, 1.47008)], [0.00932, (19.12136, 38.2731, 11.21667)]])
print(h)
