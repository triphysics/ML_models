import os
import pandas as pd
import numpy as np
from pymatgen.io.vasp.outputs import Outcar
from matminer.utils.io import load_dataframe_from_json, store_dataframe_as_json

# Assuming df is your DataFrame
df = load_dataframe_from_json("my_df_file.json")
df1 = pd.read_csv("combined_data_specified_conditions1.csv")  # Adjust the file path as needed


# Function to read piezoelectric and dielectric tensors
def read_tensors_from_outcar(outcar_path):
    outcar = Outcar(outcar_path)
    static_piezo_tensor = np.asarray(outcar.piezo_tensor)
    ionic_piezo_tensor = np.asarray(outcar.piezo_ionic_tensor)
    total_piezo_tensor = np.asarray(np.add(static_piezo_tensor, ionic_piezo_tensor))

    ionic_dielectric_tensor = outcar.dielectric_ionic_tensor
    static_dielectric_tensor = outcar.dielectric_tensor
    total_dielectric_tensor = np.add(ionic_dielectric_tensor, static_dielectric_tensor)

    BEC = outcar.born
    #print(BEC)
    max_born_charge = np.max(BEC.flatten())
    max_dielectric = np.max(total_dielectric_tensor.flatten())
    max_piezo = np.max(total_piezo_tensor.flatten())
    return static_piezo_tensor, ionic_piezo_tensor, total_piezo_tensor, ionic_dielectric_tensor, static_dielectric_tensor,  total_dielectric_tensor, BEC, max_born_charge, max_dielectric, max_piezo

# Initialize empty lists to store the tensors
#piezo_tensors = []
static_piezo_tensors = []
ionic_piezo_tensors = []
total_piezo_tensors = []

ionic_dielectric_tensors = []
static_dielectric_tensors = []
total_dielectric_tensors = []

BEC_tensors= []

max_BECs=[]
max_piezos=[]
max_dielectrics = []

# Extract the directory names from the "name" column
directory_names = df["name"].tolist()

# Specify the base directory where your data is stored
base_directory = "./"

# Iterate over the directory names and read the corresponding OUTCAR files
for directory_name in directory_names:
    # Construct the full directory path
    directory_path = os.path.join(base_directory, directory_name)
    
    # Check if the directory exists
    if os.path.exists(directory_path):
        # Assuming OUTCAR is the file you want to read
        directory_path_n = os.path.join(directory_path, "piezo")
        outcar_path = os.path.join(directory_path_n, "OUTCAR_piezo")
        
        # Check if OUTCAR file exists
        if os.path.exists(outcar_path):
             static_piezo_tensor, ionic_piezo_tensor, total_piezo_tensor, ionic_dielectric_tensor, static_dielectric_tensor,  total_dielectric_tensor, BEC,max_born_charge,max_dielectric, max_piezo = read_tensors_from_outcar(outcar_path)
             # Store the tensors in the DataFrame

             static_piezo_tensors.append(static_piezo_tensor)
             ionic_piezo_tensors.append(ionic_piezo_tensor)
             total_piezo_tensors.append(total_piezo_tensor)


             static_dielectric_tensors.append(static_dielectric_tensor)
             ionic_dielectric_tensors.append(ionic_dielectric_tensor)
             total_dielectric_tensors.append(total_dielectric_tensor)

             BEC_tensors.append(BEC)
             max_BECs.append(max_born_charge)
             max_dielectrics.append(max_dielectric)
             max_piezos.append(max_piezo)

        else:
            print(f"OUTCAR not found for directory: {directory_name}")
    else:
        print(f"Directory not found: {directory_name}")

df["static_piezo_tensor"]=static_piezo_tensors
df["ionic_piezo_tensor"]=ionic_piezo_tensors
df["total_piezo_tensor"]=total_piezo_tensors
df["static_dielectric_tensor"]=static_dielectric_tensors
df["ionic_dielectric_tensor"]=ionic_dielectric_tensors
df["total_dielectric_tensor"]=total_dielectric_tensors
df["BONR_charges"]=BEC_tensors
df["max_born_charge"]=max_BECs
df["max_dielectric"]=max_dielectrics
df["max_piezo"]=max_piezos

store_dataframe_as_json(df, "update_my_df_file.json")

###df.to_csv("updated_dataframe_file.csv", index=False)        
