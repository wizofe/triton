import numpy as np
import matplotlib as plt


class MsPeak():

    def __init__(self):
        """ Describe an ms peak this is just using mz and intensity values ie like stick data

        """

        self.x = 0
        self.y = -1  # set this to -1 so if you plot a theoretical peak your code checks and plots it at 100%
        self.charge = 0
        self.id = 0

    def __repr__(self):
        return "[MsPeak] id {0} m/z {1} intensity {2} charge {3}".format(
            self.id, self.x, self.y, self.charge)

    def __getitem__(self, item):
        return self.x

    def simulate_peak(self, xaxis, fwhm=10, peak_shape='gaussian'):
        """ This method simulates the intensity of a peak using a peak shape and an x-axis as inputs

        :return:
        """
        if peak_shape == 'lorentzian':
            return self.lorentzian(xaxis, self.y, self.x, fwhm)
        elif peak_shape == 'hybrid':
            return self.hybrid(xaxis, self.y, self.x, fwhm)
        else:
            return self.gaussian(xaxis, self.y, self.x, fwhm)

    def gaussian(self, mzs, amp, mu, fwhh):
        """Calculate a three parameter Gaussian distribution.

        :parameter mzs: x axis (numpy array or float)
        :parameter amp: Amplitude of distribution
        :parameter mu: Mean/centre of the distribution
        :parameter fwhh: Width of distribution (full width half maximum)
        """
        return amp * np.exp(
            (-(mzs - mu)**2) / (2 * (fwhh / 2.3548200450309493)**2))

    def lorentzian(self, mzs, amp, mu, fwhh):
        """Calculate a three parameter Lorentzian (Cauchy) distribution.

        :parameter mzs: x axis (numpy array or float)
        :parameter amp: Amplitude of distribution
        :parameter mu: Mean/centre of the distribution
        :parameter fwhm: Width of distribution (full width half maximum)
        """
        return amp * 1 / (np.abs(1 + ((mu - mzs) / (fwhh / 2))**2))

    def hybrid(self, mzs, amp, mu, fwhh):
        """Calculate a three parameter hybrid distribution. Distribution is
        Gaussian at values less than the mean and Lorentzian above it.

        :parameter mzs: x axis (numpy array or float)
        :parameter amp: Amplitude of distribution
        :parameter mu: Mean/centre of the distribution
        :parameter fwhh: Width of distribution (full width half maximum)
        """
        ys = mzs.copy()
        ys[mzs <= mu] = amp * np.exp(
            (-(mzs[mzs <= mu] - mu)**2) /
            (2 * (fwhh / (2 * np.sqrt(2 * np.log(2))))**2))
        ys[mzs > mu] = amp * 1 / (np.abs(1 + ((mu - mzs[mzs > mu]) /
                                              (fwhh / 2))**2))

        return ys

    # ================================================================= #
    # ====                      Plotting                           ==== #
    # ================================================================= #

    def plotSimulatedPeak(self,
                          ax,
                          xaxis,
                          fwhm=10,
                          peakShape='gaussian',
                          **kwargs):
        #TODO add switches here to also plot m/z or z with the peak
        """ Plot the simulated peak

        :param ax:
        :param xaxis:
        :param fwhm:
        :param peakShape:
        :param kwargs:
        :return:
        """
        text_to_plot = str(self.id)  # + " " + str(self.charge)
        ln = ax.plot(xaxis, self.simulate_peak(xaxis, fwhm, peakShape),
                     **kwargs)
        ln = ax.text(self.x, self.y, text_to_plot)
        return ln
