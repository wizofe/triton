from ichorlib.seqClasses.Fragmentor import Fragmentor
import rpy2

pep_sequence = 'AITEGK'

fr = Fragmentor()

fragments = fr.fragment_peptide(pep_sequence)

for fragment in fragments:
    print fragment


print rpy2.__version__
