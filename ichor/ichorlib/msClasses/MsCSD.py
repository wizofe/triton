import numpy as np
from ichorlib.msClasses.MsPeak import MsPeak
import ichorlib.msClasses.MsUtils as msutils
from scipy import optimize
import collections

#TODO add the xaxis here or pass the MassSpectrum object so you don't have to keep
# adding the xaxis in each function

class MsCSD():
    def __init__(self):
        """ Describe a charge state distribution CSD. This contains peaks that follow a
        Gaussian distribution, can calculate a mass from and used to simulate a spectrum
        The mspeaks are experimentaly picked peaks that are used to fit an overal Gaussian distribution
        This Gaussian is then used to identify potential other charge states that fit within that Gaussian
        distribution and which will be simulated later
        """
        self.name = ""
        self.mspeaks = []  # arrray holding MsPeak objects
        self.g_amp = 0
        self.g_mu = 0
        self.g_fwhh = 0
        self.p_fwhh = 0
        self.csd_mass = 0
        self.csd_mass_error = 0
        self.csd_charge_states = []
        self.charges_to_fit = []  # MsPeak objects from the ones calculated from the estimate charges function
        self.charges_to_fit_all = [] # hold all peaks corresponding to charges identified use it as a backup for when filtering


    def print_me(self):

        print ('{:-<50}').format("-")

        print('CSD {0} csd_mass {1:8.2f} g_amp: {2:5.2f} g_mu: {3:5.2f} g_fwhh {4:5.2f}'
            ' p_fwhh {5:5.2f} csd_mass_error {6:5.2f}'.format(self.name, self.csd_mass, self.g_amp, self.g_mu, self.g_fwhh, self.p_fwhh, self.csd_mass_error))

        for cs in self.mspeaks:
            print ('MS_peaks {0} {1} {2} {3}').format(cs.id, cs.x, cs.y, cs.charge)

        for cs in self.charges_to_fit:
            print ('Charges_to_fit {0} {1} {2} {3}').format(cs.id, cs.x, cs.y, cs.charge)

        print ('{:-<50}').format("-")

    def get_params_for_optimisation(self):
        """
        An easy way of getting the main params to be optimised for
        :return:
        """

        return [self.csd_mass, self.g_amp, self.g_mu, self.g_fwhh, self.p_fwhh]

    def add_ms_peak_objects(self, ms_peak):
        """ Adds peak objects and calculates the id NOTE there is no sorting based on mz

        TODO sort them based on m/z!!!
        even thoough from the peak picking algorithm they should be sorted asceding

        :param peakmz:
        :return:
        """
        self.mspeaks.append(ms_peak)

    def add_peak(self, peakmz):
        """ Adds peak objects and calculates the id NOTE there is no sorting based on mz

        TODO sort them based on m/z!!!

        :param peakmz:
        :return:
        """
        # find the last id in the array
        numPeaks = len(self.mspeaks)
        if numPeaks == 0:
            id = 1
        else:
            id = numPeaks + 1

        mypeak = MsPeak()
        mypeak.x = peakmz
        mypeak.id = id

        self.mspeaks.append(mypeak)



    def calculateMassAndCharges(self, mspeak_objects):
        """Calculate the mass of a molecular species using the given m/z
        values.
        Primarily used as a subfunction of self.calculateMass().
        """
        # TODO change this so that after the optimisation the ms_peak objects
        # are updated to include the charge

        mspeak_objects.sort(key=lambda id: id.x, reverse=True)

        charges = collections.OrderedDict()
        lowest = 10000000
        lowest_z = 0
        zs = xrange(1, 101)
        for z in zs:
            charges[z] = []
            i = 0
            for peak in mspeak_objects:
                charges[z].append(msutils.calc_mass(peak.x, z + i))
                i += 1


        for z in charges.keys():
            sd = np.std(charges[z])
            if sd < lowest:
                lowest = sd
                lowest_z = z

        # calculating error
        total_error = []
        for mass in charges[lowest_z]:
            total_error.append(abs(np.average(charges[lowest_z]) - mass))
        average_error = np.average(total_error)

        # assign charges to mspeaks
        counter = lowest_z
        for peak in mspeak_objects:
            peak.charge = counter
            counter += 1



        self.csd_mass = np.average(charges[lowest_z])
        self.csd_mass_error = average_error
        self.csd_charge_states = [lowest_z + i for i in xrange(len(mspeak_objects))]

        # return np.average(charges[lowest_z]), average_error, [lowest_z + i for i in xrange(len(iarray))]


    def estimateParameters(self, xvals, yvals):
        """| Estimate values for the 3 parameter Gaussian
        | The estimation is crude and is usually used to determine initial values for
        optimise parameters, which is much more robust.
        | If setValues is True, use the estimated parameters as the values
        for self.amplitude, self.centre and self.fwhm.
        | Otherwise values are returned as a list [amplitude,centre,fwhm]
        """
        fwhm = max(xvals) - min(xvals)
        amplitude = max(yvals)
        centre = np.average(xvals)

        #print('Estimated Gaussian  Mean: {0:8.2f} Amplitute: {1:5.2f}  FWHH: {2:8.2f}'.format(centre, amplitude, fwhm))

        self.g_amp = amplitude
        self.g_mu = centre
        self.g_fwhh = fwhm

        return amplitude, centre, fwhm

    def optimiseParameters(self):
        """| Use non linear least squares to fit the parameters of the
        Gaussian.
        | setValues means the optimised parameters are set to this object,
        else the parameters are returned as a dictionary.

        this needs the mz and intensity values of each peak identified
        from the peak picking algorithm - otherwise wont work

        """
        xvals = []
        yvals = []
        for peak in self.mspeaks:
            xvals.append(peak.x)
            yvals.append(peak.y)

        fitfunc = lambda p, x: msutils.gaussian(x, p[0], p[1], p[2])
        errorfunc = lambda p, x, y: fitfunc(p, x) - y

        h, c, f = self.estimateParameters(xvals, yvals)
        p0 = [h, c, f]
        p1, success = optimize.leastsq(errorfunc, p0[:], args=(xvals, yvals))

        if not success:
            print 'Gaussian charge state distribution estimation failed'
            d = {}
            d['amplitude'] = h
            d['centre'] = c
            d['fwhm'] = f
            self.g_amp = h
            self.g_mu = c
            self.g_fwhh = f

        else:
            d = {}
            d['amplitude'] = p1[0]
            d['centre'] = p1[1]
            d['fwhm'] = p1[2]
            self.g_amp = p1[0]
            self.g_mu = p1[1]
            self.g_fwhh = p1[2]

        #print(
        #'Optimised Gaussian  Mean: {0:8.2f} Amplitute: {1:5.2f}  FWHH: {2:8.2f}'.format(d['centre'], d['amplitude'],
         #                                                                               d['fwhm']))

        return d

    def calc_amplitude(self, mz_value):
        """ Given the overal Gaussian it calculates the intensity for one of the individual ms peaks

        :param xaxis:
        :return:
        """
        return self.g_amp * np.exp((-(mz_value - self.g_mu) ** 2) / (2 * (self.g_fwhh / 2.3548200450309493) ** 2))


    def estimateCharges(self, limit=1):
        """Estimate charges to be simulated by fitting the charge state
        Gaussian distribution.
        Used as a subfunction for self.setSpecies()
        Limit is given as a percentage of the total height of the Gaussian
        and is used as the cutoff point for whether a charge state is to
        be included or discarded.
        """
        # TODO(gns) - perhaps lower the limit for atropos at least
        # TODO (KT) - maybe change this altogether
        # probably the default value as well.

        self.charges_to_fit = []

        zs = np.arange(1, 151)
        charges = []
        for z in zs:
            xval = msutils.calc_mz(self.csd_mass, z)
            height = self.calc_amplitude(xval)

            if height > self.g_amp * (float(limit) / 100):
                charges.append(z)
                temp_peak = MsPeak()
                temp_peak.x = xval
                temp_peak.y = height
                temp_peak.charge = z
                self.charges_to_fit.append(temp_peak)
                #print('Charges to simulate: z: {0:8.2f} xval: {1:5.2f}  height: {2:8.2f} limit: {3:8.2f}'.format(z, xval,height,self.g_amp * (float(limit) / 100)))


        return charges


    def update_mass_after_optimisation(self):
        """
        After optimisation there is a new mass calculated so the
        charges_to_fit array needs to be updated.
        :return:
        """

        for peak in self.charges_to_fit:
            peak.x = msutils.calc_mz(self.csd_mass, peak.charge)
            peak.y = self.calc_amplitude(peak.x)


    def filter_theoretical_peaks_using_charges(self, charges_array):
        """ Using an array which contains the charges (z) of peaks
         return an array with those msPeaks

        :return:
        """

        charges_to_fit_all = self.charges_to_fit #make a copy of the unfiltered list
        filtered_peaks = []

        for peak in self.charges_to_fit:
            if charges_array.count(peak.charge) == 1:
                filtered_peaks.append(peak)

        self.charges_to_fit = filtered_peaks
        return filtered_peaks


    def simulateSpecies(self,xvals,peakShape='gaussian'):
        """Simulates a mass spectrum using the object's attributes
        Valid peak shapes are: 'hybrid', 'gaussian' & 'lorentzian
        if one_fwhh is to be used be sure to set self.peakFwhm before
        calling this function.
        """
        combined = np.zeros(len(xvals),dtype='float')
        for peak in self.charges_to_fit:
            z = peak.charge
            centre = msutils.calc_mz(self.csd_mass, z)
            amplitude = self.calc_amplitude(centre)
            combined += msutils.gaussian(xvals, amplitude, centre, self.p_fwhh)
            #combined += utils.draw_peaks[peakShape](xvals, amplitude, centre, self.peakFwhm)

        return combined


    def simulateSpecies_back(self,xvals,peak_shape='gaussian'):
        """Simulates a mass spectrum using the object's attributes
        This uses charges to simulate NOT the experimental peaks
        Valid peak shapes are: 'hybrid', 'gaussian' & 'lorentzian
        if one_fwhh is to be used be sure to set self.peakFwhm before
        calling this function.
        If you want to selectively simulate charge states then need to call
        filter_theoretical_peaks_using_charges before this
        """
        combined = np.zeros(len(xvals),dtype='float')
        for peak in self.charges_to_fit:
            combined += peak.simulate_peak(xvals, fwhm=self.p_fwhh, peak_shape=peak_shape)
        return combined


    # ================================================================= #
    # ====                      Plotting                           ==== #
    # ================================================================= #

    def plot_csd_gaussian(self, ax, xaxis, fwhm=10, peakShape='gaussian', **kwargs):
        """ Plot the overall Gaussian which encompases the CSD
        :param ax:
        :param xaxis:
        :return:
        """
        y_offset = 3

        text_to_plot = str(self.name) + " " + str(self.csd_mass)
        ln = ax.plot(xaxis, msutils.gaussian(xaxis, self.g_amp, self.g_mu, self.g_fwhh), **kwargs)
        ln = ax.text(self.g_mu, self.g_amp + y_offset, text_to_plot)
        return ln


    def plot_simulated_species(self, ax, xaxis, fwhm=10, peakShape='gaussian', **kwargs):
        """ Plot the CSD based on all the charge states to be considered NOT the experimentaly selected ones
        :param ax:
        :param xaxis:
        :return:
        """
        yvals = self.simulateSpecies(xaxis)
        ln = ax.plot(xaxis, yvals, **kwargs)
        for peak in self.charges_to_fit:
            ln = ax.text(peak.x, peak.y, peak.charge, **kwargs)

        return ln

    def plot_residuals_per_peak(self, ax, mspeaks_object, **kwargs):
        """
        Calulcates the residuals per each experimental peak and
        plots them. Use this to assess whether a peak does not belong to
        a particular charge state series.
        Useful when assigning peaks to a csd at the beggining
        :return:
        """

        for peak in mspeaks_object:
            residual = self.csd_mass - msutils.calc_mass(peak.x, peak.charge)
            #print self.csd_mass, residual
            ln = ax.plot(peak.x, residual, **kwargs)

        return ln






    def calculateMassAndChargesBACK(self):
        """Calculate the mass of a molecular species using the given m/z
        values.
        Primarily used as a subfunction of self.calculateMass().
        """
        # TODO change this so that after the optimisation the ms_peak objects
        # are updated to include the charge
        iarray = []
        for peak in self.mspeaks:
            iarray.append(peak.x)

        # iarray = mzs[:]
        iarray.sort()
        iarray.reverse()
        charges = collections.OrderedDict()
        lowest = 10000000
        lowest_z = 0
        zs = xrange(1, 101)
        for z in zs:
            charges[z] = []
            for i, mz in enumerate(iarray):
                charges[z].append(msutils.calc_mass(mz, z + i))

        for z in charges.keys():
            sd = np.std(charges[z])
            if sd < lowest:
                lowest = sd
                lowest_z = z

        # calculating error
        total_error = []
        for mass in charges[lowest_z]:
            total_error.append(abs(np.average(charges[lowest_z]) - mass))
        average_error = np.average(total_error)

        self.csd_mass = np.average(charges[lowest_z])
        self.csd_mass_error = average_error
        self.csd_charge_states = [lowest_z + i for i in xrange(len(iarray))]


        # return np.average(charges[lowest_z]), average_error, [lowest_z + i for i in xrange(len(iarray))]
