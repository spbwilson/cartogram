# -*- coding: utf-8 -*-
"""
Created on Fri Feb 08 16:53:05 2013

This modules handles a whole load of stuff need to create Dorling
Carotgrams

@author: nrjh
"""
from Points import Point2D

###################################################
class Apoint(Point2D):
    """An enhanced Point class to hold additional data to make Dorling-type
    Cartogram circles work well"""
    
    def __init__(self, x, y,data,radius=None,label=None): 
# call the super-class constructor        
        Point2D.__init__(self, x, y)
# define the additional attributes of some data, a symbol radius and a label
# Having both data and radius makes it easier to keep the original data
# but rescale for any plotting purposes        
        self._data=data
        self._radius=radius
        self._label=label
        
#return a clone of self (another identical Apoint object)        
    def clone(self):
        return Apoint(self._x,self._y,self._data,self._radiius,self._label)
        
    def setData(self, data):
        self._data=data
    def getData(self):
        return self._data
        
    def getRadius(self):
        return self._radius

#######################################################  

class Carto_atom(Apoint):
    """This class extends further the Apoint above to add links to other Apoints
    it actually holds a list of 'links' where a link is information about the points 
    link to this one, and the boundary length of the original connection.  Thus it 
    represents a 'cell' or 'atom' in the cartogram, including the links to other cells"""
    
    # The initialisation methods used to instantiate an instance
    def __init__(self,x,y,data,radius=None,label=None): 
#Again call the super-class constructor to initiate
        Apoint.__init__(self, x, y,data,radius,label)
        self._links=[]

    def addLink(self,selfRef,point,boundaryLength,maxSep):
        """ Adds in a single link to the list of links - the links use exisitng Points because
        we don't want to create new ones"""
        self._links.append(Carto_link(selfRef,point,boundaryLength,maxSep))

    def getLink(self,i):
        return self._links[i]
        
    def getLinks(self):
        return self._links
    
    def numLinks(self):
        return len(self._links)
        
    def normaliseBoundaries(self):
        """ Because boundary length scales are arbitrary, and we are generally interested in the
        relative connection between areas, it helps to be able to normalise all the boundary lengths 
        in the given set - in this case this has the cost of destroying the orignal data though one could
        modify to store both.  Bounaries after this have lengths 0<1"""
        bsum=0
        for link in self._links:
            bsum+=link.getBoundaryLength()
        for link in self._links:
            link.setBoundaryLength(link.getBoundaryLength()/bsum)
            
        

    def resolveForces(self,boundary_scale,damping,push_enhance=5.):
        """ A basic method to resolve forces for one Point.  In this
        case we balance overall 'attraction and repulsion' in relation to all
        other connected points"""
     
        # Set up initial x and x vectors to accumulate the total force vectors     
        x_resultant=0
        y_resultant=0

        # Iterate across all links        
        for link in self._links:
            # helps to get the points associate with a specific link and the distance to that
            # right now, and the 'maximum separation' - the distance points are apart when just touching
            otherp=link.getLink()
            distance=self.distance(otherp)
            max_sep=link.getMaxSep()
            
            #So you can now work out quickly if the linked point is overlapping
            #You need to scale velocity against separation but do it differently depening on whether
            #you are less or greater than the maximum separation
            
            #This adition prevents minute changes that can force every
            #tolerance = 0         
            #if abs(distance) > (max_sep+tolerance):
            if (distance>max_sep):
                scaling=damping*(distance-max_sep)/distance
            else:
                scaling=push_enhance*damping*(distance-max_sep)/max_sep

            # Now you need to work out separate x and y components again this overall scaling            
            xpart=scaling*(otherp.get_x()-self._x)
            ypart=scaling*(otherp.get_y()-self._y)
            
            # finally add up all the forces from all the other atoms            
            x_resultant=x_resultant+xpart
            y_resultant=y_resultant+ypart

        return (x_resultant,y_resultant)


    #-------------------------SEAN'S IMPLEMENTATION-----------------------------
    def resolveForces2(self, boundary_scale, damping, alpha = 0.3):
        """This version of the implementation is based on 
        Ryo Inoue, Eihan Shimizu's paper:
        Construction of Circular and Rectangular Cartograms 
        by Solving Constrained Non-linear Optimization Problems"""

        # Set centre of circle     
        x_resultant = 0
        y_resultant = 0

        #Summers
        bearingDif = 0
        ratDist = 0

        #For each neighbour of the point
        for link in self._links:

            #Get neighbours centre, distance and max_seperation
            otherp = link.getLink()
            distance = self.distance(otherp)
            max_sep = link.getMaxSep()
            
            #If the neighbour isn't overlapping
            if (distance>max_sep):
                
                #Get the geographical bearing to current neighbour
                gBearing = link.getGBearing()

                #Get the current cartogram bearing to current neighbour
                cBearing = self.bearingTo(Point2D(link.getLinkX(), link.getLinkY()))

                #Add to summers from equation
                ratDist += ((distance/max_sep)-1)**2
                bearingDif += (cBearing - gBearing)**2

        #Calculate the scaling
        scaling = alpha*ratDist + (1-alpha)*bearingDif
        
        # finally add up all the forces from all the other atoms            
        x_resultant = self._x * scaling
        y_resultant = self._y * scaling


        return (x_resultant,y_resultant)


######################################################################
class Carto_link(object):
    """To represent a link between one Carto_atom and another
    Includes:  The 'other' atom to be linked to (atomlink), the
    length of the connecting boundary and a 'max-separation' for them
    normally this would be the sum of the two atom radii but needs
    to be calculate/ defined elsewhere"""
    
    def __init__(self,atom,atomlink,boundaryLength,maxSep):
        self._atom = atom
        self._atomlink=atomlink
        self._boundaryLength=boundaryLength
        self._maxSep=maxSep
        self._gBearing = atom.bearingTo(atomlink)
        self._cBearing = self._gBearing
        
    def getLink(self):
        return self._atomlink
    
    def getBoundaryLength(self):
        return self._boundaryLength
    
    def setBoundaryLength(self,boundaryLength):
        self._boundaryLength=boundaryLength

#Just make it easier to get the x-y of the linked point    
    def getLinkX(self):
        return self._atomlink.get_x()
        
    def getLinkY(self):
        return self._atomlink.get_y()
        
    def getMaxSep(self):
        return self._maxSep

    def getGBearing(self):
        return self._gBearing

#######################################################################     
        
      