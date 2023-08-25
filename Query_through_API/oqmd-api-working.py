# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 23:05:33 2020

@author: ritesh
"""

import warnings
warnings.filterwarnings('ignore')
import qmpy_rester as qr
from qmpy import io
import pandas as pd
from ase.spacegroup import crystal as crys
from ase.io import read, write
from ase import Atoms

## OQMD-API format
comp = []; space_group = []; oqmd_id = []; formation_energy = []; stability = []
n_atoms = []
with qr.QMPYRester() as q:
   kwargs = {
       # 'element_set': '(Fe-Mn),O',      # composition include (Fe OR Mn) AND O
       'composition': 'Ni-C-N-S',
       'stability': '<0',            # hull distance smaller than -0.1 eV
       # 'natom': '<10',                  # number of atoms less than 10
       # 'ntypes': '<4',
       # 'filter': 'element_set=Ni OR C OR N',

       }
   list_of_data = q.get_oqmd_phases(**kwargs)

## OPTIMADE-API format
# with qr.QMPYRester() as q:
    # kwargs = {
        # 'elements': 'Ni-C-N',      # composition include (Fe OR Mn) AND O
        # '_oqmd_stability': '<0',            # hull distance smaller than -0.1 eV
        # 'nelements': '<4',                  # number of atoms less than 10
        # }
    # list_of_data = q.get_optimade_structures(**kwargs)

print(len(list_of_data['data']))
# print(list_of_data['data'][0])

def make_sym_coor(lis):
	sit = lis['sites']
	bas = [sit[i].split('@') for i in range(len(sit))]
	symbols = []; coordinate = []
	for i in range(len(bas)):
		sym = bas[i][0].split()[0]
		symbols.append(sym)
		coor = bas[i][1].split()
		coor_ = [float(coor[i]) for i in range(len(coor))]
		coordinate.append(coor_)
	return symbols, coordinate

def make_crys(lis):
	spg = lis['spacegroup']
	symbols, coordinate = make_sym_coor(lis)
	latt = lis['unit_cell']
	return Atoms(symbols=symbols, scaled_positions=coordinate, cell=latt)

for  i in range(len(list_of_data['data'])):
	name = list_of_data['data'][i]['name']
	comp.append(name)
	# sg = list_of_data['data'][i]['spacegroup']
	space_group.append(list_of_data['data'][i]['spacegroup'])
	stability.append(list_of_data['data'][i]['stability'])
	formation_energy.append(list_of_data['data'][i]['delta_e'])
	oqmd_id.append(list_of_data['data'][i]['entry_id'])
	n_atoms.append(list_of_data['data'][i]['natoms'])
	struc = make_crys(list_of_data['data'][i])
	f = str(name) + '.vasp'
	write(f, struc)

dict = {'composition': comp, 'space group':space_group, 'hull distance':stability, 
        'formation energy':formation_energy, 'oqmd id': oqmd_id, '# atoms': n_atoms}

df = pd.DataFrame(dict)
df.to_csv('list.csv', index=False)
