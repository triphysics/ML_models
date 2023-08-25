#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 09:25:09 2018
"""
import pandas as pd
from pymatgen import MPRester, Element
from pymatgen.io.vasp.sets import MPRelaxSet
import itertools
import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('orthorhombic_ternary.csv')
m = MPRester("k1gBNtKCWL30P4bZ")

for i in range(len(data)):
    mid = data['material_id'][i]
    form = data['pretty_formula'][i]
    path = form + '_' + mid
    struc = m.get_structure_by_material_id(mid)
    v = MPRelaxSet(struc)
    v.write_input(path)
