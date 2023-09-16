import matplotlib.pyplot as plt

def draw_energy_levels(singlet_levels, triplet_levels, offset=0.05):
    fig, ax = plt.subplots()

    # Sort the energy levels
    singlet_levels.sort()
    triplet_levels.sort()

    # Function to add small offset to near-degenerate states
    def add_offset(levels):
        new_levels = []
        for i, level in enumerate(levels):
            count = levels.count(level)
            if count > 1:
                for j in range(count):
                    new_levels.append(level + j * offset - (count - 1) * offset / 2)
            else:
                new_levels.append(level)
        return list(set(new_levels))

    singlet_levels = add_offset(singlet_levels)
    triplet_levels = add_offset(triplet_levels)

    # Draw singlet energy levels
    for i, level in enumerate(singlet_levels):
        ax.hlines(level, xmin=0, xmax=1, color='b', linewidth=2, label='Singlet' if i == 0 else "")
        alignment = 'left' if i % 2 == 0 else 'right'
        ax.text(0.5, level, f"{level:.2f} eV", verticalalignment='bottom', horizontalalignment=alignment, fontsize=16, color='b')

    # Draw triplet energy levels
    for i, level in enumerate(triplet_levels):
        ax.hlines(level, xmin=2, xmax=3, color='r', linewidth=2, label='Triplet' if i == 0 else "")
        alignment = 'left' if i % 2 == 0 else 'right'
        ax.text(2.5, level, f"{level:.2f} eV", verticalalignment='bottom', horizontalalignment=alignment, fontsize=16, color='r')

    # Add labels and title
    ax.set_title('Energy Level Diagram', fontsize=16)
    ax.set_xlabel('Energy Levels', fontsize=16)
    ax.set_ylabel('Energy (eV)', fontsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    
    # Place the legend in the middle
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), fontsize=16)

    # Show the plot
    plt.show()

# Sample singlet and triplet energy levels in eV
singlet_levels = [2.05, 2.07, 2.74, 2.75, 2.91, 2.93, 2.97, 2.98]
triplet_levels = [2.03, 2.06, 2.08, 2.13, 2.48, 2.69, 2.71, 2.82, 2.92, 2.95]

draw_energy_levels(singlet_levels, triplet_levels)
