Programs for the Preprint Article: 
"How does stochasticity in learning impact the accumulation of knowledge and the evolution of learning?" 
Authors: Ludovic Maisonneuve, Laurent Lehmann 
DOI: https://doi.org/10.1101/2025.08.26.672373

This repository contains scripts and data used to generate the figures and results presented in the above preprint. The project combines evolutionary analyses (in Mathematica) with individual-based simulations (in Python) to study how stochasticity influences the evolution of learning strategies.

Contents:
- IBM_stochasticity_evolution_learning/
Python scripts for simulating the individual-based model (IBM) under parameter values.

  - functions/
  Contains reusable components for modeling and saving simulations:
    - save_and_open.py: Functions for saving simulation output and reloading it for analysis or export.
    - classes.py: Defines the core classes used in the simulations.
    - dynamics.py: Defines functions to iterate the individual-based simulations.
      
  - generate_data_figure_1d/
    - generate_and_prepare_data_mathematica.py: Runs simulations and prepares the output for use in Mathematica, specifically to generate Figure 1d.
      
  - generate_data_figure_S1/
    - generate_and_prepare_data_mathematica.py: Similar to above, but for Figure S1 in the supplementary material.
      
  - generate_data_figure_S8/
  Contains three subfolders corresponding to different values of the parameter sigma_i.
  Each subfolder (e.g. sigma_i_eq_0/) contains:
    - generate_data.py: Runs the IBM.
    - prepare_data_mathematica.py: Converts the simulation results to a format suitable for Mathematica analyses (used in Figure S8).
      
  - generate_data_figure_S9/
  Contains subfolders corresponding to different combination parameter values sigma_v, sigma_o, sigma_i, used in Figure S9.
  Each subfolder (e.g. sigma_v_eq_sigma_o_eq_sigma_i_eq_0/) contains:
    - generate_data.py: Runs the IBM.
    - prepare_data_mathematica.py: Converts the simulation results to a format suitable for Mathematica analyses (used in Figure S9).
      
- make_analyses_and_plots_with_mathematica/
Contains the main Mathematica notebook used for evolutionary analysis and figure generation.
  - evolutionary_analyses.nb: A comprehensive Mathematica notebook that uses selection gradients to simulate trait evolution. It generates most of the figures in the preprint and supplements. It also produces figures using data exported from IBM.

Python
- Run with Python 3.12
- Required libraries: numpy, os, sdeint, random, json, time

Mathematica
- Run with Wolfram Mathematica 13.0.0.0
