import matplotlib.pyplot as plt

# Lists of singlet and triplet energies
singlet_energies = [3.18, 3.21, 3.27, 3.28, 3.30, 3.31, 3.32, 3.32, 3.36, 3.40, 3.41, 3.64, 3.66]
triplet_energies = [2.93, 2.94, 3.09, 3.11, 3.13, 3.13, 3.15, 3.16, 3.17, 3.18, 3.20, 3.21, 3.25, 3.26, 3.28, 3.28, 
                    3.29, 3.30, 3.31, 3.32, 3.32, 3.33, 3.33, 3.34, 3.35, 3.35, 3.36, 3.37, 3.38, 3.39, 3.40, 3.48, 
                    3.50, 3.51, 3.56, 3.57, 3.60, 3.63, 3.65]

plt.figure(figsize=(10, 6))

# Define the length of the lines
line_length = 0.4

# Plot singlet energies as horizontal lines
for energy in singlet_energies:
    plt.hlines(energy, xmin=1, xmax=1 + line_length, colors='b', linestyles='-', lw=2)

# Plot triplet energies as horizontal lines
for energy in triplet_energies:
    plt.hlines(energy, xmin=2, xmax=2 + line_length, colors='r', linestyles='-', lw=2)

plt.title('trans-dimer-LBA5057-LBA5058')
plt.xlabel('States')
plt.ylabel('Energy (eV)')
plt.xticks([1, 2], ['Singlet', 'Triplet'])
plt.ylim(2.9, 3.7)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()
