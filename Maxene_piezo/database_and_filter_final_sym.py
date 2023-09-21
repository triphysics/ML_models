import os
import shutil
import pandas as pd
import glob
from pymatgen import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# Function to check if a structure is centrosymmetric
def is_centrosymmetric(structure):
    # Use pymatgen's SpacegroupAnalyzer to determine if the structure is centrosymmetric
    sga = SpacegroupAnalyzer(structure)
    return sga.is_laue()

# Define the base directory where your structured directories are located
base_directory = './'  # Replace with your actual base directory

# Define the pattern for directory names
directory_pattern = 'Sc-Sc-C-*-*'  # Adjust the pattern to match your directory structure

# Use glob to find all directories matching the pattern
matching_directories = glob.glob(os.path.join(base_directory, directory_pattern))

output_directory = 'output_directory_final_sym_3'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame(columns=["name", "band_gap", "lattice_constant", "magnetic_moment", "isMetal"])


# Initialize an empty DataFrame to store combined data for the specified conditions
combined_data_specified_conditions = pd.DataFrame(columns=["name", "band_gap", "lattice_constant", "magnetic_moment", "isMetal", "is_centrosymmetric"])

# Loop through the matching directories and read CSV files
for directory in matching_directories:
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            # Read the CSV file into a DataFrame and select the specified columns
            df = pd.read_csv(file_path, usecols=["name", "band_gap", "lattice_constant", "magnetic_moment", "isMetal"])
            
            # Analyze the symmetry of the POSCAR file and determine if it's centrosymmetric
            poscar_file_path = os.path.join(directory, 'poscars', f'relax_POSCAR_{os.path.basename(directory)}')
            structure = Structure.from_file(poscar_file_path)
            is_centrosymmetric_value = is_centrosymmetric(structure)
            
            # Append the data to the combined DataFrame
            combined_data = combined_data.append({"name": df["name"].values[0],
                                                  "band_gap": df["band_gap"].values[0],
                                                  "lattice_constant": df["lattice_constant"].values[0],
                                                  "magnetic_moment": df["magnetic_moment"].values[0],
                                                  "isMetal": df["isMetal"].values[0],
                                                  "is_centrosymmetric": str(is_centrosymmetric_value)},
                                                 ignore_index=True)

            # Check if "isMetal" is false, magnetic_moment is zero, and is_centrosymmetric is false
            if not df["isMetal"].any() and (df["magnetic_moment"] == 0).all() and not is_centrosymmetric_value:
                # Append the data to the specified DataFrame for the specified conditions
                combined_data_specified_conditions = combined_data_specified_conditions.append({"name": df["name"].values[0],
                                                                                                "band_gap": df["band_gap"].values[0],
                                                                                                "lattice_constant": df["lattice_constant"].values[0],
                                                                                                "magnetic_moment": df["magnetic_moment"].values[0],
                                                                                                "isMetal": df["isMetal"].values[0],
                                                                                                "is_centrosymmetric": str(is_centrosymmetric_value)},
                                                                                               ignore_index=True)

                relax_poscar_file = os.path.join(directory, 'poscars', f'relax_POSCAR_{os.path.basename(directory)}')
                new_directory_name = os.path.basename(directory)
                new_directory_path = os.path.join(output_directory, new_directory_name)

                # Create a new directory with the pattern name
                os.makedirs(new_directory_path, exist_ok=True)

                # Copy the relax_POSCAR file to the new directory and rename it to "POSCAR"
                if os.path.exists(relax_poscar_file):
                    shutil.copy(relax_poscar_file, os.path.join(new_directory_path, 'POSCAR'))

# Replace 1 and 0 with "True" and "False" respectively in the "is_centrosymmetric" column
combined_data["is_centrosymmetric"] = combined_data["is_centrosymmetric"].replace({'True': True, 'False': False})
combined_data_specified_conditions["is_centrosymmetric"] = combined_data_specified_conditions["is_centrosymmetric"].replace({'True': True, 'False': False})

# Save the combined data to a new CSV file
combined_data.to_csv(os.path.join(output_directory, 'combined_data.csv'), index=False)

# Save the combined data for specified conditions to a new CSV file
combined_data_specified_conditions.to_csv(os.path.join(output_directory, 'combined_data_specified_conditions.csv'), index=False)

# Print a message indicating the process is complete
print('Files copied and data saved successfully.')

