from matminer.featurizers.base import MultipleFeaturizer
from matminer.featurizers.composition import ElementProperty, Stoichiometry, ValenceOrbital, IonProperty
from matminer.featurizers.structure import (SiteStatsFingerprint, StructuralHeterogeneity,
                                            ChemicalOrdering, StructureComposition, MaximumPackingEfficiency)
from matminer.featurizers import composition as cf
from matminer.featurizers.conversions import StrToComposition
from matminer.featurizers.conversions import DictToObject
import pandas as pd

#feature_calculators = MultipleFeaturizer([cf.Stoichiometry(), cf.ElementProperty.from_preset("magpie"),
#                                          cf.ValenceOrbital(props=['avg']), cf.IonProperty(fast=True)])
featurizer = MultipleFeaturizer([
    SiteStatsFingerprint.from_preset("CoordinationNumber_ward-prb-2017"),
    StructuralHeterogeneity(),
    ChemicalOrdering(),
    MaximumPackingEfficiency(),
    SiteStatsFingerprint.from_preset("LocalPropertyDifference_ward-prb-2017"),
    StructureComposition(Stoichiometry()),
    StructureComposition(ElementProperty.from_preset("magpie")),
    StructureComposition(ValenceOrbital(props=['frac'])),
    StructureComposition(IonProperty(fast=True))
])
#feature_labels = feature_calculators.feature_labels()
#print(len(feature_labels))

data_orig = pd.read_csv('data_with_features_structural.csv')
#data = StrToComposition(target_col_id='composition_obj').featurize_dataframe(data_or, 'composition')
#data = feature_calculators.featurize_dataframe(data, col_id='composition_obj')

dto = DictToObject(target_col_id='structure', overwrite_data=True)
data = dto.featurize_dataframe(data_orig, 'structure')
print('Total number of features:', len(featurizer.featurize(data['structure'][0])))
data.to_csv('data_with_features.csv')
