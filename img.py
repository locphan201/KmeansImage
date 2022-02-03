import matplotlib.pyplot as plt
import numpy, threading
from sklearn.cluster import KMeans

img = plt.imread('3x4.png')
plt.imshow(img)
plt.show()
K = 15
height = img.shape[0]
width = img.shape[1]

img = img.reshape(height * width, 3)
img2 = numpy.zeros_like(img)

kmeans = KMeans(n_clusters=K).fit(img)
labels = kmeans.predict(img)
clusters = kmeans.cluster_centers_

def assign_cluster(index, width):
    start = index*width
    end = (index+1)*width
    for i in range(start, end):
        img2[i] = clusters[labels[i]]

for i in range(height):
    thread = threading.Thread(target=assign_cluster(i, width))

img2 = img2.reshape(height, width, 3)

plt.imshow(img2)
plt.show()