import numpy as np
from pymatgen.core import Structure

structure = Structure.from_file("POSCAR1.vasp")

# Function to get atom indices for specified species
def get_atom_indices(structure, species):
    indices = []
    for i, site in enumerate(structure):
        if site.species_string in species:
            indices.append(i)
    return indices

# Get atom indices for Sc, Y, and C
sc_indices = get_atom_indices(structure, ['Sc'])
y_indices = get_atom_indices(structure, ['Y'])
c_indices = get_atom_indices(structure, ['C'])

# Function to calculate bond length
def bondlength(structure, index1, index2):
    atom1 = structure[index1]
    atom2 = structure[index2]
    
    # Check conditions for bond length calculation
    if np.isclose(atom2.coords[0], 0.0) and np.isclose(atom2.coords[1], 0.0):
        return np.linalg.norm(atom1.coords - atom2.coords)
    else:
        return None

# Function to calculate bond angle
def bondangle(structure, index1, index2, index3):
    atom1 = structure[index1]
    atom2 = structure[index2]
    atom3 = structure[index3]

    # Check conditions for bond angle calculation
    if np.isclose(atom2.coords[0], 0.0) and np.isclose(atom2.coords[1], 0.0):
        v1 = (atom2.coords - atom1.coords) / np.linalg.norm(atom2.coords - atom1.coords)
        v2 = (atom2.coords - atom3.coords) / np.linalg.norm(atom2.coords - atom3.coords)
        angle = np.arccos(np.dot(v1, v2)) / np.pi * 180.0
        return angle
    else:
        return None

# Calculate bond angles when either Sc or Y is present
if len(c_indices) > 1:
    # Filter c_indices based on x and y coordinates being 0.0
    filtered_c_indices = [c_idx for c_idx in c_indices if np.isclose(structure[c_idx].coords[0], 0.0) and np.isclose(structure[c_idx].coords[1], 0.0)]
    if len(filtered_c_indices) == 1:
        c_idx = filtered_c_indices[0]
        bond1 = bondlength(structure, sc_indices[0], c_idx)
        bond2 = bondlength(structure, sc_indices[1], c_idx)
        if bondlength is not None:
            print("Bond length (Sc or Y-C):", sc_indices[0], c_idx + 1, bond1)
            print("Bond length (Sc or Y-C):", sc_indices[1], c_idx + 1, bond2)
    else:
        print("Multiple atoms in c_indices have x and y coordinates as 0.0. Cannot calculate bond angles.")
elif len(c_indices) == 1:
    c_idx = c_indices[0]
    bond1 = bondlength(structure, sc_indices[0], c_idx)
    bond2 = bondlength(structure, sc_indices[0], c_idx)
    if bondlength is not None:
        print("Bond length (Sc or Y-C):", sc_indices[0], c_idx + 1, bond1)
        print("Bond length (Sc or Y-C):", sc_indices[1], c_idx + 1, bond2)
else:
    print("No atoms in c_indices. Cannot calculate bond angles.")



if len(c_indices) > 1:
    # Filter c_indices based on x and y coordinates being 0.0
    filtered_c_indices = [c_idx for c_idx in c_indices if np.isclose(structure[c_idx].coords[0], 0.0) and np.isclose(structure[c_idx].coords[1], 0.0)]
    if len(filtered_c_indices) == 1:
        c_idx = filtered_c_indices[0]
        bond_angle = bondangle(structure, sc_indices[0], c_idx, sc_indices[1])
        if bond_angle is not None:
            print("Bond angle (Sc or Y, C, Sc or Y):", sc_indices[0], c_idx + 1, sc_indices[1], bond_angle)
    else:
        print("Multiple atoms in c_indices have x and y coordinates as 0.0. Cannot calculate bond angles.")
elif len(c_indices) == 1:
    c_idx = c_indices[0]
    bond_angle = bondangle(structure, sc_indices[0], c_idx, sc_indices[1])
    if bond_angle is not None:
        print("Bond angle (Sc or Y, C, Sc or Y):", sc_indices[0], c_idx + 1, sc_indices[1], bond_angle)
else:
    print("No atoms in c_indices. Cannot calculate bond angles.")
    
