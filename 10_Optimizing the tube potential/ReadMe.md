# Chapter 10. Optimizing the tube potential

Supplementary Python scripts to this chapter are available here. The scripts are
called `cnrd kidney.py`, `cnrd nodule.py` and `metrics.py` and use the SpekPyv2 toolkit (See: [https://bitbucket.org/spekpy/spekpy_release](https://bitbucket.org/spekpy/spekpy_release)). Try running the script `cnrd kidney.py` to reproduce the results
of this chapter for the kidney versus adipose task. Now select “Gadolinium
Oxysulfide” (i.e., GOS) as the scintillator instead of “Cesium Iodide” and
re-run the script. How do the results change and why?

Hint: consider the K-edge energies of Cs (36.0 keV), I (33.2 keV) and Gd
(50.2 keV) and compare the mass attenuation coefficients of the two
scintillators over the energy range.

Prerequisites:

* Python 3
* NumPy (standard Python library)
* SciPy (standard Python library)
* matplotlib (standard Python library)
* SpekPy V2 (our custom Python library)

