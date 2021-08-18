import imageio
import matplotlib.pyplot as plt
import numpy as np

imagePath = 'maze.bmp'
imageData = np.array(imageio.imread(imagePath))

imageData = np.round(imageData/(np.max(imageData)))

print(imageData)

plt.imshow(imageData)
plt.show();