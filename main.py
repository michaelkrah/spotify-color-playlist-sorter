import color_sorter_algo












# from PIL import Image
# from sklearn.cluster import KMeans
# import numpy as np
# import colorsys
# import glob
#
#
# # From https://www.alanzucconi.com/2015/05/24/how-to-find-the-main-colours-in-an-image/
# def dom_colors(file):
#     image = Image.open(file)
#     image = image.resize((100, 100), resample=0)
#     image = image.convert("RGB")
#     pixels = list(image.getdata())
#     cluster = KMeans(n_clusters=3)
#     cluster.fit(pixels)
#     hist = centroid_histogram(cluster)
#     zipped = list(zip(hist, cluster.cluster_centers_))
#     zipped.sort(reverse=True, key=lambda x: x[0])
#     return zipped
#
#
# def centroid_histogram(clt):
#     # grab the number of different clusters and create a histogram
#     # based on the number of pixels assigned to each cluster
#     numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
#     (hist, _) = np.histogram(clt.labels_, bins=numLabels)
#
#     # normalize the histogram, such that it sums to one
#     hist = hist.astype("float")
#     hist /= hist.sum()
#
#     # return the histogram
#     return hist
#
#
# def pixel_list_to_hsv(pixel_list):
#     lis = [[pixel_list[0][0], 0], [pixel_list[1][0], 0], [pixel_list[1][0], 0]]
#     for i in range(3):
#         lis[i][1] = colorsys.rgb_to_hsv(pixel_list[i][1][0]/255, pixel_list[i][1][1]/255, pixel_list[i][1][2]/255)
#         lis[i][1] = tuple([x * 100 for x in lis[i][1]])
#     return lis
#
#
# def find_hue(color):
#     hue = color[0][1][0]
#     for c in color:
#         if c[1][2] > 15 and c[1][1] > 6:
#             hue = c[1][0]
#             return hue
#     return 0
#
#
# def generate_list(album_stack):
#     edited_stack = []
#     for album in album_stack:
#         col = album[1]
#         color = find_hue(col)
#         edited_stack.append([color, album])
#     edited_stack.sort()
#     return edited_stack
#
#
# stack = []
#
#
# for file in glob.glob("albums/*.jpg"):
#     e = dom_colors(file)
#     g = pixel_list_to_hsv(e)
#     stack.append([file, g])
#
#
# h = generate_list(stack)
#
# for album in h:
#     print(album)
