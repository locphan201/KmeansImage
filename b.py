import matplotlib.pyplot as plt
import numpy

img = plt.imread('3x4.png')
height = img.shape[0]
width = img.shape[1]
img = img.reshape(height * width, 3)

def sharp(i):
    result = img[i]
    for j in range(3):
        result[j] = round(result[j], 2)
    return result

def brighter(i, level):
    result = img[i]
    for j in range(3):
        newColor = result[j] + level/255
        if newColor > 1:
            newColor = 1
        result[j] = newColor
    return result

def darker(i, level):
    result = img[i]
    for j in range(3):
        newColor = result[j] - level/255
        if newColor < 0:
            newColor = 0
        result[j] = newColor
    return result

for i in range(height*width):
    img[i] = brighter(i, 100)

img = img.reshape(height, width, 3)
plt.imshow(img)
plt.show()