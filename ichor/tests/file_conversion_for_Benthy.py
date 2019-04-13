import pickle as pickle
import numpy as np

from ichorlib.genClasses.FileManipulations import FileManipulations
from ichorlib.imClasses.Calibration_KT import CalibrationKT

fm = FileManipulations()
cb = CalibrationKT()

out_base_dir = '/Users/Kostas/work2018/2-Collaborations/Claire_CIU/output/'

dir_recomb_paths = []
dir_recomb_paths.append('/Users/Kostas/work2018/2-Collaborations/Claire_CIU/test')

#TODO!!!!!!!!!! make sure to use the right values here
plus_mz = 3920
plus_z = 13

for dir_path in dir_recomb_paths:

    print(dir_path)
    file_ending = dir_path.split('/')
    exp_description = '' + file_ending[-3] + '_' + file_ending[-2] + '_' +file_ending[-1] + ''
    output_file = out_base_dir + exp_description + '_combined.txt'

    print(output_file)

    data = fm.dir_to_challenger_input(output_file, dir_path,
                                      exp_name = exp_description, smooth_data = True,
                                      calibrate = False)












    # atd_axis = np.asarray(data.iloc[:, 0].values)
    # print atd_axis
    #
    #
    #
    # calibration_file = '/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/13+/Z_var/170125/170125_actual.acal/170125_actual.calibration'
    # calib = pickle.load(open(calibration_file))
    #
    # print calib.coefficientA
    # print calib.coefficientB
    # print calib.waveVelocity
    # print calib.gas
    #
    # plus13mz = 3300
    # charge = 13
    #
    # calibrated_axis = cb.apply1dCalibration(plus13mz, atd_axis, charge, calib.coefficientA, calib.coefficientB )
    # print calibrated_axis
