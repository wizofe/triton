import numpy as np
from collections import OrderedDict
from ichorlib.msClasses.MsPeak import MsPeak
from . import detect_peaks 


class PeakPicking ():

    def __init__(self):
        """ Identify Peaks

        """

        self.gradient = [0]
        self.xvals  = []
        self.yvals = []

        self.msPeaks = []


    def get_peaks_using_indexes(self, index_positions):
        """ Using an array which contains the indexes of peaks
        starting at 0 return an array with the msPeaks

        :return:
        """
        return [self.msPeaks[i] for i in index_positions]



    def calculate_gradient(self, xvals, yvals):
        """when reconstructing the data, make data[0] the start value,
        skip the first gradient value then append on
        gradient[i] * (ys[i+1] - ys[i]) (actually gradient[i+1] ...)"""

        self.xvals = xvals
        self.yvals = yvals

        for i, x in enumerate(xvals):
            if i + 2 <= len(xvals):
                try:
                    gr = (float(yvals[i + 1]) - float(yvals[i])) / (float(xvals[i + 1]) - float(x))

                except:
                    print('Gradient calculation: divide by 0 replaced by 0.000001')
                    gr = 0.000001

                self.gradient.append(gr)

        self.gradient = np.array(self.gradient)


    def find_peaks(self, limit=0):
        """limit allows you to ignore slow peaks (remove noise)
        percentage of BPI e.g. 5 % cutoff should be 5"""

        # get gradient for peak picking
        #self.calculate_gradient()

        gPeaks = OrderedDict()
        found_peaks = OrderedDict()



        gradient_length = len(self.gradient)
        #print gradient_length

        count = 0
        for i in range(0, gradient_length-1):
            current_gradient = self.gradient[i]
            #print i, current_gradient
            if current_gradient > 0:
                current_plusone_gradient = self.gradient[i+1]
                if current_plusone_gradient <= 0:

                    if(self.yvals[i] > limit):
                        found_peaks[count] = []
                        found_peaks[count].append(count)
                        found_peaks[count].append(self.xvals[i])
                        found_peaks[count].append(self.yvals[i])

                        temp_ms_peak = MsPeak()
                        temp_ms_peak.x = self.xvals[i]
                        temp_ms_peak.y = self.yvals[i]
                        temp_ms_peak.id = count

                        self.msPeaks.append(temp_ms_peak)
                        count += 1

        #return found_peaks
        return self.msPeaks


    def find_peaks_back(self, limit=0):
        """limit allows you to ignore slow peaks (remove noise)
        percentage of BPI e.g. 5 % cutoff should be 5"""

        # get gradient for peak picking
        #self.calculate_gradient()

        gPeaks = OrderedDict()
        count = 0
        for i, v in enumerate(self.gradient):
            print(i, v)
            if i + 1 < len(self.gradient):
                if v > 0:
                    if self.gradient[i + 1] <= 0:
                        gPeaks[count] = []
                        gPeaks[count].append(self.xvals[i])
                        gPeaks[count].append(self.yvals[i])
                        count += 1
        if limit:
            gPeaks_out = OrderedDict()
            lim = max([gPeaks[x][1] for x in list(gPeaks.keys())]) * float(limit) / 100
            count = 0
            for i, (k, v) in enumerate(gPeaks.items()):
                if v[1] > lim:
                    gPeaks_out[count] = []
                    gPeaks_out[count].append(gPeaks[k][0])
                    gPeaks_out[count].append(gPeaks[k][1])
                    count += 1
            self.gPeaks = gPeaks_out

        else:
            self.gPeaks = gPeaks

        return self.gPeaks