# Chapter 7. Overview on Monte Carlo modelling

There is no Python related content for this chapter. A good way to start
with modelling x-ray tubes using the Monte Carlo method is to download
the EGSnrc code system and use the BEAMnrc user code (See: [https://nrccnrc.github.io/EGSnrc/](https://nrccnrc.github.io/EGSnrc/)). The input file for the example tube illustrated in
fig. 2.5 of the book is included here, along with the associated PEGS4 material data file etc.

Prerequisites:

* A Working installation of EGSnrc
* The contents of the `XSample` directory found here

Note that this example is not an introduction to or tutorial on EGSnrc/BEAMnrc. Please see the excellent documentation produced by the NRC for basic information on how to use the EGSnrc/BEAMnrc code system.

Assuming that you have familiarized yourself with EGS, run the x-ray tube example as follows:

1. Copy the `BEAM_XSample` subdirectory to your `egs_home` directory
2. Copy the `XSample.module` file to your `egs_home/beamnrc/spec_modules` directory
3. Copy the `XSample.pegs4dat` file to your `egs_home/pegs4/data` directory
4. Open up the `HEN_HOUSE/omega/beamnrc/beamnrc_user_macros.mortran` file and find the following line: `REPLACE {$BDY_TOL} WITH {1.E-5}`. Change the number `1.E-5` to the smaller value `5.E-7`. This change is necessary before compilation of the accelerator, for accurate simulations using the XTUBE module of BEAMnrc (see Chapter 7 of the book)
5. Open up the BEAMnrc GUI and load the `XSample.egsinp` input file. Compile and then run the example. Try to run the example even if you receive a compilation failed message (that message is produced if there are any warnings on compilation, but that doesn't mean an executable is not created)

The precise time taken for the run to complete will depend on the computer system used. A typical time might be 10 to 20 minutes.

In the example above, results (i.e. x rays) are scored for a plane at 100 cm source-to-detector distance and saved as a phase-space file by BEAMnrc. That phase-space file can be analyzed using the BEAMDP utility (most conveniently via the BEAMDP GUI). We did so, selecting the option *Derive spectral distribution from ph-sp data*. We then selected *photons* in a circular region with 2.5 cm radius. We scored in 0.5 keV bins and selected *planar fluence* as the quantity of interest. In the image file `BEAMnrc_spekPy.png` included in the repository, we compare the output results from BEAMnrc/BEAMDP with the predictions of SpekPy. As can be observed, there is close agreement.

There are many transport/physics input options to use in a general-purpose Monte Carlo code system such as EGSnrc. The BEAMnrc/EGSnrc options selected in the example are well suited to most x-ray tube simulations. However, we recommend that the user takes the time to read the EGS/BEAM documentation to understand the input selections. Note that the geometry simulated is a relatively simple broad-beam geometry. Much more sophisticated geometries consisting of many more components are possible.




