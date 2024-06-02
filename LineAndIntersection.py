#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 19:37:47 2024
Title: Script to identify if a line is touching a shape
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
q_s = [26, 18]
q_g = [42, 40.5]
n = 1
max_distancep = 5

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

q_rx_ini_set = []
q_ry_ini_set = []
q_rx_set = []
q_ry_set = []

for j in range(n):
    q_rx_ini = rd.uniform(0, len(map_i))
    q_ry_ini = rd.uniform(0, len(map_i))
    theta = mt.atan2((q_sy - q_ry_ini), (q_rx_ini - q_sx))
    thetaDg = (theta * 180) / mt.pi
    print('thetaDg =', thetaDg)
    #Varying the max distance
    max_distance = rd.uniform(0, max_distancep)
    print('max_distance =', max_distance)
    #Placing one point in the line that connects both points
    q_rx = q_sx + max_distance * mt.cos(theta)
    q_ry = q_sy - max_distance * mt.sin(theta)
    q_rx_ini_set.append(q_rx_ini)
    q_ry_ini_set.append(q_ry_ini)
    q_rx_set.append(q_rx)
    q_ry_set.append(q_ry)
    
    #Euclidean distance
    for k in range(len(obs_position)):
        eu_dist = mt.dist(obs_position[k], [q_ry, q_rx])
        #eu_angle = mt.atan(0.05 / eu_dist)
        eu_angle = mt.atan2((obs_position[k][0] - q_ry), (q_rx - obs_position[k][1]))
        eu_angleDg = (eu_angle * 180) / mt.pi
        #eu_ang_min = thetaDg - eu_angleDg
        #eu_ang_max = thetaDg + eu_angleDg
        if max_distance >= eu_dist - 0.5 and thetaDg <= eu_angleDg + 20 and thetaDg >= eu_angleDg - 20:
            print('Collision')
            print('eu_dist =', eu_dist)
            print('obs_position[k] =', obs_position[k])
            print('thetaDg', thetaDg)
            print('eu_angleDg', eu_angleDg)      
        
#Plot
fig1 = plt.figure(figsize = [size, size])
ax = fig1.add_subplot(111)
ax.set_title('Line intersecting and obstacle', fontdict = font)
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
        
for k in range(len(q_rx_ini_set)):
    #Initial random point
    plt.scatter(q_rx_ini_set[k], q_ry_ini_set[k], s = marker_size, c = 'y', alpha = alp)
    plt.plot([q_sx, q_rx_ini_set[k]], [q_sy, q_ry_ini_set[k]])
    
    #Point over the previous vector
    plt.scatter(q_rx_set[k], q_ry_set[k], s = marker_size, c = 'c', alpha = alp)
    plt.plot([q_sx, q_rx_set[k]], [q_sy, q_ry_set[k]])
    plt.pause(0.1) 
    
    