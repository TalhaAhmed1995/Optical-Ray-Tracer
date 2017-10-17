# Optical Ray Tracer

The ideal way to use the simulation is by running the `main.py` module in the terminal. This will start an input interface that easily allows the user to use the various aspects of the simulation, through a series of questions. Of course this interface has not been refined completely, so if the wrong input is made, you will just have to exit out of the module and run it again.

Initially, the interface will ask you if you want to investigate the imaging performance of a planoconvex lens. If yes, you'll be asked to input the parameters you require, including the position of the lens on the z-axis, `z0`, along with `aperture`, `curvature` and the refractive indices one either side of the optical system, `n1` (on the left) and `n2` (on the right). In the end you will receive a plot of the RMS spot radius against diameter for the lens.

Otherwise, you will be asked if you would like to investigate the optimal biconvex lens. If yes, after the parameters have been input, the `scipy` optimisation function will run and return the optimal curvatures.

Finally, if the previous two options are rejected, you will be free to input the rays and lenses that you wish into the system, and after a series of questions the simulation will return all the various plots for your rays.

## Example Outputs

The following are some of the outputs that can be received from the simulation. Note that the lens cannot be seen directly, but can be identified from the points where the light rays bend.

![2D visualitation of light rays (cyan lines) incoming from left to right.](/images/optimal_lens_2d.png?raw=true)
![3D visualitation of the light rays in the same setup.](/images/optimal_lens_3d.png?raw=true)
![Input plane of the beam of light rays. Each dot represents an individual light ray.](/images/optimal_lens_input.png?raw=true)
![Output plane of the beam of light rays. Also gives RMS spread of the spot.](/images/optimal_lens_output.png?raw=true)
