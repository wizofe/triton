from ichorlib.genClasses.IsotopeCalculator import IsotopeCalculator

ic = IsotopeCalculator()

elem = 'C4H10'
res = 60000
fragment = 'a1'
ic.get_isotope_spectrum(elem, res, fragment)
