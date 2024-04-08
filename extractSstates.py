"""
Purpose of the Program:
This program is designed to parse and analyze data from a text file containing results from quantum chemistry simulations, focusing specifically on electronic transitions. It extracts key information about root states and transitions between molecular orbitals, including HOMO to LUMO levels, vertical excitation energies, and oscillator strengths. This information is vital for understanding the electronic structure and optical properties of molecules, which are essential in fields such as material science, photovoltaics, and molecular electronics.

The program operates through several steps:
1. Initializes regular expressions for data extraction.
2. Parses the file to identify and extract data related to electronic transitions and final excited state results.
3. Organizes extracted data into a structured format for easy analysis.
4. Enhances the structured data with final excited state information, including excitation energies and oscillator strengths.
5. Transforms data for readability, converting numeric identifiers into conventional HOMO/LUMO notation.
6. Converts the organized data into a Pandas DataFrame for tabular representation.
7. Exports the DataFrame to an Excel file for easy sharing, storage, and further analysis.

This automated process facilitates the efficient translation of complex text-based datasets into a structured and interpretable format, enabling quicker insights into the molecular systems under study.
"""
import pandas as pd
import re

# Initialize variables and regular expressions
data = []
final_states = {}

root_re = re.compile(r'Root\s+(\d+):')
data_re = re.compile(r'(\d+)\s+->\s+(\d+)\s+:\s+D\s+->\s+V\s+:\s+([-+]?\d*\.\d+|\d+)')
final_state_re = re.compile(r'Final Excited State Results:')
energy_osc_re = re.compile(r'\s*(\d+)\s+([+-]?[0-9]*[.]?[0-9]+)\s+([+-]?[0-9]*[.]?[0-9]+)\s+([+-]?[0-9]*[.]?[0-9]+)')

file_path = 'C:/Users/Woon/Documents/DICC/111.txt' 

# Function to parse the file and extract the necessary data
def parse_file(file_path):
    with open(file_path, 'r') as file:
        reading_final_states = False
        for line in file:
            if final_state_re.search(line):
                reading_final_states = True
                continue

            if reading_final_states:
                match = energy_osc_re.search(line)
                if match:
                    root = int(match.group(1))
                    exc_energy = float(match.group(3))
                    osc_strength = float(match.group(4))
                    final_states[root] = (exc_energy, osc_strength)
            else:
                match = root_re.search(line)
                if match:
                    root = int(match.group(1))
                    continue
                
                match = data_re.search(line)
                if match:
                    from_, to_, coefficient = int(match.group(1)), int(match.group(2)), float(match.group(3))
                    # Initialize the dictionary for the root if it does not exist
                    if root not in data:
                        data.append({
                            "Root": root,
                            "Vertical excitation (eV)": None,
                            "Oscillator strength (a.u)": None,
                            "Transition From": [],
                            "To": [],
                            "Coefficient": []
                        })
                    data[-1]["Transition From"].append(from_)
                    data[-1]["To"].append(to_)
                    data[-1]["Coefficient"].append(coefficient)

# Parse the file
parse_file(file_path)

# Update the data list with information from final_states
for entry in data:
    root = entry["Root"]
    if root in final_states:
        entry["Vertical excitation (eV)"], entry["Oscillator strength (a.u)"] = final_states[root]

# Convert nested lists to string for the DataFrame
for entry in data:
    entry["Transition From"] = ", ".join(f"HOMO-{abs(x - 207)}" if x != 207 else "HOMO" for x in entry["Transition From"])
    entry["To"] = ", ".join(f"LUMO+{abs(x - 208)}" if x != 208 else "LUMO" for x in entry["To"])
    entry["Coefficient"] = ", ".join(str(x) for x in entry["Coefficient"])

# Create DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
excel_path_corrected = "C:/Users/Woon/Documents/DICC/test.xlsx"  
df.to_excel(excel_path_corrected, index=False)

excel_path_corrected
