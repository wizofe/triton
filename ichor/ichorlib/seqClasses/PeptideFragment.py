from ichorlib.seqClasses.Fragment import Fragment

__author__ = 'kthalassinos'


class PeptideFragment(Fragment):
    """Class representing a peptide fragment ion

    Representation of the seuence and name of a fragment ion.
    I deliberately do not calculate the m/z here as it can then be calculated on the fly
    based on the charge (z) that is required
    The mass calculated is the without a charge
    """

    def __init__(self, sequence='', ion=''):

        Fragment.__init__(self, sequence, ion)
        self.five_prime_end = 'H'
        self.three_prime_end = 'OH'

    def __str__(self):
        return 'Peptide  {0:<5} {1:<25} {2:<3} {3:<3} {4:<3} {5:<3}'.format(
            self.ion, self.sequence, self.position_from, self.position_to,
            self.five_prime_end, self.three_prime_end)
