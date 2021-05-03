# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 18:59:00 2021

@author: minty
"""
import numpy as np
import random
import matplotlib.pyplot as plt
import fiberloc as fl

def newstate(): #generate a new state
    i = random.randint(0, Nfiber-1)
    ifassignnew = ifassign
    whereassignnew = whereassign
    
    if ifassign[i] == 0: #fiber is not already assigned
        #check area for targets
        ptloc, ptprior = checkarea(i)
        #assign highest priority target
        whichtar = besttarget_prior(ptloc, ptprior)
        if int(whichtar) == Ntarget: #there are no good targets in the patrol area
            ifassignnew[i] = 0
        else: 
            ifassignnew[i] = 1
            tiltarray[i] = tilt(r, tx[whichtar], ty[whichtar], fx[i], fy[i])    
        whereassignnew[i] = whichtar
        return ifassignnew, whereassignnew, tiltarray
    if ifassign[i] == 1: #Fiber is already assigned
        P = np.exp(-1/T)*prior[int(whereassign[i])] #you can change this probability distribution
        PROBABLY.append(P)
        if P < .95: #play around with the probabilities, this will deassign the fiber
            ifassignnew[i] = 0
            whereassignnew[i] = Ntarget
            whichtar = i
            return ifassignnew, whereassignnew, tiltarray
        else: #we leave the fiber alone
            return ifassign, whereassign, tiltarray

        
def checkarea(i): #checks patrol area for open targets
    ptloc = [] #potential targets number
    ptprior = [] #their priorities
    for j in range(Ntarget-1):
        if circle(fx[i], fy[i], r, tx[j], ty[j], tr) == 1 : 
            #check if that target is already assigned
            if float(j) not in whereassign:
            #check if there is an intersection
                ptloc.append(j)
                ptprior.append(prior[j])
    return ptloc, ptprior

def besttarget_prior(ptloc, ptprior): #finds the best target from potential target list
    if ptloc == []:
        return Ntarget
    
    max_value = max(ptprior)
    max_index = [i for i, x in enumerate(ptprior) if x == max_value]
    
    if len(max_index) == 1:
        return ptloc[max_index[0]] #only 1 good target
    else: 
        b = random.choice(max_index) #pick randomly between highest targets if there is a tie
        return ptloc[b]


def circle(cfx, cfy, rf, ctx, cty, rt): #check if target and fiber intersect
    c1c2 = np.sqrt((cfx-ctx)**2 + (cfy-cty)**2)
    if c1c2 <= r:
        return 1
    else:
        return 0
    

def energy(ifassign, whereassign, prior, tiltarray): #calculates energy function
    energy = 0
    for m in range (Nfiber):
        if int(whereassign[m]) != Ntarget:
            energy += (ifassign[m] * prior[int(whereassign[m])] * (1-tiltarray[m]**2))
    return energy

def fiber2sky(mini, loc): #changes the fiber locations to match the sky tile locations
    loc2 = np.ones(len(loc))    
    for i in range (len(loc)):
        loc2[i] = mini + loc[i]
    return loc2

def tilt(r, txloc, tyloc, fxloc, fyloc): #calculates the tilt as a fraction of r
    t = np.sqrt((fxloc-txloc)**2 + (fyloc-tyloc)**2)
    return t/r

#Set up Inital State and Parameters

platescale = 106.7 * 3600 * 0.001

r = 7.7/platescale #patrol radius (mm)/platescale
p = 7.7/platescale #pitch
e = 1/platescale #exclusion radius
tr = 1/platescale #target radius

T_initial = 100
tstep = 0.1
T_final = 0.1

T = T_initial 

tx = np.loadtxt('OV_test_x.txt')
ty = np.loadtxt('OV_test_y.txt')


ra_min = min(tx)
dec_min = min(ty)


fx, fy , Nfiber, tr = fl.arrangefibers(r, p, e, tr) #arranges fiber on focal plane

fx = fiber2sky(ra_min, fx)
fy = fiber2sky(dec_min, fy)

prior = np.loadtxt('OV_targetgalaxytestprior.txt')
info = np.loadtxt('OV_targetinfo.txt')

PROBABLY = [] #this is used to chack the probability distributions for deassigning

Ntarget = len(tx) #number of targets

#assignment array, 1 is assigned, 0 if unassigned
ifassign = np.zeros(Nfiber) #0 if unassigned, 1 if assigned
whereassign = (Ntarget)*np.ones(Nfiber) #which target is each fiber pointing to? if none then value is 500
tiltarray = np.ones(Nfiber) #if the target is assigned to a fiber, how much is the tilt
   
E_current = 0 #current energy
E_time = [] #store energies for energy vs time graph
step = []
count = 0

elggraph = [] #store number of each type of target vs time/step
lbggraph = []
qsograph = []
clustergraph = []

while T > T_final:
        #Generate new state
        E_time.append(E_current)
        #create new arrays to compare energies
        ifassignnew, whereassignnew, tiltarray = newstate()
        E_new = energy(ifassignnew, whereassignnew, prior, tiltarray)
        
        if E_new >= E_current: #check if new energy is greater
            ifassign = ifassignnew
            whereassign = whereassignnew
            E_current = E_new
        else:
            #generate probability
            P = np.exp((E_new-E_current)/T)
            #PROBABLY.append(P) #this is to check the probabilities
            if P < np.random.rand(1): #you can also mess around with this
                ifassign = ifassignnew
                whereassign = whereassignnew
                E_current = E_new
        count += 1
        T -= tstep
        step.append(count)
        
        #analyze results as we go
        #this is NOT efficient at all, I just coded this in last minute. 
        #please change this for future
        elg = 0
        lbg = 0
        qso = 0
        cluster = 0
        
        for m in range (len(ifassign)):
            if ifassign[m] == 1:
                if info[int(whereassign[m])] == 1:
                    elg += 1
                if info[int(whereassign[m])] == 2:
                    lbg += 1
                if info[int(whereassign[m])] == 3:
                    qso += 1
                if info[int(whereassign[m])] == 4:
                    cluster += 1
            #print(whichtar)    
        elggraph.append(elg)
        lbggraph.append(lbg)
        qsograph.append(qso)
        clustergraph.append(cluster)
                
        
plt.plot(step, elggraph, label='Emission Line Galaxies')         
plt.plot(step, lbggraph, label='Lyman Break Galaxies')
plt.plot(step, qsograph, label='Lyman Alpha QSOs')
plt.plot(step, clustergraph, label='Cluster Galaxy')
plt.title('Target type per step')
plt.xlabel('Step')
plt.ylabel('Count')
plt.legend(bbox_to_anchor=(0.5, 0.75), loc='upper left')
plt.show()

print('Current Energy: ' + str(E_current))

tassign = np.zeros(Nfiber)#Ntarget) #what is this?
for n in range (len(whereassign)):
    if whereassign[n] == 1:
        tassign[n] = 1
    
fa = sum(ifassign)
print('Total targets: ' + str(Ntarget))
print('Fibers assigned: ' + str(fa))
print('Total fibers: ' + str(Nfiber))


finaltargetsx = []
finaltargetsy = []
finalprior = []
finaltilts = []
unassignedfx = []
unassignedfy = []
unassignedprior = []

elg = 0
lbg = 0
qso = 0
cluster = 0

for n in range (Nfiber):
    if ifassign[n] == 1:
#        print(n)
#        print(whereassign[n])
        finaltargetsx.append(tx[int(whereassign[n])])
        finaltargetsy.append(ty[int(whereassign[n])])
        finalprior.append(prior[int(whereassign[n])])
        '''        
        if info[int(whereassign[n])] == 1:
            elg += 1
        if info[int(whereassign[n])] == 2:
            lbg += 1
        if info[int(whereassign[n])] == 3:
            qso += 1
        if info[int(whereassign[n])] == 4:
            cluster += 1
        '''
        
        finaltilts.append(tiltarray[n])#*r*platescale)
    if ifassign[n] == 0:
        unassignedfx.append(fx[n])
        unassignedfy.append(fy[n])

for n in range (Ntarget): 
    if n not in whereassign:
        unassignedprior.append(prior[n])

print(np.max(finaltilts))
print(r*platescale)

plt.plot(unassignedfx, unassignedfy, 'x', label='Unassigned fiber')

plt.scatter(tx,ty, c=prior, s = 50, marker='*', label='Targets', cmap='cool')
plt.colorbar(label='Priority')

plt.plot(finaltargetsx,finaltargetsy, "o", markersize='5', markerfacecolor='none', color='red', label='Observed Target')
plt.xlabel('Target X location (DEC)')
plt.ylabel('Target Y location (RA)')
plt.title('Assigned Targets: ' + str(fa) + '/' + str(Ntarget) + ', Total Fibers: ' + str(Nfiber))
plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=3)
plt.show()

plt.plot(step, E_time)
plt.xlabel('T step')
plt.ylabel('Energy of current configuration')
plt.title('Energy vs Time, Final energy: ' + str(E_current))
plt.show()


plt.hist(finaltilts)
plt.xlabel('Tilt (percentage of radius(7.7mm))')
plt.ylabel('Number of fibers')
plt.title('Tilt with Median: ' + str(np.median(finaltilts)))
plt.show()


plt.hist([finalprior, unassignedprior], bins=5, stacked=True, label=['Observed','Unobserved'])
plt.xlabel('Priority')
plt.ylabel('Count')
plt.title('Number of Observed Targets vs. Priority')
plt.legend()
plt.show()

#plt.hist(PROBABLY)


