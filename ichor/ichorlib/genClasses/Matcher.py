import ichorlib.msClasses.MsUtils as msu
from ichorlib.genClasses.MassCalculator import MassCalculator
from ichorlib.genClasses.Modifications import my_mods
import pandas as pd
import numpy as np
from pyteomics import mass


__author__ = 'kthalassinos'


class Matcher(object):
    """
    Class used to perform matching between experimental and theoretical data
    The matcher will also handle the modifications

    """

    def __init__(self):
        """

        """
        self.mc = MassCalculator()
        self.column_headers = ['Sequence', 'Ion', 'Charge', 'Mass_Theor', 'Modifications', 'Oligo_base']
        self.column_headers_search_space = ['Sequence', 'Ion', 'Charge', 'Mass_Theor', 'Modifications', 'Oligo_base', 'Mass_Obs', 'Intensity']

    def modify_oligo_fragments(self, fragment, modifications):
        """
        At the moment this only takes as input a dictionary of
        name of modification - residue number where modification occurs (starting at 1)
        e.g.
        modifications = {
            '+thio':    2,
            '-NH3':     4
        }

        In cases where a mofication applies to all residues of a certain kind
        have code generate such a dictionary ie dont do it in this function instead
        pass the following

        modifications = {
            '+thio':    2,
            '+thio':    4
        }


        Args:
            fragment:
            modifications:

        Returns: Mass of modified fragment and modification

        """

        total_modification_mass = 0
        modification_string = ''

        for key, value in modifications.items():

            if isinstance(value, int):

                if fragment.position_from <= value <= fragment.position_to:
                    total_modification_mass += my_mods[key]
                    modification_string += key + ' '

        return {'modification': modification_string, 'modification_mass': total_modification_mass}

    def create_search_space(self, fragments, charges, modifications):
        """

        Args:
            fragments: An array of Fragment objects
            charges: The charges to consider
            modifications: The modifications to consider
            modifications is a dictionary with first element the
            mod name and second the residue(s) or positions affected

        Returns:
            A pandas dataframe with the fragment match information

        """
        #TODO add extra columns in dataframe so that during the match you can populate them
        data_to_save = []  # print "Searching mass {0:10.3f}".format(experimental_mass)

        for fragment in fragments:

            frag_string_modified = ''
            oligo_position = ''
            frag_mass = self.mc.calc_oligo_fragment(fragment.sequence, fragment.ion, fragment.five_prime_end,
                                                    fragment.three_prime_end)

            if fragment.ion[0] in ['a', 'b', 'c', 'd', 'M']:
                oligo_position = fragment.position_to
            if fragment.ion[0] in ['w', 'x', 'y', 'z']:
                oligo_position = fragment.position_from - 1

            for z in charges:

                fragm_mz = abs(msu.calc_mz(frag_mass, z))  # need to abs for negatively charged ions
                data_to_save.append([fragment.sequence, fragment.ion, z, fragm_mz, frag_string_modified, oligo_position])

            for modification in modifications:

                to_modify_with = self.modify_oligo_fragments(fragment, modification)

                if to_modify_with['modification_mass'] > 0:

                    frag_mass_modified = frag_mass + to_modify_with['modification_mass']
                    frag_string_modified = to_modify_with['modification']

                    for z in charges:

                        fragm_mz = abs(msu.calc_mz(frag_mass_modified, z))

                        # print '{0:<30} {1:<5} {2:<3} {3:10.3f} {4:10.3f} {5:10.3f} {6:7.1f} {7}'.format(fragment.sequence, fragment.ion, z, experimental_mass, experimental_intensity, fragm_mz, ppm_calculated, frag_string_modified)
                        data_to_save.append(
                                [fragment.sequence, fragment.ion, z,
                                 fragm_mz, frag_string_modified, oligo_position])

        df = pd.DataFrame(data_to_save, columns=self.column_headers)
        #df.to_csv('matched_fragments.csv')

        return df

    def match_oligo_fragments(self, fragments, mass_specrtum, ppm_error, charges, modifications):
        """

        Args:
            fragments: An array of Fragment objects
            mass_specrtum: A MassSpectrum object
            ppm_error: The ppm error used for the match
            charges: The charges to consider
            modifications: The modifications to consider
            modifications is a dictionary with first element the
            mod name and second the residue(s) or positions affected

        Returns:
            A pandas dataframe with the fragment match information

        """

        data_to_save = []

        for i in range(len(mass_specrtum.topN_xvals)):

            experimental_mass = mass_specrtum.topN_xvals[i]
            experimental_intensity = mass_specrtum.topN_yvals[i]

            #print "Searching mass {0:10.3f}".format(experimental_mass)

            for fragment in fragments:

                frag_string_modified = ''
                oligo_position = ''
                frag_mass = self.mc.calc_oligo_fragment(fragment.sequence, fragment.ion, fragment.five_prime_end,
                                                   fragment.three_prime_end)

                if fragment.ion[0] in ['a', 'b', 'c', 'd', 'M']:
                    oligo_position = fragment.position_to
                if fragment.ion[0] in ['w', 'x', 'y', 'z']:
                    oligo_position = fragment.position_from - 1

                for z in charges:

                    fragm_mz = abs(msu.calc_mz(frag_mass, z)) # need to abs for negatively charged ions
                    ppm_calculated = msu.calcppmerror(experimental_mass, fragm_mz)

                    if abs(ppm_calculated) < ppm_error:

                        #print '{0:<30} {1:<5} {2:<3} {3:10.3f} {4:10.3f} {5:10.3f} {6:7.1f}'.format(fragment.sequence, fragment.ion, z, experimental_mass, experimental_intensity, fragm_mz, ppm_calculated)

                        data_to_save.append([fragment.sequence, fragment.ion, z, experimental_mass, experimental_intensity, fragm_mz, ppm_calculated, frag_string_modified, oligo_position])

                for modification in modifications:

                    to_modify_with = self.modify_oligo_fragments(fragment, modification)

                    if to_modify_with['modification_mass'] > 0:

                        frag_mass_modified = frag_mass + to_modify_with['modification_mass']
                        frag_string_modified = to_modify_with['modification']

                        for z in charges:

                            fragm_mz = abs(msu.calc_mz(frag_mass_modified, z))
                            ppm_calculated = msu.calcppmerror(experimental_mass, fragm_mz)

                            if abs(ppm_calculated) < ppm_error:

                                #print '{0:<30} {1:<5} {2:<3} {3:10.3f} {4:10.3f} {5:10.3f} {6:7.1f} {7}'.format(fragment.sequence, fragment.ion, z, experimental_mass, experimental_intensity, fragm_mz, ppm_calculated, frag_string_modified)
                                data_to_save.append([fragment.sequence, fragment.ion, z, experimental_mass, experimental_intensity,
                                     fragm_mz, ppm_calculated, frag_string_modified, oligo_position])

        df = pd.DataFrame(data_to_save, columns=self.column_headers)
        #df.to_csv('matched_fragments.csv')

        return df

    def match_oligo_fragments_pandas(self, df_search_space, mass_specrtum, ppm_error):
        """

        Args:
            df_search_space:
            mass_specrtum:
            ppm_error:

        Returns:

        """

        search_results_array = []

        for i in range(len(mass_specrtum.topN_xvals)):

            experimental_mass = mass_specrtum.topN_xvals[i]
            experimental_intensity = mass_specrtum.topN_yvals[i]

            #print "Searching mass {0:10.3f}".format(experimental_mass)

            #TODO make a new function to return lower and upper masses based on ppm error
            #TODO just use 0.1 for testing the funnction at the moment

            ppm_to_daltons = msu.calc_daltons_from_ppm(experimental_mass, ppm_error)

            temp_low_mass = experimental_mass - ppm_to_daltons
            temp_high_mass = experimental_mass + ppm_to_daltons


            # TODO the following code works but I am afraid it will override values as new masses are searched
            # TODO best to create a new df with the search results
            #temp_match = df_search_space.loc[
            #    (df_search_space['Mass_exp'] > temp_low_mass) & (df_search_space['Mass_exp'] < temp_high_mass), ['ppm', 'Mass_Obs', 'Intensity']] = \
            #    [ppm_calculated, experimental_mass, experimental_intensity]

            temp_match = df_search_space.loc[
                (df_search_space['Mass_Theor'] > temp_low_mass) & (df_search_space['Mass_Theor'] < temp_high_mass)]

            if temp_match.empty:
                pass
            else:
                to_add_to_results = np.append(temp_match.as_matrix()[0], [experimental_mass, experimental_intensity])
                search_results_array.append(to_add_to_results)

        df_search_results = pd.DataFrame(search_results_array, columns=self.column_headers_search_space)
        df_search_results['ppm'] = (df_search_results['Mass_Theor'] - df_search_results['Mass_Obs']) / df_search_results['Mass_Theor'] * 1000000

        return df_search_results

    def create_search_space_peptide_fragments(self, fragments, charges, modifications):
        """

        Args:
            fragments: An array of Fragment objects
            charges: The charges to consider
            modifications: The modifications to consider
            modifications is a dictionary with first element the
            mod name and second the residue(s) or positions affected

        Returns:
            A pandas dataframe with the fragment match information

        """
        peptide_column_headers = ['Sequence', 'Ion', 'Charge', 'Mass_Theor', 'Modifications']

        #TODO implement modifications!
        data_to_save = []  # print "Searching mass {0:10.3f}".format(experimental_mass)

        for fragment in fragments:

            for z in charges:

                frag_string_modified = ''

                fragm_mz = mass.calculate_mass(sequence=fragment.sequence,
                                                ion_type=fragment.ion[0], charge=z)

                data_to_save.append([fragment.sequence, fragment.ion, z, fragm_mz, frag_string_modified])

                # print '{0:<30} {1:<5} {2:<3} {3:10.3f} {4:10.3f} {5:10.3f} {6:7.1f} {7}'.format(fragment.sequence, fragment.ion, z, experimental_mass, experimental_intensity, fragm_mz, ppm_calculated, frag_string_modified)


        df = pd.DataFrame(data_to_save, columns=peptide_column_headers)
        #df.to_csv('matched_fragments.csv')

        return df


    def match_peptide_fragments_pandas(self, df_search_space, mass_specrtum, ppm_error):
        """

        Args:
            df_search_space:
            mass_specrtum:
            ppm_error:

        Returns:

        """
        column_headers_peptide_search_space = ['Sequence', 'Ion', 'Charge', 'Mass_Theor', 'Modifications',
                                            'Mass_Obs', 'Intensity']

        search_results_array = []

        for i in range(len(mass_specrtum.topN_xvals)):

            experimental_mass = mass_specrtum.topN_xvals[i]
            experimental_intensity = mass_specrtum.topN_yvals[i]

            #print "Searching mass {0:10.3f}".format(experimental_mass)

            #TODO make a new function to return lower and upper masses based on ppm error
            #TODO just use 0.1 for testing the funnction at the moment

            ppm_to_daltons = msu.calc_daltons_from_ppm(experimental_mass, ppm_error)

            temp_low_mass = experimental_mass - ppm_to_daltons
            temp_high_mass = experimental_mass + ppm_to_daltons


            # TODO the following code works but I am afraid it will override values as new masses are searched
            # TODO best to create a new df with the search results
            #temp_match = df_search_space.loc[
            #    (df_search_space['Mass_exp'] > temp_low_mass) & (df_search_space['Mass_exp'] < temp_high_mass), ['ppm', 'Mass_Obs', 'Intensity']] = \
            #    [ppm_calculated, experimental_mass, experimental_intensity]

            temp_match = df_search_space.loc[
                (df_search_space['Mass_Theor'] > temp_low_mass) & (df_search_space['Mass_Theor'] < temp_high_mass)]

            if temp_match.empty:
                pass
            else:
                to_add_to_results = np.append(temp_match.as_matrix()[0], [experimental_mass, experimental_intensity])
                search_results_array.append(to_add_to_results)

        df_search_results = pd.DataFrame(search_results_array, columns=column_headers_peptide_search_space)
        df_search_results['ppm'] = (df_search_results['Mass_Theor'] - df_search_results['Mass_Obs']) / df_search_results['Mass_Theor'] * 1000000

        return df_search_results
