__author__ = 'kthalassinos'

class Modification(object):

    """Class representing a modification

    """

    def __init__(self, name='', formula='', residue_affected = '', fixed_modification = 0):
        """
        Constructor
        """
        self.name = name
        self.formula = formula
        self.residue_affected = residue_affected
        self.fixed_modification = fixed_modification
        self.modification_mass = 0
        self.position = 0
