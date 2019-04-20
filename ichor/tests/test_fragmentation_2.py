from ichorlib.genClasses.MassCalculator import MassCalculator
from ichorlib.seqClasses.Fragmentor import Fragmentor
from ichorlib.msClasses.MassSpectrum import MassSpectrum
from ichorlib.genClasses.Matcher import Matcher
from ichorlib.genClasses.Scorer import Scorer
from random import *

#data_file = '20160208_HYS_Oligo_M3_nonsci.tsv'
data_file = '20160208_HYS_Oligo_M3.tsv'
oligo = 'UCGUCAAGCGAUUACAAGGTT'

mc = MassCalculator()
fr = Fragmentor()
ms = MassSpectrum()
matcher = Matcher()
sc = Scorer()

top_N_peaks = 200
ppm_error = 150
charges = [-1]

modifications1 = {'+thio': 2, '-NH3': 4}
modifications2 = {'+thio': 2, '-NH3': 4}

#modifications = [modifications1]

modifications = []

ms.read_text_file(data_file, grain=10, normalisationtype='bpi')
ms.select_topN_intensity_peaks(top_N_peaks)

fragments = fr.fragment_oligo(oligo)

df_search_space = matcher.create_search_space(fragments, charges, modifications)

df_results = matcher.match_oligo_fragments_pandas(df_search_space, ms,
                                                  ppm_error)

print(df_results)

score = sc.simple_score(df_results)

min_char = len(oligo)
max_char = len(oligo)
allchar = ['A', 'G', 'C', 'T', 'U']
random_oligo_to_test = 1000

file_for_p_vals = open('p_values_1.txt', 'w')
print('Oligo: {0:<30} Score: {1:7.3f}'.format(oligo, score))
file_for_p_vals.write("{0}\t{1}\n".format(oligo, score))

for i in range(random_oligo_to_test):

    random_oligo = "".join(
        choice(allchar) for x in range(randint(min_char, max_char)))

    fragments = fr.fragment_oligo(random_oligo)
    df_search_space = matcher.create_search_space(fragments, charges,
                                                  modifications)

    df_results = matcher.match_oligo_fragments_pandas(df_search_space, ms,
                                                      ppm_error)

    score = sc.simple_score(df_results)

    print('Oligo: {0:<30} Score: {1:7.3f}'.format(random_oligo, score))
    file_for_p_vals.write("{0}\t{1}\n".format(random_oligo, score))

file_for_p_vals.close()

#plotting

#fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(12, 8), sharex=True, sharey=False)
#ms.plot(ax1)
#plt.show()
