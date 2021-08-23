from scipy import io
import numpy as np
import imageio
import matplotlib.pyplot as plt

solutionMat = np.load('solution.npy')

if False:
    plt.imshow(solutionMat)
    plt.show()

voids = np.where(solutionMat!=1)
print(voids[0].size)
randomNumber = 4107;
startingPoint = (voids[0][randomNumber],voids[1][randomNumber])
x0,y0 = (startingPoint[0],startingPoint[1]);
#x0,y0 = (34,90)
x0, y0 = (50,22)
x=x0
y=y0
pathX = [x0]
pathY = [y0]
maxIterations = solutionMat.size;
iteration = 0;

while True:
    #print(iteration)
    currentVoid = solutionMat[x,y]
    d = 1;
    neighbours = [(x - d, y), (x + d, y), (x, y + d), (x, y - d)]

    xmin,ymin,valmin = (x, y, currentVoid)
    for neighbour in neighbours:
        xn, yn = neighbour

        if solutionMat[xn,yn] < valmin:
            xmin = xn
            ymin = yn
            valmin = solutionMat[xn,yn]

    x=xmin
    y=ymin
    pathX.append(x)
    pathY.append(y)

    if currentVoid==0 or iteration==maxIterations:
        break

    iteration+=1

plt.imshow(np.array(imageio.imread('maze3.bmp')))
#plt.imshow(solutionMat)
plt.scatter(pathY,pathX,color='r')
plt.show()

