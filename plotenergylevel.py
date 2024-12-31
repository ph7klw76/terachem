import matplotlib.pyplot as plt
import numpy as np

# Data for energy levels
compounds = ['EHBIPO', 'EHBIPOBr', 'EHBIPOAz']
homo_levels = [-6.77, -6.78, -6.52]
lumo_levels = [-1.51, -1.84, -1.75]
gaps = [round(l - h, 2) for l, h in zip(lumo_levels, homo_levels)]

# Plotting setup
fig, ax = plt.subplots(figsize=(10, 6))

# Draw energy levels
for i, compound in enumerate(compounds):
    # Plot arrow between HOMO and LUMO levels
    ax.annotate('', xy=(i, lumo_levels[i]), xytext=(i, homo_levels[i]),
                arrowprops=dict(arrowstyle="<->", color='black'))

    # Plot HOMO level
    ax.plot([i - 0.2, i + 0.2], [homo_levels[i], homo_levels[i]], color='red', lw=2, label='HOMO' if i == 0 else "")
    ax.text(i, homo_levels[i] - 0.2, f"{homo_levels[i]} eV", ha='center', fontsize=14, fontweight='bold', color='red')

    # Plot LUMO level
    ax.plot([i - 0.2, i + 0.2], [lumo_levels[i], lumo_levels[i]], color='blue', lw=2, label='LUMO' if i == 0 else "")
    ax.text(i, lumo_levels[i] + 0.2, f"{lumo_levels[i]} eV", ha='center', fontsize=14, fontweight='bold', color='blue')

    # Annotate gap
    ax.text(i, (homo_levels[i] + lumo_levels[i]) / 2, f"{gaps[i]} eV",
            ha='center', va='center', fontsize=14, fontweight='bold', color='black')

# Labels and formatting
ax.set_xticks(range(len(compounds)))
ax.set_xticklabels(compounds, fontsize=14, fontweight='bold')
ax.set_ylabel('Energy (eV)', fontsize=14, fontweight='bold')
ax.set_title('Energy Levels of Compounds', fontsize=14, fontweight='bold')
ax.axhline(0, color='black', lw=0.8, linestyle='--')
#ax.legend(fontsize=10, loc='upper left')
plt.ylim(-10.0, -0.5)

# Enhance the size and boldness of y-axis numerical labels
ax.tick_params(axis='y', labelsize=14)
for label in ax.get_yticklabels():
    label.set_fontweight('bold')

# Show the plot
plt.tight_layout()
plt.show()

# Enhance the size and boldness of y-axis numerical labels
ax.tick_params(axis='y', labelsize=14)
for label in ax.get_yticklabels():
    label.set_fontweight('bold')

# Show the plot
plt.tight_layout()
plt.show()
