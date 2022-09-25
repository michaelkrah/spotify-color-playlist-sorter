import colorsys
import math
import requests
from PIL import Image
from sklearn.cluster import KMeans
from collections import Counter


def dom_colors(file, cluster_number: int):
    """
    Obtains an image's most dominant colors using K-means clustering

    :param file: Image file
    :param cluster_number: Number of clusters used for K-means algorithm
    :rType: list
    :return: list of tuples displaying a color's frequency and the colors rgb value
    """

    image = Image.open(file)
    image = image.resize((100, 100))
    image = image.convert("RGB")
    pixels = list(image.getdata())
    cluster = KMeans(n_clusters=cluster_number)
    cluster.fit(pixels)
    total_cluster = Counter(cluster.labels_).most_common()

    total_cluster.sort()
    num_pixels = sum([x[1] for x in total_cluster])
    total_cluster = [x[1]/num_pixels for x in total_cluster]

    zip_colors = list(zip(total_cluster, cluster.cluster_centers_))

    zip_colors.sort(reverse=True, key=lambda x: x[0])

    return zip_colors


def pixel_list_to_hsv(pixel_list):
    """
    Converts a list of rgb value to hsv values
    """
    lis = []
    for i in range(len(pixel_list)):
        lis.append(list(pixel_list[i]))
        lis[i][1] = colorsys.rgb_to_hsv(pixel_list[i][1][0] / 255, pixel_list[i][1][1] / 255, pixel_list[i][1][2] / 255)
        lis[i][1] = tuple([x * 100 for x in lis[i][1]])
    return lis


def find_hue_lum(color, step, color_frequency_threshold, starting_color):
    """
    Iterates through a list of colors sorted by frequency and returns one based on several given parameters
    What color is returned is based on how visible the hue is, so colors close to black, grey, and white will be skipped
    Uses principles to step sorting https://www.alanzucconi.com/2015/09/30/colour-sorting/
    If a distinct color within the parameters given cannot be found, the function will return a tuple that will be larger
    than any valid color

    :param color: A list of tuples where the first entry in the tuple is a number between 0 and 1 that represents a color's
    frequency and the second entry is a color in the HSV color space
    :type color: list
    :param step: An integer that represents how many "portions" to split the hue value into when dividing up colors
    :type step: int
    :param color_frequency_threshold: Upper bound for what frequency of a non-distinct color is allowed, higher upper bound means that there
    will have to be more of a non-distinct color for the function to not return a color.
    :type color_frequency_threshold: float
    :param starting_color: HSV color value that will determine what hue is considered the "lowest"
    :type starting_color: tuple
    """

    threshold_met = False
    for col in color:

        if (col[1][2] > 16 and col[1][1] > 15) or (col[1][1] > 7 and col[1][2] > 60):
            r, g, b = colorsys.hsv_to_rgb(col[1][0]/100, col[1][1]/100, col[1][2]/100)
            lum = round(math.sqrt(.241 * r + .691 * g + .068 * b), 3)

            hue_adjusted = col[1][0]/100
            hue_adjusted = (1 + hue_adjusted - starting_color[0]) % 1

            h2 = int(hue_adjusted * step)
            v2 = int(col[1][2]/100 * step)

            if h2 % 2 == 1:
                v2 = step - v2
                lum = 1 - lum

            if not threshold_met:
                return (h2, lum, v2)
            else:
                return (h2 + step + 2, lum + step + 2, v2 + step + 2)
        else:
            if col[0] > color_frequency_threshold: # TODO change this so that it is the sum of the frequency of all previously tested colors (will fix when albums are half black, half white with small color
                threshold_met = True

    return (step + 2, step + 2, step + 2)


def generate_list_hsv(album_stack, step, threshold, starting_color):
    """
    Takes a list of albums and given parameters and returns the stack sorted by hsv color
    Color sorting uses step sorting principles https://www.alanzucconi.com/2015/09/30/colour-sorting/

    :param album_stack: List made of albums and the dominant colors within them
    :type album_stack: list
    :param step: Number of sections hue value is broken into before luminosity is considered
    :type step: int
    :param threshold: Upper bound of frequency of a non-distinct color needed for an album cover to be excluded from being sorted
    :type threshold: float
    :param starting_color: HSV of the given starting color
    :type starting_color: tuple
    """
    edited_stack = []
    for album in album_stack:
        col = album[1]
        color = find_hue_lum(col, step, threshold, starting_color)
        edited_stack.append([color, album[0]])
    edited_stack.sort()
    return edited_stack


def color_sort_hsv(tracks, cluster_number, starting_color):
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
        print(track.name)
        dom_col_hsv = pixel_list_to_hsv(dom_col)
        stack.append([track, dom_col_hsv])

    starting_color_hsv = colorsys.rgb_to_hsv(starting_color[0], starting_color[1], starting_color[2])

    sorted_list = generate_list_hsv(stack, 25, .67, starting_color_hsv)

    sorted_list = [x[1] for x in sorted_list]

    return sorted_list


def pull_color_rgb(tracks, cluster_number, color, HSV_range):
    """TODO"""