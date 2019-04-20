from ichorlib.msClasses.MassSpectrum import MassSpectrum
from ichorlib.genClasses.PeakPicking import PeakPicking
from ichorlib.msClasses.MsCSD import MsCSD
from ichorlib.genClasses.colorPalette import tableau20
import matplotlib.pyplot as plt

import numpy as np

filename = 'testing/1-DegQnoLysozyme.txt'

#lineproperties = {'color': 'green', 'lw': 0.5, 'alpha' : 0.5}
fig, (ax1) = plt.subplots(nrows=1,
                          ncols=1,
                          figsize=(12, 8),
                          sharex=True,
                          sharey=False)

ms = MassSpectrum()
ms.read_text_file(filename, grain=20, normalisationtype='bpi')
ms.smoothingSG(window_len=7, smoothes=3)

ms.select_ms_range(7000, 10000)

#TODO add this inside the MS object
pp = PeakPicking()
gradient = pp.calculate_gradient(ms.xvals, ms.yvals)
found_peaks = pp.find_peaks(20)

CSD1 = MsCSD()
CSD1.name = 'CSD1'
CSD1.p_fwhh = 10
CSD1_peak_indexes = [0, 1, 2]
indexed_peaks = pp.get_peaks_using_indexes(CSD1_peak_indexes)
CSD1.mspeaks = indexed_peaks
CSD1.calculateMassAndCharges(CSD1.mspeaks)
CSD1.optimiseParameters()
CSD1.estimateCharges(5)
#CSD1.plot_residuals_per_peak(ax4, CSD1.mspeaks, marker='x', color='blue')

CSD2 = MsCSD()
CSD2.name = 'CSD2'
CSD2.p_fwhh = 10
CSD2_peak_indexes = [4, 5, 6, 7, 8, 9]
indexed_peaks = pp.get_peaks_using_indexes(CSD2_peak_indexes)
CSD2.mspeaks = indexed_peaks
CSD2.calculateMassAndCharges(CSD2.mspeaks)
CSD2.optimiseParameters()
CSD2.estimateCharges(5)

#CSD2.filter_theoretical_peaks_using_charges([56, 57, 58, 59])
#CSD2.plot_residuals_per_peak(ax4, CSD2.mspeaks, marker='x', color='blue',)

ms.csds.append(CSD1)
ms.csds.append(CSD2)

CSD1.print_me()
CSD2.print_me()

# -------- printing ----------- #

#ms.plot(ax1, color=tableau20[2])

#for peak in found_peaks:
#    peak.plotSimulatedPeak(ax2, ms.xvals, fwhm=50, color=tableau20[0])

#CSD1.plot_csd_gaussian(ax1, ms.xvals, color=tableau20[6])
#CSD1.plot_simulated_species(ax1, ms.xvals, color=tableau20[6])
#CSD2.plot_csd_gaussian(ax1, ms.xvals, color=tableau20[6])
#CSD2.plot_simulated_species(ax1, ms.xvals, color=tableau20[6])

#ms.plot_simulated_spectrum(ax3, color=tableau20[14])

ms.leastSquaresOptimisation(fixed_p_fwhh=60)

ms.plot_simulated_spectrum(ax1, showcharges='False')

#CSD1.plot_residuals_per_peak(ax2, CSD1.charges_to_fit, marker='o', color='red')
#CSD2.plot_residuals_per_peak(ax2, CSD2.charges_to_fit, marker='o', color='red',)

CSD1.print_me()
CSD2.print_me()

plt.show()
