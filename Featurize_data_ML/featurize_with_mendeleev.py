import pandas as pd
import re
from mendeleev import element

# Sample DataFrame with material formulas
data = {
    "Formula": ["FeFeOOO", "H2O", "NaCl", "C2H4"]
}

df = pd.DataFrame(data)

# Function to calculate mean VDW radius
def mean_vdw_radius(compound_formula):
    # Use regular expression to split the compound formula into elements and counts
    elements_and_counts = re.findall(r'([A-Z][a-z]*)(\d*)', compound_formula)

    # Initialize variables to store the total VDW radius and the total number of atoms
    total_radius = 0
    total_atoms = 0

    # Loop through the elements and calculate the mean VDW radius
    for symbol, count_str in elements_and_counts:
        try:
            count = int(count_str) if count_str else 1  # Convert count to integer, default to 1 if empty
            elem = element(symbol)
            
            # Add the VDW radius of the element multiplied by the count to the total
            total_radius += elem.vdw_radius * count
            total_atoms += count
        except ValueError:
            print(f"Element {symbol} not found in Mendeleev database.")

    # Calculate the mean VDW radius
    if total_atoms > 0:
        mean_radius = total_radius / total_atoms
        return mean_radius
    else:
        return None

# Apply the mean_vdw_radius function to the DataFrame and create a new column
df['VDWRadius'] = df['Formula'].apply(mean_vdw_radius)

# Display the DataFrame
print(df)

