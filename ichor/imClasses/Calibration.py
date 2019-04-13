"""Class for calculating travelling wave ion mobility calibration curves
for converting arrival time into collision cross section."""

__author__ = "Ganesh N. Sivalingam <g.n.sivalingam@gmail.com"

#import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from scipy import optimize
from scipy.stats import pearsonr
import collections
import ichorlib.msClasses.MsUtils as utils
import pickle as pickle

class Calibration():
    
    def __init__(self):
        self.calibrants = collections.OrderedDict()
        self.coefficientA = None
        self.coefficientB = None
        self.rSquared = None
        self.waveVelocity = None
        self.gas = None
    #===========================================================================
    # Pickling
    #===========================================================================
    def pickle(self,filename):
        """Serialise the calibration data for future use using cPickle.

        :parameter filename: Absolute path and filename to use to save the pickle.
        """
        c = Calibration()
        c.coefficientA = self.coefficientA
        c.coefficientB = self.coefficientB
        c.rSquared = self.rSquared
        c.waveVelocity = self.waveVelocity
        c.gas = self.gas        
        pickle.dump(c,open(filename,'wb'))

    def testAfterUnpickling(self):
        try:
            float(self.coefficientA)
            float(self.coefficientB)
            float(self.rSquared)
            float(self.waveVelocity)
            str(self.gas)
            return True
        except:
            print('Calibration object broken or incomplete')
            return False
        
    ###########################################################################
    # Calibration set up functions
    ###########################################################################     
    def addCalibrant(self,calibrantObj):
        """Add a calibrant (which is another protein or charge state) to the calibration.

        :parameter calibrantObj: A Calibrant() object
        """
        if not calibrantObj.name in list(self.calibrants.keys()):
            self.calibrants[calibrantObj.name] = calibrantObj
        else:
            print('Calibrant of this type exists, remove before proceeding') 
    def removeCalibrant(self,calibrantName):
        """Remove a calibrant from the calibration.

        :parameter calibrantName: Name of calibrant to be removed (dictionary key)
        """
        if calibrantName in self.calibrants:
            del self.calibrants[calibrantName]
            
    def createCalibration(self,waveVelocity,gas='Nitrogen'):
        """Calculate a calibration curve.

        :parameter waveVelocity: IM cell wave velocity (m/s)
        :parameter gas: 'Nitrogen' or 'Helium', used to calculate reduced mass
        """
        # getting the values to be fit
        tdsDoublePrime = []
        ccssPrime = []
        for name in list(self.calibrants.keys()):
            self.calibrants[name].generateCorrectedTdsAndCcss(waveVelocity,gas)
            tdsDoublePrime += self.calibrants[name].getTdsDoublePrime()
            ccssPrime += self.calibrants[name].getCcssPrime()
        tdsDoublePrime = np.array(tdsDoublePrime)
        ccssPrime =      np.array(ccssPrime) 
        
        # do the fit
        p0 = [900.,0.3]
        p1,success = optimize.leastsq(self._errorFunc,p0[:],args=(tdsDoublePrime,ccssPrime))
        
        fittedCcsValues = self._fitEvaluation(p1, tdsDoublePrime)
        self.rSquared,pValue = pearsonr(fittedCcsValues,ccssPrime)
        self.coefficientA = p1[0]
        self.coefficientB = p1[1]
        self.waveVelocity = waveVelocity
        self.gas = gas
    
    def apply1dCalibration(self,mzs,tds,charge):
        """Converts the arrival time values (tds) to collision cross section (CCS).
        Usually used to convert the arrival time axis directly into CCS. Can also be
        used to calculate individual points.

        :parameter mzs: numpy array or float
        :parameter tds: numpy array or float
        :parameter charge: integer value for charge
        """
        # TODO(gns) - why would you want to use an array for mzs with a scalar for tds,
        # TODO(gns) - I think the mzs variable should be renamed mz
        data = self._calculateOmega(tds,mzs, charge, self.gas)
        if type(data).__name__ == 'ndarray':
            data[np.isnan(data)] = 0
        return data

    def getCcsAxisGrid(self,mzs,tds,charge):
        """CCS calibration is dependent on m/z and td, so this calculates the CCS values associated
        with the matrix of intensity values in the 3 dimensional data.

        :parameter mzs: numpy array
        :parameter tds: numpy array
        :parameter charge: integer value for charge
        """
        tds = tds.reshape(len(tds),1)
        CcsGrid = self._calculateOmega(tds, mzs, charge)
        CcsGrid[np.isnan(CcsGrid)] = 0
        return CcsGrid    
    

    ###########################################################################
    # Plotting functions
    ###########################################################################
    def plotCalibrationCurve(self,ax,colourList=False,**kwargs):
        """Plot graph of the calibration including the R^2 value.

        :parameter ax: matplotlib.axes.Axes() object
        :parameter colourList: List of matplotlib colours to use. If False default colours are used
        :parameter \*\*kwargs: matplotlib.pyplot.plot() arguments
        """
        if not colourList: colourList = utils.colourList
        allTdsDoublePrime = []
        for i,(name, calibrantOb) in enumerate(self.calibrants.items()):
            tdsDoublePrime = self.calibrants[name].getTdsDoublePrime()
            allTdsDoublePrime += tdsDoublePrime
            ccssPrime = self.calibrants[name].getCcssPrime()       
            ax.scatter(tdsDoublePrime,ccssPrime,color=colourList[i],label=name,**kwargs)
        xaxis = np.linspace(min(allTdsDoublePrime)*0.9,max(allTdsDoublePrime)*1.1,1000)
        yvals = self._fitEvaluation([self.coefficientA,self.coefficientB], xaxis)
        ax.plot(xaxis,yvals,color='r')
        ax.annotate('R$^2$ = %.4f' %self.rSquared, xy=(0.05, 0.80), xycoords='axes fraction')
        ax.legend(loc='lower right',prop=FontProperties(size=utils.legendFontSize))
        ax.set_ylabel("$\Omega$'")
        ax.set_xlabel("$\mathrm{t}_d$''")
    
    ###########################################################################
    # Private functions
    ###########################################################################    
    def _errorFunc(self,p,x,y):
        """Error function for fitting the calibration curve."""
        return y - self._fitEvaluation(p, x)
    def _fitEvaluation(self,p,x):
        """Function for applying the calibration fitted values."""
        return p[0]*x**p[1]
    def _calculateOmega(self,td,mz,charge,gas='Nitrogen'):
        """Equation for calculating the collision cross section (omega)."""
        td = np.array(td)
        tdPrime = utils._calculateTdPrime(td, self.waveVelocity)
        tdDoublePrime = utils._calculateTdDoublePrime(tdPrime, mz)
        ccsPrime = self.coefficientA*tdDoublePrime**self.coefficientB
        reducedMass = utils._calculateReducedMass(mz, charge, gas)
        ccs = ccsPrime*charge*np.sqrt(1./reducedMass)
        return ccs
        
        
        
        
        
        
        
        
        
        
        
