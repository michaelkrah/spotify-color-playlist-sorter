from PIL import Image
import math


def dom_colors(file):
    image = Image.open(file)
    image = image.resize((100, 100), resample=0)
    image = image.convert("RGB")
    pixels = image.getcolors(10000)
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    sorted_pixels = sorted_pixels[::-1]
    return sorted_pixels


def pick_three(pixel_count):
    """ Quick formula to get 3 most common dissimilar colors by comparing the distance of rgb tuples, can change the
        int conditional value for different results
        returns the three most common colors with a count of the number of times the color appears"""
    pixel_list = [pixel_count[0], pixel_count[0], pixel_count[0]]
    color_2 = False
    for i in pixel_count:
        if not color_2 and math.sqrt((i[1][0] - pixel_list[0][1][0]) ** 2 + (i[1][1] - pixel_list[0][1][1]) ** 2
                                     + (i[1][2] - pixel_list[0][1][2]) ** 2) > 40:
            pixel_list[1] = i
            color_2 = True
            continue
        elif (math.sqrt((i[1][0] - pixel_list[0][1][0]) ** 2 + (i[1][1] - pixel_list[0][1][1]) ** 2 + (i[1][2] -
                                                                                    pixel_list[0][1][1]) ** 2) > 40) \
                and (math.sqrt((i[1][0] - pixel_list[1][1][0]) ** 2 + (i[1][1] - pixel_list[1][1][1]) ** 2 +
                               (i[1][2] - pixel_list[1][1][2]) ** 2) > 40):
            pixel_list[2] = i
            break

    return pixel_list


d = dom_colors("nfr.png")
print(d)
e = pick_three(d)

print(e)
