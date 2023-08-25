#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 18:41:19 2018
"""

from matminer.data_retrieval.retrieve_MP import MPDataRetrieval
mpdr = MPDataRetrieval(api_key="k1gBNtKCWL30P4bZ")
from pymatgen import Element
elem = [el.symbol for el in Element
        if el.Z in (3,11,19,37,55,87,4,12,20,38,56,88,21,22,23,24,25,26,27,28,29,30,
                    57,58,59,60,61,62,63,64,65,66,67,68,69,70,13,31,49,81,14,32,50,
                    82,15,33,51,83,17,35,53,85)]
nelem = [el.symbol for el in Element
        if el.Z not in (3,11,19,37,55,87,4,12,20,38,56,88,21,22,23,24,25,26,27,28,29,30,
                    57,58,59,60,61,62,63,64,65,66,67,68,69,70,13,31,49,81,14,32,50,
                    82,15,33,51,83,17,35,53,85)]
#print(len(elem))
#print(len(nelem))
#print(nelem)
df = mpdr.get_dataframe(criteria={"elements": {"$in": elem, "$nin": nelem}, "nelements": 3, "band_gap": {"$gt": 0.0}, "spacegroup.crystal_system": "orthorhombic", "nsites": {"$lt": 7}},
                        properties=['material_id', 'pretty_formula', 'spacegroup.symbol', 'nsites', 'band_gap'])
print(len(df))
df.to_csv('orthorhombic_ternary.csv')
