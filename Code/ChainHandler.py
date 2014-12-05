# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 21:00:53 2012

@author: nrjh
"""

from Polylines import Polyline
from Polylines import Segment
from Points import Point2D

import random
import math


def ChainLoader(fileName,seperator=None):
    """ Generates a Point field (passed as string) from and x-y file
    assuming first line is a header line"""
    lines = []
    chains = []
    
    myFile=open(fileName,'r')
    
#iterate through all the file lines to get them into a list of Strings
#makes it easier to deal with afterwards
    for line in myFile.readlines():
        lines.append(line)
        
#now process all the lines
    atEnd=False

    lineno=0
    while not(atEnd):
        #print lines[lineno]
        if lines[lineno].lstrip().upper()[0:3]=="END":
            atEndofblock=True
            atEnd=True
        else: 
            atEndofblock=False
            pl=Polyline()
            pl.setID(lines[lineno])
            lineno=lineno+1
        
        while not(atEndofblock):
            line=lines[lineno]
            if line.lstrip().upper()[0:3]=="END":
                atEndofblock=True
            else:
#                if (seperator==None):
#                    items=line.split()
#                else:
#                    items=line.split(seperator)  
                items=line.split(seperator)  
                x=float(items[0])
                y=float(items[1])
                pl.addPoint((x,y))
            lineno=lineno+1
        
        if  not(atEnd): 
            chains.append(pl)
        
    return chains

def chainWriter(fileName,chains):
    myFile=open(fileName,'w') 
    
    for i in range(len(chains)):
        myFile.writelines(str(i+1)+"\n")
        chain=chains[i]
        for j in range(chain.size()):
            p=chain.getPoint(j)
            x=p.get_x()
            y=p.get_y()
            myFile.writelines(str(x)+"\t"+str(y)+"\n")
        myFile.writelines("end"+"\n")
    myFile.writelines("end")


def rand_Segment(xlo=0.,xhi=1.,ylo=0.,yhi=1.):
    """ Generates random Segment in x-y range specified
    as parameters"""

#random numbers generated in a specific range
    x1=random.uniform(xlo,xhi)
    y1=random.uniform(ylo,yhi)
    x2=random.uniform(xlo,xhi)
    y2=random.uniform(ylo,yhi)
 
    return Segment(x1,y1,x2,y2)
    
    
# to generate a random String to test a few things*/	
def generateRanString(l,xmin,ymin,xmax,ymax,wiggly,rangy):
    
    pi2=math.pi*2.
    wiggle=pi2*wiggly
    xextent=xmax-xmin
    yextent=ymax-ymin
    extent=math.sqrt(xextent*xextent+yextent*yextent)/l
    
    sl=Polyline()
    
    x=xmin+random.random()*xextent
    y=ymin+random.random()*yextent
    
#    print "x: " + str(x) + ", y: "+str(y)
    sl.addPoint((x,y))
#    p1=sl.getPoint(0)
    
#    print "x: " + str(p1.get_x()) + ", y: "+ str(p1.get_y())
     
    
    lastAngle=random.random()*pi2
    lastx=x
    lasty=y
    intersectFound=False

#        print "just here 1"
    for i in xrange(1,l):
#            print "just here 2"
        count=0
        while True:
            angle=lastAngle+((random.random()*2-1)*wiggle)
            d=extent*(1+((random.random()*2-1)*rangy))
            x=lastx+math.sin(angle)*d
            y=lasty+math.cos(angle)*d
            lastAngle=angle
            slast=Segment(sl.getPoint(i-1),Point2D(x,y))
          
            for k in xrange(0,i-3):
                s=Segment(sl.getPoint(k),sl.getPoint(k+1))
                  
                if (slast.intersects(s)):
                    intersectFound=True
            count=count+1
            if not ((x<xmin or y<ymin or x>xmax or y>ymax or intersectFound) and count<100):
                break
            
        if (count>99):
            print "Recall"
            return generateRanString(l,xmin, ymin, xmax, ymax,wiggly,rangy)
            
        sl.addPoint((x,y))
        lastx=x
        lasty=y
          
    return sl

        