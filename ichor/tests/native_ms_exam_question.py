from ichorlib.msClasses.MsCSD import MsCSD
from ichorlib.msClasses.MsPeak import MsPeak
import matplotlib.pyplot as plt
import numpy as np


mspeaks = []
csd = MsCSD()
csd.p_fwhh = 10


ms_peak1 = MsPeak()
ms_peak1.x = 2802.7
ms_peak1.y = 40
mspeaks.append(ms_peak1)

ms_peak2 = MsPeak()
ms_peak2.x = 3153.1
ms_peak2.y = 100
mspeaks.append(ms_peak2)


ms_peak3 = MsPeak()
ms_peak3.x = 3603.7
ms_peak3.y = 65
mspeaks.append(ms_peak3)

csd.calculateMassAndCharges(mspeaks)

csd.optimiseParameters()
csd.estimateCharges(5)



csd.print_me()

fig, ax1 = plt.subplots()

xaxis = np.linspace(100, 6000, 10000)
print(xaxis)
csd.plot_simulated_species(ax1, xaxis, fwhm=20)

plt.show()
