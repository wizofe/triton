import numpy as np
import ichorlib.msClasses.MsUtils as msutils


class CalibrationKT():
    def __init__(self):
        """
        Calibrate functions
        """
        self.proton_mass = msutils.nist_mass_mono['H+']



    def apply1dCalibration(self,mzs,tds,charge, coefficientA, coefficientB, gas='Nitrogen', wave_velocity = 300):
        """Converts the arrival time values (tds) to collision cross section (CCS).
        Usually used to convert the arrival time axis directly into CCS. Can also be
        used to calculate individual points.

        :parameter mzs: numpy array or float
        :parameter tds: numpy array or float
        :parameter charge: integer value for charge
        """

        #TODO sort out gas and wave velocity I keep passing them to may functions do it somehow else?


        td_prime = self.calculate_td_prime(tds, wave_velocity)
        td_double_prime = self.calculate_td_double_prime(td_prime, mzs)
        red_mass = self.calculate_reduced_mass(mzs, charge, gas)
        ccs = self.calculate_CCS(td_double_prime, coefficientA, coefficientB, charge, red_mass)



        #print ('td {0} td\' {1} td\'\' {2} sqrt(1/reduced) {3} ccs {4}').format(tds, td_prime,
         #                                           td_double_prime, red_mass,
         #                                           ccs)

        return ccs


    def calculate_td_prime(self, td, wave_velocity):

        tm = ((0.01 * 300) / wave_velocity) * 61.0
        tt = ((0.01 * 300) / wave_velocity) * 31.0
        t_total = tm + tt
        return td - t_total

    def calculate_td_double_prime(self, td_prime, mz):

        t_dependent = (np.sqrt(mz / 1000.) * (0.044 + 0.041))
    #TODO the above is what I calculate in my excel sheet but different to what I have in
        #description of the pdf which is
        # t_dependent = np.sqrt((mz / 1000.) * (0.044 + 0.041)))

        return td_prime - t_dependent

    def calculate_reduced_mass(self, mz, charge, gas):

        mGas = 0
        if gas == 'Nitrogen':
            mGas = 28.0134
        elif gas == 'Helium':
            mGas = 4.002

        mass = (mz * charge) - (self.proton_mass * charge)
        red_mass = np.sqrt((mass + mGas) / (mass * mGas))

        return red_mass


    def calculate_CCS(self, td_double_prime, coeffA, coeffB, charge, red_mass):

        CCS = (td_double_prime**coeffB) * coeffA * charge * red_mass

        #TODO deal with values falling outside calibration in a better way
        CCS[np.isnan(CCS)] = 0

        return CCS



    def calculate_omega_prime(self, CCS, charge, mz, gas):
        """
        converts published heium ccs to nitrogen used to calibrate
        :param CCS:
        :param charge:
        :param mz:
        :param gas:
        :return:
        """

        mGas = 0
        if gas == 'Nitrogen':
            mGas = 28.0134
        elif gas == 'Helium':
            mGas = 4.002

        red_mass = self.calculate_reduced_mass(mz, charge, gas)

        omega_prime = CCS / (charge * red_mass)