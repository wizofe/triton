import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtGui import QApplication, QDialog
from os import listdir, walk
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as mplcm
import matplotlib.colors as colours
import pandas as pd
import csv
import scipy
from scipy.interpolate import spline
from math import factorial
import seaborn as sns
import itertools
from matplotlib.font_manager import FontProperties
import imageio
from scipy import signal
import pickle as pickle
from decimal import Decimal
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection

qtCreatorFile = 'parser.ui'
# qtColourDialog = 'colour.ui'

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
# Ui_Dialog, QtBaseClass = uic.loadUiType(qtColourDialog)

# class ColourBox(QDialog, Ui_Dialog):
#     def __init__(self, parent=None):
#         super(ColourBox, self).__init__(parent)
#         home = MyApp()
#         self.setupUi(self)
#         self.comboBox
#         if self.exec_():
#             print(str(self.comboBox.currentText()))
#             self.colour = str(self.comboBox.currentText())
#             home.log_2.appendPlainText('Using colour ' + str(self.comboBox.currentText()))
#             QApplication.processEvents()
#         else:
#             print('Default colour scheme used.')


class MyApp(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        #colourdialog = ColourBox()
        self.setupUi(self)

        self.tabWidget

        #################
        # TAB 1 DATA UI #
        #################

        self.block_function_list_single = [
            self.file_selector, self.SG_checkBox, self.colourbox,
            self.SG_windowsize, self.SG_parallelorder, self.SG_smoothNumber,
            self.mean_checkBox, self.mean_windowsize, self.mean_smoothNumber,
            self.start_v, self.increment, self.smoothedoutput_checkBox,
            self.mz_button, self.combined_button, self.ccs_button, self.ccs_z,
            self.ccs_mz, self.calibration_selector
        ]

        self.file_selector.clicked.connect(self.Directory_Selector)

        self.SG_checkBox.stateChanged.connect(self.SG_checked)

        self.colourbox

        self.SG_windowsize.setDisabled(True)
        win_size = self.SG_windowsize.toPlainText()
        self.SG_windowsize.setPlainText(win_size)

        self.SG_parallelorder.setDisabled(True)
        pal_order = (self.SG_parallelorder.toPlainText())
        self.SG_parallelorder.setPlainText(pal_order)

        self.SG_smoothNumber.setDisabled(True)
        SG_smoothNo = (self.SG_smoothNumber.toPlainText())
        self.SG_smoothNumber.setPlainText(SG_smoothNo)

        self.mean_checkBox.clicked.connect(self.mean_checked)

        self.mean_windowsize.setDisabled(True)
        win_size = self.mean_windowsize.toPlainText()
        self.mean_windowsize.setPlainText(win_size)

        self.mean_smoothNumber.setDisabled(True)
        mean_smoothNo = (self.mean_smoothNumber.toPlainText())
        self.mean_smoothNumber.setPlainText(mean_smoothNo)

        self.start_v

        self.increment

        self.increment_unit.setPlainText('V')
        inc = (self.increment_unit.toPlainText())
        self.increment_unit.setPlainText(inc)

        self.smoothedoutput_checkBox

        self.mz_button

        self.combined_button.setChecked(True)

        self.averaged_data_button

        self.average_ccs_button

        self.ccs_button.stateChanged.connect(self.ccs_checked)

        self.ccs_z.setDisabled(True)
        ccsz = (self.ccs_z.toPlainText())
        self.ccs_z.setPlainText(ccsz)

        self.ccs_mz.setDisabled(True)
        ccsmz = (self.ccs_mz.toPlainText())
        self.ccs_mz.setPlainText(ccsmz)

        self.calibration_selector.clicked.connect(
            self.calibration_file_selection)
        self.calibration_selector.setDisabled(True)

        self.calculate.clicked.connect(self.calculate_clicked)

        self.progressBar
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)

        self.log
        self.scrollAreaWidgetContents

        self.graph_placement.setScaledContents(True)

        self.ATD_gif.setScaledContents(True)

        #################
        # TAB 2 DATA UI #
        #################

        self.block_function_list_double = [
            self.file_selector_dataset_1, self.file_selector_dataset_2,
            self.colourbox_1, self.colourbox_2, self.SG_checkBox_2,
            self.SG_windowsize_2, self.SG_parallelorder_2,
            self.SG_smoothNumber_2, self.mean_checkBox_2,
            self.mean_windowsize_2, self.mean_smoothNumber_2, self.start_v_2,
            self.increment_2, self.increment_unit_2, self.combined_button_2,
            self.mz_button_2, self.ccs_button_2,
            self.double_calibration_selector_1,
            self.double_calibration_selector_2, self.double_ccs_z_1,
            self.double_ccs_mz_1, self.double_ccs_z_2, self.double_ccs_mz_2,
            self.dataname_1, self.dataname_2
        ]

        self.file_selector_dataset_1.clicked.connect(
            self.Double_Directory_Selector_1)

        self.file_selector_dataset_2.clicked.connect(
            self.Double_Directory_Selector_2)

        # self.double_colour_button_1.clicked.connect(self.open_colour)

        # self.double_colour_button_2.clicked.connect(self.open_colour)

        self.colourbox_1

        self.colourbox_2

        self.SG_checkBox_2.stateChanged.connect(self.double_SG_checked)

        self.SG_windowsize_2.setDisabled(True)
        win_size_2 = self.SG_windowsize_2.toPlainText()
        self.SG_windowsize_2.setPlainText(win_size_2)

        self.SG_parallelorder_2.setDisabled(True)
        pal_order_2 = (self.SG_parallelorder_2.toPlainText())
        self.SG_parallelorder_2.setPlainText(pal_order_2)

        self.SG_smoothNumber_2.setDisabled(True)
        SG_smoothNo_2 = (self.SG_smoothNumber_2.toPlainText())
        self.SG_smoothNumber_2.setPlainText(SG_smoothNo_2)

        self.mean_checkBox_2.clicked.connect(self.double_mean_checked)

        self.mean_windowsize_2.setDisabled(True)
        win_size_2 = self.mean_windowsize_2.toPlainText()
        self.mean_windowsize_2.setPlainText(win_size_2)

        self.mean_smoothNumber_2.setDisabled(True)
        mean_smoothNo_2 = (self.mean_smoothNumber_2.toPlainText())
        self.mean_smoothNumber_2.setPlainText(mean_smoothNo_2)

        self.start_v_2

        self.increment_2

        self.increment_unit_2.setPlainText('V')
        inc_2 = (self.increment_unit_2.toPlainText())
        self.increment_unit_2.setPlainText(inc)

        self.smoothedoutput_checkBox_2

        self.mz_button_2

        self.combined_button_2.setChecked(True)

        self.averaged_data_button_2

        self.average_ccs_button_2

        self.ccs_button_2.stateChanged.connect(self.double_ccs_checked)

        self.double_calibration_selector_1.clicked.connect(
            self.double_calibration_file_selection_1)
        self.double_calibration_selector_1.setDisabled(True)

        self.double_ccs_mz_1.setDisabled(True)
        double_ccsmz_1 = (self.double_ccs_mz_1.toPlainText())
        self.double_ccs_mz_1.setPlainText(double_ccsmz_1)

        self.double_ccs_mz_2.setDisabled(True)
        double_ccsmz_2 = (self.double_ccs_mz_2.toPlainText())
        self.double_ccs_mz_2.setPlainText(double_ccsmz_2)

        self.double_calibration_selector_2.clicked.connect(
            self.double_calibration_file_selection_2)
        self.double_calibration_selector_2.setDisabled(True)

        self.double_ccs_z_1.setDisabled(True)
        double_ccsz_1 = (self.double_ccs_z_1.toPlainText())
        self.double_ccs_z_1.setPlainText(double_ccsz_1)

        self.double_ccs_z_2.setDisabled(True)
        double_ccsz_2 = (self.double_ccs_z_2.toPlainText())
        self.double_ccs_z_2.setPlainText(double_ccsz_2)

        self.calculate_2.clicked.connect(self.double_calculate_clicked)

        self.progressBar_2
        self.progressBar_2.setMinimum(0)
        self.progressBar_2.setValue(0)

        self.log_2
        self.scrollAreaWidgetContents_2

        self.graph_placement_2.setScaledContents(True)

        self.ATD_gif_2.setScaledContents(True)

        #self.dataname_1.setPlainText()
        dataname_1 = (self.dataname_1.toPlainText())
        self.dataname_1.setPlainText(dataname_1)

        #self.dataname_2.setPlainText()
        dataname_2 = (self.dataname_2.toPlainText())
        self.dataname_2.setPlainText(dataname_2)

        #################
        # TAB 3 DATA UI #
        #################

        self.log_3

        self.av_selector_1.clicked.connect(self.av_directory_selector_1)

        self.av_selector_2.clicked.connect(self.av_directory_selector_2)
        self.av_selector_2.setDisabled(True)

        self.av_selector_3.clicked.connect(self.av_directory_selector_3)
        self.av_selector_3.setDisabled(True)

        self.av_CCS_button.stateChanged.connect(self.av_ccs_checked)

        self.av_calibration_selector_1.clicked.connect(
            self.av_calibration_file_selection_1)
        self.av_calibration_selector_1.setDisabled(True)

        self.av_calibration_selector_2.clicked.connect(
            self.av_calibration_file_selection_2)
        self.av_calibration_selector_2.setDisabled(True)

        self.av_calibration_selector_3.clicked.connect(
            self.av_calibration_file_selection_3)
        self.av_calibration_selector_3.setDisabled(True)

        self.av_ccs_z.setDisabled(True)
        av_ccsz = (self.av_ccs_z.toPlainText())
        self.av_ccs_z.setPlainText(av_ccsz)

        self.av_ccs_mz.setDisabled(True)

        self.calculate_4.clicked.connect(self.av_calculate_clicked)

        self.progressBar_4
        self.progressBar_4.setMinimum(0)
        self.progressBar_4.setValue(0)

    ############################
    # TAB 1 BUTTON DEFINITIONS #
    ############################

    # def open_colour(self):
    #     window = ColourBox(self)
    #     if self.double_colour_button_1.clicked():
    #         print('1')
    #     window.show()

    def SG_checked(self):

        if self.SG_checkBox.isChecked():
            self.SG_windowsize.setDisabled(False)
            self.SG_parallelorder.setDisabled(False)
            self.SG_smoothNumber.setDisabled(False)
            self.mean_checkBox.setChecked(False)
            self.mean_windowsize.setDisabled(True)
            self.mean_smoothNumber.setDisabled(True)

        else:
            self.SG_windowsize.setDisabled(True)
            self.SG_parallelorder.setDisabled(True)
            self.SG_smoothNumber.setDisabled(True)

    def mean_checked(self):

        if self.mean_checkBox.isChecked():
            self.mean_windowsize.setDisabled(False)
            self.mean_smoothNumber.setDisabled(False)
            self.SG_checkBox.setChecked(False)
            self.SG_windowsize.setDisabled(True)
            self.SG_parallelorder.setDisabled(True)
            self.SG_smoothNumber.setDisabled(True)

        else:
            self.mean_windowsize.setDisabled(True)
            self.mean_smoothNumber.setDisabled(True)

    def ccs_checked(self):

        if self.ccs_button.isChecked():
            self.ccs_mz.setDisabled(False)
            self.mz_button.setCheckState(False)
            self.ccs_z.setDisabled(False)
            self.calibration_selector.setDisabled(False)

        else:
            self.ccs_mz.setDisabled(True)
            self.ccs_z.setDisabled(True)

    def Directory_Selector(self):

        dataFn = QtGui.QFileDialog.getExistingDirectory(self,
                                                        'Select Directory')
        self.log.moveCursor(QtGui.QTextCursor.End)
        self.log.appendPlainText('Using directory location ' + dataFn)
        QApplication.processEvents()
        self.dname = str(dataFn)

        self.files_list = []
        self.curdir_files_list = []
        for files in listdir(self.dname):
            #print(files)
            if files.endswith('.txt'):
                self.curdir_files_list.append(self.dname + '\\' + files)
                self.files_list.append(files)
                self.log.moveCursor(QtGui.QTextCursor.End)
                self.log.ensureCursorVisible()
                self.log.moveCursor(QtGui.QTextCursor.End)
                self.log.appendPlainText('Found file ' + str(files))
                QApplication.processEvents()
        self.progress = 0

        self.progressBar.setMaximum(len(self.curdir_files_list) + 2)

    def calibration_file_selection(self):
        dataFn = QtGui.QFileDialog.getOpenFileName(self, 'Select File',
                                                   '*.calibration')
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        self.log.moveCursor(QtGui.QTextCursor.End)
        self.log.appendPlainText('Found calibration file ' + dataFn)
        QApplication.processEvents()
        self.objects = []
        with (open(dataFn, "rb")) as openfile:
            while True:
                try:
                    self.objects.append(pickle.load(openfile))
                except EOFError:
                    break
        self.cal = self.objects[0]

    def calculate_clicked(self):
        plt.clf()
        self.progress = 0
        self.progressBar.setValue(self.progress)
        QApplication.processEvents()

        # for item in self.block_function_list_single:
        #     item.setDisabled(True)

        def movingaverage(interval, window_size):
            window = np.ones(int(window_size)) / float(window_size)
            return np.convolve(interval, window, 'same')

        verts = []  #to be used for polygon plots down the line

        num_colours = len(self.curdir_files_list)

        fontP = FontProperties()
        fontP.set_size('small')

        Blue_cubehelix = [2.8, -.1, 0.8, 0.2]
        Red_cubehelix = [1, -.1, 0.8, 0.2]
        Green_cubehelix = [2, -.1, 0.8, 0.2]
        Rainbow_cubehelix = [2.8, 2, 0.8, 0.2]
        Reverse_Rainbow_cubehelix = [1, -2, 0.8, 0.2]
        Orange_cubehelix = [1.3, -.1, 0.8, 0.2]

        colour = []

        if str(self.colourbox.currentText()) == 'Blue - cubehelix':
            colour = Blue_cubehelix
        elif str(self.colourbox.currentText()) == 'Red - cubehelix':
            colour = Red_cubehelix
        elif str(self.colourbox.currentText()) == 'Green - cubehelix':
            colour = Green_cubehelix
        elif str(self.colourbox.currentText()) == 'Rainbow - cubehelix':
            colour = Rainbow_cubehelix
        elif str(self.colourbox.currentText()) == 'Orange - cubehelix':
            colour = Orange_cubehelix

        sns.set_style('white')
        #palette = itertools.cycle(sns.hls_palette(num_colours))
        palette_1 = itertools.cycle(
            sns.cubehelix_palette(n_colors=num_colours,
                                  start=colour[0],
                                  rot=colour[1],
                                  light=colour[2],
                                  dark=colour[3]))
        palette = itertools.cycle(sns.husl_palette(num_colours))
        sns.set_style('ticks')

        x_list = []
        y_list = []

        experiment_list = []

        if (self.start_v.value() == 0) and (self.increment.value == 0):
            self.log.moveCursor(QtGui.QTextCursor.End)
            self.log.appendPlainText(
                'No increments selected so using file name as graph title.')
            title_list = self.files_list
        else:
            s_v = self.start_v.value()

            inc = self.increment.value()

            end_v = s_v + num_colours * inc

            volt_list = []
            volt_list.append(list(range(s_v, end_v, inc)))
            title_list = []

            if self.increment_unit.toPlainText() == '':
                self.log.moveCursor(QtGui.QTextCursor.End)
                self.log.appendPlainText(
                    'No increment unit selected, using V as a standard.')

            for item in volt_list[0]:
                unit = self.increment_unit.toPlainText()
                if self.increment_unit.toPlainText() == '':
                    unit == 'V'
                new_item = str(item) + unit
                title_list.append(new_item)

            if self.ccs_button.isChecked():
                self.log.moveCursor(QtGui.QTextCursor.End)
                self.log.appendPlainText(
                    'Converting arrival time to CCS using selected calibration file'
                )
                #ccs_factor = float(self.ccs_converter_box.toPlainText())
                # else:
                #     ccs_factor = 1
                QApplication.processEvents()

        for file_n in self.files_list:

            time_smooth = []

            for curdir_filename in self.curdir_files_list:
                filename_0 = curdir_filename.replace(self.dname, '')
                filename_1 = filename_0.replace('\\', '')
                #print(filename_1)
                experiment_list.append(filename_1.replace('.txt', ''))
                self.log.moveCursor(QtGui.QTextCursor.End)
                self.log.appendPlainText('Creating graph for ' +
                                         title_list[self.progress])

                with open(curdir_filename, 'r') as file:
                    if self.averaged_data_button.isChecked():
                        reader = csv.reader(file)
                        time = []
                        intensity = []
                        sd = []
                        data_list = list(
                            zip(*(line.strip().split('\t') for line in file)))
                        for item in tuple(data_list[0]):
                            time.append(float(item))
                        for item in tuple(data_list[1]):
                            intensity.append(float(item))
                        for item in tuple(data_list[2]):
                            sd.append(float(item))

                    else:
                        reader = csv.reader(file)
                        time = []
                        intensity = []
                        sd = 0
                        data_list = list(
                            zip(*(line.strip().split('\t') for line in file)))
                        for item in tuple(data_list[0]):
                            time.append(float(item))
                        for item in tuple(data_list[1]):
                            intensity.append(float(item))

                    if self.SG_checkBox.isChecked():
                        intensity_output = []
                        intensity_smooth = []
                        SG_smooth_counter = int(
                            self.SG_smoothNumber.toPlainText())
                        while (SG_smooth_counter >= 1):
                            window_smooth = int(
                                self.SG_windowsize.toPlainText())
                            par_order = int(self.SG_parallelorder.toPlainText())
                            if len(intensity_output) == 0:
                                intensity_array = np.array(intensity)
                                intensity_smooth = scipy.signal.savgol_filter(
                                    intensity_array, window_smooth, par_order)
                                SG_smooth_counter = SG_smooth_counter - 1
                                intensity_output = intensity_smooth

                            else:
                                intensity_smooth = scipy.signal.savgol_filter(
                                    intensity_output, window_smooth, par_order)
                                SG_smooth_counter = SG_smooth_counter - 1

                    elif self.mean_checkBox.isChecked():
                        intensity_output = []
                        intensity_smooth = []
                        mean_smooth_counter = int(
                            self.mean_smoothNumber.toPlainText())
                        while (mean_smooth_counter >= 1):
                            window_smooth = int(
                                self.mean_windowsize.toPlainText())
                            if len(intensity_output) == 0:
                                intensity_array = np.array(intensity)
                                intensity_smooth = movingaverage(
                                    intensity_array, window_smooth)
                                mean_smooth_counter = mean_smooth_counter - 1
                                intensity_output = intensity_smooth
                            else:
                                intensity_smooth = movingaverage(
                                    intensity_output, window_smooth)
                                mean_smooth_counter = mean_smooth_counter - 1

                        if self.averaged_data_button.isChecked():
                            sd_output = []
                            sd_smooth = []
                            mean_smooth_counter = int(
                                self.mean_smoothNumber.toPlainText())
                            while (mean_smooth_counter >= 1):
                                window_smooth = int(
                                    self.mean_windowsize.toPlainText())
                                if len(sd_output) == 0:
                                    sd_array = np.array(sd)
                                    sd_smooth = movingaverage(
                                        sd_array, window_smooth)
                                    mean_smooth_counter = mean_smooth_counter - 1
                                    sd_output = sd_smooth
                                else:
                                    sd_smooth = movingaverage(
                                        sd_output, window_smooth)
                                    mean_smooth_counter = mean_smooth_counter - 1

                        else:
                            sd_smooth = sd
                    else:
                        intensity_smooth = intensity
                        sd_smooth = sd

                    pc_intensity = []
                    for item in intensity_smooth:
                        pc_intensity.append(
                            (100 / max(intensity_smooth) * float(item)))

                    if self.average_ccs_button.isChecked():
                        time_smooth = time
                    else:
                        time_smooth = np.linspace(time[0], time[-1],
                                                  len(pc_intensity))

                    if self.ccs_button.isChecked():
                        ccs_list = []
                        for item in time_smooth:
                            new_item = self.cal._calculateOmega(
                                item, float(self.ccs_mz.toPlainText()),
                                float(self.ccs_z.toPlainText()))
                            if math.isnan(new_item) == True:
                                new_item = 0
                            ccs_list.append(new_item)
                        time_smooth = ccs_list

                    verts.append(list(zip(time_smooth, pc_intensity)))

                    QApplication.processEvents()
                    axes = plt.gca()
                    axes.set_ylim([0, 100])
                    axes.set_xlim([time_smooth[8], time_smooth[-1]])

                    x = np.array(time_smooth)
                    y = np.array(pc_intensity)
                    # shift_intensity = []
                    # for item in pc_intensity:
                    #     shift_intensity.append(item + (25*self.progress))

                    # shift_y = np.array(shift_intensity)

                    # x_list.append(x)
                    # y_list.append(shift_y)

                    plt.plot(x, y, color=next(palette), linewidth=1)
                    if self.averaged_data_button.isChecked():
                        e = np.array(sd_smooth)
                        lower_bound = y + e
                        upper_bound = y - e
                        plt.fill_between(x,
                                         lower_bound,
                                         upper_bound,
                                         facecolor=next(palette),
                                         alpha=0.5)
                    else:
                        e = 0

                    sns.despine()
                    axes = plt.gca()
                    plt.title(title_list[self.progress])
                    plt.ylabel('Intensity %')

                    if self.ccs_button.isChecked():
                        plt.xlabel('CCS (' + '$\AA^2$' + ')')
                    elif self.mz_button.isChecked():
                        plt.xlabel('m/z')
                    elif self.average_ccs_button.isChecked():
                        plt.xlabel('CCS (' + '$\AA^2$' + ')')
                    else:
                        plt.xlabel('Time (ms)')
                    experiment_name = experiment_list[self.progress]
                    plt.tight_layout()
                    plt.savefig(self.dname + '\\' + experiment_name + '.png')
                    plt.clf()

                    self.progress = self.progress + 1
                    self.progressBar.setValue(self.progress)
                    QApplication.processEvents()

                    if self.smoothedoutput_checkBox.isChecked():
                        self.log.appendPlainText(
                            'Writing smoothed file to new subdirectory')
                        self.log.moveCursor(QtGui.QTextCursor.End)
                        QApplication.processEvents()
                        with open(
                                self.dname + '\\subdir\\' + experiment_name +
                                '_smoothed.txt', 'w') as smoothed_output:
                            writer = csv.writer(smoothed_output,
                                                delimiter='\t',
                                                lineterminator='\n')
                            writing_list = []
                            for (time, ints) in zip(time_smooth, pc_intensity):
                                writing_list = [time, ints]
                                writer.writerow(writing_list)

            self.log.appendPlainText('Creating animated gif')
            QApplication.processEvents()

            image_list = []
            images = []

            for experiment in experiment_list:
                image_list.append(experiment + '.png')

            for item in image_list:
                if item == ('Combined.png'):
                    item.replace('Combined.png', '')

            for item in image_list:
                images.append(imageio.imread(self.dname + '/' + item))

            imageio.mimsave(self.dname + '/' + 'ATD.gif', images)
            self.progress = self.progress + 1

            gif = QMovie(self.dname + '\ATD.gif')
            self.ATD_gif.setMovie(gif)
            gif.start()
            QApplication.processEvents()

            if self.combined_button.isChecked():
                self.log.moveCursor(QtGui.QTextCursor.End)
                self.log.appendPlainText('Creating combined graph')
                QApplication.processEvents()

                z_set = list(range(s_v, end_v, inc))

                fig = plt.figure()
                axes = fig.gca(projection='3d')
                palette_1 = sns.color_palette("husl", (num_colours))

                poly = PolyCollection(verts,
                                      edgecolors='black',
                                      facecolors=palette_1)
                poly.set_alpha(0.7)
                axes.add_collection3d(poly, zs=z_set, zdir='y')

                # axes.set_xlim([time_smooth[8], time_smooth[-1]])
                axes.set_title('Combined Distributions of ' + title_list[0] +
                               ' to ' + title_list[-1])

                if self.mz_button.isChecked():
                    axes.set_xlabel('m/z')
                elif self.ccs_button.isChecked():
                    axes.set_xlabel('CCS (' + '$\AA^2$' + ')')
                elif self.average_ccs_button.isChecked():
                    axes.set_xlabel('CCS (' + '$\AA^2$' + ')')
                else:
                    axes.set_xlabel('Time (ms)')

                axes.set_xlim(time_smooth[8], time_smooth[-1])

                axes.set_ylabel(self.increment_unit.toPlainText())
                axes.set_ylim3d(s_v, end_v)

                axes.set_zlabel('Intensity (%)')
                axes.set_zlim3d(0, 100)

                # for x_set in x_list:
                #     for y_set in y_list:
                #         plt.plot(x_set, y_set, color=next(palette), linewidth = 1.25)
                #         plt.legend(title_list, loc='upper left', bbox_to_anchor=(1, 1.15), fancybox=True)
                #         sns.despine()

                # plt.show()
                plt.savefig(self.dname + '\Combined.png')
                plt.clf()
                self.progress = self.progress + 1
                self.progressBar.setValue(self.progress)

                pixmap = QPixmap(self.dname + '\Combined.png')
                self.graph_placement.setPixmap(pixmap)
                QApplication.processEvents()

            self.log.moveCursor(QtGui.QTextCursor.End)
            self.log.appendPlainText(
                'Programme completed, image files saved to ' + self.dname)
            self.progressBar.setValue(len(self.files_list) + 2)
            QApplication.processEvents()

            for item in self.block_function_list_single:
                item.setDisabled(False)

        if self.SG_checkBox.isChecked():
            self.SG_windowsize.setDisabled(False)
            self.SG_parallelorder.setDisabled(False)
            self.SG_smoothNumber.setDisabled(False)
            self.mean_checkBox.setChecked(False)
            self.mean_windowsize.setDisabled(True)
            self.mean_smoothNumber.setDisabled(True)

        else:
            self.SG_windowsize.setDisabled(True)
            self.SG_parallelorder.setDisabled(True)
            self.SG_smoothNumber.setDisabled(True)

        if self.mean_checkBox.isChecked():
            self.mean_windowsize.setDisabled(False)
            self.mean_smoothNumber.setDisabled(False)
            self.SG_checkBox.setChecked(False)
            self.SG_windowsize.setDisabled(True)
            self.SG_parallelorder.setDisabled(True)
            self.SG_smoothNumber.setDisabled(True)

        else:
            self.mean_windowsize.setDisabled(True)
            self.mean_smoothNumber.setDisabled(True)

        if self.ccs_button.isChecked():
            self.ccs_mz.setDisabled(False)
            self.mz_button.setCheckState(False)
            self.ccs_z.setDisabled(False)
            self.calibration_selector.setDisabled(False)

        else:
            self.ccs_mz.setDisabled(True)
            self.ccs_z.setDisabled(True)

    ############################
    # TAB 2 BUTTON DEFINITIONS #
    ############################

    def Double_Directory_Selector_1(self):
        double_dataFn_1 = QtGui.QFileDialog.getExistingDirectory(
            self, 'Select Directory')
        self.log_2.moveCursor(QtGui.QTextCursor.End)
        self.log_2.appendPlainText('Using directory location ' +
                                   double_dataFn_1)
        QApplication.processEvents()
        self.double_dname_1 = str(double_dataFn_1)

        self.double_files_list_1 = []
        self.double_curdir_files_list_1 = []
        for files in listdir(self.double_dname_1):
            #print(files)
            if files.endswith('.txt'):
                self.double_curdir_files_list_1.append(self.double_dname_1 +
                                                       '\\' + files)
                self.double_files_list_1.append(files)
                self.log_2.moveCursor(QtGui.QTextCursor.End)
                self.log_2.ensureCursorVisible()
                self.log.moveCursor(QtGui.QTextCursor.End)
                self.log_2.appendPlainText('Found file ' + str(files))
                QApplication.processEvents()
        self.progress_2 = 0

        self.progressBar_2.setMaximum(len(self.double_curdir_files_list_1) + 2)

    def Double_Directory_Selector_2(self):
        double_dataFn_2 = QtGui.QFileDialog.getExistingDirectory(
            self, 'Select Directory')
        self.log_2.moveCursor(QtGui.QTextCursor.End)
        self.log_2.appendPlainText('Using directory location ' +
                                   double_dataFn_2)
        QApplication.processEvents()
        self.double_dname_2 = str(double_dataFn_2)

        self.double_files_list_2 = []
        self.double_curdir_files_list_2 = []
        for files in listdir(self.double_dname_2):
            #print(files)
            if files.endswith('.txt'):
                self.double_curdir_files_list_2.append(self.double_dname_2 +
                                                       '\\' + files)
                self.double_files_list_2.append(files)
                self.log_2.moveCursor(QtGui.QTextCursor.End)
                self.log_2.ensureCursorVisible()
                self.log.moveCursor(QtGui.QTextCursor.End)
                self.log_2.appendPlainText('Found file ' + str(files))
                QApplication.processEvents()
        self.progress_2 = 0

        self.progressBar_2.setMaximum(len(self.double_curdir_files_list_2) + 2)

    def double_SG_checked(self):

        if self.SG_checkBox_2.isChecked():
            self.SG_windowsize_2.setDisabled(False)
            self.SG_parallelorder_2.setDisabled(False)
            self.SG_smoothNumber_2.setDisabled(False)
            self.mean_checkBox_2.setChecked(False)
            self.mean_windowsize_2.setDisabled(True)
            self.mean_smoothNumber_2.setDisabled(True)

        else:
            self.SG_windowsize_2.setDisabled(True)
            self.SG_parallelorder_2.setDisabled(True)
            self.SG_smoothNumber_2.setDisabled(True)

    def double_mean_checked(self):

        if self.mean_checkBox_2.isChecked():
            self.mean_windowsize_2.setDisabled(False)
            self.mean_smoothNumber_2.setDisabled(False)
            self.SG_checkBox_2.setChecked(False)
            self.SG_windowsize_2.setDisabled(True)
            self.SG_parallelorder_2.setDisabled(True)
            self.SG_smoothNumber_2.setDisabled(True)

        else:
            self.mean_windowsize_2.setDisabled(True)
            self.mean_smoothNumber_2.setDisabled(True)

    def double_ccs_checked(self):

        if self.ccs_button_2.isChecked():
            self.double_ccs_z_1.setDisabled(False)
            self.double_ccs_mz_1.setDisabled(False)
            self.double_ccs_z_2.setDisabled(False)
            self.double_ccs_mz_2.setDisabled(False)
            self.mz_button_2.setCheckState(False)
            self.double_calibration_selector_1.setDisabled(False)
            self.double_calibration_selector_2.setDisabled(False)

        else:
            self.double_ccs_z_1.setDisabled(True)
            self.double_ccs_mz_1.setDisabled(True)
            self.double_ccs_z_2.setDisabled(True)
            self.double_ccs_mz_2.setDisabled(True)
            self.double_calibration_selector_1.setDisabled(True)
            self.double_calibration_selector_2.setDisabled(True)

    def double_calibration_file_selection_1(self):
        dataFn = QtGui.QFileDialog.getOpenFileName(self, 'Select File',
                                                   '*.calibration')
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        self.log_2.moveCursor(QtGui.QTextCursor.End)
        self.log_2.appendPlainText('Found calibration file ' + dataFn)
        QApplication.processEvents()
        self.objects = []
        with (open(dataFn, "rb")) as openfile:
            while True:
                try:
                    self.objects.append(pickle.load(openfile))
                except EOFError:
                    break
        self.double_cal_1 = self.objects[0]

    def double_calibration_file_selection_2(self):
        dataFn = QtGui.QFileDialog.getOpenFileName(self, 'Select File',
                                                   '*.calibration')
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        self.log_2.moveCursor(QtGui.QTextCursor.End)
        self.log_2.appendPlainText('Found calibration file ' + dataFn)
        QApplication.processEvents()
        self.objects = []
        with (open(dataFn, "rb")) as openfile:
            while True:
                try:
                    self.objects.append(pickle.load(openfile))
                except EOFError:
                    break
        self.double_cal_2 = self.objects[0]

    def double_calculate_clicked(self):
        plt.clf()
        self.progress_2 = 0
        self.progressBar_2.setValue(self.progress_2)
        QApplication.processEvents()

        # for item in self.block_function_list_double:
        #     item.setDisabled(True)

        def movingaverage2(interval_2, window_size_2):
            window_2 = np.ones(int(window_size_2)) / float(window_size_2)
            return np.convolve(interval_2, window_2, 'same')

        num_colours_1 = len(self.double_curdir_files_list_1)

        Blue_cubehelix = [2.8, -.1, 0.8, 0.2]
        Red_cubehelix = [1, -.1, 0.8, 0.2]
        Green_cubehelix = [2, -.1, 0.8, 0.2]
        Rainbow_cubehelix = [2.8, 2, 0.8, 0.2]
        Reverse_Rainbow_cubehelix = [1, -2, 0.8, 0.2]
        Orange_cubehelix = [1.5, -.1, 0.8, 0.2]
        Purple_cubehelix = [0.5, -.1, 0.8, 0.2]

        fontP = FontProperties()
        fontP.set_size('small')
        colour_1 = []
        colour_2 = []
        if str(self.colourbox_1.currentText()) == 'Blue - cubehelix':
            colour_1 = Blue_cubehelix
        elif str(self.colourbox_1.currentText()) == 'Red - cubehelix':
            colour_1 = Red_cubehelix
        elif str(self.colourbox_1.currentText()) == 'Green - cubehelix':
            colour_1 = Green_cubehelix
        elif str(self.colourbox_1.currentText()) == 'Rainbow - cubehelix':
            colour_1 = Rainbow_cubehelix
        elif str(self.colourbox_1.currentText()) == 'Orange - cubehelix':
            colour_1 = Orange_cubehelix
        elif str(self.colourbox_1.currentText()) == 'Purple - cubehelix':
            colour_1 = Purple_cubehelix

        if str(self.colourbox_2.currentText()) == 'Blue - cubehelix':
            colour_2 = Blue_cubehelix
        elif str(self.colourbox_2.currentText()) == 'Red - cubehelix':
            colour_2 = Red_cubehelix
        elif str(self.colourbox_2.currentText()) == 'Green - cubehelix':
            colour_2 = Green_cubehelix
        elif str(self.colourbox_2.currentText()) == 'Rainbow - cubehelix':
            colour_2 = Rainbow_cubehelix  #
        elif str(self.colourbox_2.currentText()) == 'Orange - cubehelix':
            colour_2 = Orange_cubehelix
        elif str(self.colourbox_2.currentText()) == 'Purple - cubehelix':
            colour_2 = Purple_cubehelix

        sns.set_style('white')
        palette_dataset_1 = itertools.cycle(
            sns.cubehelix_palette(n_colors=num_colours_1,
                                  start=colour_1[0],
                                  rot=colour_1[1],
                                  light=colour_1[2],
                                  dark=colour_1[3]))
        palette_dataset_2 = itertools.cycle(
            sns.cubehelix_palette(n_colors=num_colours_1,
                                  start=colour_2[0],
                                  rot=colour_2[1],
                                  light=colour_2[2],
                                  dark=colour_2[3],
                                  reverse=True))
        sns.set_style('ticks')

        x_list_1 = []
        y_list_1 = []

        experiment_list_1 = []

        x_list_2 = []
        y_list_2 = []

        experiment_list_2 = []

        if (self.start_v_2.value() == 0) and (self.increment_2.value == 0):
            self.log_2.moveCursor(QtGui.QTextCursor.End)
            self.log_2.appendPlainText(
                'No increments selected so using file name as graph title.')
            title_list_2 = self.double_files_list_1
        else:
            s_v_2 = self.start_v_2.value()

            inc_2 = self.increment_2.value()

            end_v_2 = s_v_2 + num_colours_1 * inc_2

            volt_list_2 = []
            volt_list_2.append(list(range(s_v_2, end_v_2, inc_2)))
            title_list_2 = []

            if self.increment_unit_2.toPlainText() == '':
                self.log_2.moveCursor(QtGui.QTextCursor.End)
                self.log_2.appendPlainText(
                    'No increment unit selected, using V as a standard.')

            for item in volt_list_2[0]:
                unit_2 = self.increment_unit_2.toPlainText()
                if self.increment_unit_2.toPlainText() == '':
                    unit_2 == 'V'
                new_item = str(item) + unit_2
                title_list_2.append(new_item)

            if self.ccs_button_2.isChecked():
                self.log_2.moveCursor(QtGui.QTextCursor.End)
                self.log_2.appendPlainText(
                    'Converting arrival time to CCS using selected calibration file'
                )

        for file_n_1, file_n_2 in zip(self.double_curdir_files_list_1,
                                      self.double_curdir_files_list_2):
            self.log_2.moveCursor(QtGui.QTextCursor.End)
            self.log_2.appendPlainText('Creating graph for ' +
                                       self.dataname_1.toPlainText() + ' and ' +
                                       self.dataname_2.toPlainText() +
                                       ', data point ' +
                                       str(title_list_2[self.progress_2]))
            QApplication.processEvents()

            with open(file_n_1, 'r') as file_1:
                reader = csv.reader(file_1)
                time_1 = []
                intensity_1 = []
                data_list_1 = list(
                    zip(*(line.strip().split('\t') for line in file_1)))
                for item in tuple(data_list_1[0]):
                    time_1.append(float(item))
                for item in tuple(data_list_1[1]):
                    intensity_1.append(float(item))

            if self.SG_checkBox_2.isChecked():
                intensity_output_1 = []
                intensity_smooth_1 = []
                SG_smooth_counter_2 = int(self.SG_smoothNumber_2.toPlainText())
                while (SG_smooth_counter_2 >= 1):
                    window_smooth_2 = int(self.SG_windowsize_2.toPlainText())
                    par_order_2 = int(self.SG_parallelorder_2.toPlainText())
                    if len(intensity_output_1) == 0:
                        intensity_array_1 = np.array(intensity_1)
                        intensity_smooth_1 = scipy.signal.savgol_filter(
                            intensity_array_1, window_smooth_2, par_order_2)
                        SG_smooth_counter_2 = SG_smooth_counter_2 - 1
                        intensity_output_1 = intensity_smooth_1

                    else:
                        intensity_smooth_1 = scipy.signal.savgol_filter(
                            intensity_output_1, window_smooth_2, par_order_2)
                        SG_smooth_counter_2 = SG_smooth_counter_2 - 1

            elif self.mean_checkBox_2.isChecked():
                intensity_output_1 = []
                intensity_smooth_1 = []
                mean_smooth_counter_2 = int(
                    self.mean_smoothNumber_2.toPlainText())
                while (mean_smooth_counter_2 >= 1):
                    window_smooth_2 = int(self.mean_windowsize_2.toPlainText())
                    if len(intensity_output_1) == 0:
                        intensity_array_1 = np.array(intensity_1)
                        intensity_smooth_1 = movingaverage2(
                            intensity_array_1, window_smooth_2)
                        mean_smooth_counter_2 = mean_smooth_counter_2 - 1
                        intensity_output_1 = intensity_smooth_1
                    else:
                        intensity_smooth_1 = movingaverage2(
                            intensity_output_1, window_smooth_2)
                        mean_smooth_counter_2 = mean_smooth_counter_2 - 1
            else:
                intensity_smooth_1 = intensity_1

            pc_intensity_1 = []
            for item in intensity_smooth_1:
                pc_intensity_1.append(
                    (100 / max(intensity_smooth_1) * float(item)))
            if self.averaged_data_button_2.isChecked():
                time_smooth_1 = time_1
            else:
                time_smooth_1 = np.linspace(time_1[0], time_1[-1],
                                            len(pc_intensity_1))

            if self.ccs_button_2.isChecked():
                ccs_list_1 = []
                for item in time_smooth_1:
                    new_item = self.double_cal_1._calculateOmega(
                        item, float(self.double_ccs_mz_1.toPlainText()),
                        float(self.double_ccs_z_1.toPlainText()))
                    if math.isnan(new_item) == True:
                        new_item = 0
                    print(new_item)
                    ccs_list_1.append(new_item)
                time_smooth_1 = ccs_list_1

            with open(file_n_2, 'r') as file_2:
                reader = csv.reader(file_2)
                time_2 = []
                intensity_2 = []
                data_list_2 = list(
                    zip(*(line.strip().split('\t') for line in file_2)))
                for item in tuple(data_list_2[0]):
                    time_2.append(float(item))
                for item in tuple(data_list_2[1]):
                    intensity_2.append(float(item))

            pc_intensity_2 = []

            if self.SG_checkBox_2.isChecked():
                intensity_output_2 = []
                intensity_smooth_2 = []
                SG_smooth_counter_2 = int(self.SG_smoothNumber_2.toPlainText())
                while (SG_smooth_counter_2 >= 1):

                    window_smooth_2 = int(self.SG_windowsize_2.toPlainText())
                    par_order_2 = int(self.SG_parallelorder_2.toPlainText())

                    if len(intensity_output_2) == 0:
                        intensity_array_2 = np.array(intensity_2)
                        intensity_smooth_2 = scipy.signal.savgol_filter(
                            intensity_array_2, window_smooth_2, par_order_2)
                        SG_smooth_counter_2 = SG_smooth_counter_2 - 1
                        intensity_output_2 = intensity_smooth_2

                    else:
                        intensity_smooth_2 = scipy.signal.savgol_filter(
                            intensity_output_2, window_smooth_2, par_order_2)
                        SG_smooth_counter_2 = SG_smooth_counter_2 - 1

            elif self.mean_checkBox_2.isChecked():

                intensity_output_2 = []
                intensity_smooth_2 = []
                mean_smooth_counter_2 = int(
                    self.mean_smoothNumber_2.toPlainText())

                while (mean_smooth_counter_2 >= 1):
                    window_smooth_2 = int(self.mean_windowsize_2.toPlainText())

                    if len(intensity_output_2) == 0:
                        intensity_array_2 = np.array(intensity_2)
                        intensity_smooth_2 = movingaverage2(
                            intensity_array_2, window_smooth_2)
                        mean_smooth_counter_2 = mean_smooth_counter_2 - 1
                        intensity_output_2 = intensity_smooth_2

                    else:
                        intensity_smooth_2 = movingaverage2(
                            intensity_output_2, window_smooth_2)
                        mean_smooth_counter_2 = mean_smooth_counter_2 - 1
            else:
                intensity_smooth_2 = intensity_2

            for item in intensity_smooth_2:
                pc_intensity_2.append(
                    (100 / max(intensity_smooth_2) * float(item)))

            if self.averaged_data_button_2.isChecked():
                time_smooth_2 = time_2
            else:
                time_smooth_2 = np.linspace(time_2[0], time_2[-1],
                                            len(pc_intensity_2))

            if self.ccs_button_2.isChecked():
                ccs_list_2 = []
                for item in time_smooth_2:
                    new_item = self.double_cal_2._calculateOmega(
                        item, float(self.double_ccs_mz_2.toPlainText()),
                        float(self.double_ccs_z_2.toPlainText()))
                    if math.isnan(new_item) == True:
                        new_item = 0
                    print(new_item)
                    ccs_list_2.append(new_item)
                time_smooth_2 = ccs_list_2

            axes = plt.gca()
            axes.set_ylim([0, 100])
            axes.set_xlim([time_smooth_1[7], time_smooth_1[-1]])

            x_1 = np.array(time_smooth_1)
            y_1 = np.array(pc_intensity_1)

            x_list_1.append(x_1)
            y_list_1.append(y_1)

            x_2 = np.array(time_smooth_2)
            y_2 = np.array(pc_intensity_2)

            x_list_2.append(x_2)
            y_list_2.append(y_2)

            # x_list.append(x)
            # y_list.append(y)
            labels = [
                self.dataname_1.toPlainText(),
                self.dataname_2.toPlainText()
            ]
            plt.plot(x_1, y_1, color=next(palette_dataset_1), linewidth=1)
            plt.plot(x_2, y_2, color=next(palette_dataset_2), linewidth=1)
            plt.legend(labels, loc='center right', fancybox=True)
            sns.despine()

            axes = plt.gca()
            # if self.progress << num_colours:
            plt.title(title_list_2[self.progress_2])
            plt.ylabel('Intensity %')
            if self.ccs_button_2.isChecked():
                plt.xlabel('CCS (' + '$\AA^2$' + ')')
            elif self.average_ccs_button_2.isChecked():
                plt.xlabel('CCS (' + '$\AA^2$' + ')')
            elif self.mz_button.isChecked():
                plt.xlabel('m/z')
            else:
                plt.xlabel('Time (ms)')
            # for i in num_colours_1:

            #     experiment_name = experiment_list_2[i]
            plt.tight_layout()
            plt.savefig(self.double_dname_2 + '\\' + 'double_' +
                        str(title_list_2[self.progress_2]) + '.png')
            #plt.show()
            plt.clf()
            self.progress_2 = self.progress_2 + 1
            self.progressBar_2.setValue(self.progress_2)
            QApplication.processEvents()

        if self.combined_button_2.isChecked():
            self.log_2.appendPlainText('Creating combined plot')
            QApplication.processEvents()
            # axes = plt.gca()
            # axes.set_ylim([0,100])
            # axes.set_xlim([time_smooth[0], time_smooth[-1]])
            plt.subplot(211)
            ax1 = plt.subplot(211)
            for x_set_1 in x_list_1:
                for y_set_1 in y_list_1:
                    plt.plot(x_set_1,
                             y_set_1,
                             color=next(palette_dataset_1),
                             linewidth=0.75)
                    axes = plt.gca()
                    axes.set_ylim([0, 100])
                    axes.set_xlim([x_list_1[0][8], x_list_1[0][-1]])
                    plt.title(self.dataname_1.toPlainText())
                    box = ax1.get_position()
                    ax1.set_position(
                        [box.x0, box.y0, box.width * 0.75, box.height])
                    plt.ylabel('Intensity %')
                    plt.legend(title_list_2,
                               loc='upper left',
                               bbox_to_anchor=(-0.25, 1.25),
                               fancybox=True)

            plt.subplot(212)
            ax2 = plt.subplot(212)
            for x_set_2 in x_list_2:
                for y_set_2 in y_list_2:
                    plt.plot(x_set_2,
                             y_set_2,
                             color=next(palette_dataset_2),
                             linewidth=0.75)
                    axes = plt.gca()
                    axes.set_ylim([0, 100])
                    axes.set_xlim([x_list_2[0][8], x_list_1[0][-1]])
                    plt.title(self.dataname_2.toPlainText())
                    box = ax2.get_position()
                    ax2.set_position(
                        [box.x0, box.y0, box.width * 0.75, box.height])
                    ax2.legend(title_list_2,
                               loc='upper left',
                               bbox_to_anchor=(-0.5, 2.65),
                               fancybox=True)
                    #bbox_to_anchor=(1.25, 1.15),
            plt.ylabel('Intensity %')
            if self.ccs_button_2.isChecked():
                plt.xlabel('CCS (' + '$\AA^2$' + ')')
            elif self.average_ccs_button_2.isChecked():
                plt.xlabel('CCS (' + '$\AA^2$' + ')')
            elif self.mz_button.isChecked():
                plt.xlabel('m/z')
            else:
                plt.xlabel('Time (ms)')
            sns.despine()
            plt.tight_layout()
            plt.savefig(self.double_dname_2 + '\\' + 'double_combined.png')
            pixmap = QPixmap(self.double_dname_2 + '\double_combined.png')
            self.graph_placement_2.setPixmap(pixmap)
            QApplication.processEvents()
            plt.clf()

        self.log_2.appendPlainText('Creating animation')
        QApplication.processEvents()

        self.progress_2 = self.progress_2 + 1
        self.progressBar_2.setValue(self.progress_2)

        image_list = []
        images = []

        for experiment in title_list_2:
            image_list.append('double_' + str(experiment) + '.png')

        for item in image_list:
            if item == ('Combined.png'):
                item.replace('Combined.png', '')

        for files in listdir(self.double_dname_2):
            for item in image_list:
                images.append(imageio.imread(self.double_dname_2 + '/' + item))

        imageio.mimsave(self.double_dname_2 + '/' + 'double_ATD.gif', images)
        self.progress_2 = self.progress_2 + 1

        gif = QMovie(self.double_dname_2 + '\double_ATD.gif')
        self.ATD_gif_2.setMovie(gif)
        gif.start()
        QApplication.processEvents()

        self.log_2.moveCursor(QtGui.QTextCursor.End)
        self.log_2.appendPlainText(
            'Programme completed, image files saved to ' + self.double_dname_2)
        self.progressBar_2.setValue(len(self.double_files_list_1) + 2)
        QApplication.processEvents()

        for item in self.block_function_list_double:
            item.setDisabled(False)

    ############################
    # TAB 3 BUTTON DEFINITIONS #
    ############################

    def av_ccs_checked(self):
        if self.av_CCS_button.isChecked():
            self.av_calibration_selector_1.setDisabled(False)
            self.av_calibration_selector_2.setDisabled(False)
            self.av_calibration_selector_3.setDisabled(False)
            self.av_ccs_z.setDisabled(False)
            self.av_ccs_mz.setDisabled(False)
        else:
            self.av_calibration_selector_1.setDisabled(True)
            self.av_calibration_selector_2.setDisabled(True)
            self.av_calibration_selector_3.setDisabled(True)
            self.av_ccs_z.setDisabled(True)
            self.av_ccs_mz.setDisabled(True)

    def av_directory_selector_1(self):
        dataFn = QtGui.QFileDialog.getExistingDirectory(self,
                                                        'Select Directory')
        self.log_3.moveCursor(QtGui.QTextCursor.End)
        self.log_3.appendPlainText('Using directory location ' + dataFn)
        QApplication.processEvents()
        self.av_dname_1 = str(dataFn)

        self.av_files_list_1 = []

        self.av_curdir_files_list_1 = []
        for files in listdir(self.av_dname_1):
            if files.endswith('.txt'):
                self.av_curdir_files_list_1.append(self.av_dname_1 + '\\' +
                                                   files)
                self.av_files_list_1.append(files)
                self.log_3.moveCursor(QtGui.QTextCursor.End)
                self.log_3.ensureCursorVisible()
                self.log_3.moveCursor(QtGui.QTextCursor.End)
                self.log_3.appendPlainText('Found file ' + str(files))
                QApplication.processEvents()
        self.progressBar.setMaximum(len(self.av_curdir_files_list_1))

        self.av_selector_2.setDisabled(False)

    def av_directory_selector_2(self):
        dataFn = QtGui.QFileDialog.getExistingDirectory(self,
                                                        'Select Directory')
        self.log_3.moveCursor(QtGui.QTextCursor.End)
        self.log_3.appendPlainText('Using directory location ' + dataFn)
        QApplication.processEvents()
        self.av_dname_2 = str(dataFn)

        self.av_files_list_2 = []
        self.av_curdir_files_list_2 = []
        for files in listdir(self.av_dname_2):
            #print(files)
            if files.endswith('.txt'):
                self.av_curdir_files_list_2.append(self.av_dname_2 + '\\' +
                                                   files)
                self.av_files_list_2.append(files)
                self.log_3.moveCursor(QtGui.QTextCursor.End)
                self.log_3.ensureCursorVisible()
                self.log_3.moveCursor(QtGui.QTextCursor.End)
                self.log_3.appendPlainText('Found file ' + str(files))
                QApplication.processEvents()
        self.progress = 0

        self.progressBar.setMaximum(
            len(self.av_curdir_files_list_1) + len(self.av_curdir_files_list_2))

        self.av_selector_3.setDisabled(False)

    def av_directory_selector_3(self):
        dataFn = QtGui.QFileDialog.getExistingDirectory(self,
                                                        'Select Directory')
        self.log_3.moveCursor(QtGui.QTextCursor.End)
        self.log_3.appendPlainText('Using directory location ' + dataFn)
        QApplication.processEvents()
        self.av_dname_3 = str(dataFn)

        self.av_files_list_3 = []
        self.av_curdir_files_list_3 = []
        for files in listdir(self.av_dname_3):
            #print(files)
            if files.endswith('.txt'):
                self.av_curdir_files_list_3.append(self.av_dname_3 + '\\' +
                                                   files)
                self.av_files_list_3.append(files)
                self.log_3.moveCursor(QtGui.QTextCursor.End)
                self.log_3.ensureCursorVisible()
                self.log_3.moveCursor(QtGui.QTextCursor.End)
                self.log_3.appendPlainText('Found file ' + str(files))
                QApplication.processEvents()
        self.progress = 0

        self.progressBar.setMaximum(
            len(self.av_curdir_files_list_1) +
            len(self.av_curdir_files_list_2) + len(self.av_curdir_files_list_3))

    def av_calibration_file_selection_1(self):
        dataFn = QtGui.QFileDialog.getOpenFileName(self, 'Select File',
                                                   '*.calibration')
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        self.log_3.moveCursor(QtGui.QTextCursor.End)
        self.log_3.appendPlainText('Found calibration file ' + dataFn)
        QApplication.processEvents()
        self.objects = []
        with (open(dataFn, "rb")) as openfile:
            while True:
                try:
                    self.objects.append(pickle.load(openfile))
                except EOFError:
                    break
        self.av_cal_1 = self.objects[0]

    def av_calibration_file_selection_2(self):
        dataFn = QtGui.QFileDialog.getOpenFileName(self, 'Select File',
                                                   '*.calibration')
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        self.log_3.moveCursor(QtGui.QTextCursor.End)
        self.log_3.appendPlainText('Found calibration file ' + dataFn)
        QApplication.processEvents()
        self.objects = []
        with (open(dataFn, "rb")) as openfile:
            while True:
                try:
                    self.objects.append(pickle.load(openfile))
                except EOFError:
                    break
        self.av_cal_2 = self.objects[0]

    def av_calibration_file_selection_3(self):
        dataFn = QtGui.QFileDialog.getOpenFileName(self, 'Select File',
                                                   '*.calibration')
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        self.log_3.moveCursor(QtGui.QTextCursor.End)
        self.log_3.appendPlainText('Found calibration file ' + dataFn)
        QApplication.processEvents()
        self.objects = []
        with (open(dataFn, "rb")) as openfile:
            while True:
                try:
                    self.objects.append(pickle.load(openfile))
                except EOFError:
                    break
        self.av_cal_3 = self.objects[0]

    def av_calculate_clicked(self):
        plt.clf()
        self.progress_3 = 0
        self.progressBar_4.setValue(self.progress)
        QApplication.processEvents()

        if self.ccs_button.isChecked():
            self.log.moveCursor(QtGui.QTextCursor.End)
            self.log.appendPlainText(
                'Converting arrival time to CCS using selected calibration files'
            )
            QApplication.processEvents()

        time_1 = []
        time_2 = []
        time_3 = []

        if len(self.av_curdir_files_list_3) == 0:
            for file_n_1, file_n_2 in zip(self.av_curdir_files_list_1,
                                          self.av_curdir_files_list_2):
                if len(self.av_curdir_files_list_1) != len(
                        self.av_curdir_files_list_2):
                    self.log_3.moveCursor(QtGui.QTextCursor.End)
                    self.log_3.appendPlainText(
                        'Number of files is not equal, cannot proceed')
                    QApplication.processEvents()

                else:
                    self.log_3.moveCursor(QtGui.QTextCursor.End)
                    self.log_3.appendPlainText(
                        'Number of files is equal, proceeding')
                    QApplication.processEvents()

                    with open(file_n_1, 'r') as file_1:
                        reader = csv.reader(file_1)
                        time_1 = []
                        intensity_1 = []
                        data_list_1 = list(
                            zip(*(line.strip().split('\t') for line in file_1)))
                        for item in tuple(data_list_1[0]):
                            time_1.append(float(item))
                        for item in tuple(data_list_1[1]):
                            intensity_1.append(float(item))

                    if self.av_CCS_button.isChecked():
                        ccs_list_1 = []
                        for item in time_1:
                            new_item = self.av_cal_1._calculateOmega(
                                item, float(self.av_ccs_mz.toPlainText()),
                                float(self.av_ccs_z.toPlainText()))
                            if math.isnan(new_item) == True:
                                new_item = 0
                            ccs_list_1.append(new_item)
                        time_1 = ccs_list_1

                    with open(file_n_2, 'r') as file_2:
                        reader = csv.reader(file_2)
                        time_2 = []
                        intensity_2 = []
                        data_list_2 = list(
                            zip(*(line.strip().split('\t') for line in file_2)))
                        for item in tuple(data_list_2[0]):
                            time_2.append(float(item))
                        for item in tuple(data_list_2[1]):
                            intensity_2.append(float(item))

                    if self.av_CCS_button.isChecked():
                        ccs_list_2 = []
                        for item in time_2:
                            new_item = self.av_cal_2._calculateOmega(
                                item, float(self.av_ccs_mz.toPlainText()),
                                float(self.av_ccs_z.toPlainText()))
                            if math.isnan(new_item) == True:
                                new_item = 0
                            ccs_list_2.append(new_item)
                        time_2 = ccs_list_2

                    if len(time_1) == len(time_2):
                        pc_intensity_1 = []
                        pc_intensity_2 = []
                        for item in intensity_1:
                            pc_intensity_1.append(
                                (100 / max(intensity_1) * float(item)))
                        for item in intensity_2:
                            pc_intensity_2.append(
                                (100 / max(intensity_2) * float(item)))

                    av_time = []

                    av_intensity = []

                    av_sd = []

                    for no in range(0, len(intensity_1)):
                        av_y = [pc_intensity_1[no], pc_intensity_2[no]]
                        av_intensity.append(np.nanmean(av_y))
                        av_sd.append(np.nanstd(av_y))

                    for no in range(0, len(time_1)):
                        av_x = [time_1[no], time_2[no]]
                        av_time.append(np.nanmean(av_x))
                        print((np.nanstd(av_x)))

                    sns.despine()
                    plt.plot(time_1, pc_intensity_1, 'b')
                    plt.plot(time_2, pc_intensity_2, 'r')
                    # plt.plot(time_3, pc_intensity_3, 'g')
                    axes = plt.gca()
                    axes.set_ylim([0, 100])
                    plt.savefig(self.av_dname_1 + '\\subdir\\' + 'av_' +
                                str([self.progress_3]) + '.png')
                    # fig.clf()
                    # plt.show()
                    plt.clf()

                self.log_3.appendPlainText(
                    'Writing averaged data for ' +
                    str(self.av_files_list_1[self.progress_3]) + ' and ' +
                    str(self.av_files_list_2[self.progress_3]) +
                    ' to new subdirectory')
                self.log_3.moveCursor(QtGui.QTextCursor.End)
                QApplication.processEvents()
                with open(
                        self.av_dname_1 + '\\subdir\\' + 'av_' +
                        str(self.av_files_list_1[self.progress_3]),
                        'w') as smoothed_output:
                    writer = csv.writer(smoothed_output,
                                        delimiter='\t',
                                        lineterminator='\n')
                    writing_list = []
                    for (time, ints, sd) in zip(av_time, av_intensity, av_sd):
                        writing_list = [time, ints, sd]
                        writer.writerow(writing_list)

                self.progress_3 = self.progress_3 + 1

        else:
            # print(len(self.av_curdir_files_list_1))
            # print(len(self.av_curdir_files_list_2))
            # print(len(self.av_curdir_files_list_3))
            for file_n_1, file_n_2, file_n_3 in zip(
                    self.av_curdir_files_list_1, self.av_curdir_files_list_2,
                    self.av_curdir_files_list_3):
                if len(self.av_curdir_files_list_1) != len(
                        self.av_curdir_files_list_2):
                    self.log_3.moveCursor(QtGui.QTextCursor.End)
                    self.log_3.appendPlainText(
                        'Number of files is not equal, cannot proceed')
                    QApplication.processEvents()
                if len(self.av_curdir_files_list_1) != len(
                        self.av_curdir_files_list_3):
                    self.log_3.moveCursor(QtGui.QTextCursor.End)
                    self.log_3.appendPlainText(
                        'Number of files is not equal, cannot proceed')
                    QApplication.processEvents()
                if len(self.av_curdir_files_list_1) == len(
                        self.av_curdir_files_list_2) == len(
                            self.av_curdir_files_list_3):
                    # print('files equal, proceed')
                    self.log_3.moveCursor(QtGui.QTextCursor.End)
                    self.log_3.appendPlainText(
                        'Number of files is equal, proceeding')
                    QApplication.processEvents()

                    with open(file_n_1, 'r') as file_1:
                        reader = csv.reader(file_1)
                        time_1 = []
                        intensity_1 = []
                        data_list_1 = list(
                            zip(*(line.strip().split('\t') for line in file_1)))
                        for item in tuple(data_list_1[0]):
                            time_1.append(float(item))
                        for item in tuple(data_list_1[1]):
                            intensity_1.append(float(item))

                    if self.av_CCS_button.isChecked():
                        ccs_list_1 = []
                        for item in time_1:
                            new_item = self.av_cal_1._calculateOmega(
                                item, float(self.av_ccs_mz.toPlainText()),
                                float(self.av_ccs_z.toPlainText()))
                            if math.isnan(new_item) == True:
                                new_item = 0
                            ccs_list_1.append(new_item)
                        time_1 = ccs_list_1

                    with open(file_n_2, 'r') as file_2:
                        reader = csv.reader(file_2)
                        time_2 = []
                        intensity_2 = []
                        data_list_2 = list(
                            zip(*(line.strip().split('\t') for line in file_2)))
                        for item in tuple(data_list_2[0]):
                            time_2.append(float(item))
                        for item in tuple(data_list_2[1]):
                            intensity_2.append(float(item))

                    if self.av_CCS_button.isChecked():
                        ccs_list_2 = []
                        for item in time_2:
                            new_item = self.av_cal_2._calculateOmega(
                                item, float(self.av_ccs_mz.toPlainText()),
                                float(self.av_ccs_z.toPlainText()))
                            if math.isnan(new_item) == True:
                                new_item = 0
                            ccs_list_2.append(new_item)
                        time_2 = ccs_list_2

                    with open(file_n_3, 'r') as file_3:
                        reader = csv.reader(file_3)
                        time_3 = []
                        intensity_3 = []
                        data_list_3 = list(
                            zip(*(line.strip().split('\t') for line in file_3)))
                        for item in tuple(data_list_3[0]):
                            time_3.append(float(item))
                        for item in tuple(data_list_3[1]):
                            intensity_3.append(float(item))

                    if self.av_CCS_button.isChecked():
                        ccs_list_3 = []
                        for item in time_3:
                            new_item = self.av_cal_3._calculateOmega(
                                item, float(self.av_ccs_mz.toPlainText()),
                                float(self.av_ccs_z.toPlainText()))
                            if math.isnan(new_item) == True:
                                new_item = 0
                            ccs_list_3.append(new_item)
                        time_3 = ccs_list_3

                    if len(time_1) == len(time_2) and len(time_1) == len(
                            time_3):
                        pc_intensity_1 = []
                        pc_intensity_2 = []
                        pc_intensity_3 = []
                        for item in intensity_1:
                            pc_intensity_1.append(
                                (100 / max(intensity_1) * float(item)))
                        for item in intensity_2:
                            pc_intensity_2.append(
                                (100 / max(intensity_2) * float(item)))
                        for item in intensity_3:
                            pc_intensity_3.append(
                                (100 / max(intensity_3) * float(item)))

                    av_time = []

                    av_intensity = []

                    av_sd = []

                    for no in range(0, len(intensity_1)):
                        av_y = [
                            pc_intensity_1[no], pc_intensity_2[no],
                            pc_intensity_3[no]
                        ]
                        av_intensity.append(np.nanmean(av_y))
                        av_sd.append(np.nanstd(av_y))

                    for no in range(0, len(time_1)):
                        av_x = [time_1[no], time_2[no], time_3[no]]
                        av_time.append(np.nanmean(av_x))
                        print((np.nanstd(av_x)))

                    sns.despine()
                    plt.plot(time_1, pc_intensity_1, 'b')
                    plt.plot(time_2, pc_intensity_2, 'r')
                    plt.plot(time_3, pc_intensity_3, 'g')
                    axes = plt.gca()
                    axes.set_ylim([0, 100])
                    plt.savefig(self.av_dname_1 + '\\subdir\\' + 'av_' +
                                str([self.progress_3]) + '.png')
                    # fig.clf()
                    # plt.show()
                    plt.clf()

                    self.log_3.appendPlainText(
                        'Writing averaged data for ' +
                        str(self.av_files_list_1[self.progress_3]) + ', ' +
                        str(self.av_files_list_2[self.progress_3]) + ' and ' +
                        str(self.av_files_list_3[self.progress_3]) +
                        ' to new subdirectory')
                    self.log_3.moveCursor(QtGui.QTextCursor.End)
                    QApplication.processEvents()
                    with open(
                            self.av_dname_1 + '\\subdir\\' + 'av_' +
                            str(self.av_files_list_1[self.progress_3]),
                            'w') as smoothed_output:
                        writer = csv.writer(smoothed_output,
                                            delimiter='\t',
                                            lineterminator='\n')
                        writing_list = []
                        for (time, ints, sd) in zip(av_time, av_intensity,
                                                    av_sd):
                            writing_list = [time, ints, sd]

                            writer.writerow(writing_list)

                # else:
                #     self.log_3.moveCursor(QtGui.QTextCursor.End)
                #     self.log_3.appendPlainText('Number of files is equal, proceeding')
                #     QApplication.processEvents()

                self.progress_3 = self.progress_3 + 1
            # self.progress_3 = self.progress_3 + 1


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
