import numpy as np
import matplotlib as plt
from ichorlib.msClasses.MassSpectrum import MassSpectrum

class IMSpectrum(MassSpectrum):

    def __init__(self):

        self.matrix = np.array([])
        self.atdaxis = np.array([])
        self.mobilogram = np.array([])

    def load_amphi_file(self, filename):
        """Load data from amphitrite data file ('.a').
        The .a file contains mobility information as well so to get the intensity
        you need to sum over the matrix array to create the intensity values of the MS
        :parameter filename: Absolute path to data file
        """
        try:
            dataList = np.load(filename)
            self.matrix = dataList[2]
            self.atdaxis = dataList[1]
            self.xvals = dataList[0]
            self.yvals = np.sum(self.matrix, axis=0)
            self.mobilogram = np.sum(self.matrix, axis=1)
            # print np.shape(self.xvals)
            # print np.shape(self.atdaxis)
            # print np.shape(self.matrix)
            return True
        except:
            print 'Opening amphitrite file failed: %s' % filename
            return False

    def extract_atd_from_mz_range(self, mzmin, mzmax):
        """ Go through the matrix and reconstruct an ATD for a given m/z range
        NOTE: because the m/z you are looking for might not be the exact value in the xvalues array
        what you do is get the absolute difference between the value you are interest and the array
        abs(a-mzmin)
        then use np.argmin to return the index of the smallest value
        (which is the smallest difference between the array values and the actual value you are interested in
        indexmin = np.argmin(abs(a - mzmin))
        You do this by searcing the xvals array the one that holds m/z info then use these indexes to search
        the matrix array the one holding the intensity info

        :param minmz:
        :param maxmz:
        :return:
        """
        indexmin = np.argmin(abs(self.xvals - mzmin))
        indexmax = np.argmin(abs(self.xvals - mzmax))
        matrixslice = self.matrix[:, indexmin:indexmax]
        extractedATDIntensity = np.sum(matrixslice, axis=1)
        print ('Extracting ATD for m/z range {0} - {1}'.format(mzmin, mzmax))

        return extractedATDIntensity

    #TODO: write a bins to ms and vice versa method

    def extract_mz_from_atd_range(self, atdmin, atdmax):
        """ Go through the matrix and reconstruct a m/z for a given ATD range
        The logic is the same as for extract_atd_from_mz_range
        NOTE: this operates on ATD bins not ATDs in ms

        :param minmz:
        :param maxmz:
        :return:
        """
        indexmin = np.argmin(abs(self.atdaxis - atdmin))
        indexmax = np.argmin(abs(self.atdaxis - atdmax))
        matrixslice = self.matrix[indexmin:indexmax, :]
        extractedMZIntensity = np.sum(matrixslice, axis=0)
        print ('Reconstructing m/z for ATD range {0} - {1}'.format(atdmin, atdmax))

        return extractedMZIntensity


    # ================================================================= #
    # ====                      Plotting                           ==== #
    # ================================================================= #

    def plot_mobilogram(self, ax, **kwargs):
        """ Plot the mass spectrum. It actually returns an axes object to plot elsewhere

        :param ax:
        :param kwargs:
        :return:
        """
        ln = ax.plot(self.atdaxis, self.mobilogram, **kwargs)
        ax.set_ylabel('Intensity')
        ax.set_xlabel('ATD')
        return ln