import numpy as np 
import matplotlib.pyplot as plt

# Function to read theoretical data
def read_theoretical_data(filename):
    data = np.loadtxt(filename)
    energy_theo = data[:, 0]  # Energy in eV
    osc_strengths = data[:, 1]  # Oscillator strengths
    return energy_theo, osc_strengths

# Function to read experimental data
def read_experimental_data(filename):
    data = np.loadtxt(filename)
    energy_exp = data[:, 0]  # Energy in eV
    absorbance_exp = data[:, 1]  # Absorbance (arbitrary units)
    return energy_exp, absorbance_exp

# Gaussian function for broadening
def gaussian(x, x0, sigma):
    return np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))

# Function to generate broadened absorbance curve from oscillator strengths
def broaden_absorbance(energy_theo, osc_strengths, sigma, energy_range):
    absorbance_curve = np.zeros_like(energy_range)
    for i in range(len(energy_theo)):
        absorbance_curve += osc_strengths[i] * gaussian(energy_range, energy_theo[i], sigma)
    return absorbance_curve

# Load the theoretical and experimental data
theo_filename = 'cisVE.txt'
exp_filename = 'experimental - Copy.txt'
energy_theo, osc_strengths = read_theoretical_data(theo_filename)
energy_exp, absorbance_exp = read_experimental_data(exp_filename)

# Define parameters for Gaussian broadening and energy range
sigma = 0.25  # Broadening value in eV
energy_range = np.linspace(min(energy_theo) - 1, max(energy_theo) + 1, 1000)

# Compute the broadened absorbance curve with shifted energy (-0.2 eV)
energy_theo_shifted = energy_theo - 0.2 # Shift theoretical energy values
absorbance_curve = broaden_absorbance(energy_theo_shifted, osc_strengths, sigma, energy_range)

# Scale experimental absorbance to match the peak of theoretical absorbance
peak_theoretical = max(absorbance_curve)
peak_experimental = max(absorbance_exp)
scaling_factor = peak_theoretical / peak_experimental
absorbance_exp_scaled = absorbance_exp * scaling_factor

fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the broadened and shifted theoretical absorbance curve on the primary y-axis
ax1.plot(energy_range, absorbance_curve, label='Theoretical Absorbance Curve (Gaussian Broadened & Shifted)')
ax1.plot(energy_exp, absorbance_exp_scaled, label='Experimental Absorbance (Scaled)', linestyle='--')
ax1.set_xlabel('Energy (eV)')
ax1.set_ylabel('Absorbance (arbitrary units)')
ax1.set_ylim(bottom=0)
ax1.legend(loc='upper left')
ax1.set_title('Comparison of Shifted Theoretical and Scaled Experimental Absorbance with Oscillator Strengths')

# Create a secondary y-axis for the histogram
ax2 = ax1.twinx()
ax2.bar(energy_theo_shifted, osc_strengths, width=0.02, color='green', alpha=0.5, label='Theoretical Oscillator Strengths (Shifted)', edgecolor='red')
ax2.set_ylabel('Oscillator Strength (arbitrary units)')

# Add legend for the histogram on the secondary y-axis
fig.legend(loc='upper right', bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

plt.show()

