__author__ = 'Kostas'

from pyteomics import mass
from ichorlib.genClasses.Modification import Modification


class Modification(object):

    """Class representing a modification

    """
    def __init__(self):
        """
        Constructor
        """

        self.modifications = []

        self.my_mods = {
            '': 0,
            '+BS3':        mass.calculate_mass(formula='C8H10O2'),
            'BS3x2':      mass.calculate_mass(formula='C16H20O4'),
            '-H2O':        - mass.calculate_mass(formula='H2O'),
            '-NH3':        - mass.calculate_mass(formula='NH3'),
            'S-S':        - mass.calculate_mass(formula='H2'),
            'S-Sx2':        - mass.calculate_mass(formula='H4'),
            'S-Sx3':        - mass.calculate_mass(formula='H6'),
            '-H20x2':        - mass.calculate_mass(formula='H4O2'),
            '-H20x3':        - mass.calculate_mass(formula='H6O3'),
            '-H2O-NH3':     - mass.calculate_mass(formula='H5ON'),
            '-dHA':     -34,
            '+thio':     +32,
        }

    def read_mods_from_JSON(self, JSON_file = './params/modifications.json'):
        print("Loading mods from " + JSON_file)

        temp_mod = Modification(name='Phospho_test', formula='PO3', residue_affected = 'S', fixed_modification = 0)

        self.modifications.append(temp_mod)

