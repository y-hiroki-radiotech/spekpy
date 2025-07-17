import spekpy as sp # Import the SpekPy library for spectral calculations
from numpy import mean, std # Import stuff from numpy

print('\nAnalyzing PTB ISO spectra')

## SpekPy physics parameters
physics = 'kqp' # Physics model
source = 'pene' # Attenuation coefficient source

## Hardcoded standard spectra definitions. See Ankerhold (2000)
## https://oar.ptb.de/resources/show/10.7795/110.20190315B
# Create empty dictionary for spectra specifications
spek_dct = {}
# Add spectra dictionaries to the the dictionary: HK spectra
spek_dct['HK60'] = {'kV':60.,'th':20.,
                  'Be':1.,'Al':3.9,'Cu':0.,'Sn':0.,'Pb':0.,'Air':950.,
                  'hvl1':0.0839,'hvl2':0.121}
spek_dct['HK100'] = {'kV':100.,'th':20.,
                   'Be':1.,'Al':4.,'Cu':0.15,'Sn':0.,'Pb':0.,'Air':950.,
                   'hvl1':0.294,'hvl2':0.462}
spek_dct['HK200'] = {'kV':200.,'th':20.,
                   'Be':7.,'Al':4.,'Cu':1.,'Sn':0.,'Pb':0.,'Air':950.,
                   'hvl1':1.54,'hvl2':2.28}
spek_dct['HK250'] = {'kV':250.,'th':20.,
                   'Be':7.,'Al':4.,'Cu':1.60,'Sn':0.,'Pb':0.,'Air':950.,
                   'hvl1':2.42,'hvl2':3.24}
spek_dct['HK280'] = {'kV':280.,'th':20.,
                   'Be':7.,'Al':4.,'Cu':3.,'Sn':0.,'Pb':0.,'Air':950.,
                   'hvl1':3.26,'hvl2':3.88}
spek_dct['HK300'] = {'kV':300.,'th':20.,
                   'Be':7.,'Al':4.,'Cu':2.2,'Sn':0.,'Pb':0.,'Air':950.,
                   'hvl1':3.22,'hvl2':4.00}
# Add spectra dictionaries to the the dictionary: W spectra
spek_dct['W60'] = {'kV':60.,'th':20.,
                 'Be':1.,'Al':4.,'Cu':0.3,'Sn':0.,'Pb':0.,'Air':950.,
                 'hvl1':0.18,'hvl2':0.215}
spek_dct['W80'] = {'kV':80.,'th':20.,
                 'Be':1.,'Al':4.,'Cu':0.5,'Sn':0.,'Pb':0.,'Air':950.,
                 'hvl1':0.349,'hvl2':0.433}
spek_dct['W110'] = {'kV':110.,'th':20.,
                  'Be':1.,'Al':4.,'Cu':2.,'Sn':0.,'Pb':0.,'Air':950.,
                  'hvl1':0.933,'hvl2':1.08}
spek_dct['W150'] = {'kV':150.,'th':20.,
                  'Be':7.,'Al':4.,'Cu':0.,'Sn':1.,'Pb':0.,'Air':950.,
                  'hvl1':1.78,'hvl2':2.03}
spek_dct['W200'] = {'kV':200.,'th':20.,
                  'Be':7.,'Al':4.,'Cu':0.,'Sn':2.,'Pb':0.,'Air':950.,
                  'hvl1':3.00,'hvl2':3.24}
spek_dct['W250'] = {'kV':250.,'th':20.,
                  'Be':7.,'Al':4.,'Cu':0.,'Sn':4.,'Pb':0.,'Air':950.,
                  'hvl1':4.14,'hvl2':4.34}
spek_dct['W300'] = {'kV':300.,'th':20.,
                  'Be':7.,'Al':4.,'Cu':0.,'Sn':6.5,'Pb':0.,'Air':950.,
                  'hvl1':5.03,'hvl2':5.18}
# Add spectra dictionaries to the the dictionary: N spectra
spek_dct['N40'] = {'kV':40.,'th':20.,
                   'Be':1.,'Al':4.,'Cu':0.21,'Sn':0.,'Pb':0.,'Air':950.,
                   'hvl1':0.085,'hvl2':0.0927}
spek_dct['N60'] = {'kV':60.,'th':20.,
                   'Be':1.,'Al':4.,'Cu':0.6,'Sn':0.,'Pb':0.,'Air':950.,
                   'hvl1':0.234,'hvl2':0.263}
spek_dct['N80'] = {'kV':80.,'th':20.,
                   'Be':1.,'Al':4.,'Cu':2.,'Sn':0.,'Pb':0.,'Air':950.,
                   'hvl1':0.578,'hvl2':0.622}
spek_dct['N100'] = {'kV':100.,'th':20.,
                    'Be':1.,'Al':4.,'Cu':5.,'Sn':0.,'Pb':0.,'Air':950.,
                    'hvl1':1.09,'hvl2':1.15}
spek_dct['N120'] = {'kV':120.,'th':20.,
                    'Be':1.,'Al':4.,'Cu':5.,'Sn':1.,'Pb':0.,'Air':950.,
                    'hvl1':1.67,'hvl2':1.73}
spek_dct['N150'] = {'kV':150.,'th':20.,
                    'Be':7.,'Al':4.,'Cu':0.,'Sn':2.5,'Pb':0.,'Air':950.,
                    'hvl1':2.30,'hvl2':2.41}
spek_dct['N200'] = {'kV':200.,'th':20.,
                    'Be':7.,'Al':4.,'Cu':2.,'Sn':3.,'Pb':1.,'Air':950.,
                    'hvl1':3.92,'hvl2':3.99}
spek_dct['N250'] = {'kV':250.,'th':20.,
                    'Be':7.,'Al':4.,'Cu':0.,'Sn':2.,'Pb':3.,'Air':950.,
                    'hvl1':5.1,'hvl2':5.14}
spek_dct['N300'] = {'kV':300.,'th':20.,
                    'Be':7.,'Al':4.,'Cu':0.,'Sn':3.,'Pb':5.,'Air':950.,
                    'hvl1':5.96,'hvl2':6.00}
# Add spectra dictionaries to the the dictionary: LK spectra
spek_dct['LK55'] = {'kV':55.,'th':20.,
                    'Be':1.,'Al':4.,'Cu':1.2,'Sn':0.,'Pb':0.,'Air':950.,
                    'hvl1':0.248,'hvl2':0.261}
spek_dct['LK70'] = {'kV':70.,'th':20.,
                    'Be':1.,'Al':4.,'Cu':2.5,'Sn':0.,'Pb':0.,'Air':950.,
                    'hvl1':0.483,'hvl2':0.505}
spek_dct['LK100'] = {'kV':100.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':0.5,'Sn':2.,'Pb':0.,'Air':950.,
                     'hvl1':1.22,'hvl2':1.25}
spek_dct['LK125'] = {'kV':125.,'th':20.,
                     'Be':7.,'Al':4.,'Cu':1.,'Sn':4.,'Pb':0.,'Air':950.,
                     'hvl1':1.98,'hvl2':2.02}
spek_dct['LK170'] = {'kV':170.,'th':20.,
                     'Be':7.,'Al':4.,'Cu':1.,'Sn':3.,'Pb':1.5,'Air':950.,
                     'hvl1':3.40,'hvl2':3.46}
spek_dct['LK210'] = {'kV':210.,'th':20.,
                     'Be':7.,'Al':4.,'Cu':0.5,'Sn':2.,'Pb':3.5,'Air':950.,
                     'hvl1':4.52,'hvl2':4.55}
spek_dct['LK240'] = {'kV':240.,'th':20.,
                     'Be':7.,'Al':4.,'Cu':0.5,'Sn':2.,'Pb':5.5,'Air':950.,
                     'hvl1':5.19,'hvl2':5.22}

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
    tube_filt = [('Be',dct['Be']), ('Al',dct['Al']), ('Cu',dct['Cu']), 
                 ('Sn',dct['Sn']), ('Pb',dct['Pb']),('Air',dct['Air'])]
    s.multi_filter(tube_filt)
    # Get the 1st and 2nd half-value layers in mm Cu
    hvl1 = s.get_hvl1(matl='Cu')
    hvl2 = s.get_hvl2(matl='Cu')
    # Get the additional Cu to exactly match the reference HVL1 value 
    t = s.get_matl(hvl_matl='Cu',hvl=hvl1_ref,matl='Cu')
    # Percentage error
    per_err_1.append(100.*(hvl1-hvl1_ref)/hvl1_ref)
    per_err_2.append(100.*(hvl2-hvl2_ref)/hvl2_ref)
    # Define and print output string for the spectrum
    strout = '\n' + key + ' \nHVL1='+str(round(hvl1,3)) + \
        ' mm Cu, HVL1ref=' + str(round(hvl1_ref,3)) + ' mm Cu (' + \
        str(round(100.*(hvl1-hvl1_ref)/hvl1_ref,2)) +'%)\nHVL2=' + \
        str(round(hvl2,3)) + ' mm Cu, HVL2ref=' + str(round(hvl2_ref,3)) + \
        ' mm Cu (' + str(round(100.*(hvl2-hvl2_ref)/hvl2_ref,2)) + '%)'
    print(strout)
 
## Print the summary statistics (mean and std) for spectra set
print('\n\nHVL1')
print('Mean discrepancy [%] +/- std [%]:',round(mean(per_err_1),1),
      '+/-',round(std(per_err_1),1))
print('\nHVL2')
print('Mean discrepancy [%] +/- std [%]:',round(mean(per_err_2),1),
      '+/-',round(std(per_err_2),1))

print('\nFinished!\n')
