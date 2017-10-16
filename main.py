import raytracer as rt
import optics2 as op
import plotting as pt
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as so


class Main:
    """A class which utilises an input interface so that the user may select which parts of the simulation to use."""      
    
    def plotRays(self, rayVectors):
        """A function which shows all the various plots of the rays"""
        
        plot = pt.Plot(rayVectors)
        plot.plotRays2D()
        plot.plotRays3D()
        plot.plotInput()
        plot.plotOutput()
        plt.show()
        
    def planoConvex(self, lens1, lens2, diameters):
        """A function which calculates and plots the RMS spot radius for the range of diameters input"""
        
        lenses = [lens1, lens2]
        testRay = rt.Ray([0.1,0,0], [0,0,1])
        
        for lens in lenses:
            lens.propagateRay(testRay)
            
        output = lenses[-1].paraxial(testRay) #Setting the output plane at the paraxial focus of the setup
        lenses.append(output)
        focalLength = output.getz() - ((lens1.getz0() + lens2.getz0())/2) #Calculating the focal length of the lens
        wavelength = 588e-6 #The wavelength of the light is 588nm (The units used in the simulation are mm)
        ray = rt.Ray([0,0,0], [0,0,1])
        diameterList = []
        RMSList = []
        diffractionList = []
        
        for i in diameters:
            diameterList.append(i)
            rays = rt.Bundle(10, i/2, 10).getBundle(ray) #Creating a bundle of rays for each diameter
            for lens in lenses:
                lens.propagateBundle(rays) #Propagating the rays through the lenses
            plot = pt.Plot(rays)
            RMS = plot.rms() #Calculating the RMS spot radius of the rays at the output for each diameter
            RMSList.append(RMS)
            diffractionLimit = (focalLength * wavelength)/i #Also calculating the diffraction scale for each diameter
            diffractionList.append(diffractionLimit)
            
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel('Diameter (mm)')
        ax.set_ylabel('RMS (mm)')
        ax.set_title('Diffaction Limit')
        plt.grid(True)
        ax.plot(diameterList, RMSList, 'green') #Plotting the RMS spot radius against diameter
        ax.plot(diameterList, diffractionList, 'red') #Plotting the diffraction scale against diameter
        
        RMSValues = np.array(RMSList, dtype='float')
        diffractionValues = np.array(diffractionList, dtype='float')
        difference = (diffractionValues - RMSValues).tolist()
        difference = [abs(i) for i in difference] #Calculating the differences between the RMS spot radius and the diffraction scale at each diameter
        
        index = difference.index(min(difference))
        intersection = diameterList[index] #Finding the point on the graph where the difference between the two functions is a minimum, and taking this to be the intersection point of the two plots.
        print 'Intersection is: ', intersection
        
    def optimalRMS(self, curvatures):
        """A function which calculates and returns the log of the RMS spot radius for two given curvatures of a biconvex lens"""
        
        lens1 = op.SphericalRefraction(100, 20, curvatures[0], 1, 1.5168)
        lens2 = op.SphericalRefraction(105, 20, curvatures[1], 1.5168, 1)
        output = op.OutputPlane(200) #The output plane is set at z=200mm
        lenses = [lens1, lens2, output]
        
        ray = rt.Ray([0,0,0], [0,0,1])
        rays = rt.Bundle(10, 5, 10).getBundle(ray) #A bundle of rays is created
        
        for lens in lenses:
            lens.propagateBundle(rays) #The rays are propagated through the biconvex lens
        plot = pt.Plot(rays)
        RMS = plot.rms() #Calculating the RMS spot radius of the rays at the output for the given curvatures
        log = np.log(RMS)
        return log
        
    def run(self):
        """This function provides an input interface for the user when the module is imported into the terminal"""
        
        terminate = False
        #Asking the user if they want to investigate the performance of a planoconvex lens
        planoConvexInput = raw_input("Do you want to investigate the imaging performance of a planoconvex lens? (Yes or No).\n")
        planoConvexInput = planoConvexInput.lower()
        if 'y' in planoConvexInput:
            #If yes, the user is asked to input the parameters for the two sides of their planoconvex lens, along with the range of diameters to investigate
            terminate = True #The interface will be terminated after the user has input all the parameters for the planoconvex investigation
            lens1Input = raw_input("Enter z0, aperture, curvature, n1 and n2 values for your first lens, separated by commas.\n")
            lens1Input = lens1Input.split(",")
            lens1Input = [float(coordinate) for coordinate in lens1Input]
            lens1 = op.SphericalRefraction(lens1Input[0], lens1Input[1], lens1Input[2], lens1Input[3], lens1Input[4])
            
            lens2Input = raw_input("Enter z0, aperture, curvature, n1 and n2 values for your second lens, separated by commas.\n")
            lens2Input = lens2Input.split(",")
            lens2Input = [float(coordinate) for coordinate in lens2Input]
            lens2 = op.SphericalRefraction(lens2Input[0], lens2Input[1], lens2Input[2], lens2Input[3], lens2Input[4])
            
            rangeInput = raw_input("Enter the lower limit and upper limit for the range of diameters you want to investigate, followed by the incremental variation.\n")
            rangeInput = rangeInput.split(",")
            rangeInput = [float(coordinate) for coordinate in rangeInput]
            
            self.planoConvex(lens1, lens2, np.arange(rangeInput[0], rangeInput[1] + rangeInput[2], rangeInput[2]))
            plt.show()
            
        if terminate == False:
            #Asking the user if they want to find the optimal biconvex lens
            biConvexInput = raw_input("Do you want to find the optimal biconvex lens? (Yes or No).\n")
            biConvexInput = biConvexInput.lower()
            if 'y' in biConvexInput:
                #If yes, the user is asked to input the parameters required for the scipy optimiser function
                terminate = True
                bounds1Input = raw_input("Enter the lower and upper bounds for the first side of your lens, separated by commas.\n")
                bounds1Input = bounds1Input.split(",")
                bounds1Input = [float(coordinate) for coordinate in bounds1Input]
                
                bounds2Input = raw_input("Enter the lower and upper bounds for the second side of your lens, separated by commas.\n")
                bounds2Input = bounds2Input.split(",")
                bounds2Input = [float(coordinate) for coordinate in bounds2Input]
                
                b = [(bounds1Input[0], bounds1Input[1]), (bounds2Input[0], bounds2Input[1])]
                
                curvaturesInput = raw_input("Enter the initial curvatures of the two sides of your lens.\n")
                curvaturesInput = curvaturesInput.split(",")
                curvaturesInput = [float(coordinate) for coordinate in curvaturesInput]
                
                x0 = np.array([curvaturesInput[0], curvaturesInput[1]])
                result = so.fmin_tnc(self.optimalRMS, x0, bounds=b, approx_grad=True)
                print result
            
        if terminate == False:
            allRays = [] #A list of all the rays created by the user
            moreRays = True
            while moreRays:
                #Asking the user to input the position and direction coordinates of their ray
                rayPositionInput = raw_input("Enter 3 values for ray position, separated with commas.\n")
                rayPositionInput = rayPositionInput.split(",")
                rayPositionInput = [float(coordinate) for coordinate in rayPositionInput]
                
                rayDirectionInput = raw_input("Enter 3 values for ray direction, separated by commas.\n")
                rayDirectionInput = rayDirectionInput.split(",")
                rayDirectionInput = [float(coordinate) for coordinate in rayDirectionInput]
                
                ray = rt.Ray(rayPositionInput, rayDirectionInput)
                allRays.append(ray)
                
                #Asking if the ray is to be collimated into a bundle of rays
                beamRequiredInput = raw_input("Do you want to collimate the ray into a beam of finite thickness? (Yes or No).\n")
                beamRequiredInput = beamRequiredInput.lower()
                if 'y' in beamRequiredInput:
                    #The paramters for the beam of rays are input
                    beamParametersInput = raw_input("Enter the number of circles, maximum diameter and multiplier in that order (separate them with commas).\n")
                    beamParametersInput = beamParametersInput.split(",")
                    beamParametersInput= [float(parameter) for parameter in beamParametersInput]
                    beam = rt.Bundle(int(beamParametersInput[0]), 0.5*beamParametersInput[1], int(beamParametersInput[2])).getBundle(ray)
                    for i in range(1, len(beam)):
                        allRays.append(beam[i]) #The new rays formed are appended to the list of rays
                moreRaysInput = raw_input("Do you want to add another ray/beam? (Yes or No)\n") #If the user says yes, the options are repeated so that more rays can be created
                moreRaysInput = moreRaysInput.lower()
                if 'n' in moreRaysInput:
                    moreRays = False
                    
            addLens = True
            lenses = [] #A list of all the lenses created by the user
            while addLens:
                #Asking the user to input the parameters for their lens
                lensInput = raw_input("Enter z0, aperture, curvature, n1 and n2 values for your lens.\n")
                lensInput = lensInput.split(",")
                lensInput = [float(coordinate) for coordinate in lensInput]
                
                lens = op.SphericalRefraction(lensInput[0], lensInput[1], lensInput[2], lensInput[3], lensInput[4])
                lenses.append(lens)
                
                #Asking the user if they want to create more lenses for the simulation
                addLensInput = raw_input("Do you want to add another lens to the system? (Yes or No).\n")
                addLensInput = addLensInput.lower()
                if 'n' in addLensInput:
                    addLens = False
            
            for lens in lenses:
                lens.propagateBundle(allRays)
            
            testRay = rt.Ray([0.1, 0, 0], [0, 0, 1])
            for lens in lenses:
                lens.propagateRay(testRay)
            output = lenses[-1].paraxial(testRay) #The output plane is set at the paraxial focus
            if output is None: #If the rays do not converge, there is no paraxial focus, so the user is asked to input the position of the output plane
                outputInput = raw_input("Your system does not have a paraxial focus. Enter the z coordinate for your Output plane.\n")
                outputInput = outputInput.split()
                outputInput = [float(coordinate) for coordinate in outputInput]
                output = op.OutputPlane(outputInput[0])
            else:
                #The user is asked if they want to keep the output at the paraxial focus
                paraxialInput = raw_input("Do you want to set your Output Plane as the paraxial focus? (Yes or No).\n")
                paraxialInput = paraxialInput.lower()
                if 'n' in paraxialInput:
                    #If no, the user is asked to input the position of the output plane
                    outputInput = raw_input("Enter the z coordinate for your Output plane.\n")
                    outputInput = outputInput.split()
                    outputInput = [float(coordinate) for coordinate in outputInput]
                    output = op.OutputPlane(outputInput[0])
                
            output.propagateBundle(allRays) #All the rays created by the user are propagated to the output plane
            
            self.plotRays(allRays) #All the plots of the simulation are shown at the end
            
        
if __name__ == "__main__": #Runs the input interface when the 'main' module is imported into the terminal
    opticalSimulation = Main()
    opticalSimulation.run()