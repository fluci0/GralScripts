#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 14:03:17 2024
Title: Script to show atan2 function
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
q_s = [25, 25]
q_g = [42, 40.5]
n = 50

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

q_rx_ini = rd.uniform(0, len(map_i))
q_ry_ini = rd.uniform(0, len(map_i))

q_rx_ini_set = []
q_ry_ini_set = []
q_rx_set = []
q_ry_set = []

for j in range(n):
    q_rx_ini = rd.uniform(0, len(map_i))
    q_ry_ini = rd.uniform(0, len(map_i))
    theta = mt.atan2((q_sy - q_ry_ini), (q_rx_ini - q_sx))
    thetaDg = (theta * 180) / mt.pi
    #Varying the max distance
    max_distance = rd.uniform(0, 15)
    #Placing one point in the line that connects both points
    q_rx = q_sx + max_distance * mt.cos(theta)
    q_ry = q_sy - max_distance * mt.sin(theta)
    q_rx_ini_set.append(q_rx_ini)
    q_ry_ini_set.append(q_ry_ini)
    q_rx_set.append(q_rx)
    q_ry_set.append(q_ry)
    

#Plot
fig1 = plt.figure(figsize = [size, size])
ax = fig1.add_subplot(111)
ax.set_title('atan2 function', fontdict = font)
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


