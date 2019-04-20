__author__ = 'kthalassinos'

from pyteomics import mass


class Fragment(object):
    """Class representing a fragment ion

    Representation of the seuence and name of a fragment ion.
    I deliberately do not calculate the m/z here as it can then be calculated on the fly
    based on the charge (z) that is required
    The mass calculated is the without a charge
    """

    def __init__(self, sequence='', ion=''):
        """
        Constructor
        """
        self.ion = ion
        self.sequence = sequence
        self.modification = ''
        self.mass = 0
        self.position_from = 0
        self.position_to = 0
        self.amino_acid = ''  # the amino acid identified from this fragment
