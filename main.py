# -*- coding: utf-8 -*-

import numpy as np

maze = np.array([[1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1]])

#set open points to 0.5
maze = 0.5*(maze+1)

#set exit point
maze[7,3]=0

#setup linear system
for x in range(0,maze.shape[0]):
    for y in range(0,maze.shape[1]):
        print((x,y))
     
