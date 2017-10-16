import numpy as np

class OpticalElement:
    """A class which allows optical elements/lens objects to be created"""
    
    def propagateRay(self, ray):
        """Propagate a ray through the optical element"""
        
        raise NotImplementedError()
        
    def propagateBundle(self, bundle):
        """Propagates each ray in a bundle through the optical element"""
        
        for ray in bundle:
            self.propagateRay(ray)
            
class SphericalRefraction(OpticalElement):
    """A subclass of OpticalElement which allows spherical refracting lenses to be created"""
    
    def __init__(self, z0, aperture, curvature, n1, n2):
        self.__z0 = float(z0)
        self.__curvature = float(curvature)
        self.__aperture = float(aperture)
        self.__n1 = float(n1)
        self.__n2 = float(n2)
        if curvature != 0:
            self.__radius = 1/float(curvature)
            self.__centre = np.array([0, 0, self.__z0 + self.__radius], dtype ='float')
        
    def __repr__(self):
        """Returns a representation of the lens object along with its parameters"""
        
        return "%s(Intercept = %g, Curvature = %g, Aperture = %g, Refractive Indices = %g, %g )" % ("Spherical Lens", self.__z0, self.__curvature, self.__aperture, self.__n1, self.__n2)
            
    def __str__(self):
        """Prints the parameters of the lens object"""
        
        return "(Intercept = %g, Curvature = %g, Aperture = %g, Refractive Indices = %g, %g )" % (self.__z0, self.__curvature, self.__aperture, self.__n1, self.__n2)
        
    def getIntercept(self, ray):
        """Calculates the intercept of a ray with the optical element"""
        
        rayPosition = ray.p()
        rayDirection = ray.k()
        if rayPosition[2] > self.__z0:
            #If the z component of the ray is greater than the intercept of the optical element on the optical axis, an exception is raised.
            #This simulation only works with rays that start off to the left of the optical element (z < z0)
            raise Exception('The z component of your ray position must be less than the intercept of the lens with the z-axis')
        if rayDirection[2] <= 0:
            return None #If the ray is travelling such that its z direction component is less than zero, it won't intersect with the lens
        if self.__curvature != 0:
            r = rayPosition - self.__centre
            factor = (np.dot(r, rayDirection))**2 - (np.dot(r, r) - (self.__radius)**2)
            if factor < 0:
                return None #If the square root factor is less than zero, mathematically there is no intercept with the sphere
            else:
                length1 = -(np.dot(r, rayDirection)) - np.sqrt(factor)
                length2 = -(np.dot(r, rayDirection)) + np.sqrt(factor)
                intercept1 = rayPosition + (float(length1) * rayDirection) #Calculating both possible intercepts of the ray with the sphere
                intercept2 = rayPosition + (float(length2) * rayDirection)
                intercept1Radius = np.round(np.sqrt((intercept1[0])**2 + (intercept1[1])**2), 6) #Also calculating the radial distance of the intercept from the optical axis
                intercept2Radius = np.round(np.sqrt((intercept2[0])**2 + (intercept2[1])**2), 6)
            if self.__curvature > 0:
                intercept = intercept1 #This corresponds to z0 < centre of sphere. The first intercept is therefore required.
                interceptRadius = intercept1Radius
                if interceptRadius <= self.__aperture: #Checking to see that the intercept is less than the lens aperture
                    return intercept
                else:
                    return None #There is no intersection if the intercept is greater than the aperture
            elif self.__curvature < 0:
                intercept = intercept2 #This corresponds to z0 > centre of sphere. The second intercept is required here.
                interceptRadius = intercept2Radius
                if interceptRadius <= self.__aperture:
                    return intercept
                else:
                    return None               
        elif self.__curvature == 0: #If the curvature is zero, the lens is a planar surface
            planePosition = self.__z0
            distance = planePosition - rayPosition[2]
            length = float(distance) / rayDirection[2]
            intercept = rayPosition + (length * rayDirection) #Calculating the position of the intercept
            interceptRadius = np.sqrt((intercept[0])**2 + (intercept[1])**2)
            if np.round(interceptRadius, 6) <= (self.__aperture)**2: #Checking if intercept is less than the aperture
                return intercept
            else:
                return None
                    
    def refractRay(self, incident, normal, n1, n2):
        """Calculates the refracted direction of a ray which intercepts with the optical element"""
        
        cosine = -(np.dot(incident, normal)) #Cosine of the incident angle
        incidentAngle = np.arccos(cosine)
        sine = np.sin(incidentAngle) #Sine of incident angle
        relativeIndex = n1/n2
        
        if sine > (1/relativeIndex): #This means that there is total internal reflection
            return None
        else:
            trigFactor = ((relativeIndex)**2) * (1 - (cosine)**2)
            refractedDirection = (relativeIndex * incident) + (((relativeIndex * cosine) - np.sqrt(1 - trigFactor)) * normal) #Calculating the refracted direction vector
            unitRefractedDirection = refractedDirection / np.linalg.norm(refractedDirection) #The new direction vector is normalised
            return unitRefractedDirection
           
    def propagateRay(self, ray):
        """Propagates a ray through the optical element by calculating the intercept then refracting it."""
        
        intercept = self.getIntercept(ray)
        rayDirection = ray.k()
        
        if intercept is None:
            #If there is no intercept, the ray is terminated by making all components 'None'
            rayDirection = [None, None, None]
            rayPosition = [None, None, None]
            ray.append(rayPosition, rayDirection)
            return
            
        if self.__curvature > 0:
            normal = intercept - self.__centre #Calculating the vector normal to the surface is dependent on the curvature
        elif self.__curvature < 0:
            normal = self.__centre - intercept
        elif self.__curvature == 0:
            normal = np.array([0, 0, -1], dtype ='float')
            
        unitNormal = normal / np.linalg.norm(normal) #The normal to the surface must be a unit vector
        refractedDirection = self.refractRay(rayDirection, unitNormal, self.__n1, self.__n2) #Calculating the refracted direction
        if refractedDirection is None:
            #If there is no refracted direction i.e. TIR, the ray is terminated by making all components 'None'
            rayDirection = [None, None, None]
            rayPosition = [None, None, None]
            ray.append(rayPosition, rayDirection)
        else:
            ray.append(intercept, refractedDirection) #Appending the intercept and refracted direction to the ray object that is being propagated through the lens
            return ray
    
    def paraxial(self, ray):
        """Calculates the position of the paraxial focus for a given lens"""
        
        rayPosition = ray.p()
        rayDirection = ray.k()
        if rayDirection[0] >= 0 or np.isnan(rayDirection[0]): #If the ray diverges there will be no paraxial focus
            return None
        else:
            distance = rayPosition[0]
            length = float(distance) / rayDirection[0]
            paraxialFocus = rayPosition - (length * rayDirection) #The paraxial focus is where the paraxial ray x and y positions are at/close to zero
            print 'Paraxial Focus: ', paraxialFocus
            output = OutputPlane(paraxialFocus[2]) #Setting the output plane at the paraxial focus
            return output
        
    def getz0(self):
        """Returns the intercept of the lens with the z axis"""
        
        return self.__z0
             
class OutputPlane(OpticalElement):
    """A subclass which creates an output plane to view the rays which have been propagated through the optical elements."""
    
    def __init__(self, z):
        self.__plane = float(z)
        
    def getPlaneIntercept(self, ray):
        """Calculates the intercept of the ray with the output plane"""
        
        rayPosition = ray.p()
        rayDirection = ray.k()
        if np.isnan(rayPosition[0]):
            return None
        else:
            distance = self.__plane - rayPosition[2]
            length = float(distance) / rayDirection[2]
            planeIntercept = rayPosition + (length * rayDirection)
            return planeIntercept
        
    def propagateRay(self, ray):
        """Propagates the ray to the output plane"""
        
        planeIntercept = self.getPlaneIntercept(ray)
        if planeIntercept is None:
            return None
        else:
            rayDirection = ray.k()
            ray.append(planeIntercept, rayDirection)
            
    def getz(self):
        """Returns the position of the output plane along the z axis"""
        
        return self.__plane