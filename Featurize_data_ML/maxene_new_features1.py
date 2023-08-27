import pandas as pd
import re
from mendeleev import element
import numpy as np
from matminer.featurizers.conversions import StrToComposition

# Sample DataFrame with material formulas
df = pd.read_csv('data.csv')
print(df.head())

mxene_column_name = 'formula'

if mxene_column_name in df:
    df[mxene_column_name] = df[mxene_column_name].str.replace("-", "")
else:
    print(f"Column '{mxene_column_name}' not found in the DataFrame.")

# Define a function to calculate VDW radius and electronegativity
def calculate_vdw_radius(compound_formula):
    # Use regular expression to split the compound formula into elements and counts
    elements_and_counts = re.findall(r'([A-Z][a-z]*)(\d*)', compound_formula)

    # Initialize variables to store the list of VDW radii and electronegativity
    vdw_radii = []
    en_p = []
    dipole_pol = []
    density = []
    nval = []
    AM = []
    heat_of_formation = []
    # Loop through the elements and calculate the VDW radius and electronegativity
    for symbol, count_str in elements_and_counts:
        try:
            count = int(count_str) if count_str else 1  # Convert count to integer, default to 1 if empty
            elem = element(symbol)

            # Calculate the VDW radius of the element and add it to the list
            vdw_radii.append(elem.vdw_radius * count)
            en_p.append(elem.en_pauling * count)
            dipole_pol.append(elem.dipole_polarizability * count)
            density.append(elem.density * count)
            AM.append(elem.atomic_number * count)
            nval.append(elem.nvalence() * count)
            heat_of_formation.append(elem.heat_of_formation * count)
        except ValueError:
            print(f"Element {symbol} not found in Mendeleev database.")
    print(nval)   
    return vdw_radii, en_p, dipole_pol, density, AM, nval, heat_of_formation

# Apply the calculate_vdw_radius function to the DataFrame and create new columns
df[['VDWRadii', 'electronegativity', 'dipole_pol', 'density', 'AN', 'nval', 'heat_of_formation']] = df['formula'].apply(calculate_vdw_radius).apply(pd.Series)

# Calculate the standard deviation and mean of VDW radii and electronegativity and create new columns

df['VDWR_StdDev'] = df['VDWRadii'].apply(lambda x: pd.Series(x).std() if x else None)
df['VDWR_mean'] = df['VDWRadii'].apply(lambda x: pd.Series(x).mean() if x else None)

df['en_StdDev'] = df['electronegativity'].apply(lambda x: pd.Series(x).std() if x else None)
df['en_mean'] = df['electronegativity'].apply(lambda x: pd.Series(x).mean() if x else None)

df['DP_StdDev'] = df['dipole_pol'].apply(lambda x: pd.Series(x).std() if x else None)
df['DP_mean'] = df['dipole_pol'].apply(lambda x: pd.Series(x).mean() if x else None)

df['rho_StdDev'] = df['density'].apply(lambda x: pd.Series(x).std() if x else None)
df['rho_mean'] = df['density'].apply(lambda x: pd.Series(x).mean() if x else None)

df['AN_StdDev'] = df['AN'].apply(lambda x: pd.Series(x).std() if x else None)
df['AN_mean'] = df['AN'].apply(lambda x: pd.Series(x).mean() if x else None)

df['nval_StdDev'] = df['nval'].apply(lambda x: pd.Series(x).std() if x else None)
df['nval_mean'] = df['nval'].apply(lambda x: pd.Series(x).mean() if x else None)

df['EH_StdDev'] = df['heat_of_formation'].apply(lambda x: pd.Series(x).std() if x else None)
df['EH_mean'] = df['heat_of_formation'].apply(lambda x: pd.Series(x).mean() if x else None)


# Drop the intermediate columns (VDWRadii and electronegativity) if needed
exclude=['VDWRadii', 'electronegativity', 'dipole_pol', 'density', 'AN', 'nval', 'heat_of_formation']

df = df.drop(exclude, axis=1)

print(df)

