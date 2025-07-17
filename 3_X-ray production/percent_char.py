import spekpy as sp # Import the SpekPy library for spectral calculations
import matplotlib.pyplot as plt # Import pyplot for plotting
from numpy import arange # Import stuff from numpy

## Set parameters
# Define arrays with filtration tuples
filters = [('Be',3.0),('Al',0.208), # Filtration [mm] <-- try changing this
           ('Air',500.)] 
# Define array with tube potentials (20 to 300 kV)
kV_set = arange(20., 301., 10.)
# Define anode angle [deg.]
theta = 12.

## Generate a list of the percentages of fluence due to characteristic x-rays
## There is one list item per kV value in kV_set
per = [] # Define an empty list
for kvp in kV_set: # Iterate through tube potentials
    s = sp.Spek(kvp=kvp,th=theta) # Generate the spectrum
    s.multi_filter(filters) # Apply filtration
    phi_tot = s.get_flu() # Get total fluence
    s.set(brem=False) # Set the bremsstrahlung component to zero
    phi_char = s.get_flu() # Get the characteristic fluence
    per.append(100.*phi_char/phi_tot) # Append percentage to list
    
## Plot the percentage against kV
plt.plot(kV_set,per) 
plt.xlabel('Tube potential  [kV]')
plt.ylabel('Perecentage of fluence  [%]')
plt.title('Percent of fluence from characteristic emissions')

## Show plots on screen
plt.show()
    


