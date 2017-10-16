import numpy as np
import raytracer as rt
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

class Plot():
    """A class which allows the rays to be plotted in various formats"""
    
    def __init__(self, rays):
        self.__rays = rays
        if not(isinstance(rays, list)):
            self.__rays = [rays]
    
    def rms(self):
        """Calculates the RMS spot radius for a bundle of rays at the output"""
        
        radiusSquareSum = 0.0
        numberOfPoints = len(self.__rays)
        centralRay = self.__rays[0].p()
        for ray in self.__rays:
            rayPosition = ray.p()
            x = rayPosition[0]
            y = rayPosition[1]
            radiusSquare = (float(x) - float(centralRay[0]))**2 + (float(y) - float(centralRay[1]))**2 
            radiusSquareSum += radiusSquare
        radiusSquareMean = radiusSquareSum/float(numberOfPoints)
        RMS = np.sqrt(radiusSquareMean)
        return RMS
            
    def plotRays2D(self):
        """Plots the trajectories of the rays in 2D"""
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for ray in self.__rays:
            points = ray.vertices()
            if np.isnan(points[-1][0]): #Checking to see if any rays have been terminated
                pass
            else:
                x, z = [], []
                for i in points:
                    x.append(i[0])
                    z.append(i[2])
                ax.set_xlabel('z axis')
                ax.set_ylabel('x axis')
                ax.set_title('RayTracer 2D')
                plt.grid(True)
                ax.plot(z, x, 'darkcyan')
            
    
    def plotRays3D(self):
        """Plots the trajectories of the rays in 3D"""
        
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.set_xlabel('z axis')
        ax.set_ylabel('y axis')
        ax.set_zlabel('x axis')
        ax.set_title('Ray Tracer 3D')
        
        for ray in self.__rays:
            points = ray.vertices()
            if np.isnan(points[-1][0]): #Checking to see if any rays have been terminated
                pass
            else:
                x, y, z = [], [], []
                for i in points:
                    x.append(i[0])
                    y.append(i[1])
                    z.append(i[2])
                ax.plot3D(z, y, x, 'darkcyan')
            
    def plotInput(self):
        """Plots the x and y postions of the rays at their initial positions"""
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x, y = [], []
        for ray in self.__rays:
            points = ray.vertices()
            x.append(points[0][0])
            y.append(points[0][1])
        ax.set_xlabel('x axis')
        ax.set_ylabel('y axis')
        ax.set_title('Input Plane')
        plt.grid(True)
        ax.scatter(x, y)
        
    def plotOutput(self):
        """Plots the x and y postions of the rays at their final positions (usually the output plane)"""
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x, y = [], []
        for ray in self.__rays:
            points = ray.vertices()
            if np.isnan(points[-1][0]):
                pass
            else:
                x.append(points[-1][0])
                y.append(points[-1][1])
        ax.set_xlabel('x axis')
        ax.set_ylabel('y axis')
        ax.set_title('Output Plane')
        plt.grid(True)
        ax.scatter(x, y)
        
        RMS = self.rms()
        #The plot is annotated with the RMS spot radius of the output
        ax.annotate('RMS: %f'% RMS, xy = (0.7, 0.9), xycoords='axes fraction', xytext= (0.7, 0.9), textcoords ='axes fraction')
        print 'RMS: ', RMS
        return RMS