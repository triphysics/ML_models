import numpy as np
from ase.io import read
from ase.db import connect
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from ase import Atoms

#prim = read('POSCAR')
#atoms_ideal = read('POSCAR_ideal')
#dim = np.diag([3, 3,3])

def setup_phonopy(prim, dim):
    atoms_phonopy = PhonopyAtoms(symbols=prim.get_chemical_symbols(),
                                 scaled_positions=prim.get_scaled_positions(),
                                 cell=prim.cell)
    phonopy = Phonopy(atoms_phonopy, supercell_matrix=dim*np.eye(3), primitive_matrix=None)
    return phonopy

def get_phonopy_supercell(prim, dim):
    phonopy = setup_phonopy(prim, dim)
    supercell = phonopy.get_supercell()
    supercell = Atoms(cell=supercell.cell, numbers=supercell.numbers, pbc=True,
                      scaled_positions=supercell.get_scaled_positions())
    return supercell



def get_band(q_start, q_stop, N):
    """ Return path between q_start and q_stop """
    return np.array([q_start + (q_stop-q_start)*i/(N-1) for i in range(N)])
