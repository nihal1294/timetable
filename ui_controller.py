from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QDialog, QMessageBox
from PyQt5 import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

import sys
import pickle
import tt
import os
from collections import OrderedDict
import json
import time
import traceback
import worddoc
import xlrd
import logging

from window import Ui_window
from window2 import Ui_window2
from window3 import Ui_window3
from window4 import Ui_window4
from window5 import Ui_window5
from elective_window import Ui_elective_window
from year_window import Ui_year_window
from about_window import Ui_aboutWindow


class subject:
	def __init__(self, name, short_name = '', credits = 0, lab = False, subcode = ''):
		if short_name == '': # if both names are provided together in name
			both_names = name
			self.name, self.short_name = both_names.split(' - ')
		else: # short name is provided separately
			self.name = name
			self.short_name = short_name
		self.credits = credits
		self.lab = lab
		self.subcode = subcode

	@property
	def both_names(self):
		both_names = self.name + ' - ' + self.short_name
		return both_names

	def __eq__(self, obj):
		return self.name == obj.name and self.short_name == obj.short_name
		
	def __repr__(self):
		return 'subject({}, {}, {}, {}, {})'.format(self.name.__repr__(), self.short_name.__repr__(), self.credits, self.lab, self.subcode.__repr__()) 

	def __hash__(self):
		return self.name.__hash__()


class faculty_class:
	def __init__(self, name, title = '', designation = ''):
		if title == '':
			name = name.split(' ')
			if len(name) > 1:
				title = name[0]
				name = ' '.join(name[1:])
			else:
				name = name[0]
		self.name = name
		self.title = title
		self.designation = designation

	def __repr__(self):
		return 'faculty_class({}, {}, {})'.format(self.name.__repr__(), self.title.__repr__(), self.designation.__repr__())

	def __str__(self):
		return self.title + ' ' + self.name

	def __eq__(self, string):
		if str(string) == str(self) or string == self.name:
			return True
		else:
			return False

	def __lt__(self, obj):
		return self.name < obj.name

	def __hash__(self):
		return self.name.__hash__()


'''class logger:
	def __init__(self, logfilename):
		self.terminal = sys.stdout
		self.err = sys.stderr
		self.log = open(logfilename, 'w')
		sys.stdout = self
		sys.stderr = self

	def __del__(self):
		self.log.close()

	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)
		self.flush()

	def flush(self):
		self.log.flush()
		self.terminal.flush()
		pass
'''


#new singular class implementing QStackedLayout
class ParentWindow(QMainWindow):

	def __init__(self, parent = None):
		super(ParentWindow,self).__init__(parent)
		#self.central_window = QMainWindow()
		self.layered_windows = QStackedLayout()

		logger.info('********************************************************************************************************************')
		logger.info('*                                           TIMETABLE GENERATOR                                                    *')
		logger.info('*                                                                                                                  *')
		logger.info('*                                                   BY:                                                            *')
		logger.info('*                                               Nihal Rao I                                                        *')
		logger.info('*                                             Sanjan S Poojari                                                     *')
		logger.info('*                                             Shishir Upadhya                                                      *')
		logger.info('*                              Department of Computer Science & Engineering                                        *')
		logger.info('*                                                                                                                  *')
		logger.info('*                                                  FOR:                                                            *')
		logger.info('*                                   NMAM Institute of Technology, Nitte                                            *')
		logger.info('********************************************************************************************************************')
		logger.info('Current Directory: %s', os.path.realpath(os.curdir))

		#code to resize the main window ...does NOT resize the widgets !
		self.screen_width = QDesktopWidget().screenGeometry().width()
		self.screen_height = QDesktopWidget().screenGeometry().height()
		logger.info('Current screen resolution: %s %s', self.screen_width, self.screen_height)
		#print('current screen res: ',self.screen_width, self.screen_height)
		#self.adjusted_width = (screen_width/1366)
		#self.adjusted_height = (screen_height/768)
		self.resize_ratio = 0.7 #70% resizing ... need a more accurate resize ratio than this.
		logger.info('Resize ratio: %s', self.resize_ratio)
		#print('resize ratio: ',self.resize_ratio)

		self.setup_year_window()
		self.setup_first_window()
		self.setup_second_window()
		self.setup_third_window()
		self.setup_fourth_window()
		self.setup_fifth_window()

		self.layered_windows.addWidget(self.YearWindow)
		self.layered_windows.addWidget(self.FirstWindow)
		self.layered_windows.addWidget(self.SecondWindow)
		self.layered_windows.addWidget(self.ThirdWindow)
		self.layered_windows.addWidget(self.FourthWindow)
		self.layered_windows.addWidget(self.FifthWindow)

		self.systemtray_icon = Qt.QSystemTrayIcon(Qt.QIcon('icons/favicon.ico'))
		self.systemtray_icon.show()

		app.aboutToQuit.connect(lambda: self.systemtray_icon.hide())
		self.YearWindow.closeEvent = self.finish_btn_event
		self.FirstWindow.closeEvent = self.finish_btn_event
		self.SecondWindow.closeEvent = self.finish_btn_event
		self.ThirdWindow.closeEvent = self.finish_btn_event
		self.FourthWindow.closeEvent = self.finish_btn_event
		self.FifthWindow.closeEvent = self.finish_btn_event

		self.current_window = ''

		#self.central_window.setLayout(self.layered_windows)
		#self.setCentralWidget(self.central_window)

		#intended original size for the app = (920, 500)
		#self.resize(916*self.adjusted_width, 460*self.adjusted_height)
		#self.resize()

	# setup year input window
	def setup_year_window(self):
		#YEAR WINDOW - ACADEMIC YEAR INPUT
		logger.debug('Initializing and setting up year window')
		self.YearWindow = QDialog()
		self.ui_year = Ui_year_window()
		self.ui_year.setupUi(self.YearWindow)

		months = ['January','February','March','April','May','June','July','August','September','October','November','December']
		for m in months:
			self.ui_year.startMonth_combobox.addItem(m)
			self.ui_year.endMonth_combobox.addItem(m)

		depts = ['Biotechnology', 'Civil Engineering', 'Computer Science & Engineering', 'Electronics & Communications Engineering',\
		 'Electrical & Electronics Engineering', 'Information Science & Engineering', 'Mechanical Engineering']
		for d in depts:
			self.ui_year.dept_combobox.addItem(d)

		self.ui_year.startYear_dateedit.setDate(QtCore.QDate.currentDate())
		#self.ui_year.startYear_dateedit.setDate(QtCore.QDate.fromString('2015', 'yyyy'))
		self.ui_year.endYear_dateedit.setDate(QtCore.QDate.currentDate())

		self.ui_year.continueBtn.clicked.connect(self.continue_btn_event)
		self.ui_year.skipBtn.clicked.connect(self.next_btn_event)

		self.startMonth = ''
		self.startYear = ''
		self.endMonth = ''
		self.endYear = ''
		self.department = ''

	# setup first input window
	def setup_first_window(self):
		#FIRST WINDOW - List Entry
		logger.debug('Initializing and setting up first window')
		self.FirstWindow = QMainWindow()
		self.ui = Ui_window()
		self.ui.setupUi(self.FirstWindow)
		#self.ui.input_list.resize(self.adjusted_width*self.ui.input_list.width(), self.adjusted_height*self.ui.input_list.height())

		self.ui.semester_combobox.setEnabled(False)
		self.ui.label_3.setEnabled(False)
		self.ui.sections_spinbox.setEnabled(False)
		self.ui.label_4.setEnabled(False)
		self.ui.input_textbox.setEnabled(False)
		self.ui.label_5.setEnabled(False)
		self.ui.title_combobox.setEnabled(False)
		self.ui.desig_combobox.setEnabled(False)
		self.ui.label_9.setEnabled(False)
		self.ui.subject_code_input.setEnabled(False)
		self.ui.label_8.setEnabled(False)
		self.ui.subject_short_input.setEnabled(False)
		self.ui.label_6.setEnabled(False)
		self.ui.lab_checkbox.setEnabled(False)
		self.ui.credits_spinbox.setEnabled(False)
		self.ui.label_7.setEnabled(False)
		self.ui.electiveBtn.setEnabled(False)
		self.ui.line.setEnabled(False)
		self.ui.line_2.setEnabled(False)
		self.ui.addBtn.clicked.connect(self.add_btn_event)
		self.ui.electiveBtn.clicked.connect(self.elective_btn_event)
		self.ui.removeBtn.clicked.connect(self.remove_btn_event)
		self.ui.nextBtn.clicked.connect(self.next_btn_event)
		self.ui.sections_spinbox.valueChanged.connect(self.section_spinbox_event)
		self.ui.inputType_combobox.addItem("Faculty")
		self.ui.inputType_combobox.addItem("Subjects")
		self.ui.inputType_combobox.setCurrentIndex(-1)
		self.ui.desig_combobox.setCurrentIndex(-1)
		self.ui.title_combobox.setCurrentIndex(-1)
		self.ui.inputType_combobox.activated[str].connect(self.inputType_combobox_event)
		self.ui.semester_combobox.activated[str].connect(self.semester_combobox_event)
		self.ui.input_textbox.returnPressed.connect(self.ui.addBtn.click)
		self.ui.subject_short_input.returnPressed.connect(self.ui.addBtn.click)
		self.ui.input_list.itemClicked.connect(self.handle_listclick_event)
		self.ui.addBtn.setAutoDefault(True)
		self.sem_list = ['III', 'IV', 'V', 'VI', 'VII', 'VIII']
		for sem in self.sem_list:
			self.ui.semester_combobox.addItem(sem)
		self.ui.semester_combobox.setCurrentIndex(-1)
		self.cur_open_filename = ''
		self.faculty_list_value = []
		self.subjects = OrderedDict()
		self.subs = dict() # store link between subject short name and its object
		self.num_sections = dict()
		for sem in self.sem_list:
			self.subjects[sem] = []
			self.num_sections[sem] = 0
		self.inputType = ""
		self.text = ""
		self.sem = ""
		self.row = self.ui.input_list.selectedItems()
		self.titles_list = ['Mr.', 'Ms.', 'Mrs.', 'Dr.', 'Prof.' ]
		for value in self.titles_list:
			self.ui.title_combobox.addItem(value)
		self.desig_list = ['Assistant Professor', 'Professor', 'Associate Professor', 'Head of Department', 'Principal']
		for val in self.desig_list:
			self.ui.desig_combobox.addItem(val)

		self.FirstWindow.resize(self.screen_width*self.resize_ratio, self.screen_height*self.resize_ratio)
		self.FirstWindow.updateGeometry()

		self.ui.menubar.triggered[QtWidgets.QAction].connect(self.filemenuevent)

		#setting up elective window and about window during first window setup
		self.setup_elective_window()
		self.setup_about_window()

	#setup elective input window
	def setup_elective_window(self):
		#ELECTIVE WINDOW - Elective Entry
		logger.debug('Initializing and setting up elective window')
		self.ElectiveWindow = QWidget()
		self.ui_elec = Ui_elective_window()
		self.ui_elec.setupUi(self.ElectiveWindow)

		self.ui_elec.semester_combobox.setEnabled(True)
		self.ui_elec.elective_spinbox.setEnabled(False)
		self.ui_elec.elective_spinbox.setValue(0)
		self.ui_elec.label_4.setEnabled(False)
		self.ui_elec.electiveGroup_combobox.setEnabled(False)
		self.ui_elec.label_3.setEnabled(False)
		self.ui_elec.elective_input_textbox.setEnabled(False)
		self.ui_elec.label_5.setEnabled(False)
		self.ui_elec.elective_code_input.setEnabled(False)
		self.ui_elec.label_8.setEnabled(False)
		self.ui_elec.elective_short_input.setEnabled(False)
		self.ui_elec.label_6.setEnabled(False)
		self.ui_elec.credits_spinbox.setEnabled(False)
		self.ui_elec.label_7.setEnabled(False)
		self.ui_elec.lab_checkbox.setEnabled(False)
		self.ui_elec.line.setEnabled(False)
		self.ui_elec.line_2.setEnabled(False)
		
		self.electives = OrderedDict()
		for sem in self.sem_list:
			self.ui_elec.semester_combobox.addItem(sem)
			self.electives[sem] = dict()
		self.ui_elec.semester_combobox.setCurrentIndex(-1)

		self.ui_elec.semester_combobox.activated[str].connect(self.semester_combobox_elective_event)
		self.ui_elec.elective_spinbox.valueChanged.connect(self.elective_spinbox_event)
		self.ui_elec.elective_short_input.returnPressed.connect(self.ui_elec.addBtn.click)
		self.ui_elec.elective_input_textbox.returnPressed.connect(self.ui_elec.addBtn.click)
		self.ui_elec.backBtn.clicked.connect(self.elective_btn_event)
		self.ui_elec.addBtn.setAutoDefault(True)
		self.ui_elec.addBtn.clicked.connect(self.add_btn_elective_event)
		self.ui_elec.elective_list.itemClicked.connect(self.handle_listclick_elective_event)
		self.ui_elec.removeBtn.clicked.connect(self.remove_btn_elective_event)
		self.ui_elec.electiveGroup_combobox.activated[str].connect(self.electivegroup_combobox_event)
		self.ui_elec.resetBtn.clicked.connect(self.reset_Btn_event)

	#setup assignment input window
	def setup_second_window(self):
		#SECOND WINDOW - Faculty assignment
		logger.debug('Initializing and setting up second window')
		self.SecondWindow = QMainWindow()
		self.ui2 = Ui_window2()
		self.ui2.setupUi(self.SecondWindow)

		self.ui2.faculty_combobox.setCurrentIndex(-1)
		self.ui2.semester_combobox.setCurrentIndex(-1)
		self.ui2.section_combobox.setCurrentIndex(-1)
		self.ui2.subject_combobox.setCurrentIndex(-1)

		self.ui2.nextBtn.clicked.connect(self.next_btn_event)
		self.ui2.backBtn.clicked.connect(self.back_btn_event)
		self.ui2.semester_combobox.activated[str].connect(self.semester_combobox2_event)
		self.ui2.assignBtn.clicked.connect(self.assign_btn_event)
		self.ui2.undoBtn.clicked.connect(self.undo_btn_event)
		self.ui2.section_combobox.activated[str].connect(self.section_combobox2_event)
		self.ui2.faculty_combobox.activated[str].connect(self.faculty_combobox2_event)

		self.sections = dict()
		self.subjects_assigned = dict() # this dict will be like {'III': {'A': [subjects], 'B': [subjects]}, 'IV': {} ..etc}
		self.faculty_subjects = dict() # stores subjects assigned to each faculty

		self.SecondWindow.resize(self.screen_width*self.resize_ratio, self.screen_height*self.resize_ratio)
		self.SecondWindow.updateGeometry()

		self.ui2.menubar.triggered[QtWidgets.QAction].connect(self.filemenuevent)

	#setup subject constraint window
	def setup_third_window(self):
		#THIRD WINDOW - Subject Constraints
		logger.debug('Initializing and setting up third window')
		self.ThirdWindow = QMainWindow()
		self.ui3 = Ui_window3()
		self.ui3.setupUi(self.ThirdWindow)

		self.ui3.section_combobox.setCurrentIndex(-1)
		self.ui3.slotType_combobox.setCurrentIndex(-1)
		self.ui3.nextBtn.clicked.connect(self.next_btn_event)
		self.ui3.backBtn.clicked.connect(self.back_btn_event)
		self.ui3.semester_combobox.activated[str].connect(self.semester_combobox3_event)
		self.ui3.section_combobox.activated[str].connect(self.section_combobox3_event)
		self.ui3.slotType_combobox.activated[str].connect(self.slotType_combobox3_event)
		self.ui3.subject_table.cellClicked.connect(self.cellClick3_event)

		for sem in self.sem_list:
			self.ui3.semester_combobox.addItem(sem)
		self.ui3.semester_combobox.setCurrentIndex(-1)
		self.section_fixed_slots = dict()

		self.ThirdWindow.resize(self.screen_width*self.resize_ratio, self.screen_height*self.resize_ratio)
		self.ThirdWindow.updateGeometry()

		self.ui3.menubar.triggered[QtWidgets.QAction].connect(self.filemenuevent)

	#setup faculty constraint window
	def setup_fourth_window(self):
		#FOURTH WINDOW - Faculty Constraints
		logger.debug('Initializing and setting up fourth window')
		self.FourthWindow = QMainWindow()
		self.ui4 = Ui_window4()
		self.ui4.setupUi(self.FourthWindow)

		self.ui4.faculty_combobox.activated[str].connect(self.faculty_combobox4_event)
		self.ui4.faculty_table.cellClicked.connect(self.cellClick4_event)
		self.ui4.generateBtn.clicked.connect(self.next_btn_event)	
		self.ui4.backBtn.clicked.connect(self.back_btn_event)
		self.ui4.generateBtn.clicked.connect(self.generate_event)

		self.faculty_fixed_slots = dict()
		
		self.ui4.faculty_combobox.setCurrentIndex(-1)

		self.FourthWindow.resize(self.screen_width*self.resize_ratio, self.screen_height*self.resize_ratio)
		self.FourthWindow.updateGeometry()

		self.ui4.menubar.triggered[QtWidgets.QAction].connect(self.filemenuevent)

	#setup timetable display window
	def setup_fifth_window(self):
		#FIFTH WINDOW - Generated timetable
		logger.debug('Initializing and setting up fifth window')
		self.FifthWindow = QMainWindow()
		self.ui5 = Ui_window5()
		self.ui5.setupUi(self.FifthWindow)

		self.ui5.finishBtn.clicked.connect(lambda: self.FifthWindow.close())
		self.ui5.backBtn.clicked.connect(self.back_btn_event)
		self.ui5.printBtn.clicked.connect(self.print_btn_event)
		self.ui5.inputType_combobox.activated[str].connect(self.inputType_combobox_event)
		self.ui5.semester_combobox.activated[str].connect(self.semester_combobox5_event)
		self.ui5.section_combobox.activated[str].connect(self.section_combobox5_event)
		self.ui5.faculty_combobox.activated[str].connect(self.faculty_combobox5_event)
		self.ui5.generated_table.cellClicked.connect(self.cellClick5_event)
		self.ui5.roomno_textbox.textEdited.connect(self.roomno_textbox_event)
		self.ui5.faculty_combobox.setEnabled(False)
		self.ui5.label_5.setEnabled(False)
		self.ui5.inputType_combobox.addItem('Students')
		self.ui5.inputType_combobox.addItem('Faculty')
		self.ui5.inputType_combobox.setCurrentIndex(-1)
		self.ui5.semester_combobox.setCurrentIndex(-1)
		self.ui5.section_combobox.setCurrentIndex(-1)
		self.ui5.faculty_combobox.setCurrentIndex(-1)

		self.timetables = ''
		self.faculty_timetables = ''
		self.selected_cell = ()

		self.FifthWindow.resize(self.screen_width*self.resize_ratio, self.screen_height*self.resize_ratio)
		self.FifthWindow.updateGeometry()

		self.ui5.menubar.triggered[QtWidgets.QAction].connect(self.filemenuevent)

	#setup about window	
	def setup_about_window(self):
		# ABOUT WINDOW
		logger.debug('Initializing and setting up about window')
		self.AboutWindow = QDialog()
		self.ui_about = Ui_aboutWindow()
		self.ui_about.setupUi(self.AboutWindow)

		self.ui_about.logoLabel.setPixmap(QtGui.QPixmap('icons/nittelogo.png'))

		self.ui_about.closeBtn.clicked.connect(self.AboutWindow.hide)


	# year window functions
	def continue_btn_event(self):
		self.startMonth = self.ui_year.startMonth_combobox.currentText()
		self.startYear = self.ui_year.startYear_dateedit.date().year()
		self.endMonth = self.ui_year.endMonth_combobox.currentText()
		self.endYear = self.ui_year.endYear_dateedit.date().year()
		self.department = self.ui_year.dept_combobox.currentText()

		logger.info('Academic year: %s %s %s %s Department: %s', self.startMonth, self.startYear, self.endMonth, self.endYear, self.department)
		#print(self.startMonth, self.startYear, self.endMonth, self.endYear, self.department)

		self.next_btn_event()

	def reset_year_window(self):
		logger.debug('Resetting Year Window')
		self.ui_year.startYear_dateedit.setDate(QtCore.QDate.fromString(str(self.startYear), 'yyyy'))
		self.ui_year.endYear_dateedit.setDate(QtCore.QDate.fromString(str(self.endYear), 'yyyy'))
		i = self.ui_year.startMonth_combobox.findText(self.startMonth)
		if i >= 0:
			self.ui_year.startMonth_combobox.setCurrentIndex(i)
		i = self.ui_year.endMonth_combobox.findText(self.endMonth)
		if i >= 0:
			self.ui_year.endMonth_combobox.setCurrentIndex(i)
		i = self.ui_year.dept_combobox.findText(self.department)
		if i >= 0:
			self.ui_year.dept_combobox.setCurrentIndex(i)


	# first form functions
	def inputType_combobox_event(self):    #function for input type combobox in first form
		if self.FirstWindow.isVisible():
			self.row = []

			self.inputType = self.ui.inputType_combobox.currentText()
			logger.info('Input type: %s', self.inputType)
			#print(self.inputType)
			if self.row:
					del self.row[0]
			logger.info('Selected row in list: %s', self.row)
			#print(self.row)
			#print(dir(self.ui.inputType_combobox))
			if self.inputType == "Faculty":
				self.ui.semester_combobox.setEnabled(False)
				self.ui.label_3.setEnabled(False)
				self.ui.sections_spinbox.setEnabled(False)
				self.ui.label_4.setEnabled(False)
				self.ui.title_combobox.setEnabled(True)
				self.ui.input_textbox.setEnabled(True)
				self.ui.label_5.setEnabled(True)
				self.ui.desig_combobox.setEnabled(True)
				self.ui.label_9.setEnabled(True)
				self.ui.subject_code_input.setEnabled(False)
				self.ui.label_8.setEnabled(False)
				self.ui.subject_short_input.setEnabled(False)
				self.ui.label_6.setEnabled(False)
				self.ui.credits_spinbox.setEnabled(False)
				self.ui.label_7.setEnabled(False)
				self.ui.lab_checkbox.setEnabled(False)
				self.ui.line.setEnabled(True)
				self.ui.line_2.setEnabled(False)
				self.ui.electiveBtn.setEnabled(False)
				self.ui.desig_combobox.setCurrentIndex(-1)
				self.ui.title_combobox.setCurrentIndex(-1)
				self.ui.input_textbox.clear()
				self.ui.input_textbox.setPlaceholderText("Please enter faculty name")
				
				self.ui.input_list.clear()
				for values in self.faculty_list_value:
					self.ui.input_list.addItem(values.name)
			else: # input type subjects
				self.ui.semester_combobox.setEnabled(True)
				self.ui.label_3.setEnabled(True)
				self.ui.sections_spinbox.setEnabled(True)
				self.ui.label_4.setEnabled(True)
				self.ui.title_combobox.setEnabled(False)
				self.ui.input_textbox.setEnabled(True)
				self.ui.label_5.setEnabled(True)
				self.ui.desig_combobox.setEnabled(False)
				self.ui.label_9.setEnabled(False)
				self.ui.subject_code_input.setEnabled(True)
				self.ui.subject_code_input.clear()
				self.ui.label_8.setEnabled(True)
				self.ui.subject_short_input.setEnabled(True)
				self.ui.subject_short_input.clear()
				self.ui.label_6.setEnabled(True)
				self.ui.credits_spinbox.setEnabled(True)
				self.ui.credits_spinbox.setValue(1)
				self.ui.label_7.setEnabled(True)
				self.ui.lab_checkbox.setEnabled(True)
				self.ui.lab_checkbox.setChecked(False)
				self.ui.line.setEnabled(True)
				self.ui.line_2.setEnabled(True)
				self.ui.input_textbox.clear()
				self.ui.input_textbox.setPlaceholderText("Please enter subject name")
				self.ui.electiveBtn.setEnabled(True)
				sem = self.ui.semester_combobox.currentText()
				self.ui.input_list.clear()
				if sem in self.subjects:
					for subject in self.subjects[sem]:
						self.ui.input_list.addItem(subject.both_names)

		#same method is used for fifth window. Do This in other combobox for other windows
		if self.FifthWindow.isVisible():
			self.inputType = self.ui5.inputType_combobox.currentText()
			logger.info(self.inputType)
			#print(self.inputType)
			if self.inputType == "Faculty":
				self.ui5.semester_combobox.setCurrentIndex(-1)
				self.ui5.section_combobox.setCurrentIndex(-1)
				self.ui5.semester_combobox.setEnabled(False)
				self.ui5.label_3.setEnabled(False)
				self.ui5.section_combobox.setEnabled(False)
				self.ui5.label_4.setEnabled(False)
				self.ui5.faculty_combobox.setEnabled(True)
				self.ui5.label_5.setEnabled(True)
				self.ui5.roomno_textbox.setEnabled(False)
				self.ui5.label_6.setEnabled(False)
				self.ui5.faculty_combobox.setCurrentIndex(-1)
				self.ui5.generated_table.clearContents()

			else:	#input type subjects
				self.ui5.semester_combobox.clear()
				for sem in self.sem_list:
					self.ui5.semester_combobox.addItem(sem)
				self.ui5.semester_combobox.setEnabled(True)
				self.ui5.label_3.setEnabled(True)
				self.ui5.semester_combobox.setCurrentIndex(-1)
				self.ui5.section_combobox.setEnabled(True)
				self.ui5.label_4.setEnabled(True)
				self.ui5.section_combobox.setCurrentIndex(-1)
				self.ui5.faculty_combobox.setCurrentIndex(-1)
				self.ui5.faculty_combobox.setEnabled(False)
				self.ui5.label_5.setEnabled(False)
				self.ui5.roomno_textbox.setEnabled(True)
				self.ui5.label_6.setEnabled(True)
				self.ui5.generated_table.clearContents()

	def semester_combobox_event(self):   #function for semester combobox
		self.row = []
		if self.sem != '' and self.sem not in self.num_sections:
			self.num_sections[self.sem] = self.ui.sections_spinbox.value()
			logger.info('No. of sections in %s: %s', self.sem, self.num_sections[self.sem])
			#print(self.sem, self.num_sections[self.sem])
		self.sem = self.ui.semester_combobox.currentText()
		if self.sem in self.num_sections:
			self.ui.sections_spinbox.setValue(self.num_sections[self.sem])
		else:
			self.ui.sections_spinbox.setValue(0)
		self.ui.input_list.clear()
		if self.sem in self.subjects:
			for sub in self.subjects[self.sem]:
				self.ui.input_list.addItem(sub.both_names)
		self.ui.input_list.clearSelection()
		if self.row:
			del self.row[0]
			self.ui.input_textbox.clear()
			self.ui.input_textbox.setPlaceholderText("Please enter subject name")
			self.ui.subject_short_input.clear()
			self.ui.credits_spinbox.setValue(1)
		logger.info('Selected row in list: %s', self.row)
		#print(self.row)
		#self.ui.input_list.repaint()

	def section_spinbox_event(self):    #function for sections spinbox
		if self.sem != '':
			self.num_sections[self.sem] = self.ui.sections_spinbox.value()  #saves the number of sections when "add" button is clicked
			logger.info('%s %s', self.sem, self.num_sections[self.sem])
			#print(self.sem, self.num_sections[self.sem])

	def add_btn_event(self):   #function for add button
		#print(dir(self.ui.input_textbox))
		logger.debug('Add button first form')
		text = self.ui.input_textbox.text()

		if self.row:   #when editing a currently selected value in list
			logger.debug('Editing selected item')
			logger.debug('Input type: %s', self.inputType)
			if self.inputType == "Subjects":
				for x in self.row:
					#print(x.text())
					subj = subject(x.text())
					sem = self.ui.semester_combobox.currentText()
					for y in self.subjects[sem]:
						if subj == y:
							if not sem:
								#self.systemtray_icon.show()
								self.systemtray_icon.showMessage('Input', 'Please select the semester.')
								logger.debug('Input-Please select the semester.')
								return
							if text != '':
								short_sub = self.ui.subject_short_input.text()
								if not short_sub:
									#self.systemtray_icon.show()
									self.systemtray_icon.showMessage('Input', 'Please enter the subject short form.')
									logger.debug('Input-Please enter the subject short form.')
									return
								subcode = self.ui.subject_code_input.text()
								credits = self.ui.credits_spinbox.value()
								lab = self.ui.lab_checkbox.isChecked()
								y.name = text
								y.short_name = short_sub
								y.credits = credits
								y.lab = lab
								y.subcode = subcode
								logger.info('Subject details(name, shortname, credits, lab) :%s %s %s %s', text, short_sub, credits, lab)
								#print(text, short_sub, credits, lab)
								t = text + " - " + short_sub
								self.ui.input_list.takeItem(self.ui.input_list.row(x))
								self.ui.input_list.addItem(t)
								if y.name != text or y.short_name != short_sub:
									self.update_subject_changes(subj, y)
								self.ui.credits_spinbox.setValue(1)
								break
			else:	#input type is faculty
				for x in self.row:
					fac = x.text()
					for y in self.faculty_list_value:
						if fac == y.name:
							y.title = self.ui.title_combobox.currentText()
							y.name = text
							y.designation = self.ui.desig_combobox.currentText()
							self.ui.input_list.takeItem(self.ui.input_list.row(x))
							self.ui.input_list.addItem(text)
							self.update_faculty_changes(fac, y.name)
							logger.debug('Faculty details(title, name, designation): %s %s %s', y.title, y.name, y.designation)
							break
			self.ui.input_list.clearSelection()
			self.row = []
			logger.info('Selected row in list: %s', self.row)
			#print(self.row)
			self.ui.input_list.repaint()

		else: #when adding a new item
			logger.debug('Adding new item')
			logger.debug('Input type: %s', self.inputType)
			if self.inputType == "Subjects":
				sem = self.ui.semester_combobox.currentText()
				if not sem:
					#self.systemtray_icon.show()
					self.systemtray_icon.showMessage('Input', 'Please select the semester.')
					logger.debug('Input-Please select the semester.')
					return
				if text != '':
					short_sub = self.ui.subject_short_input.text()
					if not short_sub:
						#self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Input', 'Please enter the subject short form.')
						logger.debug('Input-Please enter the subject short form.')
						return
					subcode = self.ui.subject_code_input.text()
					credits = self.ui.credits_spinbox.value()
					lab = self.ui.lab_checkbox.isChecked()
					sub = subject(text, short_sub, credits, lab, subcode)
					logger.info('Subject details(name, shortname, credits, lab) :%s %s %s %s', text, short_sub, credits, lab)
					#print(text, short_sub, credits, lab)
					t = text + " - " + short_sub
					for x in self.subjects[sem]:
						if sub == x:
							#self.systemtray_icon.show()
							self.systemtray_icon.showMessage('Warning!', 'Duplicate value entered.')
							logger.debug('Warning! Duplicate value entered.')
							break
					else: # loop completed without finding duplicates
						self.ui.input_list.addItem(t)
						self.subjects[sem].append(sub)
						self.subs[sub.short_name] = sub
						self.ui.credits_spinbox.setValue(1)
				else:
					#self.systemtray_icon.show()
					self.systemtray_icon.showMessage('Input', 'Please enter the subject name.')
					logger.debug('Input-Please enter the subject name.')
					
			elif self.inputType == "Faculty": # input type is Faculty
				if text != '':
					title = self.ui.title_combobox.currentText()
					t = title + " " + text
					if t not in self.faculty_list_value:
						f = faculty_class(t)
						f.designation = self.ui.desig_combobox.currentText()
						self.faculty_list_value.append(f)
						self.ui.input_list.addItem(text)
						logger.debug('Faculty details(title, name, designation): %s %s', t, f.designation)
					else:
						#self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Warning!', 'Duplicate value entered.')
						logger.debug('Warning! Duplicate value entered.')
				else:
					#self.systemtray_icon.show()
					self.systemtray_icon.showMessage('Input', 'Please enter the faculty name.')
					logger.debug('Input-Please enter the faculty name.')
				self.ui.title_combobox.setCurrentIndex(0)
			else:
				#self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Input', 'Please select the input type.')
				logger.debug('Input-Please enter the input type.')
				
		self.ui.input_list.sortItems()
		self.ui.desig_combobox.setCurrentIndex(-1)
		self.ui.title_combobox.setCurrentIndex(-1)
		self.ui.subject_short_input.clear()
		self.ui.input_textbox.clear()
		self.ui.subject_code_input.clear()
		self.ui.lab_checkbox.setChecked(False)
		self.ui.input_textbox.setFocus()
		
		logger.info('Faculty list: %s', self.faculty_list_value)
		logger.info('Subjects list: %s', self.subjects)
		#print('faculty list: ', self.faculty_list_value)
		#print('subjects list: ', self.subjects)

	def update_subject_changes(self, old_sub, new_sub):
		# changes in subs, section_fixed_slots, subjects_assigned, faculty_subjects
		if old_sub.short_name != new_sub.short_name:
			del self.subs[old_sub.short_name]
			self.subs[new_sub.short_name] = new_sub
			for sem in self.section_fixed_slots:
				for section in self.section_fixed_slots[sem]:
					for row in self.section_fixed_slots[sem][section]:
						for col in self.section_fixed_slots[sem][section][row]:
							if self.section_fixed_slots[sem][section][row][col] == old_sub.short_name:
								self.section_fixed_slots[sem][section][row][col] = new_sub.short_name
								
		
		self.subs[old_sub.short_name] = new_sub
		for sem in self.subjects_assigned:
			for section in self.subjects_assigned[sem]:
				for i, sub in enumerate(self.subjects_assigned[sem][section]):
					sub = sub.split(' - ')
					if sub[0] == old_sub.name and sub[1] == old_sub.short_name:
						self.subjects_assigned[sem][section][i] = new_sub.both_names + ' - ' + sub[2]
						teachers = sub[2].split(', ')
						for teacher in teachers:
							
							for i, sub in enumerate(self.faculty_subjects[teacher]):
								sub = sub.split(' - ')
								if sub[0] == old_sub.name and sub[1] == old_sub.short_name:
									self.faculty_subjects[teacher][i] = new_sub.both_names + ' - ' + sub[2]
						break # move to next section
		pass

	def update_faculty_changes(self, old_fac, new_fac):
		# changes in subjects_assigned, faculty_subjects, faculty_fixed_slots
		if old_fac != new_fac:
			for sem in self.subjects_assigned:
				for section in self.subjects_assigned[sem]:
					for i, sub in enumerate(self.subjects_assigned[sem][section]):
						sub = sub.split(' - ')
						
						if sub[2] == old_fac:
							self.subjects_assigned[sem][section][i] = ' - '.join(sub[:2]) + ' - ' + new_fac.name

			if old_fac in self.faculty_subjects:
				self.faculty_subjects[new_fac] = self.faculty_subjects.pop(old_fac)
			if old_fac in self.faculty_fixed_slots:
				self.faculty_fixed_slots[new_fac] = self.faculty_fixed_slots.pop(old_fac)
		pass

	def handle_listclick_event(self):
		self.row = self.ui.input_list.selectedItems()
		#print(dir(self.ui.input_list))
		sem = self.ui.semester_combobox.currentText()
		if self.inputType == "Subjects":
			for x in self.row:
				#print(x.text())
				subj = subject(x.text())
				for y in self.subjects[sem]:
					if subj.name == y.name:
						self.ui.input_textbox.setText(subj.name)
						self.ui.subject_short_input.setText(subj.short_name)
						self.ui.credits_spinbox.setValue(y.credits)
						self.ui.subject_code_input.setText(y.subcode)
						if y.lab == True:
							self.ui.lab_checkbox.setChecked(True)
						else:
							self.ui.lab_checkbox.setChecked(False)
						break
		else:
			for x in self.row:
				fac = x.text()
				for y in self.faculty_list_value:
					if fac == y.name:
						self.ui.input_textbox.setText(y.name)
						index = self.ui.title_combobox.findText(y.title)
						if index >= 0:
							self.ui.title_combobox.setCurrentIndex(index)
						else:
							self.ui.title_combobox.setCurrentIndex(-1)
						index = self.ui.desig_combobox.findText(y.designation)
						if index >= 0:
							self.ui.desig_combobox.setCurrentIndex(index)
						else:
							self.ui.desig_combobox.setCurrentIndex(-1)
						break

	def elective_btn_event(self):
		logger.debug('Elective button first form')
		if self.ElectiveWindow.isVisible():
			self.ElectiveWindow.hide()
		else:
			logger.info('Elective Window')
			self.ElectiveWindow.show()
			self.reset_Btn_event()

	def remove_btn_event(self):   #function for remove button
		logger.debug('Remove button first form')
		row = self.ui.input_list.selectedItems()
		self.row = []
		if not row:
			#self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Warning!', 'Select item to remove.')
			logger.debug('Warning! Select item to remove.')
		else:
			#print (row)
			for x in row:
				#print(dir(x))
				#print(x.text())
				self.ui.input_list.takeItem(self.ui.input_list.row(x))
				try:
					if self.inputType == "Subjects":
						#self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Subjects', x.text() + ' removed from the subject list')
						logger.debug('Subjects-%s removed from the subject list.', x.text())
						self.subjects[self.sem].remove(subject(x.text()))
					else:
						self.faculty_list_value.remove(x.text())
						#self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Faculty', x.text() + ' removed from the faculty list')
						logger.debug('Faculty-%s removed from the faculty list.', x.text())
				finally: # not catching exceptions, we want to see the error
					pass
			self.ui.input_list.clearSelection()
			self.ui.input_list.repaint()
		logger.info('Faculty list: %s', self.faculty_list_value)
		logger.info('Subjects list: %s', self.subjects)
		#print('faculty list: ', self.faculty_list_value)
		#print('subjects list: ', self.subjects)

	def reset_first_window(self):
		logger.debug('Resetting First Window')
		self.ui.semester_combobox.setEnabled(False)
		self.ui.sections_spinbox.setEnabled(False)
		self.ui.input_textbox.setEnabled(False)
		self.ui.title_combobox.setEnabled(False)
		self.ui.subject_code_input.setEnabled(False)
		self.ui.subject_short_input.setEnabled(False)
		self.ui.lab_checkbox.setEnabled(False)
		self.ui.desig_combobox.setEnabled(False)
		self.ui.credits_spinbox.setEnabled(False)
		self.ui.label_3.setEnabled(False)
		self.ui.label_4.setEnabled(False)
		self.ui.label_5.setEnabled(False)
		self.ui.label_6.setEnabled(False)
		self.ui.label_7.setEnabled(False)
		self.ui.label_8.setEnabled(False)
		self.ui.label_9.setEnabled(False)
		self.ui.line.setEnabled(False)
		self.ui.line_2.setEnabled(False)
		self.ui.electiveBtn.setEnabled(False)
		self.ui.input_textbox.setPlaceholderText("")
		self.ui.inputType_combobox.setCurrentIndex(-1)
		self.ui.semester_combobox.setCurrentIndex(-1)
		self.ui.input_list.clear()


	#elective form functions
	def semester_combobox_elective_event(self):
		self.ui_elec.electiveGroup_combobox.setCurrentIndex(-1)
		self.ui_elec.electiveGroup_combobox.clear()
		sem = self.ui_elec.semester_combobox.currentText()
		#self.ui_elec.elective_spinbox.setValue(0)
		self.ui_elec.electiveGroup_combobox.setEnabled(False)
		self.ui_elec.label_3.setEnabled(False)
		#if len(self.electives[sem]) > 0:
		for group in self.electives[sem]:
			self.ui_elec.electiveGroup_combobox.addItem(group)
			self.ui_elec.electiveGroup_combobox.setEnabled(True)
			self.ui_elec.label_3.setEnabled(True)
		self.ui_elec.elective_input_textbox.clear()
		self.ui_elec.elective_input_textbox.setPlaceholderText("")
		self.ui_elec.elective_input_textbox.setEnabled(False)
		self.ui_elec.label_5.setEnabled(False)
		self.ui_elec.elective_spinbox.setEnabled(True)
		self.ui_elec.elective_spinbox.setValue(len(self.electives[sem]))
		self.ui_elec.label_4.setEnabled(True)
		self.ui_elec.elective_code_input.clear()
		self.ui_elec.elective_code_input.setEnabled(False)
		self.ui_elec.label_8.setEnabled(False)
		self.ui_elec.elective_short_input.clear()
		self.ui_elec.elective_short_input.setEnabled(False)
		self.ui_elec.label_6.setEnabled(False)
		self.ui_elec.credits_spinbox.setValue(1)
		self.ui_elec.credits_spinbox.setEnabled(False)
		self.ui_elec.label_7.setEnabled(False)
		self.ui_elec.lab_checkbox.setChecked(False)
		self.ui_elec.lab_checkbox.setEnabled(False)
		self.ui_elec.line.setEnabled(True)
		self.ui_elec.line_2.setEnabled(False)
		self.ui_elec.elective_list.clear()
		
	def electivegroup_combobox_event(self):
		self.ui_elec.elective_input_textbox.setPlaceholderText("Please enter elective name")
		self.ui_elec.elective_input_textbox.setEnabled(True)
		self.ui_elec.label_5.setEnabled(True)
		self.ui_elec.elective_code_input.setEnabled(True)
		self.ui_elec.label_8.setEnabled(True)
		self.ui_elec.elective_short_input.setEnabled(True)
		self.ui_elec.label_6.setEnabled(True)
		self.ui_elec.credits_spinbox.setEnabled(True)
		self.ui_elec.label_7.setEnabled(True)
		self.ui_elec.lab_checkbox.setEnabled(True)
		self.ui_elec.line_2.setEnabled(True)
		self.ui_elec.elective_list.clear()
		sem = self.ui_elec.semester_combobox.currentText()
		electivegroup = self.ui_elec.electiveGroup_combobox.currentText()
		if electivegroup in self.electives[sem]:
			for sub in self.electives[sem][electivegroup]:
				self.ui_elec.elective_list.addItem(sub.both_names)
		self.ui_elec.elective_list.clearSelection()

	def elective_spinbox_event(self):
		no_of_ele_grp = self.ui_elec.elective_spinbox.value()
		logger.info('No of elective groups %s',no_of_ele_grp)
		#print(no_of_ele_grp)
		self.ui_elec.electiveGroup_combobox.setEnabled(True)
		self.ui_elec.label_3.setEnabled(True)
		self.ui_elec.electiveGroup_combobox.clear()
		for i in range(0, no_of_ele_grp):
			s = 'Elective ' + str(i+1)
			self.ui_elec.electiveGroup_combobox.addItem(s)
		self.ui_elec.electiveGroup_combobox.setCurrentIndex(-1)

	def add_btn_elective_event(self):
		logger.debug('Add button elective form')
		text = self.ui_elec.elective_input_textbox.text()
		sem = self.ui_elec.semester_combobox.currentText()
		row = self.ui_elec.elective_list.selectedItems()
		elective_group = self.ui_elec.electiveGroup_combobox.currentText()
		short_sub = self.ui_elec.elective_short_input.text()
		subcode = self.ui_elec.elective_code_input.text()
		logger.debug('Adding %s elective to %s in %s', text, sem, elective_group)
		if not sem:
			#self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please select the semester.')
			logger.debug('Input-Please select the semester.')
			return
		if not short_sub:
			#self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please enter the elective short form.')
			logger.debug('Input-Please enter the subject short form.')
			return
		if not elective_group:
			#self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please select the elective group.')
			logger.debug('Input-Please select the elective group.')
			return

		if row:   #when editing a currently selected value in list
			for x in row:
				subj = subject(x.text())
				sem = self.ui_elec.semester_combobox.currentText()
				for y in self.electives[sem][elective_group]:
					if subj == y:
						if text != '':
							credits = self.ui_elec.credits_spinbox.value()
							lab = self.ui_elec.lab_checkbox.isChecked()
							y.name = text
							y.short_name = short_sub
							y.credits = credits
							y.lab = lab
							y.subcode = subcode
							logger.info('Elective details(name, shortname, credits, lab) :%s %s %s %s', text, short_sub, credits, lab)
							#print(text, short_sub, credits, lab)
							t = text + " - " + short_sub
							self.ui_elec.elective_list.takeItem(self.ui_elec.elective_list.row(x))
							self.ui_elec.elective_list.addItem(t)
							'''
							if subj in self.subjects[sem]:
								self.subjects[sem].remove(subj)
								self.subjects[sem].append(y)
							'''
							self.update_subject_changes(subj, y)
							self.ui_elec.credits_spinbox.setValue(1)
							break
						else:
							#self.systemtray_icon.show()
							self.systemtray_icon.showMessage('Input', 'Please enter the elective name.')
							logger.debug('Input-Please enter the elective name.')
		else:
			
			if text != "":
				credits = self.ui_elec.credits_spinbox.value()
				lab = self.ui_elec.lab_checkbox.isChecked()
				sub = subject(text, short_sub, credits, lab, subcode)
				logger.info('Elective details(name, shortname, credits, lab) :%s %s %s %s', text, short_sub, credits, lab)
				#print(text, short_sub, credits, lab)
				t = text + " - " + short_sub
				#if elective_group in self.electives[sem]:
				for group in self.electives[sem]:
					if group == elective_group:
						for x in self.electives[sem][group]:
							if sub == x:
								#self.systemtray_icon.show()
								self.systemtray_icon.showMessage('Warning!', 'Duplicate value entered.')
								logger.debug('Warning! Duplicate value entered.')
								break
				else:
					self.ui_elec.elective_list.addItem(t)
					if elective_group not in self.electives[sem]:
						self.electives[sem][elective_group] = []
					self.electives[sem][elective_group].append(sub)
					self.subjects[sem].append(sub)
					self.subs[sub.short_name] = sub
					self.ui_elec.credits_spinbox.setValue(1)
			else:
				#self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Input', 'Please enter the elective name.')
				logger.debug('Input-Please enter the elective name.')
		self.ui_elec.elective_list.sortItems()
		self.ui_elec.elective_short_input.clear()
		self.ui_elec.elective_input_textbox.clear()
		self.ui_elec.elective_code_input.clear()
		self.ui_elec.lab_checkbox.setChecked(False)
		self.ui_elec.elective_input_textbox.setFocus()
		
		logger.info('Electives list: %s', self.electives)
		#print('electives list: ', self.electives)

	def remove_btn_elective_event(self):
		logger.debug('Remove button elective form')
		row = self.ui_elec.elective_list.selectedItems()
		sem = self.ui_elec.semester_combobox.currentText()
		elective_group = self.ui_elec.electiveGroup_combobox.currentText()
		if not row:
			#self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Warning!', 'Select item to remove.')
			logger.debug('Warning! Select item to remove.')
		elif not elective_group:
			#self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Warning!', 'Select elective group.')
			logger.debug('Warning! Select elective group.')
		else:
			for x in row:
				self.ui_elec.elective_list.takeItem(self.ui_elec.elective_list.row(x))
				try:
					#self.systemtray_icon.show()
					self.systemtray_icon.showMessage('Subjects', x.text() + ' removed from the subject list')
					logger.debug('Subjects-%d removed from the subject list', x.text())
					sub = subject(x.text())
					self.electives[sem][elective_group].remove(sub)
					self.subjects[sem].remove(sub)

				finally:
					pass
			self.ui_elec.elective_list.clearSelection()
			self.ui_elec.elective_list.repaint()

		logger.info('Electives list: %s', self.electives)
		#print('electives list: ', self.electives)
	
	def handle_listclick_elective_event(self):
		row = self.ui_elec.elective_list.selectedItems()
		sem = self.ui_elec.semester_combobox.currentText()
		for x in row:
			subj = subject(x.text())
			for group in self.electives[sem]:
				for y in self.electives[sem][group]:
					if subj.name == y.name:
						self.ui_elec.elective_input_textbox.setText(subj.name)
						self.ui_elec.elective_short_input.setText(subj.short_name)
						self.ui_elec.credits_spinbox.setValue(y.credits)
						self.ui_elec.elective_code_input.setText(y.subcode)
						if y.lab == True:
							self.ui_elec.lab_checkbox.setChecked(True)
						else:
							self.ui_elec.lab_checkbox.setChecked(False)
						break

	def reset_Btn_event(self):
		logger.debug('Resetting Elective Window')
		self.ui_elec.electiveGroup_combobox.setCurrentIndex(-1)
		self.ui_elec.electiveGroup_combobox.clear()
		self.ui_elec.elective_input_textbox.clear()
		self.ui_elec.elective_input_textbox.setPlaceholderText("")
		self.ui_elec.elective_input_textbox.setEnabled(False)
		self.ui_elec.label_5.setEnabled(False)
		self.ui_elec.elective_spinbox.setValue(0)
		self.ui_elec.elective_code_input.clear()
		self.ui_elec.elective_code_input.setEnabled(False)
		self.ui_elec.label_8.setEnabled(False)
		self.ui_elec.elective_short_input.clear()
		self.ui_elec.elective_short_input.setEnabled(False)
		self.ui_elec.label_6.setEnabled(False)
		self.ui_elec.credits_spinbox.setValue(1)
		self.ui_elec.credits_spinbox.setEnabled(False)
		self.ui_elec.label_7.setEnabled(False)
		self.ui_elec.lab_checkbox.setChecked(False)
		self.ui_elec.lab_checkbox.setEnabled(False)
		self.ui_elec.elective_list.clear()
		self.ui_elec.elective_spinbox.setEnabled(False)
		self.ui_elec.label_4.setEnabled(False)
		self.ui_elec.semester_combobox.setCurrentIndex(-1)
		self.ui_elec.semester_combobox.setFocus()
		self.ui_elec.electiveGroup_combobox.setEnabled(False)
		self.ui_elec.label_3.setEnabled(False)
		self.ui_elec.line.setEnabled(False)
		self.ui_elec.line_2.setEnabled(False)

	
	# second form functions
	def populate_second_window(self):
		logger.debug('Resetting/Populating Second Window')
		self.faculty_list_value.sort()
		self.ui2.faculty_combobox.clear()
		self.ui2.semester_combobox.clear()
		self.ui2.section_combobox.clear()
		self.ui2.subject_combobox.clear()
		self.ui2.assigned_list.clear()
		for value in self.faculty_list_value:
			self.ui2.faculty_combobox.addItem(value.name)
		for sem in self.sem_list:
			self.ui2.semester_combobox.addItem(sem)
		self.ui2.faculty_combobox.setCurrentIndex(-1)
		self.ui2.semester_combobox.setCurrentIndex(-1)

		for sem in self.sem_list:
			self.sections[sem] = list(map(chr, range(65, 65+26)))[:self.num_sections[sem]]
			if sem not in self.subjects_assigned:
				self.subjects_assigned[sem] = dict()
			for section in self.sections[sem]:
				if section not in self.subjects_assigned[sem]:
					self.subjects_assigned[sem][section] = []

		
		for faculty in self.faculty_list_value:
			if faculty not in self.faculty_subjects:
				self.faculty_subjects[faculty.name] = []
		#print(self.subjects_assigned)
		
	def semester_combobox2_event(self): # semester combobox in second form
		self.sem = self.ui2.semester_combobox.currentText()
		self.ui2.subject_combobox.clear()
		for sub in self.subjects[self.sem]:
			self.ui2.subject_combobox.addItem(sub.both_names)
		self.ui2.section_combobox.clear()
		for section in self.sections[self.sem]:
			self.ui2.section_combobox.addItem(section)

		self.section_combobox2_event() # to display assigned subjects

	def section_combobox2_event(self):
		# display assigned subjects in list widget
		sem = self.ui2.semester_combobox.currentText()
		section = self.ui2.section_combobox.currentText()
		if sem and section:
			self.ui2.assigned_list.clear()
			logger.info('Displaying assigned subjects for %s %s', sem, section)
			logger.info('Subject assignments: %s', self.subjects_assigned[sem][section])
			for sub in self.subjects_assigned[sem][section]:
				self.ui2.assigned_list.addItem(sub)
		else:
			self.ui2.assigned_list.clear()

	def faculty_combobox2_event(self):
		faculty = self.ui2.faculty_combobox.currentText()
		logger.info('Displaying assigned subjects for %s', faculty)
		logger.info('Faculty subject allotments: %s', self.faculty_subjects[faculty])
		self.ui2.assigned_list.clear()
		for sub in self.faculty_subjects[faculty]:
			self.ui2.assigned_list.addItem(sub)
		pass

	def assign_btn_event(self):
		faculty = self.ui2.faculty_combobox.currentText()
		if faculty == '':
			#self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please select a faculty member.')
			logger.debug('Input-Please select a faculty member.')
			return
		sem = self.ui2.semester_combobox.currentText()
		if sem == '':
			#self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please select the semester.')
			logger.debug('Input-Please select the semester.')
			return
		section = self.ui2.section_combobox.currentText()
		if section == '':
			#self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please select a section.')
			logger.debug('Input-Please select a section.')
			return
		sub = self.ui2.subject_combobox.currentText()
		if sub == '':
			#self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please select a subject.')
			logger.debug('Input-Please select a subject.')
			return

		for i, x in enumerate(self.subjects_assigned[sem][section]):
			x = x.split(' - ')
			subj = ' - '.join(x[:2])
			teachers = x[2].split(', ')
			if subj == sub:
				try:
					if self.subs[x[1]].lab == False or faculty in teachers: # if theory subject or teacher already assigned to subject
						#self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Warning!', 'Duplicate assignment')
						logger.debug('Warning! Duplicate assignment.')
					else: # assigned additional teachers
						self.subjects_assigned[sem][section][i] += ', ' + faculty
						fac_subject = sub + ' - ' + sem + ' ' + section
						self.faculty_subjects[faculty].append(fac_subject)
				except KeyError as e:
					logger.info(self.subs)
					logger.exception(e)
					#print(self.subs)
					raise
				break
		else: # assigning a subject for the first time
			sub_faculty = sub + ' - ' + faculty
			self.subjects_assigned[sem][section].append(sub_faculty)
			fac_subject = sub + ' - ' + sem + ' ' + section
			self.faculty_subjects[faculty].append(fac_subject)
		#self.ui2.assigned_list.addItem(sub)
		self.section_combobox2_event()

		logger.info('Subject assignments', self.subjects_assigned)
		logger.info('Faculty subject allotments', self.faculty_subjects)
		#print(self.subjects_assigned)
		#print(self.faculty_subjects)
		pass

	def undo_btn_event(self):
		selected = self.ui2.assigned_list.selectedItems()
		if not selected:
			#self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Warning!', 'Select item to remove.')
			logger.debug('Warning! Select item to remove.')
		else:
			for x in selected:
				self.ui2.assigned_list.takeItem(self.ui2.assigned_list.row(x))
				x = x.text()
				x = x.split(' - ')
				if len(x) == 3: # deleting from section view
					sub = x[0] + ' - ' + x[1]
					faculty = x[2]
					section = self.ui2.section_combobox.currentText()
					sem = self.ui2.semester_combobox.currentText()
					self.subjects_assigned[sem][section].remove(sub + ' - ' + faculty)
					self.faculty_subjects[faculty].remove(sub + ' - ' + sem + ' ' + section)
					pass
				else: # deleting from faculty view
					sub = x[0] + ' - ' + x[1]
					sem = x[2]
					section = x[3]
					faculty = self.ui2.faculty_combobox.currentText()
					self.subjects_assigned[sem][section].remove(sub + ' - ' + faculty)
					self.faculty_subjects[faculty].remove(sub + ' - ' + sem + ' ' + section)
					pass
				logger.debug('Subject assignment %s removed', self.subjects_assigned[sem][section])
				logger.debug('Faculty assignment %s removed', self.faculty_subjects[faculty])
		pass


	#third form functions
	def semester_combobox3_event(self):	#load the number of sections in sec combobox and load the slot allotments made when semester is changed
		self.ui3.subject_table.clearContents()
		sem = self.ui3.semester_combobox.currentText()
		logger.info('Semester: %s', sem)
		self.ui3.slotType_combobox.clear()
		for sub in self.subjects[sem]:
			self.ui3.slotType_combobox.addItem(sub.both_names)
		self.ui3.slotType_combobox.addItem('-')
		for group in self.electives[sem]:
			if len(self.electives[sem][group]) > 0:
				self.ui3.slotType_combobox.addItem(group)
		self.ui3.section_combobox.clear()
		for section in self.sections[sem]:
			self.ui3.section_combobox.addItem(section)
		section = self.ui3.section_combobox.currentText()
		logger.info('Subject constraints: %s', self.section_fixed_slots)
		#print(self.section_fixed_slots)
		if sem in self.section_fixed_slots and section in self.section_fixed_slots[sem]:
			for row in self.section_fixed_slots[sem][section]:
				for column in self.section_fixed_slots[sem][section][row]:
					logger.info('%s %s %s %s', sem, section, row, column)
					#print(sem, section, row, column)
					a = self.section_fixed_slots[sem][section][row][column]
					item = QtWidgets.QTableWidgetItem()
					item.setText(a)
					self.ui3.subject_table.setItem(row, column, item)

	def section_combobox3_event(self):	#load the slot allotments made when section is changed
		self.ui3.subject_table.clearContents()
		sem = self.ui3.semester_combobox.currentText()
		section = self.ui3.section_combobox.currentText()
		logger.info('Section %s', section)
		logger.info('Displaying subject constraints for: %s %s', sem, section)
		#print(self.section_fixed_slots)
		if sem in self.section_fixed_slots and section in self.section_fixed_slots[sem]:
			logger.info('Subject constraints: %s', self.section_fixed_slots[sem][section])
			for row in self.section_fixed_slots[sem][section]:
				for column in self.section_fixed_slots[sem][section][row]:
					logger.info('%s %s %s %s', sem, section, row, column)
					#print(sem, section, row, column)
					a = self.section_fixed_slots[sem][section][row][column]
					item = QtWidgets.QTableWidgetItem()
					item.setText(a)
					self.ui3.subject_table.setItem(row, column, item)

	def slotType_combobox3_event(self):
		self.slot = self.ui3.slotType_combobox.currentText()
		logger.info('Slot type: %s', self.slot)

	def cellClick3_event(self, row, column):
		slot = self.ui3.slotType_combobox.currentText()
		logger.info('Assigning subject constraints')
		logger.info('%s %s', str(row), str(column))
		#print (str(row), str(column))
		item = QtWidgets.QTableWidgetItem()

		sem = self.ui3.semester_combobox.currentText()
		section = self.ui3.section_combobox.currentText()
		
		slot = slot.split(' - ') # slot is either subject - short name, Elective #, or -
		if len(slot) > 1:
			slot = slot[1]
		else:
			slot = slot[0]

		dict_entry_exists = sem in self.section_fixed_slots and section in self.section_fixed_slots[sem] and row in self.section_fixed_slots[sem][section] and column in self.section_fixed_slots[sem][section][row]

		if slot.startswith('Elective'):
			if dict_entry_exists:
				sub = self.section_fixed_slots[sem][section][row][column] 
				sub = sub.split('/')
				if len(sub) > 1 and self.subs[sub[0]] in self.electives[sem][slot]:
					for section in self.sections[sem]:
						self.section_fixed_slots[sem][section][row].pop(column)
					logger.info('%s exists', slot)
					#print(slot + 'exists')
					item.setText('')
					assign_elective = False
				else:
					# assign elective
					assign_elective = True
			else:
				# assign elective
				assign_elective = True
			if assign_elective:
				electives = []
				for sub in self.electives[sem][slot]:
					electives.append(sub.short_name)
				t = '/'.join(electives)
				item.setText(t)
				if sem not in self.section_fixed_slots:
					self.section_fixed_slots[sem] = dict()
				for section in self.sections[sem]:
					if section not in self.section_fixed_slots[sem]:
						self.section_fixed_slots[sem][section] = dict()
					if row not in self.section_fixed_slots[sem][section]:
						self.section_fixed_slots[sem][section][row] = dict()
					self.section_fixed_slots[sem][section][row][column] = t

		elif dict_entry_exists and self.section_fixed_slots[sem][section][row][column] == slot:
			logger.info('%s exists', slot)
			#print(slot + ' exists')
			self.section_fixed_slots[sem][section][row].pop(column)
			item.setText('')
		else:
			if sem not in self.section_fixed_slots:
				self.section_fixed_slots[sem] = dict()
			if section not in self.section_fixed_slots[sem]:
				self.section_fixed_slots[sem][section] = dict()
			if row not in self.section_fixed_slots[sem][section]:
				self.section_fixed_slots[sem][section][row] = dict()
			item.setText(slot)
			self.section_fixed_slots[sem][section][row][column] = slot
			
		self.ui3.subject_table.setItem(row, column, item)
		logger.info('Subject constraints: %s', self.section_fixed_slots)
		#print(self.section_fixed_slots)

	def reset_third_window(self):
		logger.debug('Resetting Third Window')
		if self.ui3.semester_combobox.count() == 0:
			for sem in self.sem_list:
				self.ui3.semester_combobox.addItem(sem)
		self.ui3.semester_combobox.setCurrentIndex(-1)
		self.ui3.section_combobox.setCurrentIndex(-1)
		self.ui3.slotType_combobox.setCurrentIndex(-1)
		self.ui3.subject_table.clearContents()


	#fourth form functions
	def faculty_combobox4_event(self):
		faculty = self.ui4.faculty_combobox.currentText()
		logger.debug('Displaying faculty constraints for %s', faculty)
		self.ui4.faculty_table.clearContents()
		if faculty in self.faculty_fixed_slots:
			for row in self.faculty_fixed_slots[faculty]:
				for column in self.faculty_fixed_slots[faculty][row]:
					logger.info('%s %s %s', faculty, row, column)
					#print(faculty, row, column)
					a = self.faculty_fixed_slots[faculty][row][column]
					item = QtWidgets.QTableWidgetItem()
					item.setText(a)
					self.ui4.faculty_table.setItem(row, column, item)

	def cellClick4_event(self, row, column):
		logger.info('Assigning faculty constraints')
		logger.info('%s %s', str(row), str(column))
		#print (str(row), str(column))
		item = QtWidgets.QTableWidgetItem()
		item.setText('-')		

		faculty = self.ui4.faculty_combobox.currentText()
		if faculty in self.faculty_fixed_slots and row in self.faculty_fixed_slots[faculty] and column in self.faculty_fixed_slots[faculty][row] and self.faculty_fixed_slots[faculty][row][column] == '-':
			self.faculty_fixed_slots[faculty][row].pop(column)
			item = QtWidgets.QTableWidgetItem()
			item.setText('')
			self.ui4.faculty_table.setItem(row, column, item)
		else:
			self.ui4.faculty_table.setItem(row, column, item)
			if faculty not in self.faculty_fixed_slots:
				self.faculty_fixed_slots[faculty] = dict()
			if row not in self.faculty_fixed_slots[faculty]:
				self.faculty_fixed_slots[faculty][row] = dict()
			self.faculty_fixed_slots[faculty][row][column] = item.text()
		logger.info('Faculty constraints: %s', self.faculty_fixed_slots)
		#print(self.faculty_fixed_slots)

	def generate_event(self):
		logger.debug('Generating timetable...\nScheduling slots...\nAlotting subjects to slots...')
		self.timetables, self.faculty_timetables, dayclash = tt.produce_timetable(self, loc)
		self.section_combobox5_event()
		self.show_results_dialog(dayclash)

	def reset_fourth_window(self):
		logger.debug('Resetting Fourth Window')
		self.ui4.faculty_combobox.setCurrentIndex(-1)
		self.ui4.faculty_table.clearContents()


	#fifth form functions
	def semester_combobox5_event(self):
		self.ui5.generated_table.clearContents()
		sem = self.ui5.semester_combobox.currentText()
		logger.debug('Populating section combobox for %s semester', sem)
		self.ui5.section_combobox.clear()
		for section in self.sections[sem]:
			self.ui5.section_combobox.addItem(section)
		section = self.ui5.section_combobox.currentText()
		self.section_combobox5_event()

	def section_combobox5_event(self):
		self.ui5.generated_table.clearContents()
		sem = self.ui5.semester_combobox.currentText()
		section = self.ui5.section_combobox.currentText()
		logger.debug('Displaying timetable for %s %s', sem, section)
		if sem in self.timetables and section in self.timetables[sem]:
			if self.timetables[sem][section].roomno:
				self.ui5.roomno_textbox.setText(self.timetables[sem][section].roomno)
			for day in self.timetables[sem][section]:
				for timeslot in self.timetables[sem][section][day]:
					sub = self.timetables[sem][section][day][timeslot]
					if sub == '':
						a = '-'
					else:
						#print(sub)
						a = sub[3] # 3rd field is subject short name
					item = QtWidgets.QTableWidgetItem()
					item.setText(a)
					row = tt.day_row_num[day]
					column = timeslot-1
					self.ui5.generated_table.setItem(row, column, item)

	def faculty_combobox5_event(self):
		faculty = self.ui5.faculty_combobox.currentText()
		logger.debug('Displaying timetable for %s', faculty)
		self.ui5.generated_table.clearContents()
		if faculty in self.faculty_timetables:
			for day in self.faculty_timetables[faculty]:
				for timeslot in self.faculty_timetables[faculty][day]:
					if self.faculty_timetables[faculty][day][timeslot] == '':
						a = '-'
					else:
						section = self.faculty_timetables[faculty][day][timeslot][0]
						sub = self.faculty_timetables[faculty][day][timeslot][1]
						a = '{} ({})'.format(sub[3], section)
					item = QtWidgets.QTableWidgetItem()
					item.setText(a)
					row = tt.day_row_num[day]
					column = timeslot-1
					self.ui5.generated_table.setItem(row, column, item)

	def show_swap_conflict_dialog(self, conflicts):
		#print(conflicts)
		logger.debug('Conflicts during swapping in generated timetable dialog')
		logger.debug(conflicts)
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		msg.setText('Conflicts:')
		msg.setInformativeText('\n'.join(map(lambda x: '%s %s %s: %s' % x, conflicts)))
		msg.setWindowTitle("Conflicts")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()

	def cellClick5_event(self, row, column):
		if self.selected_cell:
			logger.info('Swapping alloted classes between two slots at user\'s risk')
			r, c = self.selected_cell
			logger.info('%s %s', r, c)
			#print(r, c)
			logger.info('%s %s', str(row), str(column))
			#print(str(row), str(column))
			if r == row and c == column: # if same cell is selected twice
				self.ui5.generated_table.clearSelection()
				self.selected_cell = ''
			else: # if 2 different cells are selected
				if self.ui5.inputType_combobox.currentText() == "Faculty": # faculty timetable
					faculty = self.ui5.faculty_combobox.currentText()
					logger.debug('For Faculty %s', faculty)
					if faculty in self.faculty_timetables:
						cur_cell = self.ui5.generated_table.currentItem() 
						for day, ro in tt.day_row_num.items():
							if r == ro:
								prev_d = day
							if row == ro:
								cur_d = day
						prev_t = c + 1
						cur_t = column + 1
						cur_sub = self.faculty_timetables[faculty][cur_d][cur_t]
						can_swap = True
						conflicts = []
						if cur_sub != '':
							sec = cur_sub[0]
							sec = sec.split(' ')
							cur_sem = sec[0]
							cur_sec = sec[1]
							logger.info('Swap element 1: %s %s %s', cur_sem, cur_sec, cur_sub)
							#print(cur_sem, cur_sec, cur_sub)
							if self.timetables[cur_sem][cur_sec][prev_d][prev_t]:
								can_swap = False
								conflicts.append((cur_sem + ' ' + cur_sec, prev_d, prev_t, self.timetables[cur_sem][cur_sec][prev_d][prev_t][3]))
						prev_sub = self.faculty_timetables[faculty][prev_d][prev_t]
						if prev_sub != '':
							sec = prev_sub[0]
							sec = sec.split(' ')
							prev_sem = sec[0]
							prev_sec = sec[1]
							prev_cell_text = '{} ({})'.format(prev_sub[1][3], prev_sem + ' ' + prev_sec) 
							logger.info('Swap element 2: %s %s %s', prev_sem, prev_sec, prev_sub)
							#print(prev_sem, prev_sec, prev_sub)
							if self.timetables[prev_sem][prev_sec][cur_d][cur_t]:
								can_swap = False
								conflicts.append((prev_sem + ' ' + prev_sec, cur_d, cur_t, self.timetables[prev_sem][prev_sec][cur_d][cur_t][3]))
						else:
							prev_cell_text = '-'

						if cur_sub and prev_sub and cur_sem == prev_sem and cur_sec == prev_sec:
							can_swap = True

						if can_swap:
							logger.debug('Swap successful')
							prev_cell = QtWidgets.QTableWidgetItem()
							prev_cell.setText(prev_cell_text) # previous cell contents
							new_cell = QtWidgets.QTableWidgetItem()
							new_cell.setText(cur_cell.text())
							self.ui5.generated_table.setItem(r, c, new_cell)
							self.ui5.generated_table.setItem(row, column, prev_cell) # swap cell contents in table
							f = self.faculty_timetables[faculty]
							f[cur_d][cur_t], f[prev_d][prev_t] = f[prev_d][prev_t], f[cur_d][cur_t] # swap in faculty timetable
							if prev_sub:
								self.timetables[prev_sem][prev_sec][cur_d][cur_t] = self.timetables[prev_sem][prev_sec][prev_d][prev_t]
								self.timetables[prev_sem][prev_sec][prev_d][prev_t] = ''
							if cur_sub:
								self.timetables[cur_sem][cur_sec][prev_d][prev_t] = self.timetables[cur_sem][cur_sec][cur_d][cur_t]
								self.timetables[cur_sem][cur_sec][cur_d][cur_t] = ''
						else:
							logger.debug('Swap failed')
							self.show_swap_conflict_dialog(conflicts)
						
						self.ui5.generated_table.clearSelection()

				else: # section timetable
					sem = self.ui5.semester_combobox.currentText()
					section = self.ui5.section_combobox.currentText()
					logger.debug('For %s %s', sem, section)
					cur_cell = self.ui5.generated_table.currentItem()
					for day, ro in tt.day_row_num.items():
						if r == ro:
							prev_d = day
						if row == ro:
							cur_d = day
					prev_t = c + 1
					cur_t = column + 1
					prev_sub = self.timetables[sem][section][prev_d][prev_t]
					cur_sub = self.timetables[sem][section][cur_d][cur_t]
					can_swap = True
					conflicts = []
					if prev_sub != '':
						#print(prev_sub)
						prev_cell_text = prev_sub[3]
						logger.info('Swap element 1: %s', prev_cell_text)
						if self.subs[prev_sub[3]].lab == True:
							can_swap = False
						else:
							prev_teacher = prev_sub[2]
							if self.faculty_timetables[prev_teacher][cur_d][cur_t]:
								sec, sub = self.faculty_timetables[prev_teacher][cur_d][cur_t]
								can_swap = False
								conflicts.append((prev_teacher, cur_d, cur_t, sec + ' ' + sub[3]))
					else:
						prev_cell_text = '-'
					if cur_sub != '':
						if self.subs[cur_sub[3]].lab == True:
							can_swap = False
						else:
							cur_teacher = cur_sub[2]
							if self.faculty_timetables[cur_teacher][prev_d][prev_t]:
								sec, sub = self.faculty_timetables[cur_teacher][prev_d][prev_t]
								can_swap = False
								conflicts.append((cur_teacher, prev_d, prev_t, sec + ' ' + sub[3]))

					'''
					if prev_sub and cur_sub and prev_teacher == cur_teacher:
						can_swap = True
					'''
					logger.info('Swap element 2: %s', cur_cell.text())

					if can_swap:
						logger.debug('Swap successful')
						prev_cell = QtWidgets.QTableWidgetItem()
						prev_cell.setText(prev_cell_text) # previous cell
						new_cell = QtWidgets.QTableWidgetItem()
						new_cell.setText(cur_cell.text()) # current cell
						self.ui5.generated_table.setItem(r, c, new_cell)
						self.ui5.generated_table.setItem(row, column, prev_cell)

						self.timetables[sem][section][cur_d][cur_t] = prev_sub
						self.timetables[sem][section][prev_d][prev_t] = cur_sub # swap in section timetable

						if prev_sub != '':
							self.faculty_timetables[prev_teacher][cur_d][cur_t] = self.faculty_timetables[prev_teacher][prev_d][prev_t]
							self.faculty_timetables[prev_teacher][prev_d][prev_t] = ''
						if cur_sub != '':
							self.faculty_timetables[cur_teacher][prev_d][prev_t] = self.faculty_timetables[cur_teacher][cur_d][cur_t]
							self.faculty_timetables[cur_teacher][cur_d][cur_t] = ''
					else:
						logger.debug('Swap failed')
						self.show_swap_conflict_dialog(conflicts)

					self.ui5.generated_table.clearSelection()

			self.selected_cell = '' # after 2 clicks, reset the selection
		else:
			self.selected_cell = (row, column) # first click

	def roomno_textbox_event(self):
		logger.info('Storing room number alloted to each section in each semester')
		sem = self.ui5.semester_combobox.currentText()
		sec = self.ui5.section_combobox.currentText()
		if sem and sec:
			roomno = self.ui5.roomno_textbox.text()
			self.timetables[sem][sec].roomno = roomno

	def get_free_rooms(self):
		logger.info('Finding free classrooms during every slot on each day')
		if isinstance(self.timetables, dict):
			rooms = dict()
			for day in 'monday', 'tuesday', 'wednesday', 'thursday', 'friday':
				rooms[day] = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
			rooms['saturday'] = {1: [], 2: [], 3: [], 4: []}

			num_rooms = 0
			for sem in self.timetables:
				for sec in self.timetables[sem]:
					tt = self.timetables[sem][sec]
					if tt.roomno:
						num_rooms += 1
						for day in tt:
							for timeslot in tt[day]:
								if not tt[day][timeslot]: 
									rooms[day][timeslot].append(tt.roomno)
									#print(day, timeslot, tt.roomno)
			for day in rooms:
				for timeslot in rooms[day]:
					if len(rooms[day][timeslot]) == num_rooms and num_rooms > 0: # at times such as lunch breaks
						rooms[day][timeslot] = ['all']
		logger.debug('Free rooms: %s', rooms)
		try:
			filepath = os.path.join('Output', 'Free Rooms.docx')
			worddoc.make_docx(rooms, 'rooms', filepath, self.department)						
			os.startfile(filepath)
		except OSError as err:
			self.show_printerror_dialog(err)
			logger.exception(err)

	def print_btn_event_plaintext(self):
		inputType = self.ui5.inputType_combobox.currentText()
		if inputType == "Students":
			sem = self.ui5.semester_combobox.currentText()
			sec = self.ui5.section_combobox.currentText()
			if sem =='' or sec == '':
				#self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Warning!', 'Select Semester and Section to print timetable')
			else:
				tt = self.timetables[sem][sec]
				f = open('Output/Class Timetables/' + sem + ' ' + sec + '.txt','w')
				filename = 'Output\Class Timetables\\' + sem + ' ' + sec + '.txt'
				print('NMAM Institute of Technology, Nitte\nDept. of Computer Science & Engineering\nTime Table (Autonomy) Even Semester\n\n', file = f)
				print('Semester:' + sem + '\nSection:' + sec + '\n\n', file = f)
				print(('%-20s ' * 9) % ('', '9:00-9:55', '9:55-10:50', '11:10-12:05', '12:05-1:00', '1:00-1:55', '1:55-2:50', '2:50-3:40', '3:40-4:30'), file = f)
				print('\n', file = f)
				for day in tt:
					print('%-20s' % day, end = ' ', file = f)
					for timeslot in tt[day]:
						if tt[day][timeslot] == '':
							print('%-20s' % '-', end = ' ', file = f)
						else:
							print('%-20s' % tt[day][timeslot][3], end = ' ', file = f)
					print('\n', file = f)
				print('\n', file = f)
				print('Faculty Assigned\n', file = f)
				fac = self.subjects_assigned[sem][sec]
				print('%-50s %-15s %-30s'  % ('SUBJECT', 'SHORT-NAME', 'FACULTY'), file = f)
				for s in fac:
					sub_name, short_sub, faculty = s.split(' - ')
					print('%-50s %-15s %-30s'  % (sub_name, short_sub, faculty), file = f)
				f.close()
				os.startfile(filename)
		else:
			faculty = self.ui5.faculty_combobox.currentText()
			if faculty == '':
				#self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Warning!', 'Select the Faculty to print timetable')
			else:
				tt = self.faculty_timetables[faculty]
				f = open('Output/Personal Timetables/' + faculty + '.txt','w')
				filename = 'Output\Personal Timetables\\' + faculty + '.txt'
				print('NMAM Institute of Technology, Nitte\nPersonal Time Table\n\n', file = f)
				print('Department :  CSE\nStaff Name:' + faculty + '\n\n', file = f)
				print(('%-20s ' * 9) % ('', '9:00-9:55', '9:55-10:50', '11:10-12:05', '12:05-1:00', '1:00-1:55', '1:55-2:50', '2:50-3:40', '3:40-4:30'), file = f)
				print('\n', file = f)
				for day in tt:
					print('%-20s' % day, end = ' ', file = f)
					for timeslot in tt[day]:
						if tt[day][timeslot] == '':
							print('%-20s' % '-', end = ' ', file = f)
						else:
							section = tt[day][timeslot][0]
							subject = tt[day][timeslot][1][3]
							print('%-20s' % (subject + ' (' + section + ')') , end = ' ', file = f)
					print('\n', file = f)
				print('\n', file = f)
				f.close()
				os.startfile(filename)

	def print_btn_event(self):
		logger.info('Printing...')
		inputType = self.ui5.inputType_combobox.currentText()
		if inputType == 'Students':
			logger.info('Students')
			sem = self.ui5.semester_combobox.currentText()
			sec = self.ui5.section_combobox.currentText()
			if sem =='' or sec == '':
				#self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Warning!', 'Select Semester and Section to print timetable.')
				logger.debug('Warning! Select Semester and Section to print timetable.')
			else:
				tt = self.timetables[sem][sec]
				logger.info('Printing timetable for %s', tt.name)
				filepath = os.path.join('Output', 'Class Timetables', '{}.docx'.format(tt.name))
				try:
					year = '{}. {} - {}. {}'.format(self.startMonth[:3], self.startYear, self.endMonth[:3], self.endYear)
					#roomno = self.ui5.roomno_textbox.text()
					#tt.roomno = roomno
					worddoc.make_docx(tt, 'section', filepath, self.subjects_assigned[sem][sec], self.subs, self.faculty_list_value, year)
					os.startfile(filepath)
				except OSError as err:
					self.show_printerror_dialog(err)
					logger.exception(err)
				
		else:
			logger.info('Faculty')
			faculty = self.ui5.faculty_combobox.currentText()
			if faculty == '':
				#self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Warning!', 'Select the Faculty to print timetable')
				logger.debug('Warning! Select the faculty to print timetable.')
			else:
				tt = self.faculty_timetables[faculty]
				logger.info('Printing timetable for %s', faculty_class(tt.name).name)
				filepath = os.path.join('Output', 'Personal Timetables', '{}.docx'.format(faculty_class(tt.name).name))
				try:
					i = self.faculty_list_value.index(faculty)
					designation = self.faculty_list_value[i].designation
					worddoc.make_docx(tt, 'faculty', filepath, self.faculty_subjects[faculty], self.subs, self.timetables, designation)
					os.startfile(filepath)
				except OSError as err:
					self.show_printerror_dialog(err)
					logger.exception(err)

	def show_printerror_dialog(self, error):
		logger.debug('Print error dialog')
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		msg.setText('There was an error with printing. Please close the docx file before printing it again.')
		msg.setInformativeText(error.strerror + ': ' + error.filename)
		msg.setWindowTitle("Error")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()

	def show_results_dialog(self, dayclash):
		logger.debug('Results display dialog')
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)	
		msg.setText('Completed generation')
		msg.setInformativeText('There were ' + str(len(dayclash)) + ' unallocated subjects.')
		info = 'They are: \n' + '\n'.join(map(lambda x: '{} {} {}'.format(x[0].name, x[1][2], x[1][3]), dayclash))
		msg.setDetailedText(info)
		msg.setWindowTitle("Info")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()

	def reset_fifth_window(self):
		logger.debug('Resetting Fifth Window')
		self.ui5.inputType_combobox.setCurrentIndex(-1)
		self.ui5.semester_combobox.clear()
		self.ui5.semester_combobox.setCurrentIndex(-1)
		self.ui5.section_combobox.setCurrentIndex(-1)
		self.ui5.faculty_combobox.setCurrentIndex(-1)
		self.ui5.generated_table.clearContents()
		self.ui5.roomno_textbox.clear()

	def finish_btn_event(self, event):
		logger.debug('User has clicked on Exit/Finish/\'X\'')
		buttonReply = QMessageBox.warning(self, 'EXIT Confirmation', "Are you sure you want to EXIT? All unsaved data will be lost on quitting. If you would like to save and quit, please click on Save.", QMessageBox.Yes | QMessageBox.Save | QMessageBox.Cancel, QMessageBox.Cancel)
		if buttonReply == QMessageBox.Yes:
			logger.debug('User clicked Yes')
			logger.debug('Quitting Program by user\'s choice, no errors')
			#sys.exit()
		elif buttonReply == QMessageBox.Save:
			logger.debug('User clicked Save. Program will save and exit')
			if self.cur_open_filename:
				if self.cur_open_filename.endswith('.json'):
					success = self.save_state_json(self.cur_open_filename)
				else:
					success = self.save_state(self.cur_open_filename)
				if success:
					#self.systemtray_icon.show()
					self.systemtray_icon.showMessage('Success', 'Saved to ' + self.cur_open_filename)
					logger.debug('Success. Saved to %s', self.cur_open_filename)
				else:
					event.ignore()
			else:
				saved = self.show_save_file_dialog()
				if not saved:
					event.ignore()
			logger.debug('Quitting Program by user\'s choice, no errors')
			#sys.exit()
		elif buttonReply == QMessageBox.Cancel:
			logger.debug('Exit Cancelled')
			event.ignore()


	#common functions
	def next_btn_event(self):
		if self.YearWindow.isVisible():
			if self.FirstWindow.isVisible() or self.SecondWindow.isVisible() or self.ThirdWindow.isVisible() or self.FourthWindow.isVisible() or self.FifthWindow.isVisible(): # if year window is opened from menu option
				self.YearWindow.hide()
			else:						# when year window is opened when app is started
				self.YearWindow.hide()
				self.FirstWindow.show()
				self.current_window = self.FirstWindow
				logger.debug('First Window')
		elif self.FirstWindow.isVisible():
			self.FirstWindow.hide()
			self.SecondWindow.show()
			self.current_window = self.SecondWindow
			logger.debug('Second Window')
			self.populate_second_window()
		elif self.SecondWindow.isVisible():
			self.SecondWindow.hide()
			self.ThirdWindow.show()
			self.current_window = self.ThirdWindow
			logger.debug('Third Window')
		elif self.ThirdWindow.isVisible():
			self.ThirdWindow.hide()
			self.FourthWindow.show()
			self.current_window = self.FourthWindow
			logger.debug('Fourth Window')
			if self.ui4.faculty_combobox.currentText() == "" and self.ui4.faculty_combobox.count() == 0:
				for faculty in self.faculty_list_value:
					self.ui4.faculty_combobox.addItem(faculty.name)
				self.ui4.faculty_combobox.setCurrentIndex(-1)
		elif self.FourthWindow.isVisible():
			self.FourthWindow.hide()
			self.FifthWindow.show()
			self.current_window = self.FifthWindow
			logger.debug('Fifth Window')
			if self.ui5.faculty_combobox.currentText() == "" and self.ui5.faculty_combobox.count() == 0:
				for faculty in self.faculty_list_value:
					self.ui5.faculty_combobox.addItem(faculty.name)
				self.ui5.faculty_combobox.setCurrentIndex(-1)

	def back_btn_event(self):
		if self.SecondWindow.isVisible():
			self.SecondWindow.hide()
			self.FirstWindow.show()
			self.current_window = self.FirstWindow
			logger.debug('First Window')
		elif self.ThirdWindow.isVisible():
			self.ThirdWindow.hide()
			self.SecondWindow.show()
			self.current_window = self.SecondWindow
			logger.debug('Second Window')
		elif self.FourthWindow.isVisible():
			self.FourthWindow.hide()
			self.ThirdWindow.show()
			self.current_window = self.ThirdWindow
			logger.debug('Third Window')
		elif self.FifthWindow.isVisible():
			self.FifthWindow.hide()
			self.FourthWindow.show()
			self.current_window = self.FourthWindow
			logger.debug('Fourth Window')

		
	#menubar function
	def filemenuevent(self, option):
		option = option.text()
		logger.info('File Menu option clicked: %s', option)
		#print(option)
		if option == "Exit":
			#self.finish_btn_event()
			self.current_window.close()
		elif option == "Save":
			if self.cur_open_filename:
				if self.cur_open_filename.endswith('.json'):
					success = self.save_state_json(self.cur_open_filename)
				else:
					success = self.save_state(self.cur_open_filename)
				if success:
					#self.systemtray_icon.show()
					self.systemtray_icon.showMessage('Success', 'Saved to ' + self.cur_open_filename)
					logger.debug('Success. Saved to %s', self.cur_open_filename)
			else:
				self.show_save_file_dialog()
		elif option == "Save As":
			self.show_save_file_dialog()
		elif option == "Load":
			buttonReply = QMessageBox.question(self, 'Load Confirmation', "Are you sure you want to load data? All unsaved data will be lost on loading.", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
			if buttonReply == QMessageBox.Ok:
				logger.debug('Load confirmed')
				dialog = QtWidgets.QFileDialog(caption = "Choose file to load")
				dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
				if dialog.exec_():
					fname = dialog.selectedFiles()[0]
					logger.info('File name: %s', fname)
					#print(fname)
					if fname.endswith('.json'):
						success = self.load_state_json(fname)
					elif fname.endswith('.xlsx') or fname.endswith('.xls'):
						success = self.load_excel(fname)
					else:
						success = self.load_state(fname)
					if success:
						#self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Success', 'Loaded all saved data from ' + fname)
						logger.debug('Success. Loaded all saved data from %s', fname)
						logger.debug('Reset all windows and displaying 1st window')
						if not fname.endswith('.xls') and not fname.endswith('.xlsx'):
							self.cur_open_filename = fname
						self.reset_first_window()
						self.populate_second_window()
						self.reset_third_window()
						self.reset_fourth_window()
						self.reset_fifth_window()
						self.reset_Btn_event()	#reset elective window
						self.reset_year_window()
						if self.SecondWindow.isVisible() or self.ThirdWindow.isVisible() or self.FourthWindow.isVisible() or self.FifthWindow.isVisible() or self.ElectiveWindow.isVisible():
							self.ElectiveWindow.hide()
							self.SecondWindow.hide()
							self.ThirdWindow.hide()
							self.FourthWindow.hide()
							self.FifthWindow.hide()
							self.FirstWindow.show()
			else:
				logger.debug('Load cancelled')
				pass
		elif option == "Clear All":
			buttonReply = QMessageBox.question(self, 'Reset Confirmation', "Are you sure you want to clear all data? All unsaved data will be lost and the program will be reset.", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
			if buttonReply == QMessageBox.Ok:
				logger.debug('Clear All confirmed')
				logger.info('Clearing all unsaved data')
				self.cur_open_filename = ''
				self.faculty_list_value = []
				self.subjects = dict()
				self.subs = dict()
				self.num_sections = dict()
				self.electives = dict()
				for sem in self.sem_list:
					self.subjects[sem] = []
					self.num_sections[sem] = 0
					self.electives[sem] = dict()
				self.row = self.ui.input_list.selectedItems()
				self.sections = dict()
				self.subjects_assigned = dict()
				self.faculty_subjects = dict()
				self.section_fixed_slots = dict()
				self.faculty_fixed_slots = dict()
				self.reset_first_window()
				self.populate_second_window()
				self.reset_third_window()
				self.reset_fourth_window()
				self.reset_fifth_window()
				self.reset_Btn_event()	#reset elective window
				self.reset_year_window()
				logger.debug('All variables and forms cleared and reset')
				#self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Reset', 'All unsaved data have been cleared.')
				logger.debug('Reset-All unsaved data have been cleared.')
			else:
				logger.debug('Clear All cancelled')
				pass
		elif option == "Print All":
			try:
				fp = os.path.realpath(os.curdir) + '\\Output' 
				s = os.path.realpath(os.curdir) + '\\Output\\Class Timetables'
				logger.debug('Printing all class timetables to %s', s)
				for sem in self.timetables:
					for sec in self.timetables[sem]:
						tt = self.timetables[sem][sec]
						filepath = os.path.join('Output', 'Class Timetables', '{}.docx'.format(tt.name))
						year = '{}. {} - {}. {}'.format(self.startMonth[:3], self.startYear, self.endMonth[:3], self.endYear)
						worddoc.make_docx(tt, 'section', filepath, self.subjects_assigned[sem][sec], self.subs, self.faculty_list_value, year)
				
				f = os.path.realpath(os.curdir) + '\\Output\\Personal Timetables'
				logger.debug('Printing all faculty timetables to %s', f)
				for faculty in self.faculty_timetables:
					tt = self.faculty_timetables[faculty]
					filepath = os.path.join('Output', 'Personal Timetables', '{}.docx'.format(faculty_class(tt.name).name))
					i = self.faculty_list_value.index(faculty)
					designation = self.faculty_list_value[i].designation
					worddoc.make_docx(tt, 'faculty', filepath, self.faculty_subjects[faculty], self.subs, self.timetables, designation)
				
				#self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Print All', 'All timetables have been printed to ' + fp)
				logger.debug('Print All-All timetables have been printed to %s', fp)
				os.startfile(fp)
			except OSError as err:
				self.show_printerror_dialog(err)
				logger.exception(err)
		elif option == "Show Free Classrooms":
			self.get_free_rooms()
		elif option == "Set Year/Department":
			self.YearWindow.show()
		elif option == "About":
			self.AboutWindow.show()


	#save and load functions
	def show_save_file_dialog(self):
		logger.debug('Save file dialog')
		dialog = QtWidgets.QFileDialog(caption = "Choose save file")
		dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
		success = False
		while dialog.exec_():
			fname = dialog.selectedFiles()[0]
			logger.info('File name: %s', fname)
			if os.path.isfile(fname):
				buttonReply = QMessageBox.question(self, 'Save confirmation', 'File already exists. Are you sure you want to overwrite?', QMessageBox.Ok | QMessageBox.Cancel)
				if buttonReply == QMessageBox.Cancel:
					logger.debug('Overwrite Cancelled')
					continue
			#print(fname)
			if fname.endswith('.json'):
				success = self.save_state_json(fname)
			else:
				success = self.save_state(fname)
			if success:
				#self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Success', 'Saved to ' + fname)
				logger.debug('Success. Saved to %s', fname)
				self.cur_open_filename = fname
			break
		return success

	def save_state(self, fname):
		try:
			with open(fname, "wb") as file:
				state = (self.startMonth, self.startYear, self.endMonth, self.endYear, self.department,
						 self.faculty_list_value,
						 self.subjects,
						 #self.subs,
						 self.num_sections,
						 self.sections,
						 self.subjects_assigned,
						 self.faculty_subjects,
						 self.section_fixed_slots,
						 self.faculty_fixed_slots,
						 self.electives)
				pickle.dump(state, file)
				logger.info('Saving as binary file')
			return True
		except IOError as err:
			self.file_error_dialog(err.strerror + ': ' + err.filename)
			logger.exception(err)
		except:
			self.file_error_dialog('Error pickling data')
			logger.exception('Error pickling data')

	def update_sub(self):
		for sem in self.subjects:
			for i, sub in enumerate(self.subjects[sem]):
				self.subjects[sem][i] = subject(sub.name, sub.short_name, sub.credits, sub.lab)
		 
	def merge_data(self, faculty_list_value, subjects, electives):
		self.faculty_list_value = list(set(faculty_list_value).union(set(self.faculty_list_value)))
		self.faculty_list_value.sort()
		for sem in subjects:
			self.subjects[sem] = list(set(subjects[sem]).union(set(self.subjects[sem])))
		for sem in electives:
			n_groups = len(self.electives[sem])
			for group in electives[sem]:
				n_groups += 1
				self.electives[sem]['Elective ' + str(n_groups)] = electives[sem][group]

		self.subs = dict()
		for sem in self.subjects:
			for sub in self.subjects[sem]:
				self.subs[sub.short_name] = sub

	def load_state(self, fname):
		try:
			with open(fname, "rb") as file:
				state = pickle.load(file)
				(	startMonth, startYear, endMonth, endYear, department, 
					faculty_list_value,
					subjects,
					self.num_sections,
					self.sections,
					self.subjects_assigned,
					self.faculty_subjects,
					self.section_fixed_slots,
					self.faculty_fixed_slots,
					electives ) = state
			logger.info('Loading from binary file')
			self.startMonth = startMonth or self.startMonth
			self.startYear = startYear or self.startYear
			self.endMonth = endMonth or self.endMonth
			self.endYear = endYear or self.endYear
			self.department = department or self.department

			self.merge_data(faculty_list_value, subjects, electives)

			
			#print(self.subs)
			logger.info('Subjects assigned to faculty: %s', self.faculty_subjects)
			logger.info('Faculty fixed slots: %s', self.faculty_fixed_slots)
			#print(self.faculty_subjects)
			#print(self.faculty_fixed_slots)
			return True
		except IOError as err:
			self.file_error_dialog(err.strerror + ': ' + err.filename)
			logger.exception(err)
		except:
			self.file_error_dialog('Error with the file or format')
			logger.exception('Error with the file or format')

	def save_state_json(self, fname):
		try:
			faculty_list_value = []
			for teacher in self.faculty_list_value:
				faculty_list_value.append(teacher.__repr__())
			subjects = dict()
			for sem in self.subjects:
				subjects[sem] = []
				for sub in self.subjects[sem]:
					subjects[sem].append(sub.__repr__())
			'''
			faculty_fixed_slots = dict()
			for teacher in self.faculty_fixed_slots:
				if type(teacher) == type('str'):
					faculty_fixed_slots[teacher] = self.faculty_fixed_slots[teacher]
				else:
					faculty_fixed_slots[teacher.name] = self.faculty_fixed_slots[teacher]
			faculty_subjects = dict()
			for teacher in self.faculty_subjects:
				if type(teacher) == type('str'):
					try:
						name = self.faculty_list_value[self.faculty_list_value.index(teacher)].name
					except ValueError:
						pass
					faculty_subjects[name] = self.faculty_subjects[teacher]
				else:
					faculty_subjects[teacher.name] = self.faculty_subjects[teacher]
			'''
			electives = dict()
			for sem in self.electives:
				electives[sem] = dict()
				for group in self.electives[sem]:
					electives[sem][group] = []
					for sub in self.electives[sem][group]:
						electives[sem][group].append(sub.__repr__())
			state = (
				self.startMonth, self.startYear, self.endMonth, self.endYear, self.department,
				faculty_list_value,
				subjects,
				self.num_sections,
				self.sections,
				self.subjects_assigned,
				self.faculty_subjects,
				self.section_fixed_slots,
				self.faculty_fixed_slots,
				electives
				)
			logger.info('Saving as json file')
			dump = json.dumps(state, indent = 4)
			with open(fname, 'w') as file:
				file.write(dump)
			return True
		except IOError as err:
			self.file_error_dialog(err.strerror + ': ' + err.filename)
			logger.exception(err)
		except Exception as err:
			self.file_error_dialog('Error encoding json')
			logger.exception('Error encoding json')

	def load_state_json(self, fname):
		try:
			with open(fname, "r") as file:
				state = json.loads(file.read())

			(startMonth, startYear, endMonth, endYear, department,
				faculty_list_value,
				subjects,
				self.num_sections,
				self.sections,
				self.subjects_assigned,
				self.faculty_subjects,
				sfs,
				ffs,
				electives) = state
			logger.info('Loading from json file')
			self.startMonth = startMonth or self.startMonth
			self.startYear = startYear or self.startYear
			self.endMonth = endMonth or self.endMonth
			self.endYear = endYear or self.endYear
			self.department = department or self.department

			flv = []
			for teacher in faculty_list_value:
				flv.append(eval(teacher))
			subjs = dict()
			for sem in subjects:
				subjs[sem] = []
				for sub in subjects[sem]:
					s = eval(sub)
					subjs[sem].append(s)
				
			elec = dict()
			for sem in electives:
				elec[sem] = dict()
				for group in electives[sem]:
					elec[sem][group] = []
					for sub in electives[sem][group]:
						s = eval(sub)
						elec[sem][group].append(s)
			self.merge_data(flv, subjs, elec)
			self.section_fixed_slots = dict()
			self.faculty_fixed_slots = dict()
			for sem in sfs:
				self.section_fixed_slots[sem] = dict()
				for sec in sfs[sem]:
					self.section_fixed_slots[sem][sec] = dict()
					for row in sfs[sem][sec]:
						self.section_fixed_slots[sem][sec][int(row)] = dict()
						for col in sfs[sem][sec][row]:
							self.section_fixed_slots[sem][sec][int(row)][int(col)] = sfs[sem][sec][row][col]
			for teacher in ffs:
				self.faculty_fixed_slots[teacher] = dict()
				for row in ffs[teacher]:
					self.faculty_fixed_slots[teacher][int(row)] = dict()
					for col in ffs[teacher][row]:
						self.faculty_fixed_slots[teacher][int(row)][int(col)] = ffs[teacher][row][col]
			return True
		except IOError as err:
			self.file_error_dialog(err.strerror + ': ' + err.filename)
			logger.exception(err)
		except Exception as err:
			self.file_error_dialog('Error with the file or format')
			logger.exception('Error with the file or format')
			logger.exception(err)

	def file_error_dialog(self, error):
		logger.debug('File error dialog')
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		msg.setText('There was an error opening the file')
		msg.setInformativeText(error)
		msg.setWindowTitle("Error")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()

	def load_excel(self, fname):
		try:
			with xlrd.open_workbook(fname) as book:
				sheet = book.sheet_by_index(0)
			rows = sheet.nrows
			cols = sheet.ncols
			faculty = set()
			logger.info('Loading from Excel file')
			subjects = {'III': [], 'IV': [], 'V': [], 'VI': [], 'VII': [], 'VIII': []}
			electives = {'III': dict(), 'IV': dict(), 'V': dict(), 'VI': dict(), 'VII': dict(), 'VIII': dict()}
			subjects_assigned = {'III': dict(), 'IV': dict(), 'V': dict(), 'VI': dict(), 'VII': dict(), 'VIII': dict()}
			faculty_subjects = dict()
			sections = {'III': [], 'IV': [], 'V': [], 'VI': [], 'VII': [], 'VIII': []}
			cur_sem = ''
			cur_sub = ''
			cur_sec = 1
			for r in range(1, rows):
				cur_sec += 1
				if sheet.cell_value(r, 4).strip():
					cur_sem = sheet.cell_value(r, 4).strip()
					cur_sec = 1
				if sheet.cell_value(r, 1).strip():
					sub_code = sheet.cell_value(r, 0).strip()
					sub_name = sheet.cell_value(r, 1).strip()
					sub_short =  sheet.cell_value(r, 2).strip()
					credits = sheet.cell_value(r, 3) or 0
					credits = int(credits)
					lab = sub_name.endswith('Lab')
					if not cur_sub or sub_name != cur_sub.name:
						if not sub_short.upper().startswith('ELE'):
							if lab:
								sub_short = sub_short.split('|')
								sub_short = ' | '.join(map(str.strip, sub_short))
							cur_sub = subject(sub_name, sub_short, credits, lab, sub_code)
							subjects[cur_sem].append(cur_sub)
						else: # elective
							sub_short = sub_short.split(',')
							sub_short = list(map(str.strip, sub_short))
							group = 'Elective ' + sub_short[0].split('-')[1].strip()
							sub_short = sub_short[1]
							cur_sub = subject(sub_name, sub_short, credits, lab, sub_code)
							subjects[cur_sem].append(cur_sub)
							if group not in electives[cur_sem]:
								electives[cur_sem][group] = []
							electives[cur_sem][group].append(cur_sub)

				section = chr(64 + cur_sec)
				if section not in subjects_assigned[cur_sem]:
					subjects_assigned[cur_sem][section] = []
					sections[cur_sem].append(section)
				
				f = sheet.cell_value(r, 5).strip()
				f = f.split(',')
				for i, fac_name in enumerate(f):
					fac_name = fac_name.strip()
					f[i] = fac_name
					if fac_name not in faculty:
						faculty.add(faculty_class(fac_name, ' '))
						faculty_subjects[fac_name] = []
					faculty_subjects[fac_name].append('{} - {} - {} {}'.format(sub_name, sub_short, cur_sem, section))
				subjects_assigned[cur_sem][section].append('{} - {} - {}'.format(sub_name, sub_short, ', '.join(f)))

			self.merge_data(faculty, subjects, electives)
			self.subjects_assigned = subjects_assigned
			logger.info('Subjects Assigned: %s', self.subjects_assigned)
			#print(self.subjects_assigned)
			self.faculty_subjects = faculty_subjects
			self.sections = sections
			num_sections = dict()
			for sem in sections:
				num_sections[sem] = len(sections[sem])
			self.num_sections = num_sections
			self.section_fixed_slots = dict()
			self.faculty_fixed_slots = dict()
			return True
		except IOError as err:
			self.file_error_dialog(err.strerror + ': ' + err.filename)
			logger.exception(err)
		except Exception as err:
			self.file_error_dialog('Error with the file or format')
			logger.exception('Error with the file or format')
			logger.exception(err)

	# end class


def my_excepthook(excType, excValue, traceback):
	logger.error("Logging an uncaught exception", exc_info=(excType, excValue, traceback))
	sys.exit(0)

def my_logger():
	global logger
	logger = logging.getLogger('tt_main')
	logging.basicConfig(filename = loc, level = logging.DEBUG)

'''def my_excepthook(type, value, tb):
	traceback.print_exception(type, value, tb)
	sys.exit(0)
'''


if __name__ == "__main__":

	if os.path.isdir('logs') == False:
		os.mkdir('logs')
	if os.path.isdir('Output') == False:
		os.mkdir('Output')
		os.mkdir('Output\\Class Timetables')
		os.mkdir('Output\\Personal Timetables')
	else:
		if os.path.isdir('Output\\Class Timetables') == False:
			os.mkdir('Output\\Class Timetables')
		if os.path.isdir('Output\\Personal Timetables') == False:
			os.mkdir('Output\\Personal Timetables')

	global loc
	loc = os.path.realpath(os.curdir) + '\\' + os.path.join('logs', time.strftime("%a, %d %b %Y %H-%M-%S.txt", time.localtime()))
	my_logger()

	sys.excepthook = my_excepthook
	
	app = QApplication(sys.argv)
	app.setApplicationName('TimeTable Scheduler')
	main = ParentWindow()
	logger.debug('Year Window')
	#main.show()
	sys.exit(app.exec_())