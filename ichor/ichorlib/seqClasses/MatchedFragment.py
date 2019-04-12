from ichorlib.seqClasses.Fragment import Fragment

__author__ = 'kthalassinos'



class MatchedFragment(Fragment):
    """Class representing a fragment ion

    Representation of the seuence and name of a fragment ion.
    I deliberately do not calculate the m/z here as it can then be calculated on the fly
    based on the charge (z) that is required
    """

    def __init__(self, sequence='', ion='', z=1, mz_theoretical=0, mz_experimental=0, modification=0, ppm=0):
        """
        Constructor
        """
        self.ion = ion
        self.sequence = sequence
        self.modification = modification
        self.z = z
        self.mz_theoretical = mz_theoretical
        self.mz_experimental = mz_experimental
        self.ppm = 0
