from ichorlib.msClasses.MassSpectrum import MassSpectrum
from ichorlib.genClasses.PeakPicking import PeakPicking
from ichorlib.genClasses.detect_peaks import detect_peaks
import peakutils


import matplotlib.pyplot as plt

lineproperties = {'color': 'green', 'lw': 0.5, 'alpha' : 0.5}
fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, ncols=1, figsize=(10, 8), sharex=True, sharey=False)



#Smooth the derivative!!!

#xfilename = 'testing/1-DegQnoLysozyme.txt'
filename = 'testing/degQMSMS-chargeStripped.txt'

ms = MassSpectrum()
ms.read_text_file(filename, grain=20, normalisationtype='bpi')

print ms.xvals

pp = PeakPicking()
gradient = pp.calculate_gradient(ms.xvals, ms.yvals)
print pp.gradient
found_peaks = pp.find_peaks(1)
ms.plot(ax2)
for peak in found_peaks:
    print found_peaks[peak][0], found_peaks[peak][1]
    ax2.plot(found_peaks[peak][0], found_peaks[peak][1], 'rx')


ind = detect_peaks(ms.yvals, mph=None, mpd=None, show=False)
print(ind)
ms.plot(ax3)
ax3.plot(ms.xvals[ind], ms.yvals[ind], 'go')


indexes = peakutils.indexes(ms.yvals, thres=0.0, min_dist=1)
peaks_x = peakutils.interpolate(ms.xvals, ms.yvals, ind=indexes)
print peaks_x

ms.plot(ax4)
ax4.plot(ms.xvals[indexes], ms.yvals[indexes], 'bo')
base = peakutils.baseline(ms.yvals, 2)
baseline_corrected = ms.yvals-base
ax4.plot(ms.xvals, baseline_corrected, 'r')
indexes_baseline = peakutils.indexes(baseline_corrected, thres=0.0, min_dist=1)
ax4.plot(ms.xvals[indexes_baseline], baseline_corrected[indexes_baseline], 'ro')



#ms.plot(ax1)
ax1.plot(ms.xvals, pp.gradient*100, 'r')




plt.show()


