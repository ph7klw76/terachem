# This program compares experimental and theoretical data on absorption spectra by converting wavelengths to energy, 
# simulating absorption spectra using Gaussian distributions, and optimizing parameters to minimize differences between 
# simulated and experimental spectra. It plots the best-fitted simulated spectrum against experimental data for analysis.

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import minimize
from scipy.interpolate import interp1d

# Load the experimental data
data_experimental = np.loadtxt('D:/mathing.txt')  # Update the path accordingly

# Convert wavelength (nm) to energy (eV) for the experimental data
wavelength_experimental, intensity_experimental = data_experimental[:,0], data_experimental[:,1]
energy_experimental = 1240 / wavelength_experimental

# Ensure the energy is in ascending order for interpolation and comparison
sort_indices = np.argsort(energy_experimental)
energy_experimental = energy_experimental[sort_indices]
intensity_experimental = intensity_experimental[sort_indices]

# Load the theoretical data (or the first dataset)
data_theoretical = np.loadtxt('D:/excitation.txt')  # Update the path accordingly
energy, osc_strength = data_theoretical[:,0], data_theoretical[:,1]

# Function to simulate the absorption spectrum for given parameters
def simulate_absorption(energy_experimental, sigma, translation):
    energy_translated = energy + translation
    simulated_intensity = np.zeros_like(energy_experimental)
    for e0, strength in zip(energy_translated, osc_strength):
        gaussian = strength * norm.pdf(energy_experimental, e0, sigma)
        simulated_intensity += gaussian
    simulated_intensity /=simulated_intensity.max()
    return simulated_intensity

# Optimization function to minimize the difference between simulated and experimental spectra
def optimization_function(params):
    sigma, translation = params
    simulated_intensity = simulate_absorption(energy_experimental, sigma, translation)
    mse = np.mean((simulated_intensity - intensity_experimental)**2)  # Mean squared error
    return mse

# Perform the optimization
initial_guess = [0.1, 0.25]  # Initial guess for Gaussian disorder and energy translation
result = minimize(optimization_function, initial_guess, bounds=[(0.01, 0.13), (0.35, 0.5)])

# Extract the optimized parameters
optimized_sigma, optimized_translation = result.x

# Generate the best-fit simulated spectrum
best_fit_intensity = simulate_absorption(energy_experimental, optimized_sigma, optimized_translation)

# Print out the optimized parameters
print("Optimized Gaussian Disorder (sigma):", optimized_sigma, "eV")
print("Optimized Energy Translation (x):", optimized_translation, "eV")

# Plotting the comparison
plt.figure(figsize=(12, 8))
plt.plot(1240 / energy_experimental, intensity_experimental, 'o', label='Experimental Data', markersize=5)
plt.plot(1240 / energy_experimental, best_fit_intensity, '-', label='Best-Fitted Simulated Spectrum')
plt.title('Experimental Data vs. Best-Fitted Simulated Spectrum')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Absorption Intensity')
plt.legend()
plt.grid(True)
plt.show()
