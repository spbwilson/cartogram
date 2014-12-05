# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 17:26:55 2013

@author: Sean Wilson
"""
from ChainHandler import ChainLoader 
from PointPlotter import PointPlotter
from DorlingPolygonHandler import *
import math

#These variables can be messed with for different results
boundaryScale = 0.25
dampingValue = 0.10
alpha = 0.3


#==============================PLOT ATOMS=======================================
def plotAtoms(atoms, pp):
    """This is used to plot atoms onto an existing pointPlotter"""
    for atom in atoms:
        for other in atom.getLinks():
            otherp=other.getLink()
            pp.plotVector(atom,otherp,'yellow')  
    pp.plotPoint(atoms)    
    pp.plotCircle(atoms,'red')

#===============================ITERATOR========================================
def iterateOverData(atoms):
    """This iterates over the atoms and moves them as needed
        Use either resolveForces or resolveForces2"""
    global boundaryScale
    global dampingValue
    global alpha

    moves=[]
        
    #For each atom, get the move distance from resolve
    for atom in atoms:
        moves.append(atom.resolveForces(boundaryScale, dampingValue))
        #moves.append(atom.resolveForces2(boundaryScale, alpha))
      
    #Move each atom  
    for i in range(len(atoms)):
        atoms[i].move(moves[i][0],moves[i][1])

    return atoms


#===============================TEST DATA=======================================
def testData(iterate):
    """This method uses a test environment"""
    
    #---------------Set simple grid environment-------------
    rows = 5          #No. atoms in row
    cols = 5          #No. atoms in column
    step = 10.        #Gap between each atom
    data_scale = 5.   #Fuck knows
    xor = 5.          #
    yor = 5.          #
    boundary = 10.    #  

    #Create point plotter
    pp = PointPlotter()

    xmin = xor - step
    ymin = yor - step
    xmax = xor + ((cols)*step)
    ymax = yor + ((rows)*step)
    print xmin,ymin,xmax,ymax

    atoms = simple_Dorling(rows,cols,step,xor,yor,data_scale,boundary)
   
    
    #Print initial data before being resolved
    pp.set_axis(xmin,xmax,ymin,ymax)
    plotAtoms(atoms, pp) 
    pp.show()


    #------------------Iterate over data--------------------
    #Iterate for number specified
    for repeat in xrange(iterate):
        atoms = iterateOverData(atoms)

        #See intermediate stage, every 20%
        if math.fmod(repeat, iterate*0.2) == 0:
            pp.set_axis(xmin,xmax,ymin,ymax)
            plotAtoms(atoms, pp)
            pp.show()
   

    #Print final data
    pp.set_axis(xmin,xmax,ymin,ymax)
    plotAtoms(atoms, pp) 
    pp.show()

        

#================================REAL DATA======================================
def realData(iterate):
    """This method uses real world data and plots against world map"""
    
    xmin = -180.0
    xmax = 180
    ymin = -90.
    ymax = 90.

    #Create point plotter
    pp = PointPlotter()

    #--------------Get Country Boundaries-------------------
    print 'Reading data'
    #read in some data
    all_lines = ChainLoader('Global_Borders.txt')


    summer = 0
    for line in all_lines:
        summer += line.size()
    print 'Orignal data contains ' +str(summer)+' nodes'

    gen_lines = []

    print 'Generalising'
    for line in all_lines:
        gen_lines.append(line.generalise(0.02))
        
    summer = 0
    for line in gen_lines:
        summer += line.size()
    print 'Generalised data contains ' +str(summer)+' nodes'


    #--------------Get Cartogram Data-----------------------
    print 'Loading atom data'
    atoms = dorlingUpload1("Global_PolyAdjacent1.csv", data_scale=0.001)

    
    #Print initial data before being resolved
    print 'Plotting'
    pp.set_axis(xmin,xmax,ymin,ymax)
    pp.plotPolylines(gen_lines,'green')
    
    for atom in atoms:
        for other in atom.getLinks():
        	#Get the link
            otherp = other.getLink()
            pp.plotVector(atom,otherp,'yellow')  
    
    pp.plotPoint(atoms)    
    pp.plotCircle(atoms,'red')
    pp.show() 


    #------------------Iterate over data--------------------
    for repeat in xrange(iterate):
        atoms = iterateOverData(atoms)
      

    #Print final Cartogram 
    print 'Plotting'
    pp.set_axis(xmin,xmax,ymin,ymax)
    pp.plotPolylines(gen_lines,'green')    
    
    for atom in atoms:
        for other in atom.getLinks():
            #Get the link
            otherp = other.getLink()
            pp.plotVector(atom,otherp,'yellow')  
    
    pp.plotPoint(atoms)    
    pp.plotCircle(atoms,'red')
    pp.show()

    #Print without map  
    pp.plotPoint(atoms)    
    pp.plotCircle(atoms,'red')
    pp.show()

#===============================MAIN============================================

#Get what data set we are using
while True:
    try:
        dataType = int(raw_input("What data would you like to use? Enter 0 for test, enter 1 for real: "))
        break
    except ValueError:
        print "Invalid input"

#Get how many iterations we want
while True:
    try:
        iterationNum = int(raw_input("How many iterations?: "))
        break
    except ValueError:
        print "Invalid input"

#Run test environment
if dataType == 0:
    testData(iterationNum)

#Run real data environment
else:
    realData(iterationNum)