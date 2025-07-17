import spekpy as sp # Import the SpekPy library for spectral calculations
from numpy import sum # Import stuff from numpy

print('\nRunning mean coeff script')

## Generate the reference spectrum
filters = [('Be',3.0),('Al',0.208), # Filtration [mm] <-- try changing this
           ('Air',500)]
s=sp.Spek(kvp=30.,dk=0.2,th=20.) # Generate the spectrum model
s.multi_filter(filters) # Apply all the filtration in one step

## Find the homogeneity index and print
h_i = s.get_hc() 
print('\nHomogeneity index\n-----------------')
print('h_i:',round(h_i,2))

## Get the fluence, energy fluence and air kerma spectra
k, phi_k = s.get_spectrum() # Fluence spectrum 
k, psi_k = s.get_spectrum(flu=False) # Energy fluence spectrum
MuEnData = sp.Spek().muen_air_data # Access SpekPy's absorp. coeff. data
muen_over_rho = MuEnData.get_muen_over_rho_air(k)
kair_k = psi_k*muen_over_rho # Air kerma spectrum

## Calculate mean energies and print
# Fluence weighted, Eq. 4.19
kmean_phi = sum(k*phi_k)/sum(phi_k) 
# Energy fluence weighted, Eq. 4.20
kmean_psi = sum(k*psi_k)/sum(psi_k) 
 # Kerma weighted, Eq. 4.21
kmean_kair = sum(k*kair_k)/sum(kair_k)
# Print results to screen
print('\nMean energy\n-----------------')
print('Fluence weighted:',round(kmean_phi,2),'keV')
print('Energy fluence weighted :',round(kmean_psi,2),'keV')
print('Kerma weighted:',round(kmean_kair,2),'keV')

## Calculate mass energy absorption coefficient using mean energy and print
# Fluence weighted
muen_over_rho_phi = MuEnData.get_muen_over_rho_air(kmean_phi) 
# Energy fluence weighted
muen_over_rho_psi = MuEnData.get_muen_over_rho_air(kmean_psi)
# Kerma weighted
muen_over_rho_kair = MuEnData.get_muen_over_rho_air(kmean_kair)
# Print results to screen
print('\nMass energy absorption coefficient (in air) from kmean\n----------------')
print('Fluence weighted:',round(muen_over_rho_phi,3),'cm2/g')
print('Energy fluence weighted:',round(muen_over_rho_psi,3),'cm2/g')
print('Kerma weighted:',round(muen_over_rho_kair,3),'cm2/g')

## Calculate mass energy absorption coefficient using spectra and print
# Fluence weighted
muen_over_rho_phi = sum(muen_over_rho*phi_k)/sum(phi_k)
# Energy fluence weighted
muen_over_rho_psi = sum(muen_over_rho*psi_k)/sum(psi_k)
# Kerma weighted
muen_over_rho_kair = sum(muen_over_rho*kair_k)/sum(kair_k)
# Print results to screen
print('\nMass energy absorption coefficient (in air) from spectrum\n-----------------')
print('Fluence weighted:',round(muen_over_rho_phi,3),'cm2/g')
print('Energy fluence weighted:',round(muen_over_rho_psi,3),'cm2/g')
print('Kerma weighted:',round(muen_over_rho_kair,3),'cm2/g')

## Calculate mass attenuation coefficient using mean energy and print
MuData = sp.Spek().mu_data # Access SpekPy's att. coeff. data
# Using fluence weighted mean energy
mu_over_rho_phi,rho = MuData.get_mu_over_rho_composition('Air',[kmean_phi])
# Using energy fluence weighted mean energy
mu_over_rho_psi,rho = MuData.get_mu_over_rho_composition('Air',[kmean_psi])
# Using kerma weighted mean energy
mu_over_rho_kair,rho = MuData.get_mu_over_rho_composition('Air',[kmean_kair])
# Print results to screen
print('\nMass attenuation coefficient (in air) from kmean\n-----------------')
print('Fluence weighted:',round(mu_over_rho_phi[0],3),'cm2/g')
print('Energy fluence weighted:',round(mu_over_rho_psi[0],3),'cm2/g') # Eq. 4.22
print('Kerma weighted:',round(mu_over_rho_kair[0],3),'cm2/g')

## Calculate mass attenuation coefficient using spectra and print
mu_over_rho,rho = MuData.get_mu_over_rho_composition('Air',k)
# Fluence weighted
mumean_phi = sum(mu_over_rho*phi_k)/sum(phi_k)
# Energy fluence weighted
mumean_psi = sum(mu_over_rho*psi_k)/sum(psi_k)
# Kerma weighted
mumean_kair = sum(mu_over_rho*kair_k)/sum(kair_k)
# Print results to screen
print('\nMass attenuation coefficient (in air) from spectrum\n-----------------')
print('Fluence weighted:',round(mumean_phi,3),'cm2/g')
print('Energy fluence weighted:',round(mumean_psi,3),'cm2/g')
print('Kerma weighted:',round(mumean_kair,3),'cm2/g')

print('\nFinished!\n')