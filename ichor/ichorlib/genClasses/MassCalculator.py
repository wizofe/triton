from pyteomics import mass
import ichorlib.msClasses.MsUtils as msu

__author__ = 'kthalassinos'


class MassCalculator(object):
    """Class used to calculate the m/z of ions, the mass etc
    the class uses as a default the fact that ions are protonated but they can also be
    sodiated, potasiated etc.

    """

    DNA_in_base = {}
    std_aa_mass = {}

    def __init__(self, sequence='', z=1, ion='H+', modification=''):
        """
        Constructor
        Make it calculate it based on what type of ion it is

                massOfPO4H=massOfPhosphorous+4*massOfOxygen+massOfHydrogen,
        massOfRibose=5*massOfCarbon+7*massOfHydrogen+2*massOfOxygen,
        massOfAdenine=5*massOfCarbon+4*massOfHydrogen+5*massOfNitrogen+massOfRibose,
        massOfCytosine=4*massOfCarbon+4*massOfHydrogen+3*massOfNitrogen+massOfOxygen+massOfRibose,
        massOfGuanine=5*massOfCarbon+4*massOfHydrogen+5*massOfNitrogen+massOfOxygen+massOfRibose,
        massOfThymine=5*massOfCarbon+5*massOfHydrogen+2*massOfNitrogen+massOfOxygen+massOfRibose,
        massOfUracil=4*massOfCarbon+3*massOfHydrogen+2*massOfNitrogen+2*massOfOxygen+massOfRibose;



        """

        self.DNA_in_base['A'] = mass.calculate_mass(formula='C5H4N5')
        self.DNA_in_base['G'] = mass.calculate_mass(formula='C5H4N5O')
        self.DNA_in_base['C'] = mass.calculate_mass(formula='C4H4N3O')
        self.DNA_in_base['T'] = mass.calculate_mass(formula='C5H5N2O2')
        self.DNA_in_base['U'] = mass.calculate_mass(formula='C4H3N2O2')
        self.DNA_in_base['DeoxyRibose'] = mass.calculate_mass(formula='C5H7O2')
        self.DNA_in_base['H'] = mass.calculate_mass(formula='H')
        self.DNA_in_base['H+'] = mass.calculate_mass(formula='H+')
        self.DNA_in_base['O'] = mass.calculate_mass(formula='O')
        self.DNA_in_base['P'] = mass.calculate_mass(formula='P')

        self.std_aa_mass = {
            'G': 57.02146,
            'A': 71.03711,
            'S': 87.03203,
            'P': 97.05276,
            'V': 99.06841,
            'T': 101.04768,
            'C': 103.00919,
            'L': 113.08406,
            'I': 113.08406,
            'N': 114.04293,
            'D': 115.02694,
            'Q': 128.05858,
            'K': 128.09496,
            'E': 129.04259,
            'M': 131.04049,
            'H': 137.05891,
            'F': 147.06841,
            'R': 156.10111,
            'Y': 163.06333,
            'W': 186.07931,
        }

    def calc_mass(self, sequence='', z=1, ion='H+', modification=''):
        """

        Args:
            sequence:
            z:
            ion:
            modification:

        Returns:

        """

    def calc_peptide_fragment(self, peptide_sequence, peptide_name,
                              peptide_five_prime_end, peptide_three_prime_end):
        """
        This uses the pyteomics mass calculator. It assumes all peptides are
        H and OH as 5 and 3 prime ends.

        Args:
            peptide_sequence:
            peptide_name:
            peptide_five_prime_end:
            peptide_three_prime_end:

        Returns:

        """

        ion_mass = 0
        pep_length = len(peptide_sequence)
        pep_type = peptide_name[0]

        #temp_mass = mass.fast_mass(peptide_sequence, ion_type=peptide_name, charge=0)

        for temp_aa in peptide_sequence:
            ion_mass += self.std_aa_mass[temp_aa]

        if pep_type in ['a']:
            ion_mass -= (self.DNA_in_base['O'] + self.DNA_in_base['H'] * 2)
        if pep_type in ['b']:
            ion_mass += 0

        return ion_mass

    def calc_oligo_fragment(self, oligo_sequence, oligo_name,
                            oligo_five_prime_end, oligo_three_prime_end):
        """

        Calculate the mass as follows:


        Args:
            oligo_sequence:
            oligo_name:

        Returns:

        """
        ion_mass = 0
        oligo_length = len(oligo_sequence)
        oligo_type = oligo_name[0]
        #print oligo_type, oligo_length, oligo_five_prime_end, oligo_three_prime_end

        # calculate mass of ion as all others are based on this one
        ion_mass = 0

        for temp_base in oligo_sequence:

            temp_mass = self.DNA_in_base[temp_base]
            ion_mass += temp_mass
            ion_mass += self.DNA_in_base['DeoxyRibose']

        mass_of_PO4 = (oligo_length -
                       1) * (self.DNA_in_base['P'] + self.DNA_in_base['O'] * 4 +
                             self.DNA_in_base['H'])

        ion_mass += mass_of_PO4
        ion_mass += mass.calculate_mass(
            formula=oligo_five_prime_end)  # usually default is OH
        ion_mass += mass.calculate_mass(
            formula=oligo_three_prime_end)  # usually default is OH

        if oligo_type in ['a']:
            ion_mass -= (self.DNA_in_base['O'] + self.DNA_in_base['H'] * 2)
        if oligo_type in ['b']:
            ion_mass += 0
        if oligo_type in ['c']:
            ion_mass += (self.DNA_in_base['P'] + self.DNA_in_base['O'] * 2 -
                         self.DNA_in_base['H'])
        if oligo_type in ['d']:
            ion_mass += (self.DNA_in_base['P'] + self.DNA_in_base['O'] * 3 +
                         self.DNA_in_base['H'])

        if oligo_type in ['w']:
            ion_mass += self.DNA_in_base['P'] + self.DNA_in_base[
                'O'] + self.DNA_in_base['H']
        if oligo_type in ['x']:
            ion_mass += self.DNA_in_base['P'] - self.DNA_in_base['H']
        if oligo_type in ['y']:
            ion_mass -= self.DNA_in_base['O'] * 2
        if oligo_type in ['z']:
            ion_mass -= self.DNA_in_base['O'] * 3 + self.DNA_in_base['H'] * 2

        return abs(
            ion_mass)  # in case ion s negative need to return the abs value

        #TODO potential bug for end fragments ie 20th in a 20mer oligo
