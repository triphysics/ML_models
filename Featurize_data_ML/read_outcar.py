from pymatgen.io.vasp.outputs import Outcar
import numpy as np

# Load the OUTCAR file
outcar_file = "OUTCAR1"  # Replace with the actual path to your OUTCAR file
outcar = Outcar(outcar_file)

## Extract the piezoelectric tensor components
static_piezo_tensor = outcar.piezo_tensor
ionic_piezo_tensor = outcar.piezo_ionic_tensor

# Calculate the total piezoelectric tensor
total_piezo_tensor = np.add(static_piezo_tensor, ionic_piezo_tensor)

# Print the piezoelectric tensor in the desired array form
print("Static Piezoelectric Tensor:")
print(static_piezo_tensor)
print("\nIonic Piezoelectric Tensor:")
print(ionic_piezo_tensor)
print("\nTotal Piezoelectric Tensor:")
print(total_piezo_tensor)

# Extract the dielectric tensor components
ionic_dielectric_tensor = outcar.dielectric_ionic_tensor
static_dielectric_tensor = outcar.dielectric_tensor
BEC = outcar.born
total_dielectric_tensor=np.add(ionic_dielectric_tensor,static_dielectric_tensor)

# Print the dielectric tensor in array form
print("Ionic Dielectric Tensor:")
print(ionic_dielectric_tensor)

print("Static Dielectric Tensor:")
print(static_dielectric_tensor)

print("Total Dielectric Tensor:")
print(total_dielectric_tensor)

print("BORN effcetive charges:")
print(BEC)

