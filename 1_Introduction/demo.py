import spekpy as sp # Import the SpekPy library for spectral calculations
import matplotlib.pyplot as plt # Import pyplot for plotting

print('\nRunning demo script (1 mAs, 100 cm)\n')

## Generate spectrum for 100 kV potential, 10 deg. anode angle & 6 mm Al filtr.
s=sp.Spek(kvp=100.,th=10.) # Create the spectrum model
s.filter('Al',6.) # Add the filtration [mm]
k, phi_k = s.get_spectrum(edges=True) # Get arrays of energy & fluence spectrum

## Calculate metrics (1 mAs, 100 cm source-to-detector distance)
hvl1 = s.get_hvl1() # Get 1st HVL
hvl2 = s.get_hvl2() # Get 2nd HVL
kair = s.get_kerma() # Get air kerma 
phi = s.get_flu() # Get total fluence

## Print metrics to screen
print('HVL1:',round(hvl1,2),'mm Al')
print('HVL2:',round(hvl2,2),'mm Al') 
print('Kair:',round(kair,2),'uGy') 
print('Fluence:',"{:e}".format(phi),'cm-2') 

## Plot the x-ray spectrum
plt.plot(k, phi_k)
plt.xlabel('Energy  [keV]')
plt.ylabel('Differential fluence  [cm$^{-2}$ keV$^{-1}$]')
plt.title('An example x-ray spectrum')
plt.show()

print('\nFinished!\n')
