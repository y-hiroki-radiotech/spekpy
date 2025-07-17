import spekpy as sp # Import the SpekPy library for spectral calculations
import matplotlib.pyplot as plt # Import pyplot for plotting
from numpy import rad2deg, arctan, zeros, arange # Import stuff from numpy

## Set parameters
t = 2.5 # Thickness of aluminium filtration [mm] <-- try changing this
pot = 80. # Tube potential for spectra [kV]
th1 = 12. # Low anode angle [deg.]
th2 = 24. # High anode angle [deg.]

## Generate two spectra at different anode angles
# Low anode angle spectrum
s1=sp.Spek(kvp=pot,th=th1) # Create spectrum
s1.filter('Al',t) # Apply filtration
# High anode angle spectrum
s2=sp.Spek(kvp=pot,th=th2) # Create spectrum
s2.filter('Al',t) # Apply filtration

## Generate fluence profiles (anode-cathode direction)
z = 100. # Source-to-detector distance (default SpekPy value) [cm]
x=arange(-45.,45.,1.) # Array of x-axis positions (anode-cathode dir.) [cm]
phi1=zeros(x.shape) # Preallocate arrays for low angle spectrum
phi2=zeros(x.shape) # Preallocate arrays for high angle spectrum

for i in range(x.size): # Loop through all x positions
  # if-statement to check whether the x-rays can escape the anode
  if rad2deg(arctan(x[i]/z)) > -th1: 
    s1.set(x=x[i]) # If the x-ray can escape the anode, set the x value
    phi1[i]=s1.get_flu() # And get the total integrated fluence at x
  else:
    phi1[i]=0. # If cannot escape the anode, set fluence to zero   
  # if-statement to check whether the x-rays can escape anode
  if rad2deg(arctan(x[i]/z)) > -th2:
    s2.set(x=x[i]) # If the x-ray can escape the anode, set the x value
    phi2[i]=s2.get_flu() # And get the total integrated fluence at x
  else:
    phi2[i]=0. # If cannot escape the anode, set fluence to zero

## Plot the spectra 
fig1, (ax1) = plt.subplots(nrows=1,ncols=1)
ax1.ticklabel_format(useMathText=True)
ax1.plot(x,phi1,'0.0',label="Anode angle: 12$^\circ$")
ax1.plot(x,phi2,'0.5',label="Anode angle: 24$^\circ$")
ax1.legend(frameon=False,fontsize=12,loc='lower right')
ax1.set_xlabel('Off-axis position (anode-cathode direction)  [cm]',fontsize=12)
ax1.set_ylabel('Fluence  [cm$^{-2}$]',fontsize=12)
ax1.tick_params(axis='both', which='major', labelsize=12)
ax1.set_xlim((-45.,45.))

## Show plots on screen
plt.show()