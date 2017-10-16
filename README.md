# Optical Ray Tracer

The ideal way to use the simulation is by running the main.py module in the terminal. This will start an input interface that easily allows the user to use the various aspects of the simulation, through a series of questions. Of course this interface has not been refined completely, so if the wrong input is made, you will just have to exit out of the module and run it again.

Initially, the interface will ask you if you want to investigate the imaging performance of a planoconvex lens. If yes, you'll be asked to input the parameters you require, and in the end will receive a plot of the RMS spot radius against diameter for the lens.

Otherwise, you will be asked if you would like to investigate the optimal biconvex lens. If yes, after the parameters have been input, the scipy optimisation function will run and return the optimal curvatures.

Finally, if the previous two options are rejected, you will be free to input the rays and lenses that you wish into the system, and after a series of questions the simulation will return all the various plots for your rays.
