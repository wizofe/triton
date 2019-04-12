import pandas as pd
import numpy as np
import cPickle as pickle
import ichorlib.msClasses.MsUtils as msutils
from ichorlib.imClasses.Calibration_KT import CalibrationKT
import os


class FileManipulations():

    def __init__(self):
        """
        Class for handling file conversions
        """

    def dir_to_pandas_frame(self, dir_path, experiment_name="Experiment1", smooth_data = False):
        """
        Given a directory it looks at all the .txt files and combines them
        into a challenger input file
        The txt file should have an ending of _TrapV and this will describe the
        column of each data file
        :return:
        """

        self.smoothes = 5
        self.window_len = 5
        self.poly_order = 1

        if smooth_data == True:
            print('Smoothing... Smoothes {0} Window length {1} Polynomial order {2}').format(self.smoothes, self.window_len, self.poly_order)

        intensity_array = []
        atd_array = []
        count = 1

        data = {}

        for temp_file in os.listdir(dir_path):

            if temp_file.endswith(".txt"):

                filepath = os.path.join(dir_path, temp_file)
                print filepath

                temp_voltage = filepath.split('_')
                temp_voltage = temp_voltage[-1].strip('.txt')

                result = []
                f = open(filepath, "r")
                lines = f.readlines()

                for x in lines:
                    stripped = x.strip('\r\n')
                    tokens = stripped.split('\t')

                    print tokens[1]
                    e_notations = tokens[1].replace("E", "e")
                    print e_notations
                    result.append(float(e_notations))

                    if count == 1:  #only get the atd values once
                        atd_array.append(float(tokens[0]))

                f.close()


                temp_voltage = '\"' + temp_voltage + '\"'  # this is so that Javascript Challenger works

                result = np.asarray(result)

                if smooth_data == True:

                    for i in xrange(self.smoothes):
                        result = msutils.sg(result, window_size=self.window_len, order=self.poly_order)


                result = result / result.max()

                data[temp_voltage] = result
                intensity_array.append(result)


                if count == 1:
                    exp_name_string = '\"' + experiment_name + '\"' #this is so that Javascript Challenger works
                    data[exp_name_string] = atd_array
                    count += 1 # increase counter so as to stop

        frame = pd.DataFrame(data)

        return frame


    def dir_to_challenger_input(self, output_file, directory_path, exp_name="Experiment1", smooth_data = False, calibrate = False, charge = 12, mz = 3300, gas='Nitrogen', wave_velocity = 300):


        pandas_frame = self.dir_to_pandas_frame(directory_path, experiment_name=exp_name, smooth_data=smooth_data)

        if calibrate == True:
            self.calibrate_pandas_frame(directory_path, pandas_frame, charge, mz, gas='Nitrogen', wave_velocity = wave_velocity)

        pandas_frame.to_csv(output_file, sep='\t', index=False, quoting=3)

        return pandas_frame



    def calibrate_pandas_frame(self, dir_path, data_frame, charge, mz, gas='Nitrogen', wave_velocity = 300):


        for temp_file in os.listdir(dir_path):

            if temp_file.endswith(".calibration"):
                filepath = os.path.join(dir_path, temp_file)
                print filepath

                cb = CalibrationKT()

                calib = pickle.load(open(filepath))

                print ('Calibrating... Charge: {0},  m/z: {1}, Coefficient A {2} Coefficient B {3}, Calibration R squared {4} Calibrant Wave Velocity {5} Data Wave Velocity {6}').format(charge, mz, calib.coefficientA, calib.coefficientB, calib.rSquared, calib.waveVelocity, wave_velocity)

                atd_axis = np.asarray(data_frame.iloc[:, 0].values)

                calibrated_axis = cb.apply1dCalibration(mz, atd_axis, charge, calib.coefficientA,
                                                        calib.coefficientB, gas='Nitrogen', wave_velocity = wave_velocity)

                data_frame.iloc[:, 0] = calibrated_axis
