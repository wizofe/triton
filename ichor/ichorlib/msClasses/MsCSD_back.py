import numpy as np
import operator
from operator import itemgetter
import matplotlib as plt
import collections
from ichorlib.msClasses.MsPeak import MsPeak
import ichorlib.msClasses.MsUtils as msutils


class MsCSD():

    def __init__(self):
        """ Describe a charge state distribution CSD. This contains peaks that follow a
        Gaussian distribution, can calculate a mass from and used to simulate a spectrum
        """
        self.mspeaks = []  #arrray holding MsPeak objects
        self.expmass = 0
        self.expmaassSD = 0
        self.name = 'CSD'
        self.mass = 0
        self.massStd = 0
        self.gaussianParams = [
        ]  #not sure whether I should delete this and go with individual values as below
        self.amp = 0
        self.mu = 0
        self.fwhh = 0

    def set_gaussian_params(self, amp, mu, fwhh):
        self.gaussianParams.append(amp)
        self.gaussianParams.append(mu)
        self.gaussianParams.append(fwhh)
        self.amp = amp
        self.mu = mu
        self.fwhh = fwhh

    def add_peak(self, peakmz):
        """ Adds peak objects and calculates the id NOTE there is no sorting based on mz

        :param peakmz:
        :return:
        """
        #find the last id in the array
        numPeaks = len(self.mspeaks)
        if numPeaks == 0:
            id = 1
        else:
            id = numPeaks + 1

        mypeak = MsPeak()
        mypeak.x = peakmz
        mypeak.id = id

        self.mspeaks.append(mypeak)

    def calc_mass_and_charge(self):

        self.mspeaks.sort(key=operator.itemgetter(0), reverse=True)

        charges = collections.OrderedDict()
        masses = []
        zs = range(1, 101)
        for z in zs:
            charges[z] = []
            for i in range(len(self.mspeaks)):
                mz = self.mspeaks[i].x
                mass = msutils.calc_mass(mz, z + i)
                charges[z].append(mass)
                #print "Charge {0} - mz {1} - mass {2}".format(z+i, mz, mass)
            calcmass = np.average(charges[z])
            stdev = np.std(charges[z])
            #print "z {0} - Mass {1} - StDev {2}\n".format(z, calcmass, stdev)
            masses.append([stdev, z, calcmass, charges[z]])

        masses.sort(key=operator.itemgetter(0), reverse=False)

        # Go though the best solution and set mass to this object and charges to
        # the msPeak objects
        tz = masses[0][1]
        self.mass = masses[0][2]
        self.massStd = masses[0][0]
        i = 0
        for tmass in masses[0][3]:
            self.mspeaks[i].charge = tz
            #diff = self.mass - tmass
            #print "z: {0} m/z: {1} mass: {2} massDiff {3} mspeakmx {4}".format(tz, tmass, self.mass, diff, self.mspeaks[i].x)
            tz += 1
            i += 1

    def print_error_per_peak(self):
        """ Print what the deviation from the average mass is for each peak
        so that it helps with identifying outlier peaks

        :return:
        """
        if self.mass != 0:
            for peak in self.mspeaks:
                calcmass = msutils.calc_mass(peak.x, peak.charge)
                diff = self.mass - calcmass
                print(
                    "z {1: <3} m/z {0: 9.3f} mass {2:8.2f} massDiff {3:8.2f} ".
                    format(peak.x, peak.charge, calcmass, diff))

    def plot_gaussian(self, ax, xaxis, **kwargs):
        gaussian = self.amp * np.exp(
            (-(xaxis - self.mu)**2) / (2 * (self.fwhh / 2.3548200450309493)**2))
        ln = ax.plot(xaxis, gaussian, **kwargs)
        return ln

    def plot_simulated_csd(self,
                           ax,
                           xaxis,
                           fwhm=10,
                           peakShape='gaussian',
                           **kwargs):
        """ Plot theoretical peaks. If the intensity for each peak has not been set
        it will be plotted using 100 % as the intensity

        :param ax:
        :param xaxis:
        :param fwhm:
        :param peakShape:
        :param kwargs:
        :return:
        """

        #simulate_peak(self, xaxis, fwhm=10, peakShape='gaussian'):
        simulatedCSD = 0
        if self.mass != 0:
            for peak in self.mspeaks:
                if peak.y == -1:  # this is when the intensity of a peak has not been set
                    peak.y = 100
                simulatedCSD += peak.simulate_peak(xaxis, fwhm, peakShape)
                ln = ax.text(
                    peak.x, peak.y,
                    peak.charge)  #tidy this up to get charge state centered
                #ln = ax.plot(xaxis, simulatedCSD, **kwargs)
                print(simulatedCSD)

        print(simulatedCSD)
        ln = ax.plot(xaxis, simulatedCSD, **kwargs)
        return ln

    def calcMassAndChargeOld(self):

        for pe in self.mspeaks:
            print(pe.x)

        self.mspeaks.sort(key=operator.itemgetter(0), reverse=False)

        for pe2 in self.mspeaks:
            print(pe2.x)

        mzarray = []
        for peak in self.mspeaks:
            mzarray.append(peak.x)

        mzarray.sort(reverse=True)

        charges = collections.OrderedDict()
        masses = []
        zs = range(1, 101)
        for z in zs:
            charges[z] = []
            for i, mz in enumerate(mzarray):
                mass = msutils.calc_mass(mz, z + i)
                charges[z].append(mass)
                #print "Charge {0} - mz {1} - mass {2}".format(z+i, mz, mass)
            calcmass = np.average(charges[z])
            stdev = np.std(charges[z])
            #print "z {0} - Mass {1} - StDev {2}\n".format(z, calcmass, stdev)
            masses.append([stdev, z, calcmass, charges[z]])

        masses.sort(key=operator.itemgetter(0), reverse=False)

        tz = masses[0][1]
        avgmass = masses[0][2]
        for tmass in masses[0][3]:
            diff = avgmass - tmass
            print("z: {0} m/z: {1} mass: {2} massDiff {3}".format(
                tz, tmass, avgmass, diff))
            tz += 1

        return avgmass, masses[0]
