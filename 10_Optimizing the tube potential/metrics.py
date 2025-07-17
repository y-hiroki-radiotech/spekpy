import spekpy as sp # Import the SpekPy library for spectral calculations
from numpy import arange, zeros, exp, sum, sqrt # import stuff from numpy

def get_metrics(bg,sg,SDD,SOD,kV_inc,physics,matd,td,rhod,f,w,G):
    """
    A function to calculate contrast, noise, incident air kerma for an
    imaging scenario (defined by bg, sg, SDD, SOD, kVinc, physics) and
    detector (defined by matd, td, rhod, f, w, G)

    :param dictionary bg: Specific. of background tissues and thicknesses [cm]
    :param dictionary sg: Specific. of signal tissues and thicknesses [cm]
    :param float SDD:  source-to-detector distance [cm]
    :param float SDD:  source-to-object distance (to signal feature) [cm]
    :param float kV_inc: the increment for tube potential [kV]
    :param str physics: the SpekPy physics model requested
    :param str matd: the name of the scintillator material
    :param float td: the thickness of the scintillator [cm]
    :param float rhod: scintillator density [g/cm3]
    :param float f: detector full factor
    :param float w: pixel size [cm]
    :param float G: anti-scatter grid factor (fraction of primary transmitted)
    :return float array kV_set: the set of tube potentials evaluated [kV]
    :return float array contrast: the set of relative contrasts
    :return float array cnr: the set of contrast-to-noise (CNR)
    :return float array ki: the set of incident air kerma [uGy/mAs]
    :return float array cnrd: the set of dose-normalized CNR (CNRD)
    """
    # Get attenuation coeff. data from SpekPy
    MuData = sp.Spek().mu_data 
    # Calculate source-to-skin distance [cm]
    thickness = 0.
    for item in bg.items():
        thickness = thickness + item[1]
    SSD = SDD - thickness
    # Define array of kV values
    kV_set = arange(50., 151., kV_inc) 
    # Create empty arrays for contrast, CNRD, CNR and incident air kerma
    contrast = zeros(kV_set.shape) 
    cnrd = zeros(kV_set.shape)
    cnr = zeros(kV_set.shape)
    ki = zeros([kV_set.size])
    # Define detector gain (doesn't affect results)
    kf = 1
    # Detector element area [cm2]
    a = w**2
    # Loop increment index
    i=0 
    for kV in kV_set: # Loop through tube potentials
        # Create spectrum model (3.5 mm Al, 0.1 mm Cu, air column)
        s = sp.Spek(kvp=kV,th=12,physics=physics)
        s.filter('Al',3.5).filter('Cu',0.1).filter('Air',SSD*10) 
        # Get x-ray bin energies and bin width
        k = s.get_k()
        dk = k[1]-k[0]
        # Get mass attenuation coefficient for detector material
        mu_over_rho, rho = \
            MuData.get_mu_over_rho_composition(matd,k)
        # Calculate the quantum efficiency
        alpha = 1. - exp(-mu_over_rho*td*rhod)
        # Clone the spectrum and filter by the background tissue set
        sb = sp.Spek.clone(s)
        for item in bg.items():
            sb.filter(item[0],item[1]*10)
        # Get the spectrum reaching detector after passing through background
        k, phib_k = sb.get_spectrum(z=SDD)
        # Apply the grid correction
        phib_k = G*phib_k
        # Clone the spectrum and filter by the signal tissue set
        ss = sp.Spek.clone(s)
        for item in sg.items():
            ss.filter(item[0],item[1]*10)
        # Get the spectrum reaching detector after passing signal tissue
        k, phis_k = ss.get_spectrum(z=SDD)
        # Apply the grid correction
        phis_k = G*phis_k
        # Detector signal (background)
        sigb = kf*f*a*sum(phib_k*alpha*k)*dk
        sigs = kf*f*a*sum(phis_k*alpha*k)*dk
        # Detector signal variance (background)
        varb = (kf**2)*f*a*sum(phib_k*alpha*k**2)*dk
        # Relative ontrast
        contrast[i] = (sigb-sigs)/sigb
        # Contrast-to-noise ratio (CNR)
        cnr[i] = contrast[i]*sigb/sqrt(varb)
        # Incident air kerma [uGy]
        ki[i] = s.get_kerma(z=SSD)
        # Dose normalized CNR
        cnrd[i] = cnr[i]/sqrt(ki[i])
        # Increment the counter
        i = i + 1 

    return kV_set,contrast,cnr,ki,cnrd
