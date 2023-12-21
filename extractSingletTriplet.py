def extract_energy(file):
    singlets = []
    triplets = []
    oscillator_strengths = []

    with open(file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 7:  # Skip lines that don't have enough data
                continue

            if 'singlet' in line:
                energy = float(parts[4])
                osc_strength = float(parts[6]) if 'singlet' in parts else 0.0
                singlets.append(energy)
                oscillator_strengths.append(osc_strength)
            elif 'triplet' in line:
                energy = float(parts[4])
                triplets.append(energy)

    return singlets, triplets, oscillator_strengths
