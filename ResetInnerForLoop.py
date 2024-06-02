#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:30:54 2024
Title: Code to reset inner for loop
"""

import random as rd

n = 3
for j in range(n):
    print('j:', j)
    a = rd.randint(0, 2)
    b = rd.randint(0, 2)
    
    restart = True
    while restart:
        print('a:', a)
        for k in range(4):
            print('k:', k)
            c = rd.randint(0, 2)
            d = rd.randint(0, 2)
            if a == c and b == c:
                print('coincidence')
                a = 5
                restart = True
                break
            restart = False