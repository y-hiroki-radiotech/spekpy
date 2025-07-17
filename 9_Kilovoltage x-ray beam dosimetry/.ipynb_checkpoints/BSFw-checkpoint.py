import spekpy as sp # Import the SpekPy library for spectral calculations
from numpy import sum, load # Import stuff from numpy
from scipy.interpolate \
    import RegularGridInterpolator # Import interpolator from scipy

## Set parameters
# Geometry specs
ssd = 100. # Source-to-skin distance [cm]
d = 10. # Beam diameter at SSD [cm]
# Spectrum specifications
pot = 150. # Tube potential [kV]
hvl = 10. # First half-value layer (HVL) [mm Al]

## Import monoenergy backscatter factor data
## Note that this is the same data as in the ALL-SSDs_PHOTONS-MONO_BSFw.dat
## file. The .dat file is supplied as an extra and not used in this script
data = load('monoBSFw.npz')
SSD = data['SSD']
K = data['k']
D = data['D']
Bw = data['Bw']

## Define an interpolation function for the backscatter factor
points = (SSD, K, D)
bsf = RegularGridInterpolator(points, Bw, bounds_error=False, fill_value=0.)

# Generate the spectrum
s = sp.Spek(kvp=pot) # Generate spectrum model
t = s.get_matl(hvl=hvl) # Find the filtration necessary for specified 1st HVL
s.filter('Al',t) # Apply that filtration
k, phi_k = s.get_spectrum() # Get the fluence spectrum

## Get mass energy absorption coefficient at the energies k
MuEnData = sp.Spek().muen_air_data
muen_over_rho = MuEnData.get_muen_over_rho_air(k)

## Interpolate mono BSFvalues based on ssd, k, and d values
points = (ssd,k,d)
bsf_mono = bsf(points)

## Calculate backscatter factor (water) for the specified spectrum
bsf_Q = sum(k*phi_k*muen_over_rho*bsf_mono)/sum(k*phi_k*muen_over_rho)

## Print the factor and inputs to screen
print('\nBw(Q):', bsf_Q,'\n')
print('SSD =',ssd,'cm')
print('Diameter =',d,'cm')
print('Tube potential =',pot,'kV')
print('HVL1 =',hvl,'mm Al')


