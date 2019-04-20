from ichorlib.seqClasses.PeptideFragment import PeptideFragment
from ichorlib.seqClasses.OligoFragment import OligoFragment
from ichorlib.genClasses.Modifications import my_mods
import copy

__author__ = 'kthalassinos'


class Fragmentor(object):
    '''
    classdocs
    '''

    def __init__(self):
        """Create fragments, sort fragments, modify fragments

        """

        print('I am the Fragmentor hahahaha!')

    def fragment_peptide(self, peptide_sequence):
        """Given a peptide sequence returns all a,b,c and x,y,z ions

        :param peptide: the peptide sequence
        :return: fragments: an array containing fragment objects sorted by name

        """
        fragments = []

        peptidelength = len(peptide_sequence)

        for i in range(0, peptidelength - 1):

            sequence = peptide_sequence[:i + 1]
            position_from = 1
            position_to = i + 1

            a_ion = 'a' + str(i + 1)
            b_ion = 'b' + str(i + 1)
            c_ion = 'c' + str(i + 1)

            afragment = PeptideFragment(sequence, a_ion)
            bfragment = PeptideFragment(sequence, b_ion)
            cfragment = PeptideFragment(sequence, c_ion)

            afragment.position_from = position_from
            afragment.position_to = position_to
            bfragment.position_from = position_from
            bfragment.position_to = position_to
            cfragment.position_from = position_from
            cfragment.position_to = position_to

            k = i + 1

            x_ion = 'x' + str(peptidelength - 1 - i)
            y_ion = 'y' + str(peptidelength - 1 - i)
            z_ion = 'z' + str(peptidelength - 1 - i)

            sequence = peptide_sequence[k:peptidelength]
            position_from = k + 1
            position_to = peptidelength

            xfragment = PeptideFragment(sequence, x_ion)
            yfragment = PeptideFragment(sequence, y_ion)
            zfragment = PeptideFragment(sequence, z_ion)

            xfragment.position_from = position_from
            xfragment.position_to = position_to
            yfragment.position_from = position_from
            yfragment.position_to = position_to
            zfragment.position_from = position_from
            zfragment.position_to = position_to

            fragments.append(afragment)
            fragments.append(bfragment)
            fragments.append(cfragment)
            fragments.append(xfragment)
            fragments.append(yfragment)
            fragments.append(zfragment)

            #print i, peptidelength-i, peptide[:i], peptide[i:]

        precursorfragment = PeptideFragment(peptide_sequence, 'M1')
        precursorfragment.posFrom = 1
        precursorfragment.posTo = peptidelength
        fragments.append(precursorfragment)

        fragments.sort(key=lambda x: x.ion, reverse=False)

        return fragments

    def fragment_oligo(self, oligo_sequence):
        """
        Given an oligo sequence calculates all the fragments
        :param oligo_sequence:
        :return:
        """
        fragments = []

        oligo_length = len(oligo_sequence)

        for i in range(0, oligo_length - 1):

            sequence = oligo_sequence[:i + 1]
            position_from = 1
            position_to = i + 1

            a_ion = 'a' + str(i + 1)
            b_ion = 'b' + str(i + 1)
            c_ion = 'c' + str(i + 1)
            d_ion = 'd' + str(i + 1)

            afragment = OligoFragment(sequence, a_ion)
            bfragment = OligoFragment(sequence, b_ion)
            cfragment = OligoFragment(sequence, c_ion)
            dfragment = OligoFragment(sequence, d_ion)

            afragment.position_from = position_from
            afragment.position_to = position_to
            bfragment.position_from = position_from
            bfragment.position_to = position_to
            cfragment.position_from = position_from
            cfragment.position_to = position_to
            dfragment.position_from = position_from
            dfragment.position_to = position_to

            k = i + 1

            w_ion = 'w' + str(oligo_length - 1 - i)
            x_ion = 'x' + str(oligo_length - 1 - i)
            y_ion = 'y' + str(oligo_length - 1 - i)
            z_ion = 'z' + str(oligo_length - 1 - i)

            sequence = oligo_sequence[k:oligo_length]
            position_from = k + 1
            position_to = oligo_length

            wfragment = OligoFragment(sequence, w_ion)
            xfragment = OligoFragment(sequence, x_ion)
            yfragment = OligoFragment(sequence, y_ion)
            zfragment = OligoFragment(sequence, z_ion)

            wfragment.position_from = position_from
            wfragment.position_to = position_to
            xfragment.position_from = position_from
            xfragment.position_to = position_to
            yfragment.position_from = position_from
            yfragment.position_to = position_to
            zfragment.position_from = position_from
            zfragment.position_to = position_to

            fragments.append(afragment)
            fragments.append(bfragment)
            fragments.append(cfragment)
            fragments.append(dfragment)
            fragments.append(wfragment)
            fragments.append(xfragment)
            fragments.append(yfragment)
            fragments.append(zfragment)

            #print i, peptidelength-i, peptide[:i], peptide[i:]

        precursorfragment = OligoFragment(oligo_sequence, 'M1')
        precursorfragment.posFrom = 1
        precursorfragment.posTo = oligo_length
        fragments.append(precursorfragment)

        fragments.sort(key=lambda x: x.ion, reverse=False)

        return fragments

    def modifyFragments(self, fragments, typetomodify, modification):
        """
        TODO delete this and have it so that the matcher class performs the modifications
        the logic is that a modification is a parameter of the match
        :param fragments:
        :param typetomodify:
        :param modification:
        :return:
        """

        modifiedfragments = []

        maxfragments = len(fragments)

        for i in range(0, maxfragments):

            if fragments[i].ion[0] == typetomodify:

                modfragment = copy.deepcopy(fragments[i])

                modfragment.ion += modification
                modfragment.mz += my_mods[modification]
                modifiedfragments.append(modfragment)

                #print modfragment.printme()

        return modifiedfragments
