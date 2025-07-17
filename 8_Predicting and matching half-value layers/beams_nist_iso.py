import spekpy as sp # Import the SpekPy library for spectral calculations
from numpy import mean, std, nan, nanmean, nanstd # Import stuff from numpy

print('\nAnalyzing NIST ISO spectra')

## SpekPy physics parameters
physics = 'kqp' # Physics model
source = 'pene' # Attenuation coefficient source

## Hardcoded standard spectra definitions. See O'Brien (2021)
## https://www.nist.gov/system/files/documents/2021/07/13/procedure03v460.pdf
## Note that the NIST document claims the HK60 and HK100 have 3.19 and 3.9 mm
## of Al in addition to 4 mm inherent filtration (see Table 3a there in).
## We do not think this can be true and assume 3.19 and 3.9 mm as total Al   
# Create empty dictionary for spectra specifications
spek_dct = {}
# Add spectra dictionaries to the the dictionary: HK spectra

spek_dct['HK60'] = {'kV':60.,'th':20.,
                  'Be':0.,'Al':3.19,'Cu':0.,'Sn':0.,'Pb':0.,'Air':950.,
                  'hvl1':0.079,'hvl2':0.113}
spek_dct['HK100'] = {'kV':100.,'th':20.,
                     'Be':0.,'Al':3.9,'Cu':0.15,'Sn':0.,'Pb':0.,'Air':950.,
                     'hvl1':0.298,'hvl2':0.463}
spek_dct['HK200'] = {'kV':200.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':1.15,'Sn':0.,'Pb':0.,'Air':950.,
                     'hvl1':1.669,'hvl2':2.447}
spek_dct['HK250'] = {'kV':250.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':1.60,'Sn':0.,'Pb':0.,'Air':950.,
                     'hvl1':2.463,'hvl2':3.37}
spek_dct['HK280'] = {'kV':280.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':3.06,'Sn':0.,'Pb':0.,'Air':950.,
                     'hvl1':3.493,'hvl2':4.089}
spek_dct['HK300'] = {'kV':300.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':2.51,'Sn':0.,'Pb':0.,'Air':950.,
                     'hvl1':3.474,'hvl2':4.205}
# Add spectra dictionaries to the the dictionary: WS spectra
spek_dct['WS60'] = {'kV':60.,'th':20.,
                    'Be':0.,'Al':4.,'Cu':0.3,'Sn':0.,'Pb':0.,'Air':950.,
                    'hvl1':0.179,'hvl2':0.206}
spek_dct['WS80'] = {'kV':80.,'th':20.,
                    'Be':0.,'Al':4.,'Cu':0.529,'Sn':0.,'Pb':0.,'Air':950.,
                    'hvl1':0.337,'hvl2':0.44}
spek_dct['WS110'] = {'kV':110.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':2.029,'Sn':0.,'Pb':0.,'Air':950.,
                     'hvl1':0.97,'hvl2':1.13}
spek_dct['WS150'] = {'kV':150.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':0.,'Sn':1.03,'Pb':0.,'Air':950.,
                     'hvl1':1.88,'hvl2':2.13}
spek_dct['WS200'] = {'kV':200.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':0.,'Sn':2.01,'Pb':0.,'Air':950.,
                     'hvl1':3.09,'hvl2':3.35}
spek_dct['WS250'] = {'kV':250.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':0.,'Sn':4.01,'Pb':0.,'Air':950.,
                     'hvl1':4.30,'hvl2':4.5}
spek_dct['WS300'] = {'kV':300.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':0.,'Sn':6.54,'Pb':0.,'Air':950.,
                     'hvl1':5.23,'hvl2':5.38}
# Add spectra dictionaries to the the dictionary: NS spectra
spek_dct['NS40'] = {'kV':40.,'th':20.,
                    'Be':0.,'Al':4.,'Cu':0.21,'Sn':0.,'Pb':0.,'Air':950.,
                    'hvl1':0.082,'hvl2':0.094}
spek_dct['NS60'] = {'kV':60.,'th':20.,
                    'Be':0.,'Al':4.,'Cu':0.6,'Sn':0.,'Pb':0.,'Air':950.,
                    'hvl1':0.241,'hvl2':0.271}
spek_dct['NS80'] = {'kV':80.,'th':20.,
                    'Be':0.,'Al':4.,'Cu':2.,'Sn':0.,'Pb':0.,'Air':950.,
                    'hvl1':0.59,'hvl2':0.62}
spek_dct['NS100'] = {'kV':100.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':5.,'Sn':0.,'Pb':0.,'Air':950.,
                     'hvl1':1.14,'hvl2':1.19}
spek_dct['NS120'] = {'kV':120.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':4.99,'Sn':1.04,'Pb':0.,'Air':950.,
                     'hvl1':1.76,'hvl2':1.84}
spek_dct['NS150'] = {'kV':150.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':0.,'Sn':2.5,'Pb':0.,'Air':950.,
                     'hvl1':2.41,'hvl2':2.57}
spek_dct['NS200'] = {'kV':200.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':2.04,'Sn':2.98,'Pb':1.003,'Air':950.,
                     'hvl1':4.09,'hvl2':4.20}
spek_dct['NS250'] = {'kV':250.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':0.,'Sn':2.01,'Pb':2.97,'Air':950.,
                     'hvl1':5.34,'hvl2':5.40}
spek_dct['NS300'] = {'kV':300.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':0.,'Sn':2.99,'Pb':4.99,'Air':950.,
                     'hvl1':6.17,'hvl2':6.30}
# Add spectra dictionaries to the the dictionary: LK spectra
spek_dct['LK55'] = {'kV':55.,'th':20.,
                    'Be':0.,'Al':4.,'Cu':1.19,'Sn':0.,'Pb':0.,'Air':950.,
                    'hvl1':0.260,'hvl2':nan}
spek_dct['LK70'] = {'kV':70.,'th':20.,
                    'Be':0.,'Al':4.,'Cu':2.64,'Sn':0.,'Pb':0.,'Air':950.,
                    'hvl1':0.509,'hvl2':nan}
spek_dct['LK100'] = {'kV':100.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':0.52,'Sn':2.,'Pb':0.,'Air':950.,
                     'hvl1':1.27,'hvl2':nan}
spek_dct['LK125'] = {'kV':125.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':1.,'Sn':4.,'Pb':0.,'Air':950.,
                     'hvl1':2.107,'hvl2':2.094}
spek_dct['LK170'] = {'kV':170.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':1.,'Sn':3.,'Pb':1.5,'Air':950.,
                     'hvl1':3.565,'hvl2':3.592}
spek_dct['LK210'] = {'kV':210.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':0.5,'Sn':2.,'Pb':3.5,'Air':950.,
                     'hvl1':4.726,'hvl2':4.733}
spek_dct['LK240'] = {'kV':240.,'th':20.,
                     'Be':0.,'Al':4.,'Cu':0.5,'Sn':2.,'Pb':5.5,'Air':950.,
                     'hvl1':5.515,'hvl2':5.542}

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
    s = sp.Spek(kvp=pot,th=theta,physics=physics,mu_data_source=source)
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
print('Mean discrepancy [%] +/- std [%]:',round(nanmean(per_err_2),1),
      '+/-',round(nanstd(per_err_2),1))

print('\nFinished!\n')
