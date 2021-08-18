# -*- coding: utf-8 -*-

import numpy as np
import imageio
import matplotlib.pyplot as plt

def xy2i(x,y,l):
    #return y*l+x
    return (y-1)*l+(x-1)

def i2xy(i,l):
    #return divmod(i,l)[::-1]
    return divmod(i,l)[1]+1,divmod(i,l)[0]+1

#maze = np.array([[1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1]])
#maze[5,3]=1

#imagePath = 'maze.bmp'
#imagePath = 'maze2.bmp'
imagePath = 'maze3.bmp'
imageData = np.array(imageio.imread(imagePath))
imageData = np.round(imageData/(np.max(imageData)))

maze=np.pad(1-imageData,1,mode='constant',constant_values=1)

#set open points to 0.5
maze = 0.5*(maze+1)

#set exit point
#maze[7,3]=0
#maze[210,0]=0;
maze[74:80,100]=0;

#initialize system matrix
lx=maze.shape[0]-2
ly=maze.shape[1]-2
systemMatrix=np.zeros((lx*ly,lx*ly))
systemRHS=np.zeros(lx*ly)

#setup linear system
for y in range(1,maze.shape[1]-1):
    for x in range(1,maze.shape[0]-1):
        i=xy2i(x,y,lx)
        
        if maze[x,y]==0.5:
            systemMatrix[i,i]=-4
            
            neighbours=[(x-1,y),(x+1,y),(x,y+1),(x,y-1)]
            for neighbour in neighbours:
                xn,yn=neighbour
                inn=xy2i(xn,yn,lx)
                if maze[xn,yn]==0.5:
                    systemMatrix[i,inn]=1
                else:
                    systemRHS[i]-=maze[xn,yn]
        else:
            systemMatrix[i,i]=1
            systemRHS[i]=maze[x,y]
        
        #print((x,y,i))
        #print(i2xy(i,lx))

print('linear system defined')
        
solutionVec=np.linalg.inv(systemMatrix).dot(systemRHS)
solutionMat=np.copy(maze)
for i in range(0,solutionVec.shape[0]):
    x,y=i2xy(i,lx)
    solutionMat[x,y]=solutionVec[i]

plt.imshow(imageData)
    
if False:
    from scipy import io
    io.savemat('systemMatrix.mat', {'mydata': systemMatrix})
    io.savemat('systemRHS.mat', {'mydata': systemRHS})
    
