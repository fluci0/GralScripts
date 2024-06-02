#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 19:54:30 2024
Title: Script to obtain a points sequence free of obstacles, this is not RRT
"""

import numpy as np
import matplotlib.pyplot as plt
import random as rd
import cv2
import glob
import math as mt
import matplotlib as mpl

#List with maps
maps_set = glob.glob('*.jpg')

#Parameters:
#q_s = [26, 18]
q_s = [10, 10]
q_g = [42, 40.5]
n = 100
max_distancep = 25

q_gx = q_g[0]
q_gy = q_g[1]
q_sx = q_s[0]
q_sy = q_s[1]

#Plot parameters:
alp = 0.3
font = {'family': 'sans-serif', 'color': 'black','weight': 'bold', 'size': 12}
size = 10
marker_size = 200

for i in maps_set:
    map_i = cv2.imread(i)
    map_i = cv2.cvtColor(map_i, cv2.COLOR_BGR2GRAY)
    map_i = np.where(map_i > 250, 255, map_i)
    map_i = np.where(map_i < 250, 0, map_i)

#Position of shapes
obs_index = np.argwhere(map_i <= 10)
obs_position = obs_index + 0.5

q_rx_set = [q_sx]
q_ry_set = [q_sy]


for j in range(n):
    #print('j:', j)
    q_rx_ini = rd.uniform(0, len(map_i)) #Initial points
    q_ry_ini = rd.uniform(0, len(map_i))
    theta = mt.atan2((q_ry_set[j] - q_ry_ini), (q_rx_ini - q_rx_set[j]))
    thetaDg = (theta * 180) / mt.pi
    max_d = rd.uniform(0, max_distancep)
    q_rx = q_rx_set[j] + max_d * mt.cos(theta) #Real point to test
    q_ry = q_ry_set[j] - max_d * mt.sin(theta)
    
    restart = True
    while restart:
    
        for k in range(len(obs_position)):
            #print('k:', k)
            d_obs = mt.dist(obs_position[k], [q_ry_set[j], q_rx_set[j]]) #Distance from the obstacle to the previous valid point
            alfa = mt.atan2((q_ry_set[j] - obs_position[k][0]), (obs_position[k][1] - q_rx_set[j]))
            alfaDg = (alfa * 180) / mt.pi
            if max_d >= d_obs - 0.8 and thetaDg <= alfaDg + 40 and thetaDg >= alfaDg - 40:
                #print('coincidence')
                #print('q_ry collision=', q_ry)
                #print('q_rx collision=', q_rx)
                q_rx_ini = rd.uniform(0, len(map_i))
                q_ry_ini = rd.uniform(0, len(map_i))
                theta = mt.atan2((q_ry_set[j] - q_ry_ini), (q_rx_ini - q_rx_set[j]))
                thetaDg = (theta * 180) / mt.pi
                max_d = rd.uniform(0, max_d)
                q_rx = q_rx_set[j] + max_d * mt.cos(theta)
                q_ry = q_ry_set[j] - max_d * mt.sin(theta)
                restart = True
                break

            restart = False
    q_rx_set.append(q_rx)
    q_ry_set.append(q_ry)

        
print('q_ry_set', q_ry_set)
print('q_rx_set', q_rx_set)


#Plot
fig1 = plt.figure(figsize = [size, size])
ax = fig1.add_subplot(111)
ax.set_title('Sequence of points avoiding Obstacle Collision - This is not RRT \nFor teaching purposes', fontdict = font)
ax.set_xlabel('x', fontdict = font)
ax.set_ylabel('y', fontdict = font)
ax.scatter(q_sx, q_sy, label =' Start', c = 'g', alpha = alp)
ax.scatter(q_gx, q_gy, label = 'Goal', c = 'r', alpha = alp)
ax.legend()
plt.gca().invert_yaxis()
cmap = mpl.colors.ListedColormap(['k', 'w'])
plt.pcolormesh(map_i, vmax = 255.0, cmap = cmap)
plt.grid(color = 'darkcyan', linestyle = '--', linewidth = 1)
plt.scatter(q_sx, q_sy, s = marker_size, c = 'g', alpha = alp) 
plt.scatter(q_gx, q_gy, s = marker_size, c = 'r', alpha = alp)          
        
for k in range(len(q_rx_set) - 1):
    #Initial random point
    plt.scatter(q_rx_set[k + 1], q_ry_set[k + 1], s = marker_size, c = 'y', alpha = alp)
    plt.plot([q_rx_set[k], q_rx_set[k + 1]], [q_ry_set[k], q_ry_set[k + 1]])
    plt.pause(0.2)
