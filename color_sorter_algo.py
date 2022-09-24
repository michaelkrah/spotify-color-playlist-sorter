import colorsys
import glob
import math

import requests

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


# From https://www.alanzucconi.com/2015/05/24/how-to-find-the-main-colours-in-an-image/
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


def pixel_list_to_hsv(pixel_list):
    lis = []
    for i in range(len(pixel_list)):
        lis.append(list(pixel_list[i]))
        lis[i][1] = colorsys.rgb_to_hsv(pixel_list[i][1][0] / 255, pixel_list[i][1][1] / 255, pixel_list[i][1][2] / 255)
        lis[i][1] = tuple([x * 100 for x in lis[i][1]])
    return lis


def find_hue(color):
    hue = color[0][1][0]
    for c in color:
        if c[1][2] > 16 and c[1][1] > 6:
            hue = c[1][0]
            return hue
    return 1000


def find_hue_lum(color, step):
    for col in color:
        if col[1][2] > 20 and col[1][1] > 6:

            r, g, b = colorsys.hsv_to_rgb(col[1][0]/100, col[1][1]/100, col[1][2]/100)
            lum = math.sqrt(.241 * r + .691 * g + .068 * b )

            h2 = int(col[1][0] * step)
            lum2 = int(lum * step)
            v2 = int(col[1][2] * step)

            return (h2, lum2, v2)

    return (1000, 1000, 1000)


def generate_list(album_stack):
    edited_stack = []
    for album in album_stack:
        col = album[1]
        color = find_hue_lum(col, 8)
        edited_stack.append([color, album[0]])
    edited_stack.sort()
    print(edited_stack)
    return edited_stack


# def main(tracks):
#     stack = []
#
#     for file in glob.glob("albums/*.jpg"):
#         e = dom_colors(file)
#         g = pixel_list_to_hsv(e)
#         stack.append([file, g])
#
#     h = generate_list(stack)
#
#     for album in h:
#         print(album)


def color_sort_HSV(tracks):
    """Takes a list of track objects as input, sorts them by HSV value, and returns the sorted list"""
    stack = []
    for track in tracks:
        try:
            URL = track.image[0]['url']
        except IndexError:
            print("No URL found")
            continue
        print(URL)
        file = requests.get(URL, stream=True).raw
        try:
            dom_col = dom_colors(file)
        except Exception:
            print("Unable to find colors")
            continue
        print(track.name, dom_col)
        dom_col_hsv = pixel_list_to_hsv(dom_col)
        stack.append([track, dom_col_hsv])

    sorted_list = generate_list(stack)

    stack_2 = []
    for item in sorted_list:
        stack_2.append(item[1])

    return stack_2
