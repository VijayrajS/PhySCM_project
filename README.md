INSTRUCTIONS:
config.py : Contains a function to read the config file, no need of running this

init_config.py:
Generates an initial random configuration of 108 argon atoms in a 18x18x18 Ā^3 box, satisfying periodic boundary conditions (minimum image distance)
HOW TO RUN:
python init_config.py

U_minimizer.py:
Uses gradient descent to minimise potential energy between atoms from the initial_config. 
HOW TO RUN:
python U_minimizer.py
NOTE: To change the alpha or delta of the regression, go to CONFIG.txt and change the values of regressison_alpha and/or regressison_delta

frame_generator.py
Generates frames of the atoms moving, with a normal velocity distribution.
HOW TO RUN:
python frame_generator.py
NOTE: To change the temperature of the system, the time step, or the number of frames, go to CONFIG.txt and change the values of temperature, dt and/or n_frames respectively.

For the following files, the input file format is as follows: (say there are m atoms and n frames)
<Number of atoms>
<Description of system>
x11 y11 z11
x21 y21 z21
...
xm1 ym1 zm1
END 
...
x1n y1n z1n
x2n y2n z2n
...
xmn ymn zmn
END 
<--End of file-->

Where END => end of a frame
Where xij can be either position/velocity of the i'th atom in the j'th timeframe.

MSD.py
Generates the MSD plot, and prints the value of the diffusion constant. (It takes the position frame file)
HOW TO RUN:
python MSD.py <position frame file name>

VelCor.py
Generates the Velocity correlation plot, and prints the value of the diffusion constant. (It takes the velocity frame file)
HOW TO RUN:
python VelCor.py <velocity frame file name>

DSF.py
Generates the DSF plot, and prints the value of the diffusion constant. (It takes the position frame file)
HOW TO RUN:
python DSF.py <position frame file name>

Vanhove.py
Generates the VanHove plot, and prints the value of the diffusion constant. (It takes the position frame file)
HOW TO RUN:
python Vanhove.py <position frame file name>
