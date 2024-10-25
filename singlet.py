#The program is designed to process multiple .out files within a specified folder, extract specific columns of data related to "Ex. Energy (eV)" and "Osc. (a.u.)" from each file, and then combine, sort, and save the results into a single output file.

import os

# Function to extract Ex. Energy and Osc. values from a file
def extract_energy_and_osc(file_path):
    extracted_lines = []
    target_header = "  Root   Total Energy (a.u.)   Ex. Energy (eV)   Osc. (a.u.)   < S^2 >   Max CI Coeff.      Excitation"
    
    # Open the file and read its contents
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Flag to start appending lines after the header is found
    start_appending = False

    # Search for the target header and start appending lines after it
    for line in content:
        if target_header in line:
            start_appending = True  # Found the header, start appending subsequent lines
            continue  # Skip the header line itself

        if start_appending:
            extracted_lines.append(line.strip())  # Append each line after the header

    # Extract the first 101 entries (if available) and save the 3rd (Ex. Energy) and 4th (Osc.) columns
    extracted_data = []
    for n in range(1, 102):  # Process first 101 entries
        try:
            ex_energy = float(extracted_lines[n].split()[2])  # Convert to float for sorting
            osc = extracted_lines[n].split()[3]
            extracted_data.append([ex_energy, osc])
        except (IndexError, ValueError):
            # Skip if a line doesn't have enough columns or contains invalid data
            continue
    
    return extracted_data

# Function to process all .out files in a directory and sort the data before saving
def process_all_out_files(directory_path, output_file_path):
    # Initialize a list to store the combined data from all files
    combined_data = []
    
    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.out'):
            # Process each .out file
            file_path = os.path.join(directory_path, filename)
            print(f"Processing file: {file_path}")
            extracted_data = extract_energy_and_osc(file_path)
            
            # Add the extracted data to the combined list
            combined_data.extend(extracted_data)
    
    # Sort the combined data by the first column (Ex. Energy)
    combined_data_sorted = sorted(combined_data, key=lambda x: x[0])

    # Open the output file to save the sorted data
    with open(output_file_path, 'w') as output_file:
        # Write the sorted data to the output file
        for ex_energy, osc in combined_data_sorted:
            output_file.write(f"{ex_energy:.8f}\t{osc}\n")
    
    print(f"All sorted data has been saved to {output_file_path}")

# Set the directory containing the .out files and the output file path
directory_path = 'C:/Users/Woon/Documents/UM/master/test/'  # Replace with the folder containing .out files
output_file_path = 'C:/Users/Woon/Documents/UM/master/test/extracted_energy_osc_sorted.txt'  # Path for the output file

# Process all .out files in the specified directory, sort the data, and save the results
process_all_out_files(directory_path, output_file_path)
