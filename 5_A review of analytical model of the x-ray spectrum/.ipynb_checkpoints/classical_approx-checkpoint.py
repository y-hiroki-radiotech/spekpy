import spekpy as sp # Import the SpekPy library for spectral calculations
import matplotlib.pyplot as plt # Import pyplot for plotting
from numpy import pi, sqrt, sum, arange, zeros, rad2deg, arctan, finfo \
    # Import stuff from numpy

eps = finfo(float).eps # Floating point accuracy for float64

## Setting choices
pot = 100. # Tube potential [kV] <-- try changing this
theta = 12. # Anode angle [deg.]
dx = 2. # Increment in lateral direction (= 0.5 in book figures) [cm]
z = 100. # Source-to-dector distance [cm]
dk = 0.5  # Width of energy bin [keV] 

## Constants
m = 9.1094e-31 # Electron mass [kg]
c = 2.998e8 # Speed of light [m/s]
hbar = 6.626e-34/(2e0*pi) # Reduced Planck constant [J/Hz]
re = 2.81794e-15 # Classical electron radius [m]
L = 6. # Logarithm term (according to Kramers)
Z = 74 # Atomic number of tungsten
keV_per_J = 1e-3*(1.602e-19)**-1 # Conversion of J to keV
mAs_per_e = 1e3*1.602e-19 # Conversion of electrons to mAs
B = (keV_per_J**-1)*(4./(3.*sqrt(3.)*c*hbar))*re/L # Eq. 5.10

## Get KQP fluence spectrum
## Bremsstrahlung only (char=False) and ...
## no oblique paths through filtration (obli=False)
s = sp.Spek(th=theta,kvp=pot,physics='kqp',char=False,obli=False)
k,phis0_k = s.get_spectrum(addend=True) # Unfiltered spectrum
s.filter('Al',1.)
k,phis1_k = s.get_spectrum(addend=True) # Filtered spectrum
phis1 = s.get_flu() # Integrated fluence

## Get classical fluence spectrum with Kramers' thin target cross-section
## Bremsstrahlung only (char=False) and ...
## no oblique paths through filtration (obli=False) 
t = sp.Spek(th=theta,kvp=pot,physics='classical',char=False,obli=False)
t.filter('Al',1.)
k,phit1_k = t.get_spectrum(addend=True)
phit1 = t.get_flu()

## Get Kramers-Whiddington fluence spectrum
## Only bremsstrahlung model available
phiu0_k = Z*mAs_per_e**-1*((B/(4.*pi*z**2))*(pot-k)/k) # Eq. 5.11 [cm-2 keV-1 mAs-1]
attn_fac = phis1_k/(phis0_k+eps) # Energy dependent attenuation factor ...
# The eps is included to avoid a division of a zero by zero
phiu1_k = phiu0_k*attn_fac 
phiu1 = sum(phiu1_k*dk)

## Plot the fluence-normalized spectra
fig1, (ax1) = plt.subplots(nrows=1,ncols=1)
ax1.plot(k, phiu1_k/phiu1,'0.0',label='Kramers-Whiddington')
ax1.plot(k, phit1_k/phit1,'0.5',label='SpekPy (classical)')
ax1.plot(k, phis1_k/phis1,'0.0',linestyle='dashed',label='SpekPy (kqp)')
ax1.set_ylabel('Normalized fluence spectrum  [keV$^{-1}$]',fontsize=12)
ax1.set_ylabel('Normalized fluence spectrum  [keV$^{-1}$]',fontsize=12)
ax1.legend(frameon=False,fontsize=12,loc='upper right')
ax1.tick_params(axis='both', which='major', labelsize=12)
ax1.set_xlim((10.,pot))
ax1.set_xlabel('Bremsstrahlung energy  [keV]',fontsize=12)

## Get absolute fluence profile predictions
x = arange(-25.,25.,dx) # Define positions in anode-cathode direction [cm]
phis=zeros(x.shape)
phit=zeros(x.shape)
phiu=zeros(x.shape)
for i in range(x.size): # Loop through positions and get fluences
  if rad2deg(arctan(x[i]/z)) > -theta: # Check rays escape the anode
    s.set(x=x[i]) # Set the x position
    t.set(x=x[i]) # Set the x position
    phis[i] = s.get_flu() # Get KQP fluence
    phit[i] = t.get_flu() # Get classical fluence
    phiu[i] = phiu1*z**2/(z**2+x[i]**2) # Get Kramers-Whiddington fluence
  else: # Set fluences to zero if x-rays can't escape the anode
    phis[i]=0.
    phit[i]=0.
    phiu[i]=0.

## Plot absolute fluence profiles
fig2, (ax2) = plt.subplots(nrows=1,ncols=1)
ax2.ticklabel_format(useMathText=True)
ax2.plot(x,phiu,'0.0',label="Kramers-Whiddington")
ax2.plot(x,phit,'0.5',label="SpekPy (classical)")
ax2.plot(x,phis,'0.0',linestyle='dashed',label="SpekPy (kqp)")
ax2.legend(frameon=False,fontsize=12,loc='lower right')
ax2.set_xlabel('Off-axis position (anode-cathode direction)  [cm]',fontsize=12)
ax2.set_ylabel('Fluence  [cm$^{-2}$]',fontsize=12)
ax2.tick_params(axis='both', which='major', labelsize=12)
ax2.set_xlim((-25.,25.))

## Show plots on screen
plt.show()

