# Chapter 6. An analytical model in detail

A supplementary Python script to this chapter is available here. It is called
`physics_models.py` and uses the SpekPy-v2 toolkit (See: [https://bitbucket.org/spekpy/spekpy_release](https://bitbucket.org/spekpy/spekpy_release)). The script plots the RQR5
spectrum for four physics models and calculates the first half-value layers.
The physics models are (in order of increasing accuracy): “diff”, “uni”, “sim”
and “kqp”. Are the differences between fluence spectra consistent with the
discussion at the end of Section 6.1.1? Compare the half-value layers. Do
you think the full KQP shape function is necessary?

Note on physics models:

- “diff”—instant electron diffusion and uniform shape function
- “uni”—detailed electron angular distribution and uniform shape function
- “sim”—detailed electron angular distribution and SIM shape function
- “kqp”—detailed electron angular distribution and KQP shape function

Prerequisites:

* Python 3
* NumPy (standard Python library)
* SciPy (standard Python library)
* matplotlib (standard Python library)
* SpekPy V2 (our custom Python library)

