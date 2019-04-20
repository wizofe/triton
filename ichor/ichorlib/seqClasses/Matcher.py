__author__ = 'kthalassinos'


class Matcher(object):
    """Class that performs the match between experimental and theoretical masses

    Here modifications and what charge states to be conidered are specified.
    """

    def __init__(self, sequence='', ion='', modification=''):
        """
        Constructor
        """
        self.ion = ion
        self.sequence = sequence
        self.modification = modification
        self.mass = 0
        self.position_from = 0
        self.position_to = 0
        self.calculate_mass()

    def print_me(self):
        return "Matcher ", self.ion, self.sequence, self.modification, self.position_from, self.position_to, self.mass
