import os
import shutil
import pandas as pd
import glob
from pymatgen import Structure
from pymatgen.io.vasp import Poscar
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# specify potcar here as per used in mxene database

potcar_content_dict = {
    'H':  'H',
    'Sc': 'Sc_sv',
    'Ti': 'Ti_sv',
    'V':  'V_sv',
    'Cr':  'Cr_pv',
    'Y':  'Y_sv',
    'Zr': 'Zr_sv',
    'Nb': 'Nb_sv',
    'Mo': 'Mo_pv',
    'Hf': 'Hf_pv',
    'Ta': 'Br',
    'W' : 'W_pv',
    'C':  'C_s',
    'N':  'N_s',
    'O':  'O_s',
    'F':  'F',
    'Cl': 'Cl',
    'Br': 'Br',
    'P':  'P',
    'S' : 'S'
}

# Function to generate POTCAR content for given elements based on a specified dictionary. Pymatgen???
def generate_potcar(elements, pseudopotential_dir, output_potcar_path):
    # Initialize an empty POTCAR content
    potcar_content = ""

    # Read and append pseudopotential data for each element
    for element in elements:
        # Replace 'element' with the corresponding match from the dictionary
        element_key = element
        if element in potcar_content_dict:
            element_key = potcar_content_dict[element]
        pseudopotential_file_path = os.path.join(pseudopotential_dir, element_key, 'POTCAR')
        with open(pseudopotential_file_path, 'r') as f:
            pseudopotential_data = f.read()
            potcar_content += pseudopotential_data  # Remove the newline after each element's POTCAR content

    # Write the combined POTCAR content to a new file, overwriting if it already exists
    with open(output_potcar_path, 'w') as f:
        f.write(potcar_content)

# Function to check if a structure is centrosymmetric
def is_centrosymmetric(structure):
    # Use pymatgen's SpacegroupAnalyzer to determine if the structure is centrosymmetric
    sga = SpacegroupAnalyzer(structure)
    return sga.is_laue()

def get_space_and_point_groups(structure):
    sga = SpacegroupAnalyzer(structure)
    space_group = sga.get_space_group_symbol()
    point_group = sga.get_point_group_symbol()
    return space_group, point_group

def calculate_number_of_sites(structure):
    return len(structure)

# Define the base directory where your structured directories are located
base_directory = './'  # Replace with your actual base directory

# Define the pattern for directory names
directory_pattern = 'Y-Y-N-*-*'  # Adjust the pattern to match your directory structure

# Use glob to find all directories matching the pattern
matching_directories = glob.glob(os.path.join(base_directory, directory_pattern))
potcar_directory = '/home/tribhuwan/Softwares/VASP_Pseudo/potpaw_PBE'

output_directory = 'output_directory_final_sym_pot_final_run'


# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame(columns=["name", "band_gap", "lattice_constant", "magnetic_moment", "isMetal"])


# Initialize an empty DataFrame to store combined data for the specified conditions
combined_data_specified_conditions = pd.DataFrame(columns=["name", "band_gap", "lattice_constant", "magnetic_moment", "isMetal", "is_centrosymmetric", "space_group", "point_group", "num_sites", "structure"])

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
            print(structure)
#            structure1= poscar.structure
            is_centrosymmetric_value = is_centrosymmetric(structure)
            elements = [str(element) for element in structure.composition.elements]
#           print(elements)
            space_group, point_group = get_space_and_point_groups(structure)
#            print(space_group, point_group)
            num_sites = calculate_number_of_sites(structure)
            poscar = Poscar.from_file(poscar_file_path)
            structure1=poscar.structure
 #           print(structure1)
            
            # Append the data to the combined DataFrame
            combined_data = combined_data.append({"name": df["name"].values[0],
                                                  "band_gap": df["band_gap"].values[0],
                                                  "lattice_constant": df["lattice_constant"].values[0],
                                                  "magnetic_moment": df["magnetic_moment"].values[0],
                                                  "isMetal": df["isMetal"].values[0],
                                                  "is_centrosymmetric": str(is_centrosymmetric_value),
                                                  "space_group": space_group,
                                                  "point_group": point_group,
                                                  "num_sites": num_sites,
                                                  "structure": structure1},
                                                 ignore_index=True)

            # Check if "isMetal" is false, magnetic_moment is zero, and is_centrosymmetric is false
            if not df["isMetal"].any() and (df["magnetic_moment"] == 0).all() and not is_centrosymmetric_value:
                # Append the data to the specified DataFrame for the specified conditions
                combined_data_specified_conditions = combined_data_specified_conditions.append({"name": df["name"].values[0],
                                                                                                "band_gap": df["band_gap"].values[0],
                                                                                                "lattice_constant": df["lattice_constant"].values[0],
                                                                                                "magnetic_moment": df["magnetic_moment"].values[0],
                                                                                                "isMetal": df["isMetal"].values[0],
                                                                                                "is_centrosymmetric": str(is_centrosymmetric_value),
                                                                                                "space_group": space_group,
                                                                                                "point_group": point_group,
                                                                                                "num_sites": num_sites,
                                                                                                "structure": structure1},
                                                                                               ignore_index=True)

                relax_poscar_file = os.path.join(directory, 'poscars', f'relax_POSCAR_{os.path.basename(directory)}')
                new_directory_name = os.path.basename(directory)
                new_directory_path = os.path.join(output_directory, new_directory_name)

                # Create a new directory with the pattern name
                os.makedirs(new_directory_path, exist_ok=True)

                # Copy the relax_POSCAR file to the new directory and rename it to "POSCAR"
                if os.path.exists(relax_poscar_file):
                    shutil.copy(relax_poscar_file, os.path.join(new_directory_path, 'POSCAR'))

                generate_potcar(elements, potcar_directory, os.path.join(new_directory_path, 'POTCAR'))

# Replace 1 and 0 with "True" and "False" respectively in the "is_centrosymmetric" column
combined_data["is_centrosymmetric"] = combined_data["is_centrosymmetric"].replace({'True': True, 'False': False})
combined_data_specified_conditions["is_centrosymmetric"] = combined_data_specified_conditions["is_centrosymmetric"].replace({'True': True, 'False': False})

# Save the combined data to a new CSV file
combined_data.to_csv(os.path.join(output_directory, 'combined_data.csv'), index=False)

# Save the combined data for specified conditions to a new CSV file
combined_data_specified_conditions.to_csv(os.path.join(output_directory, 'combined_data_specified_conditions.csv'), index=False)

# Print a message indicating the process is complete
print('Files copied and data saved successfully.')
