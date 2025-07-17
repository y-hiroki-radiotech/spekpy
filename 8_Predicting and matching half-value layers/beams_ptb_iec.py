import spekpy as sp # Import the SpekPy library for spectral calculations
from numpy import mean, std # Import stuff from numpy

print('\nAnalyzing PTB IEC spectra')

## SpekPy physics parameters
physics = 'kqp' # Physics model
source = 'pene' # Attenuation coefficient source

## Hardcoded standard spectra definitions. See Ankerhold (2000)
## https://oar.ptb.de/resources/show/10.7795/110.20190315B
# Create empty dictionary for spectra specifications
spek_dct={}
# Add spectra dictionaries to the the dictionary: RQR spectra
spek_dct['RQR2']={'kV':40.,'th':20.,'Be':1.,'Al':2.5,'Air':950.,
                  'hvl1':1.36,'hvl2':1.72}
spek_dct['RQR3']={'kV':50.,'th':20.,'Be':1.,'Al':2.5,'Air':950.,
                  'hvl1':1.72,'hvl2':2.30}
spek_dct['RQR4']={'kV':60.,'th':20.,'Be':1.,'Al':2.5,'Air':950.,
                  'hvl1':2.02,'hvl2':2.84}
spek_dct['RQR5']={'kV':70.,'th':20.,'Be':1.,'Al':2.5,'Air':950.,
                  'hvl1':2.29,'hvl2':3.37}
spek_dct['RQR6']={'kV':80.,'th':20.,'Be':1.,'Al':2.5,'Air':950.,
                  'hvl1':2.59,'hvl2':3.96}
spek_dct['RQR7']={'kV':90.,'th':20.,'Be':1.,'Al':2.5,'Air':950.,
                  'hvl1':2.91,'hvl2':4.57}
spek_dct['RQR8']={'kV':100.,'th':20.,'Be':1.,'Al':2.5,'Air':950.,
                  'hvl1':3.23,'hvl2':5.19}
spek_dct['RQR9']={'kV':120.,'th':20.,'Be':1.,'Al':2.5,'Air':950.,
                  'hvl1':3.88,'hvl2':6.37}
spek_dct['RQR10']={'kV':150.,'th':20.,'Be':7.,'Al':2.5,'Air':950.,
                   'hvl1':5.01,'hvl2':8.15}
# Add spectra dictionaries to the the dictionary: RQA spectra
spek_dct['RQA2']={'kV':40.,'th':20.,'Be':1.,'Al':6.5,'Air':950.,
                  'hvl1':2.13,'hvl2':2.41}
spek_dct['RQA3']={'kV':50.,'th':20.,'Be':1.,'Al':12.5,'Air':950.,
                  'hvl1':3.67,'hvl2':4.05}
spek_dct['RQA4']={'kV':60.,'th':20.,'Be':1.,'Al':18.5,'Air':950.,
                  'hvl1':5.24,'hvl2':5.70}
spek_dct['RQA5']={'kV':70.,'th':20.,'Be':1.,'Al':23.5,'Air':950.,
                  'hvl1':6.64,'hvl2':7.16}
spek_dct['RQA6']={'kV':80.,'th':20.,'Be':1.,'Al':28.5,'Air':950.,
                  'hvl1':7.96,'hvl2':8.50}
spek_dct['RQA7']={'kV':90.,'th':20.,'Be':1.,'Al':32.5,'Air':950.,
                  'hvl1':9.03,'hvl2':9.57}
spek_dct['RQA8']={'kV':100.,'th':20.,'Be':1.,'Al':36.5,'Air':950.,
                  'hvl1':9.93,'hvl2':10.47}
spek_dct['RQA9']={'kV':120.,'th':20.,'Be':1.,'Al':42.5,'Air':950.,
                  'hvl1':11.37,'hvl2':11.97}
spek_dct['RQA10']={'kV':150.,'th':20.,'Be':7.,'Al':50.0,'Air':950.,
                   'hvl1':12.97,'hvl2':13.66}

## Calculate results for each spectrum
per_err_1 = []
per_err_2 = []
for spectrum in spek_dct.items(): # Iterate through the spectra
    # Extract the spectrum parameters for the particular spectrum
    key = spectrum[0]
    dct = spectrum[1]
    pot = dct['kV']
    theta = dct['th']
    hvl1_ref = dct['hvl1']
    hvl2_ref = dct['hvl2']
    # Generate the spectrum
    s = sp.Spek(kvp=pot,th=theta,physics=physics,mu_data_source=source) \
        .filter('Kapton Polyimide Film',250e-3)
    tube_filt=[('Be',dct['Be']), ('Al',dct['Al']), ('Air',dct['Air'])]
    s.multi_filter(tube_filt)
    # Get the 1st and 2nd half-value layers in mm Al
    hvl1 = s.get_hvl1()
    hvl2 = s.get_hvl2()
    # Get the additional Al to exactly match the reference HVL1 value 
    t = s.get_matl(hvl=hvl1_ref)
    # Pertcentage error (without exact matching)
    per_err_1.append(100.*(hvl1-hvl1_ref)/hvl1_ref)
    per_err_2.append(100.*(hvl2-hvl2_ref)/hvl2_ref)
    # Define and print output string for the spectrum
    strout = '\n' + key + ' \nHVL1='+str(round(hvl1,3)) + \
        ' mm Al, HVL1ref=' + str(round(hvl1_ref,3)) + ' mm Al (' + \
        str(round(100.*(hvl1-hvl1_ref)/hvl1_ref,2)) +'%)\nHVL2=' + \
        str(round(hvl2,3)) + ' mm Al, HVL2ref=' + str(round(hvl2_ref,3)) + \
        ' mm Al (' + str(round(100.*(hvl2-hvl2_ref)/hvl2_ref,2)) + \
        '%)\nt=' + str(round(t,2))+' mm Al'
    print(strout)
 
## Print the summary statistics (mean and std) for spectra set
print('\n\nHVL1')
print('Mean discrepancy [%] +/- std [%]:',round(mean(per_err_1),1),
      '+/-',round(std(per_err_1),1))
print('\nHVL2')
print('Mean discrepancy [%] +/- std [%]:',round(mean(per_err_2),1),
      '+/-',round(std(per_err_2),1))

print('\nFinished!\n')
