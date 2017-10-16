import numpy as np

"""
Optical Ray Tracer
"""

class Ray:
    """A class which allows ray objects to be created with a position and direction vector"""
    
    def __init__(self, point, direction):
        #The position and direction vectors are stored as numpy arrays in a list
        self.__p = [np.array(point, dtype='float')]
        self.__k = [np.array(direction, dtype='float') / \
                    np.linalg.norm(np.array(direction, dtype='float'))] #The direction vector is normalised to a unit vector

        #An exception is raised if the position or direction vector has more/less than 3 components
        if len(point) != 3:
            raise Exception('Your position vector must have 3 components')
            
        if len(direction) != 3:
            raise Exception('Your direction vector must have 3 components')
            
    def __repr__(self):
        """Returns a representation of the ray object along with its parameters"""
        
        return "%s(Point=[%g, %g, %g], Direction=[%g, %g, %g])" % ("Ray", self.__p[-1][0], self.__p[-1][1], self.__p[-1][2], self.__k[-1][0], self.__k[-1][1], self.__k[-1][2])

    def __str__(self):
        """Prints the parameters of the ray object"""
        
        return "(Point=[%g, %g, %g], Direction=[%g, %g, %g])" % (self.__p[-1][0], self.__p[-1][1], self.__p[-1][2], self.__k[-1][0], self.__k[-1][1], self.__k[-1][2])
        
        
    def p(self):
        """Returns the final position of the ray object"""
        
        return self.__p[-1]
        
    def k(self):
        """Returns the final direction vector of the ray"""
        
        return self.__k[-1]
        
    def append(self, p, k):
        """Appends a new position and direction vector to the ray object"""
        
        if len(p) != 3:
            raise Exception('Your position vector must have 3 components')
            
        if len(k) != 3:
            raise Exception('Your direction vector must have 3 components')
        
        self.__p.append(np.array(p, dtype='float'))
        self.__k.append(np.array(k, dtype='float')/ \
        np.linalg.norm(np.array(k, dtype='float'))) #The new direction vector must be normalised before it is appended
        
    def vertices(self):
        """Returns a list which contains all of the position vectors (as numpy arrays) along the ray"""
        
        return self.__p
        
class Bundle:
    """A class which allows a collection of ray objects to be created with position and direction vectors"""
    
    def __init__(self, n, rmax, m):
        self.n = n
        self.rmax = float(rmax)
        self.m = m
        self.rays = [] #A list which contains all the ray objects in the bundle/beam
        
    def rtuniform(self):
        """Generates the initial positions of the rays that are uniformly spaced in polar coordinates"""
        
        for i in range(0, self.n+1):
            radius = (i * self.rmax)/self.n
        
            angle = 0.0
            if i == 0:
                    yield radius, angle
            else:
                for x in range(0, self.m*i):
                    angle = angle + (2.0*np.pi)/(self.m*i)
                    yield radius, angle
                    
    def getBundle(self, ray):
        """Creates a beam of rays which have the same direction as the ray input into this function.
        The beam is also centred around this initial ray."""
        
        rayPosition = ray.p()
        rayDirection = ray.k()
        for r, t in self.rtuniform():
            point = [(r * np.cos(t)) + rayPosition[0], (r * np.sin(t)) + rayPosition[1], rayPosition[2]]
            ray = Ray(point, rayDirection)
            self.rays.append(ray)
        return self.rays #Returns the list of rays once they have all been created