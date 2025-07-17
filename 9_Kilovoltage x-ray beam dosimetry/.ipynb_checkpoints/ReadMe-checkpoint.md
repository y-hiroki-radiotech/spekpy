# Chapter 9. Kilovoltage x-ray beam dosimetry

A supplementary Python script to this chapter is available here. It is
called BSFw.py and uses the SpekPy-v2 toolkit (See: [https://bitbucket.org/spekpy/spekpy_release](https://bitbucket.org/spekpy/spekpy_release)). The script calculates
Bw(Q, ∅, SSD), given a spectrum, field size and SSD. In Section 9.2.1 it
was stated that SSD only weakly affects the magnitude of the backscatter
factor (a few percent effect). You can verify this by calculating Bw (for a
fixed spectrum and field size) for SSD values ranging from 10 to 100 cm.

Prerequisites:

* Python 3
* NumPy (standard Python library)
* SciPy (standard Python library)
* SpekPy V2 (our custom Python library)

