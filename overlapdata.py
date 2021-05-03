# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 12:23:46 2021

@author: minty
"""
import numpy as np
import matplotlib.pyplot as plt

#this takes the cluster data and the redshift survey data to make 1 data set

Rtx = np.loadtxt('RSS_test_x.txt')
Rty = np.loadtxt('RSS_test_y.txt')
Rprior = np.loadtxt('RSS_targetgalaxytestprior.txt')
Rprior1 = np.ones(len(Rtx))

Gtx = np.loadtxt('GC_test_x.txt')
Gty = np.loadtxt('GC_test_y.txt')
Gprior = np.loadtxt('GC_targetgalaxytestprior.txt')
Gprior1 = np.ones(len(Gtx))

Rminx = min(Rtx)
Gminx = min(Gtx)
Rminy = min(Rty)
Gminy = min(Gty)

for i in range(len(Rtx)):
    Rtx[i] = Rtx[i] - Rminx
    Rty[i] = Rty[i] - Rminy
    
    
for i in range (len(Gtx)):
    Gtx[i] = Gtx[i] - Gminx
    Gty[i] = Gty[i] - Gminy    
    
RA = []
DEC = []
PRIOR = []
PRIOR1 = []
targetinfo = []

for i in range(len(Rtx)):
    RA.append(Rtx[i])
    DEC.append(Rty[i])
    PRIOR.append(Rprior[i])
    PRIOR1.append(Rprior1[i])
    if Rprior[i] == 0.6:
        targetinfo.append(1) #elg
    elif Rprior[i] == 0.5:
        targetinfo.append(2) #lbg
    elif Rprior[i] == 0.4:
        targetinfo.append(3) #qso

for i in range(len(Gtx)):
    RA.append(Gtx[i])
    DEC.append(Gty[i])
    PRIOR.append(Gprior[i])
    PRIOR1.append(Gprior1[i])
    targetinfo.append(4) #cluster
    
    
plt.plot(RA, DEC, '*')
plt.show()

plt.hist(PRIOR)
plt.show()

np.savetxt('OV_test_x.txt', RA)
np.savetxt('OV_test_y.txt', DEC)
np.savetxt('OV_targetgalaxytestprior.txt', PRIOR1)
np.savetxt('OV_targetinfo.txt', targetinfo)

