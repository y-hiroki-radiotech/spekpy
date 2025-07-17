import spekpy as sp # Import the SpekPy library for spectral calculations
import matplotlib.pyplot as plt # Import pyplot for plotting

## Set tube specifications
pot = 70. # Tube potential [kV]
theta = 20. # Takeoff/anode angle [deg.]
filters = [('Be',1.0),('Al',2.5),('Air',950.)] # Filtration [mm]

## Calculate fluence spectra for various models
# Instant electron DIFFusion with uniform bremsstrahlung
d = sp.Spek(kvp=pot,th=theta,physics='diff') # Generate model
d.multi_filter(filters) # Apply filtrations
k, phid_k = d.get_spectrum() # Get differential fluence spectrum
# UNIform bremsstrahlung angular distribution
u = sp.Spek(kvp=pot,th=theta,physics='uni')
u.multi_filter(filters)
k, phiu_k = u.get_spectrum()
# SIMple bremsstrahlung angular distribution
s = sp.Spek(kvp=pot,th=theta,physics='sim')
s.multi_filter(filters)
k, phis_k = s.get_spectrum()
# Kissel-Quarles-Pratt bremsstrahlung angular distribution
q = sp.Spek(kvp=pot,th=theta,physics='kqp')
q.multi_filter(filters)
k, phiq_k = q.get_spectrum()

## Plot the spectra
plt.plot(k,phid_k,'0.0',linestyle='dashed',label='diff')
plt.plot(k,phiu_k,'0.5',label='uni')
plt.plot(k,phis_k,'0.5',linestyle='dashed',label='sim')
plt.plot(k,phiq_k,'0.0',label='kqp')
plt.xlabel('Energy  [keV]')
plt.ylabel('Differential fluence  [cm$^{-2}$ keV$^{-1}$]')
plt.legend(frameon=False,loc='upper left')
plt.title('Four physics models')

## Get the first half-value-layers (HVLs)
hvld = d.get_hvl()
hvlu = u.get_hvl()
hvls = s.get_hvl()
hvlq = q.get_hvl()

## Print the HVL values to screen
print('\nFirst half-value-layers\n')
print('HVL_1(diff):',hvld,'mm Al')
print('HVL_1(uni):',hvlu,'mm Al')
print('HVL_1(sim):',hvls,'mm Al')
print('HVL_1(kqp):',hvlq,'mm Al')

# Show plot on screen
plt.show()
