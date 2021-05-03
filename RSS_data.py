# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 13:28:58 2021

@author: minty
"""
import numpy as np
import matplotlib.pyplot as plt

#This data is from MSE, given to me by Jen Marshall and Jen Sobeck
data = np.genfromtxt('RSS_data.txt', delimiter=',' , skip_header=True)#, usecols=(1,2,4,5,6,7,8,9,10,11,12,13,14,15))


OBJID0 = data[:,0]
RA0 = data[:,1]
DEC0 = data[:,2]
SPECTRO0 = data[:,3]
UMAG0 = data[:, 4]
GMAG0 = data[:, 5]
RMAG0 = data[:, 6]
IMAG0 = data[:, 7]
ZMAG0 = data[:, 8]
JMAG0 = data[:, 9]
HMAG0 = data[:, 10]
NOBSREQ0 = data[:, 11]
NREPEAT0 = data[:, 12]
PRIORITY0 = data[:, 13]
SURVEYPRIORITY0 = data[:, 13]
NOBSDONE0 = data[:, 14]

OBJID = []
RA = []
DEC = []
UMAG = []
PRIORITY = []

#You can use whatever selection criteria you want to create a list of targets
for i in range (len(UMAG0)-1):
    if (-0.15 < DEC0[i] < 0.15 and 178 < RA0[i] < 178.3):
        OBJID.append(OBJID0[i])
        RA.append(RA0[i])
        DEC.append(DEC0[i])
        UMAG.append(UMAG0[i])

#Assigning priorities based on the type of object
for p in OBJID:
    if p == 3:#'cosmo_elg':
        PRIORITY.append(0.6)
    if p == 2:#'cosmo_lbg':
        PRIORITY.append(0.5)
    if p == 1:#'cosmo_qso':
        PRIORITY.append(0.4)

plt.plot(RA,DEC, "*", markersize=5)
plt.show()

np.savetxt('RSS_test_x.txt', RA)
np.savetxt('RSS_test_y.txt', DEC)
np.savetxt('RSS_targetgalaxytestprior.txt', PRIORITY)
