# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 17:08:54 2013

@author: nrjh
"""
from DorlingCarto import Carto_atom
import math
import numpy as np
import random

def simple_Dorling(rows,cols,step,xor,yor,data_scale,boundary):
    """ sets up a simple grid of Dorling carto-atoms with topology based on 
simple x-y adjacency in the array.  Set up to create array of any given size and 
same boundary length in each case.  Can set cell spacing and origin of array.  The radius
range of the carto-atom is controlled by the data_scale parameter"""     
    
    atom_list=[]
# set up some tuples to define i,j offsets for up-down, left-right    
    delta=((-1,0),(1,0),(0,1),(0,-1))
 
#First iteration of a simple list but for as many rows and colums as we might have in our grid
    for i in range(rows):
        for j in range(cols):
#The +0.2 just hacked in here to make thingss look better - you could pass a 'nub' as a
#parameter            
            data=(math.sqrt(random.random())+0.2)
# provides the x-y co-ordinate for the atom, data value
            atom_list.append(Carto_atom(i*step+xor,j*step+yor,data,data*data_scale))

# now array-format the list for the given row-column sizing
    atom_array=np.array(atom_list)
    atom_array.shape=(rows,cols)


# now iterate again to insert the relevant links between atoms in the array        
    for i in range(rows):
        for j in range  (cols):
           # print 'i '+str(i)+' j '+str(j)+'x '+str(atom_array[i,j].get_coord(0))+'y '+str(atom_array[i,j].get_coord(1))
            for delta_c in delta:
                ii=i+delta_c[0]
                jj=j+delta_c[1]
                if (ii>-1 and ii <rows and jj>-1 and jj<cols):
                    maxSep=atom_array[i,j].getRadius()+atom_array[ii,jj].getRadius()
                    atom_array[i,j].addLink(atom_array[i,j],atom_array[ii,jj],boundary,maxSep)
   
#reshape to a 1-D form and return as a simple list         
    atom_array.shape=(rows*cols)
        
    return list(atom_array)
    
    
    



def dorlingUpload1(fileName, data_scale = 1.0):
    """ Generates a set of point-links for use in a Dorling Cartogram construction"""
    lines = []
    atom_list = []
    
    myFile=open(fileName,'r')
    myFile.readline()    
    
#iterate through all the file lines to get them into a list of Strings
#makes it easier to deal with afterwards
    for line in myFile.readlines():
        lines.append(line)
        print line
        
    count=0   
    items=lines[count].split(',')
    current=items
    names=[]

    while True:
        while True:
             count+=1
             #If at end of file, break
             if (count>=len(lines)-1):
                 break
             #Starts at 1 as line 0 is headings for table format
             items=lines[count].split(',')
             nextone=items
            
             if (nextone[1]!=current[1]):
                 print "count "+str(count)+' '+current[1]
                 names.append(current[1])
                 x=float(current[4])
                 y=float(current[5])
                 data=float(current[3])
                 label=current[1]
                 radius=math.sqrt(data/math.pi)*data_scale
                 print x,y,data,radius,label
                 atom_list.append(Carto_atom(x,y,data,radius,label))
                 break
             current=nextone
        current=nextone 
        if (count>=len(lines)-1):
                 break
        
    #print "last count "+str(count)+' '+current[1]
    names.append(current[1])
    x=float(current[4])
    y=float(current[5])
    data=float(current[3])
    label=current[1]
    radius=math.sqrt(data/math.pi)*data_scale
    atom_list.append(Carto_atom(x,y,data,radius,label))
    indexes=range(len(names))
   
    
    d=dict(zip(names,indexes))
    
    for name in names:
        print name+' '+str(d[name])
    #print names
    
    for line in lines:
        items=line.split(',')
        name=items[1]
        link_name=items[2]
        boundaryLen=float(items[6])
        index=d[name]
        link_index=d[link_name]
        print name, index, link_name,link_index
        maxSep=atom_list[index].getRadius()+atom_list[link_index].getRadius()

        #atom_list[index] added so that can get bearing to self       
        atom_list[index].addLink(atom_list[index],atom_list[link_index],boundaryLen,maxSep)
    
    
    return atom_list
    
    