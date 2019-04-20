import numpy as np
from scipy import optimize
import time
from ichorlib.genClasses.colorPalette import tableau20
import ichorlib.msClasses.MsUtils as msutils
import matplotlib as plt
import matplotlib.pyplot as pyplt


class MassSpectrum():

    def __init__(self):

        self.name = ''
        self.xvals = np.array([])
        self.yvals = np.array([])
        self.topN_xvals = np.array([])
        self.topN_yvals = np.array([])
        self.originalyvals = []
        self.gradient = []
        self.normalisationtype = 'none'
        self.csds = []  #holds MsCSD objects

    def read_text_file(self,
                       filename,
                       x_range=0,
                       grain=1,
                       normalisationtype='none'):
        """ Reads in x y coordinate pairs from text file
        ' ' separator as in copy spectrum list in MassLynx

        x_range - allows you to select lower and upper bounds
        in the format of [lower,upper]

        grain - allows the missing of data to speed up processing
        a grain of 2 means that every second value will be used

        :param filename:
        :param x_range:
        :param grain:
        :param normalisationtype:
        :return:
        """
        raw_data = open(filename, 'r').readlines()
        count = 0
        self.xvals = []
        self.yvals = []
        for x in raw_data:
            count += 1
            if count == grain:
                temp = x.rstrip('\r\n')
                vals = list(map(float, temp.split('\t')))
                if not x_range:
                    self.xvals.append(vals[0])
                    self.yvals.append(vals[1])
                else:
                    if vals[0] > x_range[0]:
                        if vals[0] < x_range[1]:
                            self.xvals.append(vals[0])
                            self.yvals.append(vals[1])
                count = 0
        self.xvals = np.array(self.xvals)
        self.yvals = np.array(self.yvals)

        # so that it isn't overwritten by smoothing
        self.originalxvals = self.xvals.copy()
        self.originalyvals = self.yvals.copy()

        if normalisationtype == 'bpi':
            self.normalisation_bpi()
        elif normalisationtype == 'area':
            self.normalisation_area()

    def normalisation_bpi(self):
        """ Normalise to base peak intensity (0-100)
        :return:
        """
        maxintensity = self.yvals.max()
        self.yvals = (self.yvals / maxintensity) * 100
        self.normalisationtype = 'bpi'

    def normalisation_area(self):
        """ Normalise to total area
        :return:
        """
        self.yvals = self.yvals / np.sum(self.yvals)
        self.normalisationtype = 'area'

    def restore_raw_yvals(self):
        """ Restore intensity values
        :return:
        """
        self.yvals = self.originalyvals.copy()
        self.normalisationtype = 'none'

    def smoothingSG(self, window_len=3, smoothes=2, poly_order=1):
        '''Should only really be used on equally spaced data
        Actual window length used is 2*window_len+1 to avoid breakage'''
        window_len = 2 * window_len + 1
        self.restore_raw_yvals()
        for i in range(smoothes):
            self.yvals = msutils.sg(self.yvals,
                                    window_size=window_len,
                                    order=poly_order)
        #self.normalisation_bpi()

    def simulateSpectrum(self, peak_shape='gaussian'):
        """Builds a simulated spectrum using the fitted parameters of given species names.
         (uses the result of deconvolution)
         """
        combined = np.zeros(len(self.xvals), dtype='float')
        for csd in self.csds:
            combined += csd.simulateSpecies(self.xvals)

        return combined

    def find_nearest(self, array, value):
        idx = (np.abs(array - value)).argmin()
        return idx

    def select_ms_range(self, min, max):

        #self.xvals = self.originalxvals.copy()
        #self.yvals = self.originalyvals.copy()

        min_index = self.find_nearest(self.xvals, min)
        max_index = self.find_nearest(self.xvals, max)

        print(('Min {0} Max {1} Total length off original array {2}').format(
            min_index, max_index, len(self.originalxvals)))

        self.xvals = self.xvals[min_index:max_index]
        self.yvals = self.yvals[min_index:max_index]

    def select_topN_intensity_peaks(self, topN):
        """

        Args:
            topN: to N peaks to return based on intensity
            Sets the cooresponding topN arrays

        """

        #TODO if an external function uses topN_xvals directly there will be an exception if this
        #function hasn't been set - fix
        index = self.yvals.argsort()
        self.topN_xvals = self.xvals[index][-topN:]
        self.topN_yvals = self.yvals[index][-topN:]

    def leastSquaresOptimisation(self, fixed_p_fwhh=0):
        """
        if fixed_p_fwhh > 0 it uses the p_fwhm from the csd object
        do not optimise it
        :param fixed_pfwhm:
        :return:
        """

        p0 = [
        ]  #change this to the current params from the CSD objects as they have aready been optimised somewhat

        for csd in self.csds:
            p0.extend(csd.get_params_for_optimisation())

        #print p0

        # using scipy optimize
        def errorfunc(p, fixed_p_fwhh):
            return self.forLeastSquaresOptimisation(p,
                                                    fixed_p_fwhh) - self.yvals

        startTime = time.time()
        p1, success = optimize.leastsq(errorfunc, p0, args=(fixed_p_fwhh))
        print(("Optimisation took:", time.time() - startTime, "s"))
        #print p1

        #update csds with optimised params
        params_per_csd = [p1[pos:pos + 5] for pos in range(0, len(p1), 5)]
        #print params_per_csd

        print("Updating CSD after optimisation")
        for i in range(len(self.csds)):

            print(('{0} {1} {2} {3}').format(params_per_csd[i][0],
                                             params_per_csd[i][1],
                                             params_per_csd[i][2],
                                             params_per_csd[i][3]))
            self.csds[i].csd_mass = params_per_csd[i][0]
            self.csds[i].g_amp = params_per_csd[i][1]
            self.csds[i].g_mu = params_per_csd[i][2]
            self.csds[i].g_fwhh = params_per_csd[i][3]

            if (fixed_p_fwhh > 0):
                self.csds[i].p_fwhh = fixed_p_fwhh
            else:
                self.csds[i].p_fwhh = params_per_csd[i][4]

            self.csds[i].update_mass_after_optimisation()

        return p1

    def forLeastSquaresOptimisation(self, p0, fixed_p_fwhh=False):
        """Creates the simulated mass spectrum for MassSpectrum.leastSquaresOptimisation().
         p0 - parameters to be used in simulation
         zs - charges to be simulated
         oneFwhm """

        params_per_csd = [p0[pos:pos + 5] for pos in range(0, len(p0), 5)]
        #print params_per_csd

        for i in range(len(self.csds)):

            self.csds[i].csd_mass = params_per_csd[i][0]
            self.csds[i].g_amp = params_per_csd[i][1]
            self.csds[i].g_mu = params_per_csd[i][2]
            self.csds[i].g_fwhh = params_per_csd[i][3]

            if fixed_p_fwhh > 0:
                self.csds[i].p_fwhh = fixed_p_fwhh
            else:
                self.csds[i].p_fwhh = params_per_csd[i][4]

        return self.simulateSpectrum()

    # def leastSquaresOptimisation(self,speciesNames,oneFwhm=False):
    #     """Deconvolute mass spectrum using non linear least squares.
    #     Setting oneFwhm to true results in the same value for peak full width
    #     half height being used for all species.
    #     """
    #     # setting up initial parameters
    #     zs,p0 = [],[]
    #     for name in speciesNames:
    #         zs.append(self.species[name].charges)
    #         p0 += self.species[name].getp0(oneFwhm)
    #
    #     print('[KT] {0}'.format(p0))
    #
    #     # using scipy optimize
    #     def errorfunc(p,xvals,yvals,zs,oneFwhm):
    #         return self.forLeastSquaresOptimisation(p,xvals,zs,oneFwhm) - yvals
    #
    #     startTime = time.time()
    #     p1, success = optimize.leastsq(errorfunc,p0[:],args=(self.xvals,self.yvals,zs,oneFwhm))
    #     print "Optimisation took:", time.time()-startTime, "s"
    #
    #     # storing the fit
    #     for i,p in enumerate(self._splitPs(p1)):
    #         tempSp = Species(speciesNames[i])
    #         if not oneFwhm:
    #             peakFwhm = p[4]
    #         else:
    #             peakFwhm = oneFwhm
    #         tempSp.setValsFromp1([p[0],p[1],p[2],p[3],peakFwhm])
    #         tempSp.setCharges(zs[i])
    #         self.simulatedSpecies[speciesNames[i]] = tempSp
    #         if oneFwhm:
    #             self.simulatedSpecies[speciesNames[i]].peakFwhm = p1[4]
    #     self.simulatedSpectrum = self._simulateSpectrum(speciesNames, self.xvals)

    # def forLeastSquaresOptimisation(self,p0,xvals,zs,oneFwhm):
    #     """Creates the simulated mass spectrum for MassSpectrum.leastSquaresOptimisation().
    #     p0 - parameters to be used in simulation
    #     zs - charges to be simulated
    #     oneFwhm - if True use same FWHM for each species.
    #     """
    #     ps = self._splitPs(p0)
    #     combined = np.zeros(len(xvals))
    #     zGauss = Gaussian()
    #
    #     for i,p in enumerate(ps):
    #
    #         print('[KT] i:{0} p:{1}'.format(i, p))
    #
    #         zGauss.setParameters(p[1], p[2], p[3])
    #         for j,z in enumerate(zs[i]):
    #             print('[KT] j:{0} z:{1}'.format(j, z))
    #             centre = utils.get_mz(p[0], z)
    #             amplitude = zGauss.calculateAmplitude(centre)
    #             if oneFwhm:
    #                 combined += utils.draw_peaks['hybrid'](xvals,amplitude,centre,p0[4]) #TODO KT bug should not be p and not p0 unless it refers to the stabdard value of 10 fwhm???
    #             else:
    #                 combined += utils.draw_peaks['hybrid'](xvals,amplitude,centre,p[4])
    #     return combined

    # ================================================================= #
    # ====                      Plotting                           ==== #
    # ================================================================= #

    def plot_me(self, ax=None, **kwargs):

        if ax is None:
            ax = pyplt.gca()

        ax.plot(self.xvals, self.yvals, **kwargs)
        ax.set_ylabel('Intensity')
        ax.set_xlabel('$m/z$')

        return ax

    def plot(self, ax, **kwargs):
        """ Plot the mass spectrum. It actually returns an axes object to plot elsewhere

        :param ax:
        :param kwargs:
        :return:
        """
        ln = ax.plot(self.xvals, self.yvals, **kwargs)
        ax.set_ylabel('Intensity')
        ax.set_xlabel('$m/z$')

        return ln

    def plot_simulated_spectrum_simple(self, ax, peakShape='gaussian',
                                       **kwargs):
        """ Plot the simulated spectrum based on the CSDs
        :param ax:
        :param xaxis:
        :return:
        """

        ln = ax.plot(self.xvals, self.yvals, color=tableau20[0])
        ax.set_ylabel('Intensity')
        ax.set_xlabel('$m/z$')

        return ln

    def plot_simulated_spectrum(self,
                                ax,
                                showcharges='True',
                                peakShape='gaussian',
                                **kwargs):
        """ Plot the simulated spectrum based on the CSDs
        :param ax:
        :param xaxis:
        :return:
        """

        offset = 20
        labelSize = 'medium'

        color_index = 4
        for csd in self.csds:

            yvals = csd.simulateSpecies(self.xvals) + offset
            max = yvals.max()
            xleft = self.xvals.max() - 300
            ln = ax.plot(self.xvals, yvals, color=tableau20[color_index])
            ln = ax.annotate('%.2f Da' % csd.csd_mass,
                             xy=(xleft, offset + 3),
                             size=labelSize,
                             horizontalalignment='right')

            if showcharges == 'True':
                for peak in csd.charges_to_fit:
                    ln = ax.text(peak.x,
                                 peak.y + offset,
                                 peak.charge,
                                 color=tableau20[color_index])

            offset += 20
            color_index += 2

        offset += 100
        yvals = self.simulateSpectrum() + offset
        ln = ax.plot(self.xvals, yvals, color=tableau20[2])

        offset += 50

        ln = ax.plot(self.xvals, self.yvals + offset, color=tableau20[0])
        ax.set_ylabel('Intensity')
        ax.set_xlabel('$m/z$')

        return ln
