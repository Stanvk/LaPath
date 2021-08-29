# -*- coding: utf-8 -*-

import numpy as np
import imageio
import matplotlib.pyplot as plt
from mpmath import mp
mp.dps = 70

def xy2i(x,y,l):
    #return y*l+x
    return (y-1)*l+(x-1)

def i2xy(i,l):
    #return divmod(i,l)[::-1]
    return divmod(i,l)[1]+1,divmod(i,l)[0]+1

## READ-IN MAZE
#imagePath = 'maze2.bmp'
imagePath = 'maze3.bmp'
imageData = np.array(imageio.imread(imagePath))
imageData = np.round(imageData/(np.max(imageData)))

maze=1-imageData

#set open points to 0.5
maze = -1.5*maze+0.5

maze=np.pad(maze,1,mode='constant',constant_values=1)

#set exit point
#maze[7,3]=0
#maze[210,0]=0;
maze[70:77,100]=0;

plt.figure()
plt.imshow(maze)
plt.show()

##SET-UP SYSTEM MATRIX

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
            
            neighbours=[(x-1,y),(x,y+1),(x+1,y),(x,y-1)]
            for i_neighbour in range(0,4):
                xn,yn=neighbours[i_neighbour]
                inn=xy2i(xn,yn,lx)
                if maze[xn,yn]==0.5:
                    systemMatrix[i,inn]+=1
                else:
                    if maze[xn,yn]==-1: #neumann boundary
                        i_neumann=i_neighbour%3
                        xn_neu,yn_neu=neighbours[i_neumann]
                        inn_neu=xy2i(xn_neu,yn_neu,lx)
                        if maze[xn_neu,yn_neu]==0.5:
                            #systemMatrix[i,inn_neu]+=1 #mirror in node
                            systemMatrix[i,i]+=1 #mirror in edge
                        else:
                            systemMatrix[i,i]+=1 #path is 1 pixel wide
                    else: #dirichlet boundary
                        systemRHS[i]-=maze[xn,yn]
        else:
            systemMatrix[i,i]=1
            systemRHS[i]=maze[x,y]

print('linear system defined')

##SOLVE
# solutionVec=np.linalg.inv(systemMatrix).dot(systemRHS)
solutionVec = np.linalg.solve(systemMatrix, systemRHS);
# solutionVec = sp.solve(systemMatrix, systemRHS)
# solutionVec = mp.lu_solve(systemMatrix,systemRHS);

solutionMat=np.copy(maze)
for i in range(0,solutionVec.shape[0]):
    x,y=i2xy(i,lx)
    solutionMat[x,y]=solutionVec[i]

##SAVE AND SHOW
np.save('solution.npy', solutionMat);

plt.figure()
plt.imshow(solutionMat)
plt.show()

    
if False:
    from scipy import io
    io.savemat('systemMatrix.mat', {'matrix': systemMatrix})
    io.savemat('systemRHS.mat', {'rhs': systemRHS})