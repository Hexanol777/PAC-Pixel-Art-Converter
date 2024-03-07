import math
import json

data = {
    'Width': [1098, 1200, 1000, 3999, 1889, 3612, 1000, 1893, 1280, 1421, 1280, 1024, 973, 1750, 2194, 3334, 3334, 1700, 1920, 1280, 2000, 2500, 3508, 1920, 1000, 1640, 1679, 1200, 2500, 2000, 6000, 2327, 1000, 2048, 3857, 2000, 1920, 1414, 1980, 3840, 1059, 600, 1788, 2048, 3627, 4000, 1277, 1295, 2048, 2160, 2480, 1300, 3297, 4800, 1500, 1273, 1920, 1053, 2269, 1000, 1920, 2500, 1920, 1000, 1920, 1600, 1200, 1920, 346, 3000, 2411, 3584, 2916, 4096, 1440, 1920, 1722, 1440, 2319, 2150, 2150, 719],
    'Height': [822, 900, 800, 3199, 1063, 2551, 1465, 1287, 993, 3137, 816, 935, 700, 1080, 2194, 2193, 2193, 1202, 1160, 640, 1125, 1001, 2339, 1080, 1493, 1000, 1000, 899, 1080, 1157, 3000, 1342, 663, 983, 2000, 1091, 1080, 2000, 1320, 2160, 1500, 1091, 1035, 1294, 5440, 6000, 2048, 1800, 1518, 3840, 3508, 1950, 1984, 2800, 1896, 1800, 1080, 1500, 3052, 521, 1200, 3536, 1200, 750, 1200, 1095, 847, 499, 291, 4385, 4000, 5376, 4096, 3003, 2048, 2880, 2435, 2160, 3656, 3035, 3035, 798],
    'Aspect_Ratio': [1.335766423, 1.333333333, 1.25, 1.250078149, 1.777046096, 1.415915327, 0.682593857, 1.470862471, 1.289023162, 0.452980555, 1.568627451, 1.095187166, 1.39, 1.62037037, 1.0, 1.520291838, 1.520291838, 1.414309484, 1.655172414, 2.0, 1.777777778, 2.497502498, 1.499786233, 1.777777778, 0.669792364, 1.64, 1.679, 1.334816463, 2.314814815, 1.72860847, 2.0, 1.733979136, 1.508295626, 2.083418108, 1.9285, 1.833180568, 1.777777778, 0.707, 1.5, 1.777777778, 0.706, 0.54995417, 1.727536232, 1.582689335, 0.666727941, 0.666666667, 0.623535156, 0.719444444, 1.34914361, 0.5625, 0.70695553, 0.666666667, 1.661794355, 1.714285714, 0.791139241, 0.707222222, 1.777777778, 0.702, 0.74344692, 1.919385797, 1.6, 0.707013575, 1.6, 1.333333333, 1.6, 1.461187215, 1.416765053, 3.847695391, 1.189003436, 0.684150513, 0.60275, 0.666666667, 0.711914063, 1.363969364, 0.703125, 0.666666667, 0.707186858, 0.666666667, 0.634299781, 0.708401977, 0.708401977, 0.901002506],
    'Pixel_Size': [2, 3, 3, 4, 2, 5, 5, 5, 2, 5, 2, 2, 2, 2, 5, 5, 8, 4, 1, 2, 3, 2, 6, 3, 3, 3, 3, 2, 3, 2, 4, 3, 2, 2, 3, 4, 3, 3, 3, 3, 5, 3, 2, 3, 8, 6, 3, 5, 4, 5, 6, 3, 5, 7, 3, 4, 3, 3, 5, 1, 3, 6, 1, 3, 2, 2, 4, 2, 1, 9, 8, 10, 5, 5, 4, 4, 10, 4, 6, 4, 6, 3],
    'Colors': [768, 764, 757, 724, 768, 768, 717, 719, 752, 661, 766, 768, 762, 768, 744, 616, 616, 768, 678, 768, 768, 729, 765, 728, 748, 564, 757, 768, 768, 691, 762, 718, 762, 767, 768, 768, 733, 768, 768, 750, 756, 692, 766, 757, 768, 764, 765, 768, 768, 768, 750, 689, 761, 720, 768, 751, 743, 754, 768, 765, 768, 756, 768, 645, 768, 663, 768, 357, 768, 768, 687, 729, 768, 768, 763, 754, 768, 768, 754, 768, 768, 749],
    'Color_Palette': [20, 16, 20, 25, 19, 25, 30, 25, 25, 21, 16, 23, 18, 12, 16, 25, 28, 24, 50, 17, 22, 25, 20, 25, 19, 24, 16, 21, 18, 22, 29, 25, 19, 18, 23, 26, 24, 24, 35, 30, 25, 30, 16, 30, 20, 28, 25, 25, 25, 25, 20, 25, 20, 25, 30, 22, 30, 30, 23, 25, 30, 25, 30, 25, 30, 20, 25, 16, 25, 30, 25, 22, 22, 22, 30, 30, 20, 25, 30, 25, 35, 25],
    'Brightness': [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 85, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    'Sharpness': [10, 10, 10, 10, 10, 10, 12, 10, 10, 12, 10, 10, 10, 10, 10, 12, 20, 12, 11, 10, 12, 10, 13, 10, 12, 11, 10, 11, 15, 15, 9, 10, 15, 10, 10, 12, 10, 11, 15, 14, 14, 15, 15, 15, 12, 10, 15, 12, 12, 15, 11, 10, 12, 15, 12, 16, 16, 15, 12, 14, 13, 12, 13, 12, 14, 14, 12, 14, 12, 15, 16, 16, 15, 15, 15, 12, 15, 20, 20, 15, 20, 10],
    'Vibrance': [100, 100, 100, 100, 150, 120, 140, 100, 100, 120, 180, 100, 100, 110, 100, 125, 125, 100, 100, 100, 100, 100, 120, 100, 100, 100, 100, 100, 100, 120, 120, 170, 140, 140, 140, 150, 130, 100, 130, 130, 120, 100, 140, 121, 160, 120, 130, 120, 140, 100, 130, 120, 120, 150, 100, 125, 110, 100, 120, 140, 110, 170, 120, 150, 121, 110, 130, 130, 100, 120, 120, 149, 130, 120, 120, 125, 107, 120, 125, 140, 130, 100]
}


def euclidean_distance(point1, point2):
    return math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)))

def find_closest_pixelsize(width, height):
    closest_distance = float('inf')
    closest_pixel_size = None
    closest_sharpness = None
    
    for i in range(len(data['Width'])):
        w = data['Width'][i]
        h = data['Height'][i]
        aspect_ratio = w / h
        pixel_size = data['Pixel_Size'][i]
        sharpness = data['Sharpness'][i]
        
        current_distance = euclidean_distance([width, height, aspect_ratio], [w, h, w/h])
        
        if current_distance < closest_distance:
            closest_distance = current_distance
            closest_pixel_size = pixel_size
            closest_sharpness = sharpness
    print(closest_pixel_size, closest_sharpness)
    return closest_pixel_size, closest_sharpness

def count_colors(image):
    image = image.convert('RGB')
    hist = image.histogram()
    num_colors = sum(1 for count in hist if count != 0)
    return num_colors


def find_closest_color_palette(image):
    closest_distance = float('inf')
    closest_brightness = None
    closest_vibrance = None
    closest_palette = None

    image = image.convert('RGB')
    hist = image.histogram()
    num_colors = sum(1 for count in hist if count != 0)

    for i in range(len(data['Colors'])):
        colors = data['Colors'][i]
        brightness = data['Brightness'][i]
        vibrance = data['Vibrance'][i]
        color_palette = data['Color_Palette'][i]
        
        current_distance = abs(num_colors - colors)
        
        if current_distance < closest_distance:
            closest_distance = current_distance
            closest_brightness = brightness
            closest_vibrance = vibrance
            closest_palette = color_palette
    
    return closest_brightness, closest_vibrance, closest_palette
