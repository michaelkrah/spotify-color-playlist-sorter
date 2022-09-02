from PIL import Image
import math
from sklearn.cluster import KMeans
import numpy as np
import colorsys
import glob


def dom_colors(file):
    image = Image.open(file)
    image = image.resize((100, 100), resample=0)
    image = image.convert("RGB")
    pixels = list(image.getdata())
    cluster = KMeans(n_clusters=3)
    cluster.fit(pixels)
    hist = centroid_histogram(cluster)
    zipped = list(zip(hist, cluster.cluster_centers_))
    zipped.sort(reverse=True, key=lambda x: x[0])
    return zipped


def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist


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

    return total


def generate_closest(pixel_list, album_stack):
    """ begins with a pixel list or color and returns the image in the list closest to it"""

    stack_albums = []

    for album in album_stack:
        sim = picture_similarity(pixel_list, album[1])
        album_info = [sim, album]
        stack_albums.append(album_info)

    stack_albums.sort()
    return stack_albums


def generate_list(pixel_list, album_stack):
    """Parent function for generate closest, prints the albums in descending order based on a starting album"""

    while len(album_stack) != 0:
        closest_list = generate_closest(pixel_list, album_stack)
        album = closest_list.pop()
        print(album)
        pixel_list = album[1][1]

        album_stack.remove(album[1])

    return True


def pixel_list_to_hsv(pixel_list):
    lis = [[pixel_list[0][0], 0], [pixel_list[1][0], 0], [pixel_list[1][0], 0]]
    for i in range(3):
        lis[i][1] = colorsys.rgb_to_hsv(pixel_list[i][1][0]/255, pixel_list[i][1][1]/255, pixel_list[i][1][2]/255)
        lis[i][1] = tuple([x * 100 for x in lis[i][1]])
    return lis


def find_hue(color):
    hue = color[0][1][0]
    for c in color:
        if c[1][2] > 15 and c[1][1] > 6:
            hue = c[1][0]
            return hue
    return 0


def generate_list_2(album_stack):
    edited_stack = []
    for album in album_stack:
        col = album[1]
        color = find_hue(col)
        edited_stack.append([color, album])
    edited_stack.sort()
    return edited_stack


stack = []


for file in glob.glob("albums/*.jpg"):
     e = dom_colors(file)

     g = pixel_list_to_hsv(e)
     stack.append([file, g])


h = generate_list_2(stack)

for album in h:
    print(album)