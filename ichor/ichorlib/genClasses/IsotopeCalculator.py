import numpy as np
import rpy2
import rpy2.robjects as robjects
from ichorlib.msClasses.MassSpectrum import MassSpectrum


class IsotopeCalculator():

    def __init__(self):
        return

    def get_orbitrap_resolution(self, mz, res_at_400 = 60000):

        ratio = np.divide(400., mz)
        resolution = np.sqrt(ratio) * res_at_400

        return resolution

    def get_isotope_spectrum(self, elemental_formulae, resolution, fragment):

        rstring = """
        data(isotopes)
    
        pattern<-isopattern(
          isotopes,
          "{0}",
          threshold=0.1,
          plotit=FALSE,
          charge=FALSE,
          emass=0.00054858,
          algo=1
        )
    
        profiles<-envelope(
            pattern,
            ppm=FALSE,
            dmz=0.0001,   
            frac=1/4,
            env="Gaussian",
            resolution={1},
            plotit=FALSE
        )
    
    
        frame = as.data.frame(profiles)
        frame
    
        """.format(elemental_formulae, resolution)

        # results in a pandas dataframe
        results_df = robjects.r(rstring)
        # x = results_df.iloc[:,0].values
        # y = results_df.iloc[:,1].values
        ms = MassSpectrum()
        ms.name = fragment + '-' + elemental_formulae
        ms.xvals = results_df.iloc[:, 0].values
        ms.yvals = results_df.iloc[:, 1].values

        return ms

