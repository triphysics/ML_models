#!/usr/bin/env python
"""Use it for generating POSCARs and other input files from materials project"""
"""repsoitory using pymatgen"""

from pymatgen import MPRester
## Can use relax, single_point or bandstructure_pbe instead of latt_opt (as of now) ##
from pymatgen.io.vasp.sets import latt_opt
import warnings
warnings.filterwarnings("ignore")

m = MPRester("0LZXWNczpRl2CyOJ")
file1 = open('A2B2CS2O8.dat','w')

data = m.query("*2*2*S2O8",['material_id','pretty_formula','formation_energy_per_atom','spacegroup.symbol'])
###               ^                             ###
###               |                             ###
###   required formula of the structures        ###
###################################################

for i in range(len(data)):
        if data[i]['formation_energy_per_atom'] <= 0.2:
            f = 'POSCAR' + str(i) + '.vasp'
            g = 'POTCAR' + str(i)
            m_id = data[i]['material_id']
            form = data[i]['pretty_formula']
            tot = form + '_' + m_id; path = tot + '/latt_opt'
            structure = m.get_structure_by_material_id(m_id)
            v = latt_opt(structure)
            v.write_input(tot)
            file1.write('{:12} {:12} {:12.8f} {:12}\n'.format(data[i]['material_id'],data[i]['pretty_formula'],data[i]['formation_energy_per_atom'],data[i]['spacegroup.symbol']))
