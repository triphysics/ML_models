from __future__ import print_function
import ase.db
from ase.phasediagram import PhaseDiagram

con = ase.db.connect('cubic_perovskites.db')

references = [(row.formula, row.energy)
              for row in con.select('reference')]

fd = open('abo3.csv', 'w')
# print('# id, formula, heat of formation [eV/atom]', file=fd)
for row in con.select(combination='ABO3'):
    pd = PhaseDiagram(references, filter=row.formula, verbose=False)
    energy = pd.decompose(row.formula)[0]
    heat = (row.energy - energy) / row.natoms
    if (heat < 0.21):
        formula = row.A_ion + row.B_ion + row.anion
        # print('{0}, {1}, {2:.3f}'.format(row.id, formula, heat), file=fd)
        print formula
