import pickle as pickle
import numpy as np

from ichorlib.genClasses.FileManipulations import FileManipulations
from ichorlib.imClasses.Calibration_KT import CalibrationKT

fm = FileManipulations()
cb = CalibrationKT()

out_base_dir = '/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/ciu_files_new/'

dir_tester = []
dir_tester.append(('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/12_plus/tester/170303'))


dir_recomb_paths = []

dir_recomb_paths.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/12_plus/G117F/170720run2')
dir_recomb_paths.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/12_plus/K154N/170825')
dir_recomb_paths.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/12_plus/recWT/170719')



dir_paths_13 = []

# dir_paths_13.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/13+/M_var/161217')
# dir_paths_13.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/13+/M_var/170213')
# dir_paths_13.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/13+/M_var/170216')
#
# dir_paths_13.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/13+/S_var/170209')
# dir_paths_13.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/13+/S_var/170314run1')
# dir_paths_13.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/13+/S_var/170314run2')
#
# dir_paths_13.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/13+/Z_var/170125')
# dir_paths_13.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/13+/Z_var/170127')



dir_paths_13.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/13_plus/M_var/170213')
dir_paths_13.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/13_plus/Z_var/170125')
dir_paths_13.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/13_plus/S_var/170314')


# -------------- 14 make sure to use the right m/z -------------- #

dir_paths_14 = []

# dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/14+/M_var/170216')
# dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/14+/M_var/170313')
# dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/14+/M_var/170315')
#
# dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/14+/S_var/170320')
# dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/14+/S_var/1703171')
# dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/14+/S_var/1703172')
#
#
# dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/14+/Z_var/170113')
# dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/14+/Z_var/170125')
# dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/BMSS_2017_data/Challenger_ciu_files/14+/Z_var/170127')


dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/14_plus/M_var/170313')
dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/14_plus/S_var/1703171')
dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/14_plus/Z_var/170125')

dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/14_plus/M_var/170216')
dir_paths_14.append('/Users/Kostas/work2017/3-Projects/2017-08-30-BMSS_Talk2017/New_BMSS_data/14_plus/M_var/170315')

#TODO!!!!!!!!!! make sure to use the right values here
plus_mz = 3920
plus_z = 13

for dir_path in dir_paths_13:

    file_ending = dir_path.split('/')
    exp_description = '' + file_ending[-3] + '_' + file_ending[-2] + '_' +file_ending[-1] + ''
    output_file = out_base_dir + exp_description + '_combined.txt'

    print(output_file)

    data = fm.dir_to_challenger_input(output_file, dir_path,
                                      exp_name = exp_description, smooth_data = True,
                                      calibrate = True, charge = plus_z, mz = plus_mz,
                                      gas = 'Nitrogen', wave_velocity = 250)












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
