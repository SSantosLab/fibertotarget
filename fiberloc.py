# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 18:22:39 2021

@author: minty
"""
import numpy as np
#import matplotlib.pyplot as plt

def build_checkerboard(w, h) :
      re = np.r_[ w*[0,1] ]              # even-numbered rows
      ro = np.r_[ w*[1,0] ]              # odd-numbered rows
      return np.row_stack(h*(re, ro))

platescale = 106.7 * 3600 * 0.001# mm / degree

def arrangefibers(r, p, e, tr):
    
    N_fib = int((np.sqrt(0.3**2 + 0.3**2)//p) - 1) #number of fibers in a row
    #The 0.3 corresponds to a .3 degree field. Please change if if you change field size. 
    
    checkerboard = build_checkerboard(2*N_fib, 2*N_fib)
    
    flocx = [] #Fill this with fiber locations
    flocy = []
    counter = 0
    offset = p*np.sin(np.pi /4)
    
    for x in range (N_fib):
        for y in range (N_fib):
            flocx.append(checkerboard[x,y] * x * p * np.sin(np.pi / 4) + offset)
            flocy.append(checkerboard[x,y] * y * p * np.sin(np.pi / 4) + offset)
            counter += 1
            
    extrax = min(flocx)
    extray = min(flocy)

    fx = []
    fy = []
    
    #this removes the extra points that the checkerboard creates
    for i in range(len(flocx)):
        if flocx[i] != extrax or flocy[i] != extray:
            fx.append(flocx[i])
            fy.append(flocy[i])

    Nfiber = len(fx)
    
    return fx, fy, Nfiber, tr

