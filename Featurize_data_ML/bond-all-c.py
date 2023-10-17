import numpy as np
from pymatgen.core import Structure

# Function to calculate bond length
def bondlength(structure, index1, index2):
    atom1 = structure[index1]
    atom2 = structure[index2]
    return np.linalg.norm(atom1.coords - atom2.coords)

# calculate bond angle, we assume index 2 is the center atom for bond angle
def bondangle(structure, index1, index2, index3):
    atom1 = structure[index1]
    atom2 = structure[index2]
    atom3 = structure[index3]

    v1 = (atom2.coords-atom1.coords)/np.linalg.norm(atom2.coords-atom1.coords)
    v2 = (atom2.coords-atom3.coords)/np.linalg.norm(atom2.coords-atom3.coords)
    angle = np.arccos(np.dot(v1, v2))/np.pi*180.0
    # convert radius to angle
    return angle


# Function to reduce the input string to one element at a time
def reduce_input_string(input_string):
    elements = input_string.split('-')
    reduced_string = '-'.join([elements[0], elements[1], elements[2]])
    for i in range(3, len(elements)):
        if elements[i] in ['OH', 'OCN', 'NCO', 'SCN', 'CN', 'NCS']:
            reduced_string += '-' + elements[i][:1]
        else:
            reduced_string += '-' + elements[i]
    return reduced_string

# Example input string
input_string = "Sc-Sc-C-OH-OCN"

# Reduce the input string
reduced_input_string = reduce_input_string(input_string)

print("Reduced input string:", reduced_input_string)


# Load structure from file (replace with the appropriate file path)
structure = Structure.from_file("POSCAR1.vasp")

# Modified function to measure bond lengths and angles and label atoms based on the reduced input string
def map_labels_to_indices(structure, reduced_input_string):
    elements = reduced_input_string.split('-')

    labels_to_indices = {
        'CM': None,
        'M1': None,
        'M2': None,
        'FG1': None,
        'FG2': None
    }

    # Map CM to the first carbon atom with x and y as 0.0
    cm_indices = [index for index, site in enumerate(structure) if site.species_string == elements[2] and np.allclose(site.coords[:2], [0.0, 0.0])]
    if cm_indices:
        labels_to_indices['CM'] = cm_indices[0]

    # Find all Sc atom indices
    sc_indices = [index for index, site in enumerate(structure) if site.species_string == elements[0]]

    # If there are two Sc atoms, assign them as M1 and M2 based on their positions
    if len(sc_indices) == 2:
        # Determine M1 and M2 based on z positions
        sc_atom1 = structure[sc_indices[0]]
        sc_atom2 = structure[sc_indices[1]]

        if sc_atom1.coords[2] < sc_atom2.coords[2]:
            labels_to_indices['M1'] = sc_indices[0]
            labels_to_indices['M2'] = sc_indices[1]
        else:
            labels_to_indices['M1'] = sc_indices[1]
            labels_to_indices['M2'] = sc_indices[0]

    # Map FG1 and FG2 based on their z positions or element type if z is the same
    fg1_indices = [index for index, site in enumerate(structure) if site.species_string == elements[-2]]
    fg2_indices = [index for index, site in enumerate(structure) if site.species_string == elements[-1]]

    if elements[-2] == 'O' or elements[-1] == 'O':
        # Check length of fg1_indices and fg2_indices
        if len(fg1_indices) > 1:
            # Compare z positions to determine FG1 and FG2
            fg1_atom = structure[max(fg1_indices, key=lambda i: structure[i].coords[2])]
            labels_to_indices['FG2'] = structure.index(fg1_atom)
            labels_to_indices['FG1'] = fg2_indices[0]
        elif len(fg1_indices) == 1 and len(fg2_indices) == 1:
            fg1_atom = structure[fg1_indices[0]]
            fg2_atom = structure[fg2_indices[0]]

            if fg1_atom.coords[2] < fg2_atom.coords[2]:
                labels_to_indices['FG1'] = fg1_indices[0]
                labels_to_indices['FG2'] = fg2_indices[0]
            else:
                labels_to_indices['FG1'] = fg2_indices[0]
                labels_to_indices['FG2'] = fg1_indices[0]
    else:
        # Assign FG1 and FG2 based on their z positions
        if fg1_indices and fg2_indices:
            if len(fg1_indices) == 1 and len(fg2_indices) == 1:
                fg1_atom = structure[fg1_indices[0]]
                fg2_atom = structure[fg2_indices[0]]

                if fg1_atom.coords[2] < fg2_atom.coords[2]:
                    labels_to_indices['FG1'] = fg1_indices[0]
                    labels_to_indices['FG2'] = fg2_indices[0]
                else:
                    labels_to_indices['FG1'] = fg2_indices[0]
                    labels_to_indices['FG2'] = fg1_indices[0]

    return labels_to_indices


# Map labels to atom indices
label_to_indices = map_labels_to_indices(structure, reduced_input_string)

# Print the mapping of labels to atom indices
print("Mapping of labels to atom indices:")
for label, index in label_to_indices.items():
    print(f"{label}: {index}")

FG2_M2_CM=bondangle(structure,label_to_indices['FG2'],label_to_indices['M2'], label_to_indices['CM'])
M2_CM_M1=bondangle(structure,label_to_indices['M2'],label_to_indices['CM'], label_to_indices['M1'])
CM_M1_FG1=bondangle(structure,label_to_indices['CM'],label_to_indices['M1'], label_to_indices['FG1'])
FG2_M2=bondlength(structure,label_to_indices['FG2'], label_to_indices['M2'])
M2_CM=bondlength(structure,label_to_indices['M2'], label_to_indices['CM'])
CM_M1=bondlength(structure,label_to_indices['CM'], label_to_indices['M1'])
M1_FG1=bondlength(structure,label_to_indices['M1'], label_to_indices['FG1'])

print(FG2_M2_CM)
print(M2_CM_M1)
print(CM_M1_FG1)
print(FG2_M2)
print(M2_CM)
print(CM_M1)
print(M1_FG1)
    
