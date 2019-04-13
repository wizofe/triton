import pandas as pd
from random import *
from ichorlib.seqClasses.Fragmentor import Fragmentor
from ichorlib.genClasses.Matcher import Matcher
from ichorlib.msClasses.MassSpectrum import MassSpectrum
from scipy.stats import genextreme
import seaborn as sns
import numpy as np

__author__ = 'kthalassinos'


class Scorer(object):
    """
    Class used to calculate a score after a match is performed
    The matches are stored in a pandas dataframe

    """

    def __init__(self):
        """

        """

    def read_dataframe_from_csv(self, filepath):
        """

        Args:
            filepath: path to file with csv file

        Returns:
            a dataframe

        """

        df = pd.DataFrame.from_csv(filepath)
        return df


    def simple_score(self, df):

        #split the Ion column into ion type and ion number
        df = df.join(df.Ion.str.extract('([a-z]|[A-Z])([0-9]*)', expand=True).rename(columns={0: 'Ion_type'}))
        new_ppm_bins = [-10, 0., 5., 10., 50., 100,
                        500]  # i add the -10 as the first value so to avoid having 0 in the resulting bins
        df['ppm_bins'] = pd.cut(abs(df.ppm), new_ppm_bins, labels=False)
        new_intensity_bins = [-10, 0., 5., 10., 25., 50., 100]
        df['intensity_bins'] = pd.cut(df.Intensity, new_intensity_bins, labels=False)
        df = df.assign(Inten_weighted_ppm_2=lambda df: abs(
            df.intensity_bins / df.ppm_bins))  # for this score to work need to remove the precursor and rescale remaining intensities!!!

        score = df.Inten_weighted_ppm_2.sum()


        return score

    def calc_match_statistics(self, oligo, charges, modifications, ms, ppm_error, score_to_test, random_oligo_to_test = 1000):

        fr = Fragmentor()
        matcher = Matcher()
        column_headers = ['Sequence', 'Score']

        min_char = len(oligo)
        max_char = len(oligo)
        allchar = ['A', 'G', 'C', 'T', 'U']

        data_to_save = []

        for i in range(random_oligo_to_test):

            random_oligo = "".join(choice(allchar) for _ in range(randint(min_char, max_char)))

            fragments = fr.fragment_oligo(random_oligo)
            df_search_space = matcher.create_search_space(fragments, charges, modifications)
            df_results = matcher.match_oligo_fragments_pandas(df_search_space, ms, ppm_error)

            score = self.simple_score(df_results)

            print('Oligo: {0:<30} Score: {1:7.3f}'.format(random_oligo, score))

            data_to_save.append([random_oligo, score])

        dist_df = pd.DataFrame(data_to_save, columns=column_headers)

        extreme_fit = genextreme.fit(dist_df.Score)
        c = extreme_fit[0]
        loc = extreme_fit[1]
        scale = extreme_fit[2]
        print(("Extreme value fits c = {0}, loc = {1}, scale = {2}").format(c, loc, scale))

        extreme_to_plot = genextreme(c, loc, scale)
        p_value = extreme_to_plot.pdf(score_to_test)
        print(("p value of score {0} = {1}").format(score_to_test, p_value))

        return dist_df, p_value, score_to_test, extreme_to_plot


    def plot_match_statistics(self, dist_df, p_value, score_to_test, extreme_to_plot):

        string_to_print = ("p value of score {0} = {1}").format(score_to_test, p_value)
        x_axes_min_val = dist_df.Score.min() - 5
        x_axes_max_val = dist_df.Score.max() + 5
        ax1 = sns.distplot(dist_df.Score, fit=genextreme, kde=False)
        x = np.linspace(x_axes_min_val, x_axes_max_val, 100)
        ax1.plot(x, extreme_to_plot.pdf(x), 'r-', lw=2, label='pdf')
        ax1.axvline(score_to_test)
        ax1.set_title(string_to_print)
        ax1.set_xlabel('score')
        ax1.set_ylabel('number of matches')

        return ax1






