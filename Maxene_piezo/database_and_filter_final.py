import os
import shutil
import pandas as pd
import glob

# Define the base directory where your structured directories are located
base_directory = './'  # Replace with your actual base directory

# Define the pattern for directory names
directory_pattern = 'Y-Y-C-*-*'  # Adjust the pattern to match your directory structure

# Use glob to find all directories matching the pattern
matching_directories = glob.glob(os.path.join(base_directory, directory_pattern))

# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame(columns=["name", "band_gap", "lattice_constant", "magnetic_moment", "isMetal"])

# Initialize an empty DataFrame to store combined data when isMetal is false and magnetic_moment is zero
combined_data_no_metal_moment = pd.DataFrame(columns=["name", "band_gap", "lattice_constant", "magnetic_moment", "isMetal"])

# Define the output directory path
output_directory = 'output_directory_final'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Loop through the matching directories and read CSV files
for directory in matching_directories:
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            # Read the CSV file into a DataFrame and select the specified columns
            df = pd.read_csv(file_path, usecols=["name", "band_gap", "lattice_constant", "magnetic_moment", "isMetal"])
            # Append the data to the combined DataFrame
            combined_data = combined_data.append(df, ignore_index=True)

            # Check if "isMetal" is false and magnetic_moment is zero, then copy the file
            if not df["isMetal"].any() and (df["magnetic_moment"] == 0).all():
                # Append the data to the specific DataFrame for cases with no metal and magnetic moment
                combined_data_no_metal_moment = combined_data_no_metal_moment.append(df, ignore_index=True)

                relax_poscar_file = os.path.join(directory, 'poscars', f'relax_POSCAR_{os.path.basename(directory)}')
                new_directory_name = os.path.basename(directory)
                new_directory_path = os.path.join(output_directory, new_directory_name)

                # Create a new directory with the pattern name
                os.makedirs(new_directory_path, exist_ok=True)

                # Copy the relax_POSCAR file to the new directory and rename it to "POSCAR"
                if os.path.exists(relax_poscar_file):
                    shutil.copy(relax_poscar_file, os.path.join(new_directory_path, 'POSCAR'))

# Save the combined data to a new CSV file
combined_data.to_csv(os.path.join(output_directory, 'combined_data.csv'), index=False)

# Save the combined data for cases with no metal and magnetic moment to a new CSV file
combined_data_no_metal_moment.to_csv(os.path.join(output_directory, 'combined_data_no_metal_moment.csv'), index=False)

# Print a message indicating the process is complete
print('Files copied and data saved successfully.')
