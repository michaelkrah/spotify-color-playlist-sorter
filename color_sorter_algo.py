import colorsys
import math

import requests

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


# From https://www.alanzucconi.com/2015/05/24/how-to-find-the-main-colours-in-an-image/
def dom_colors(file, cluster_number=3):
    image = Image.open(file)
    image = image.resize((100, 100), resample=0)
    image = image.convert("RGB")
    pixels = list(image.getdata())
    cluster = KMeans(n_clusters=cluster_number)
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


def find_hue_lum(color, step, color_threshold):
    threshold_met = False
    for col in color:

        if col[1][2] > 20 and col[1][1] > 15:
            print(col)

            r, g, b = colorsys.hsv_to_rgb(col[1][0]/100, col[1][1]/100, col[1][2]/100)
            lum = math.sqrt(.241 * r + .691 * g + .068 * b )

            h2 = int(col[1][0]/100 * step)
            v2 = int(col[1][2]/100 * step)

            if h2 % 2 == 1:
                v2 = step - v2
                lum = 1 - lum

            if not threshold_met:
                return (h2, lum, v2)
            else:
                return (h2 + step + 2, lum + step + 2, v2 + step + 2)
        else:
            if col[0] > color_threshold:

                threshold_met = True

    return (step + 2, step + 2, step + 2)


def generate_list(album_stack):
    edited_stack = []
    for album in album_stack:
        col = album[1]
        color = find_hue_lum(col, 15, .63)
        edited_stack.append([color, album[0]])
    edited_stack.sort()
    return edited_stack


def color_sort_HSV(tracks, cluster_number, starting_color):
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
            dom_col = dom_colors(file, cluster_number)
        except Exception:
            print("Unable to find colors")
            continue
        print(track.name, dom_col)
        dom_col_hsv = pixel_list_to_hsv(dom_col)
        stack.append([track, dom_col_hsv])

    sorted_list = generate_list(stack)
    for i in sorted_list:
        print(i)

    sorted_list = [x[1] for x in sorted_list]

    return sorted_list
