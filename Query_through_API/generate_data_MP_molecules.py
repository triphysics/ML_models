#!/usr/bin/env python3

from mp_api import MPRester
import pandas as pd
api = MPRester('EdEVdNMEIH1znawl2bTNWsGAwkaU390P')

search = api.molecules.search(nelements=[2,6])

smiles = []
ion_energy = []
elec_aff = []
mpid = []
charge = []
for i in range(len(search)):
    smiles.append(search[i].smiles)
    ion_energy.append(search[i].IE)
    elec_aff.append(search[i].EA)
    mpid.append(search[i].task_id)
    charge.append(search[i].charge)

fin_dict = {'task_id': mpid, 'smiles': smiles, 'IE': ion_energy, 'EA': elec_aff, 'charge': charge}
df = pd.DataFrame(fin_dict)
df.to_csv('init_MP_data.csv', index=False)
