# Chapter 8. Predicting and matching half-value layers

The Python scripts used for generating the data of tables 8.5 to 8.8 are
available here. The
scripts are called beams `ptb_iec.py`, `beams_ptb_iso.py`, `beams_nist_iso.py` and
`beams_bipm.py` and use the SpekPy-v2 toolkit (See: [https://bitbucket.org/spekpy/spekpy_release](https://bitbucket.org/spekpy/spekpy_release)). In the scripts, the physics
model of SpekPy is set to the most advanced: “kqp”. Try changing this
to “spekcalc” in `beams_bipm.py` and running the script. Where does the
SpekCalc model perform poorly and why? Note that this model does not
include L-lines in the characteristic spectrum.

Hint: see Section 5.4 for a discussion of the performance of SpekCalc and
other models.

Prerequisites:

* Python 3
* NumPy (standard Python library)
* SciPy (standard Python library)
* SpekPy V2 (our custom Python library)

