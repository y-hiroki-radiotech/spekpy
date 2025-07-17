import spekpy as sp # Import the SpekPy library for spectral calculations
from numpy import mean, std # Import stuff from numpy

print('\nAnalyzing BIPM spectra')

## SpekPy physics parameters
physics = 'kqp' # Physics model
source = 'pene' # Attenuation coefficient source

## Hardcoded standard spectra definitions. See Kessler and Burns (2018)
## https://www.bipm.org/en/publications/rapports-bipm
# Create empty dictionary for spectra specifications
spek_dct = {}
# Add spectra dictionaries to the the dictionary: W low spectra
spek_dct['BIPM30']={'kV':30.,'th':20.,
                    'Be':3.,'Al':0.208,'Cu':0.,'Mo':0.,'Air':500.,
                    'hvl1':0.169}
spek_dct['BIPM25']={'kV':25.,'th':20.,
                    'Be':3.,'Al':0.372,'Cu':0.,'Mo':0.,'Air':500.,
                    'hvl1':0.242}
spek_dct['BIPM50a']={'kV':50.,'th':20.,
                     'Be':3.,'Al':1.008,'Cu':0.,'Mo':0.,'Air':500.,
                     'hvl1':1.017}
spek_dct['BIPM50b']={'kV':50.,'th':20.,
                     'Be':3.,'Al':3.989,'Cu':0.,'Mo':0.,'Air':500.,
                     'hvl1':2.262}
# Add spectra dictionaries to the the dictionary: W low spectra. moly filtr.
spek_dct['BIPM23M']={'kV':23.,'th':20.,
                     'Be':3.0,'Al':0.0,'Cu':0.0,'Mo':0.06,'Air':500.,
                     'hvl1':0.332}
spek_dct['BIPM25M']={'kV':25.,'th':20.,
                     'Be':3.,'Al':0.,'Cu':0.,'Mo':0.06,'Air':500.,
                     'hvl1':0.342}
spek_dct['BIPM28M']={'kV':28.,'th':20.,
                     'Be':3.,'Al':0.,'Cu':0.,'Mo':0.06,'Air':500.,
                     'hvl1':0.355}
spek_dct['BIPM30M']={'kV':30.,'th':20.,
                     'Be':3.,'Al':0.,'Cu':0.,'Mo':0.06,'Air':500.,
                     'hvl1':0.364}
spek_dct['BIPM35M']={'kV':35.,'th':20.,
                     'Be':3.,'Al':0.,'Cu':0.,'Mo':0.06,'Air':500.,
                     'hvl1':0.388}
spek_dct['BIPM40M']={'kV':40.,'th':20.,
                     'Be':3.,'Al':0.,'Cu':0.,'Mo':0.06,'Air':500.,
                     'hvl1':0.417}
spek_dct['BIPM50M']={'kV':50.,'th':20.,
                     'Be':3.,'Al':0.,'Cu':0.,'Mo':0.06,'Air':500.,
                     'hvl1':0.489}
# Add spectra dictionaries to the the dictionary: W high spectra
spek_dct['BIPM100']={'kV':100.,'th':20.,
                     'Be':3.,'Al':3.431,'Cu':0.,'Mo':0.,'Air':1150.,
                     'hvl1':0.149}
spek_dct['BIPM135']={'kV':135.,'th':20.,
                     'Be':3.,'Al':2.228,'Cu':0.232,'Mo':0.,'Air':1150.,
                     'hvl1':0.489}
spek_dct['BIPM180']={'kV':180.,'th':20.,
                     'Be':3.,'Al':2.228,'Cu':0.485,'Mo':0.,'Air':1150.,
                     'hvl1':0.977}
spek_dct['BIPM250']={'kV':250.,'th':20.,
                     'Be':3.,'Al':2.228,'Cu':1.57,'Mo':0.,'Air':1150.,
                     'hvl1':2.484}

## Calculate results for each spectrum
per_err_1 = []
for spectrum in spek_dct.items(): # Iterate through the spectra
    # Extract the spectrum parameters for the particular spectrum
    key = spectrum[0]
    dct = spectrum[1]
    pot = dct['kV']
    theta = dct['th']
    hvl1_ref = dct['hvl1']
    # Generate the spectrum
    s = sp.Spek(kvp=pot,th=theta,physics=physics,mu_data_source=source) 
    tube_filt=[('Be',dct['Be']), ('Al',dct['Al']), ('Cu',dct['Cu']), 
               ('Mo',dct['Mo']),('Air',dct['Air'])]
    s.multi_filter(tube_filt)
    # Get the 1st half-value layer in mm Cu or mm Al
    if pot>50.: # If the condition is satisfied, HVL1 is specified in mm Cu
        hvl1 = s.get_hvl1(matl='Cu')
    else: # Otherwise HVL1 specified in mm Al
        hvl1 = s.get_hvl1(matl='Al')   
    # Percentage error
    per_err_1.append(100.*(hvl1-hvl1_ref)/hvl1_ref)
    # Define and print output string for the spectrum
    if pot>50.: # If the condition is satisfied, HVL1 is specified in mm Cu
        strout = '\n' + key + ' \nHVL1='+str(round(hvl1,3)) + \
            ' mm Cu, HVL1ref=' + str(round(hvl1_ref,3)) + ' mm Cu (' + \
            str(round(100.*(hvl1-hvl1_ref)/hvl1_ref,2)) +'%)'
    else: # Otherwise HVL1 specified in mm Al
        strout = '\n' + key + ' \nHVL1='+str(round(hvl1,3)) + \
            ' mm Al, HVL1ref=' + str(round(hvl1_ref,3)) + ' mm Al (' + \
            str(round(100.*(hvl1-hvl1_ref)/hvl1_ref,2)) +'%)'    
    print(strout)
 
## Print the summary statistics (mean and std) for spectra set
print('\n\nHVL1')
print('Mean discrepancy [%] +/- std [%]:',round(mean(per_err_1),1),
      '+/-',round(std(per_err_1),1))

print('\nFinished!\n')
