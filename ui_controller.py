from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
from PyQt5 import Qt
from collections import OrderedDict
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pickle
import tt

from window import Ui_window
from window2 import Ui_window2
from window3 import Ui_window3
from window4 import Ui_window4
from window5 import Ui_window5
from elective_window import Ui_elective_window

class subject:
	def __init__(self, name, short_name = '', credits = 0, lab = False):
		if short_name == '': # if both names are provided together in name
			both_names = name
			self.name, self.short_name = both_names.split(' - ')
		else: # short name is provided separately
			self.name = name
			self.short_name = short_name
		self.credits = credits
		self.lab = lab

	@property
	def both_names(self):
		both_names = self.name + ' - ' + self.short_name
		return both_names

	def __eq__(self, obj):
		return self.name == obj.name and self.short_name == obj.short_name
		
	def __repr__(self):
		return 'subject({}, {}, {}, {})'.format(self.name, self.short_name, self.credits, self.lab) 

class faculty_class:
	def __init__(self, name, title = ''):
		if title == '':
			name = name.split(' ')
			if len(name) > 1:
				title = name[0]
				name = ' '.join(name[1:])
			else:
				name = name[0]
		self.name = name
		self.title = title

	def __repr__(self):
		return 'faculty_class({}, {})'.format(self.name, self.title)

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

#new singular class implementing QStackedLayout
class ParentWindow(QMainWindow):

	def __init__(self, parent = None):
		super(ParentWindow,self).__init__(parent)
		self.central_window = QMainWindow()
		self.layered_windows = QStackedLayout()

		#code to resize the main window ...does NOT resize the widgets !
		self.screen_width = QDesktopWidget().screenGeometry().width()
		self.screen_height = QDesktopWidget().screenGeometry().height()
		print('current screen res: ',self.screen_width, self.screen_height)
		#self.adjusted_width = (screen_width/1366)
		#self.adjusted_height = (screen_height/768)
		self.resize_ratio = (self.screen_height/self.screen_width) #need a more accurate resize ratio than this.
		print('resize ratio: ',self.resize_ratio)

		self.setup_first_window()
		self.setup_second_window()
		self.setup_third_window()
		self.setup_fourth_window()
		self.setup_fifth_window()

		self.layered_windows.addWidget(self.FirstWindow)
		self.layered_windows.addWidget(self.SecondWindow)
		self.layered_windows.addWidget(self.ThirdWindow)
		self.layered_windows.addWidget(self.FourthWindow)
		self.layered_windows.addWidget(self.FifthWindow)

		self.central_window.setLayout(self.layered_windows)
		self.setCentralWidget(self.central_window)

		#intended original size for the app = (920, 500)
		#self.resize(916*self.adjusted_width, 460*self.adjusted_height)
		#self.resize()


	# setup functions
	def setup_first_window(self):
		#FIRST WINDOW - List Entry
		self.FirstWindow = QMainWindow()
		self.ui = Ui_window()
		self.ui.setupUi(self.FirstWindow)
		#self.ui.input_list.resize(self.adjusted_width*self.ui.input_list.width(), self.adjusted_height*self.ui.input_list.height())

		#nihal mods
		self.ui.semester_combobox.setEnabled(False)
		self.ui.sections_spinbox.setEnabled(False)
		self.ui.input_textbox.setEnabled(False)
		self.ui.title_combobox.setEnabled(False)
		self.ui.subject_short_input.setEnabled(False)
		self.ui.lab_checkbox.setEnabled(False)
		self.ui.credits_spinbox.setEnabled(False)
		self.ui.addBtn.clicked.connect(self.add_btn_event)
		self.ui.electiveBtn.clicked.connect(self.elective_btn_event)
		self.ui.removeBtn.clicked.connect(self.remove_btn_event)
		self.ui.nextBtn.clicked.connect(self.next_btn_event)
		self.ui.sections_spinbox.valueChanged.connect(self.section_spinbox_event)
		self.ui.inputType_combobox.addItem("Faculty")
		self.ui.inputType_combobox.addItem("Subjects")
		self.ui.inputType_combobox.setCurrentIndex(-1)
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
		self.faculty_list_value = []
		self.subjects = OrderedDict()
		self.subs = dict() # store link between subject name and its object
		self.num_sections = dict()
		for sem in self.sem_list:
			self.subjects[sem] = []
			self.num_sections[sem] = 0
		self.sections = 0
		self.inputType = ""
		self.text = ""
		self.sem = ""
		self.row = self.ui.input_list.selectedItems()
		self.lab = 0
		self.credits = 1
		self.titles_list = ['Mr.', 'Ms.', 'Mrs.', 'Dr.', 'Prof.' ]
		for value in self.titles_list:
			self.ui.title_combobox.addItem(value)
		self.systemtray_icon = Qt.QSystemTrayIcon(Qt.QIcon('E:\The Usual\WaRbxZN.png'))

		self.FirstWindow.resize(self.screen_width*self.resize_ratio, self.screen_height*self.resize_ratio)
		self.FirstWindow.updateGeometry()

		self.ui.menuFile.triggered[QtWidgets.QAction].connect(self.filemenuevent)

		#setting up elective window during first window setup
		self.setup_elective_window()

	def setup_elective_window(self):
		#ELECTIVE WINDOW - Elective Entry
		self.ElectiveWindow = QWidget()
		self.ui_elec = Ui_elective_window()
		self.ui_elec.setupUi(self.ElectiveWindow)

		self.ui_elec.elective_spinbox.setEnabled(False)
		self.ui_elec.electiveGroup_combobox.setEnabled(False)
		self.ui_elec.elective_input_textbox.setEnabled(False)
		self.ui_elec.elective_short_input.setEnabled(False)
		self.ui_elec.credits_spinbox.setEnabled(False)
		self.ui_elec.lab_checkbox.setEnabled(False)

		self.ui_elec.backBtn.clicked.connect(self.elective_btn_event)

	def setup_second_window(self):
		#SECOND WINDOW - Faculty assignment
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

		self.ui2.menuFile.triggered[QtWidgets.QAction].connect(self.filemenuevent)

	def setup_third_window(self):
		#THIRD WINDOW - Subject Constraints
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

		self.ui3.menuFile.triggered[QtWidgets.QAction].connect(self.filemenuevent)

	def setup_fourth_window(self):
		#FOURTH WINDOW - Faculty Constraints
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

		self.ui4.menuFile.triggered[QtWidgets.QAction].connect(self.filemenuevent)

	def setup_fifth_window(self):
		#FIFTH WINDOW - Generated timetable
		self.FifthWindow = QMainWindow()
		self.ui5 = Ui_window5()
		self.ui5.setupUi(self.FifthWindow)

		self.ui5.finishBtn.clicked.connect(self.next_btn_event)
		self.ui5.backBtn.clicked.connect(self.back_btn_event)
		self.ui5.inputType_combobox.activated[str].connect(self.inputType_combobox_event)
		self.ui5.semester_combobox.activated[str].connect(self.semester_combobox5_event)
		self.ui5.section_combobox.activated[str].connect(self.section_combobox5_event)
		self.ui5.faculty_combobox.activated[str].connect(self.faculty_combobox5_event)
		#self.ui5.generated_table.cellClicked.connect(self.cellClick5_event)
		self.ui5.faculty_combobox.setEnabled(False)
		self.ui5.inputType_combobox.addItem('Students')
		self.ui5.inputType_combobox.addItem('Faculty')
		for sem in self.sem_list:
			self.ui5.semester_combobox.addItem(sem)
		self.ui5.semester_combobox.setCurrentIndex(-1)
		self.ui5.section_combobox.setCurrentIndex(-1)
		self.ui5.faculty_combobox.setCurrentIndex(-1)

		self.timetables = ''
		self.faculty_timetables = ''

		self.FifthWindow.resize(self.screen_width*self.resize_ratio, self.screen_height*self.resize_ratio)
		self.FifthWindow.updateGeometry()

		self.ui5.menuFile.triggered[QtWidgets.QAction].connect(self.filemenuevent)

	def reset_first_window(self):
		self.ui.semester_combobox.setEnabled(False)
		self.ui.sections_spinbox.setEnabled(False)
		self.ui.input_textbox.setEnabled(False)
		self.ui.title_combobox.setEnabled(False)
		self.ui.subject_short_input.setEnabled(False)
		self.ui.lab_checkbox.setEnabled(False)
		self.ui.credits_spinbox.setEnabled(False)
		self.ui.inputType_combobox.setCurrentIndex(-1)
		self.ui.semester_combobox.setCurrentIndex(-1)
		self.ui.input_list.clear()


	# first form functions
	def inputType_combobox_event(self):    #function for input type combobox in first form
		if self.FirstWindow.isVisible():
			self.row = []

			self.inputType = self.ui.inputType_combobox.currentText()
			print(self.inputType)
			#print(dir(self.ui.inputType_combobox))
			if self.inputType == "Faculty":
				self.ui.semester_combobox.setEnabled(False)
				self.ui.sections_spinbox.setEnabled(False)
				self.ui.title_combobox.setEnabled(True)
				self.ui.input_textbox.setEnabled(True)
				self.ui.lab_checkbox.setEnabled(False)
				self.ui.credits_spinbox.setEnabled(False)
				self.ui.input_textbox.clear()
				self.ui.input_textbox.setPlaceholderText("Please enter faculty name")
				self.ui.subject_short_input.setEnabled(False)
				self.ui.input_list.clear()
				for values in self.faculty_list_value:
					self.ui.input_list.addItem(values.name)
			else: # input type subjects
				self.ui.semester_combobox.setEnabled(True)
				self.ui.sections_spinbox.setEnabled(True)
				self.ui.input_textbox.setEnabled(True)
				self.ui.input_textbox.clear()
				self.ui.input_textbox.setPlaceholderText("Please enter subject name")
				self.ui.lab_checkbox.setEnabled(True)
				self.ui.lab_checkbox.setChecked(False)
				self.ui.credits_spinbox.setEnabled(True)
				self.ui.credits_spinbox.setValue(1)
				self.ui.title_combobox.setEnabled(False)
				self.ui.subject_short_input.setEnabled(True)
				self.ui.subject_short_input.clear()
				
				self.ui.input_list.clear()
				if self.sem in self.subjects:
					for subject in self.subjects[self.sem]:
						self.ui.input_list.addItem(subject.both_names)

		#	sanjan mods - same method is used for fifth window. Do This in other combobox for other windows
		if self.FifthWindow.isVisible():
			self.inputType = self.ui5.inputType_combobox.currentText()
			print(self.inputType)
			if self.inputType == "Faculty":
				self.ui5.semester_combobox.setCurrentIndex(-1)
				self.ui5.section_combobox.setCurrentIndex(-1)
				self.ui5.semester_combobox.setEnabled(False)
				self.ui5.section_combobox.setEnabled(False)
				self.ui5.faculty_combobox.setEnabled(True)
				self.ui5.faculty_combobox.setCurrentIndex(-1)
				self.ui5.generated_table.clearContents()

			else:
				self.ui5.semester_combobox.setEnabled(True)
				self.ui5.semester_combobox.setCurrentIndex(-1)
				self.ui5.section_combobox.setEnabled(True)
				self.ui5.section_combobox.setCurrentIndex(-1)
				self.ui5.faculty_combobox.setCurrentIndex(-1)
				self.ui5.faculty_combobox.setEnabled(False)
				self.ui5.generated_table.clearContents()

	def semester_combobox_event(self):   #function for semester combobox
		self.row = []
		if self.sem != '' and self.sem not in self.num_sections:
			self.num_sections[self.sem] = self.ui.sections_spinbox.value()
			print(self.sem, self.num_sections[self.sem])
		self.sem = self.ui.semester_combobox.currentText()
		if self.sem in self.num_sections:
			self.ui.sections_spinbox.setValue(self.num_sections[self.sem])
		else:
			self.ui.sections_spinbox.setValue(0)
		self.ui.input_list.clear()
		if self.sem in self.subjects:
			for sub in self.subjects[self.sem]:
				self.ui.input_list.addItem(sub.both_names)

	def section_spinbox_event(self):    #function for sections spinbox
		if self.sem != '':
			self.num_sections[self.sem] = self.ui.sections_spinbox.value()  #saves the number of sections when "add" button is clicked
			print(self.sem, self.num_sections[self.sem])

	def add_btn_event(self):   #function for add button
		#print(dir(self.ui.input_textbox))
		text = self.ui.input_textbox.text()

		if self.row:   #when editing a currently selected value in list
			if self.inputType == "Subjects":
				for x in self.row:
					#print(x.text())
					subj = subject(x.text())
					sem = self.ui.semester_combobox.currentText()
					for y in self.subjects[sem]:
						if subj == y:
							if not sem:
								self.systemtray_icon.show()
								self.systemtray_icon.showMessage('Input', 'Please select the semester.')
								return
							if text != '':
								short_sub = self.ui.subject_short_input.text()
								if not short_sub:
									self.systemtray_icon.show()
									self.systemtray_icon.showMessage('Input', 'Please enter the subject short form.')
									return
								credits = self.ui.credits_spinbox.value()
								lab = self.ui.lab_checkbox.isChecked()
								y.name = text
								y.short_name = short_sub
								y.credits = credits
								y.lab = lab
								print(text, short_sub, credits, lab)
								t = text + " - " + short_sub
								self.ui.input_list.takeItem(self.ui.input_list.row(x))
								self.ui.input_list.addItem(t)
								self.update_subject_changes(subj, y)
								self.ui.credits_spinbox.setValue(1)
								break
			else:
				for x in self.row:
					fac = x.text()
					for y in self.faculty_list_value:
						if fac == y.name:
							y.title = self.ui.title_combobox.currentText()
							y.name = text
							self.ui.input_list.takeItem(self.ui.input_list.row(x))
							self.ui.input_list.addItem(text)
							self.update_faculty_changes(fac, y)
							break
			self.ui.input_list.clearSelection()
			self.row = []
			print(self.row)
			self.ui.input_list.repaint()

		else: #when adding a new item

			if self.inputType == "Subjects":
				sem = self.ui.semester_combobox.currentText()
				if not sem:
					self.systemtray_icon.show()
					self.systemtray_icon.showMessage('Input', 'Please select the semester.')
					return
				if text != '':
					short_sub = self.ui.subject_short_input.text()
					if not short_sub:
						self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Input', 'Please enter the subject short form.')
						return
					credits = self.ui.credits_spinbox.value()
					lab = self.ui.lab_checkbox.isChecked()
					sub = subject(text, short_sub, credits, lab)
					print(text, short_sub, credits, lab)
					t = text + " - " + short_sub
					for x in self.subjects[sem]:
						if sub == x:
							self.systemtray_icon.show()
							self.systemtray_icon.showMessage('Warning!', 'Duplicate value entered.')
							break
					else: # loop completed without finding duplicates
						self.ui.input_list.addItem(t)
						self.subjects[sem].append(sub)
						self.subs[sub.short_name] = sub
						self.ui.credits_spinbox.setValue(1)
				else:
					self.systemtray_icon.show()
					self.systemtray_icon.showMessage('Input', 'Please enter the subject name.')
					
			elif self.inputType == "Faculty": # input type is Faculty
				if text != '':
					title = self.ui.title_combobox.currentText()
					t = title + " " + text
					if t not in self.faculty_list_value:
						self.faculty_list_value.append(faculty_class(t))
						self.ui.input_list.addItem(text)
					else:
						self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Warning!', 'Duplicate value entered.')
				else:
					self.systemtray_icon.show()
					self.systemtray_icon.showMessage('Input', 'Please enter the faculty name.')
				self.ui.title_combobox.setCurrentIndex(0)
			else:
				self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Input', 'Please select the input type.')
				
		self.ui.input_list.sortItems()
		self.ui.subject_short_input.clear()
		self.ui.input_textbox.clear()
		self.ui.lab_checkbox.setChecked(False)
		self.ui.input_textbox.setFocus()
		
		print('faculty list: ', self.faculty_list_value)
		print('subjects list: ', self.subjects)

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
		print(self.row)
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
						if y.lab == True:
							self.ui.lab_checkbox.setChecked(True)
						else:
							self.ui.lab_checkbox.setChecked(False)
		else:
			for x in self.row:
				fac = x.text()
				for y in self.faculty_list_value:
					if fac == y.name:
						self.ui.input_textbox.setText(y.name)
						index = self.ui.title_combobox.findText(y.title)
						if index >= 0:
							self.ui.title_combobox.setCurrentIndex(index)

	def elective_btn_event(self):
		if self.ElectiveWindow.isVisible():
			self.ElectiveWindow.hide()
		else:
			self.ElectiveWindow.show()

	def remove_btn_event(self):    #function for remove button
		row = self.ui.input_list.selectedItems()
		self.row = []
		if not row:
			self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Warning!', 'Select item to remove.')
		else:
			#print (row)
			for x in row:
				#print(dir(x))
				#print(x.text())
				self.ui.input_list.takeItem(self.ui.input_list.row(x))
				try:
					if self.inputType == "Subjects":
						self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Subjects', x.text() + ' removed from the subject list')
						self.subjects[self.sem].remove(subject(x.text()))
					else:
						self.faculty_list_value.remove(x.text())
						self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Faculty', x.text() + ' removed from the faculty list')
				finally: # not catching exceptions, we want to see the error
					pass
			self.ui.input_list.clearSelection()
			self.ui.input_list.repaint()
		print('faculty list: ', self.faculty_list_value)
		print('subjects list: ', self.subjects)


	# second form functions
	def populate_second_window(self):
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
				self.faculty_subjects[faculty] = []
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
			for sub in self.subjects_assigned[sem][section]:
				self.ui2.assigned_list.addItem(sub)
		pass

	def faculty_combobox2_event(self):
		faculty = self.ui2.faculty_combobox.currentText()
		self.ui2.assigned_list.clear()
		for sub in self.faculty_subjects[faculty]:
			self.ui2.assigned_list.addItem(sub)
		pass

	def assign_btn_event(self):
		faculty = self.ui2.faculty_combobox.currentText()
		if faculty == '':
			self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please select a faculty member')
			return
		sem = self.ui2.semester_combobox.currentText()
		if sem == '':
			self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please select the semester')
			return
		section = self.ui2.section_combobox.currentText()
		if section == '':
			self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please select a section')
			return
		sub = self.ui2.subject_combobox.currentText()
		if sub == '':
			self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please select a subject')
			return

		for i, x in enumerate(self.subjects_assigned[sem][section]):
			x = x.split(' - ')
			subj = ' - '.join(x[:2])
			teachers = x[2].split(', ')
			if subj == sub:
				try:
					if self.subs[x[1]].lab == False or faculty in teachers: # if theory subject or teacher already assigned to subject
						self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Warning!', 'Duplicate assignment')
					else: # assigned additional teachers
						self.subjects_assigned[sem][section][i] += ', ' + faculty
						fac_subject = sub + ' - ' + sem + ' ' + section
						self.faculty_subjects[faculty].append(fac_subject)
				except KeyError as e:
					print(self.subs)
					raise
				break
		else: # assigning a subject for the first time
			sub_faculty = sub + ' - ' + faculty
			self.subjects_assigned[sem][section].append(sub_faculty)
			fac_subject = sub + ' - ' + sem + ' ' + section
			self.faculty_subjects[faculty].append(fac_subject)
		#self.ui2.assigned_list.addItem(sub)
		self.section_combobox2_event()

		print(self.subjects_assigned)
		print(self.faculty_subjects)
		pass

	def undo_btn_event(self):
		selected = self.ui2.assigned_list.selectedItems()
		if not selected:
			self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Warning!', 'Select item to remove.')
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
		pass


	#third form functions
	def semester_combobox3_event(self):	#load the number of sections in sec combobox and load the slot allotments made when semester is changed
		self.ui3.subject_table.clearContents()
		sem = self.ui3.semester_combobox.currentText()
		self.ui3.slotType_combobox.clear()
		for sub in self.subjects[sem]:
			self.ui3.slotType_combobox.addItem(sub.both_names)
		self.ui3.slotType_combobox.addItem('-')
		self.ui3.section_combobox.clear()
		for section in self.sections[sem]:
			self.ui3.section_combobox.addItem(section)
		section = self.ui3.section_combobox.currentText()
		print(self.section_fixed_slots)
		if sem in self.section_fixed_slots and section in self.section_fixed_slots[sem]:
			for row in self.section_fixed_slots[sem][section]:
				for column in self.section_fixed_slots[sem][section][row]:
					print(sem, section, row, column)
					a = self.section_fixed_slots[sem][section][row][column]
					item = QtWidgets.QTableWidgetItem()
					item.setText(a)
					self.ui3.subject_table.setItem(row, column, item)

	def section_combobox3_event(self):	#load the slot allotments made when section is changed
		self.ui3.subject_table.clearContents()
		sem = self.ui3.semester_combobox.currentText()
		section = self.ui3.section_combobox.currentText()
		print(self.section_fixed_slots)
		if sem in self.section_fixed_slots and section in self.section_fixed_slots[sem]:
			for row in self.section_fixed_slots[sem][section]:
				for column in self.section_fixed_slots[sem][section][row]:
					print(sem, section, row, column)
					a = self.section_fixed_slots[sem][section][row][column]
					item = QtWidgets.QTableWidgetItem()
					item.setText(a)
					self.ui3.subject_table.setItem(row, column, item)

	def slotType_combobox3_event(self):
		self.slot = self.ui3.slotType_combobox.currentText()

	def cellClick3_event(self, row, column):
		slot = self.ui3.slotType_combobox.currentText()
		print (str(row), str(column))
		item = QtWidgets.QTableWidgetItem()
		if slot == '-':
			item.setText('-')
		else:
			item.setText(slot.split(' - ')[1])
		self.ui3.subject_table.setItem(row, column, item)

		sem = self.ui3.semester_combobox.currentText()
		section = self.ui3.section_combobox.currentText()
		if sem not in self.section_fixed_slots:
			self.section_fixed_slots[sem] = dict()
		if section not in self.section_fixed_slots[sem]:
			self.section_fixed_slots[sem][section] = dict()
		if row not in self.section_fixed_slots[sem][section]:
			self.section_fixed_slots[sem][section][row] = dict()
		self.section_fixed_slots[sem][section][row][column] = item.text()
		print(self.section_fixed_slots)


	#fourth form functions
	def faculty_combobox4_event(self):
		faculty = self.ui4.faculty_combobox.currentText()
		self.ui4.faculty_table.clearContents()
		if faculty in self.faculty_fixed_slots:
			for row in self.faculty_fixed_slots[faculty]:
				for column in self.faculty_fixed_slots[faculty][row]:
					print(faculty, row, column)
					a = self.faculty_fixed_slots[faculty][row][column]
					item = QtWidgets.QTableWidgetItem()
					item.setText(a)
					self.ui4.faculty_table.setItem(row, column, item)

	def cellClick4_event(self, row, column):
		print (str(row), str(column))
		item = QtWidgets.QTableWidgetItem()
		item.setText('-')
		self.ui4.faculty_table.setItem(row, column, item)

		faculty = self.ui4.faculty_combobox.currentText()
		if faculty not in self.faculty_fixed_slots:
			self.faculty_fixed_slots[faculty] = dict()
		if row not in self.faculty_fixed_slots[faculty]:
			self.faculty_fixed_slots[faculty][row] = dict()
		self.faculty_fixed_slots[faculty][row][column] = item.text()
		print(self.faculty_fixed_slots)

	def generate_event(self):
		self.timetables, self.faculty_timetables = tt.produce_timetable(self)
		self.section_combobox5_event()

	#fifth form functions
	def semester_combobox5_event(self):
		self.ui5.generated_table.clearContents()
		sem = self.ui5.semester_combobox.currentText()
		self.ui5.section_combobox.clear()
		for section in self.sections[sem]:
			self.ui5.section_combobox.addItem(section)
		section = self.ui5.section_combobox.currentText()
		self.section_combobox5_event()

	def section_combobox5_event(self):
		self.ui5.generated_table.clearContents()
		sem = self.ui5.semester_combobox.currentText()
		section = self.ui5.section_combobox.currentText()
		if sem in self.timetables and section in self.timetables[sem]:
			for day in self.timetables[sem][section]:
				for timeslot in self.timetables[sem][section][day]:
					sub = self.timetables[sem][section][day][timeslot]
					if sub == '':
						a = '-'
					else:
						a = sub[3] # 3rd field is subject short name
					item = QtWidgets.QTableWidgetItem()
					item.setText(a)
					row = tt.day_row_num[day]
					column = timeslot-1
					self.ui5.generated_table.setItem(row, column, item)

	def faculty_combobox5_event(self):
		faculty = self.ui5.faculty_combobox.currentText()
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

	def cellClick5_event(self, row, column):
		print (str(row), str(column))
		item = QtWidgets.QTableWidgetItem()
		item.setText('-')
		self.ui5.generated_table.setItem(row, column, item)

		if self.inputType == "Faculty":
			faculty = self.ui5.faculty_combobox.currentText()
			if faculty not in self.faculty_fixed_slots: #replace with generated table stuff
				self.faculty_fixed_slots[faculty] = dict()
			if row not in self.faculty_fixed_slots[faculty]:
				self.faculty_fixed_slots[faculty][row] = dict()
			self.faculty_fixed_slots[faculty][row][column] = item.text()
		else:
			sem = self.ui5.semester_combobox.currentText()
			section = self.ui5.section_combobox.currentText()
			if sem not in self.section_fixed_slots: #replace with generated table stuff
				self.section_fixed_slots[sem] = dict()
			if section not in self.section_fixed_slots[sem]:
				self.section_fixed_slots[sem][section] = dict()
			if row not in self.section_fixed_slots[sem][section]:
				self.section_fixed_slots[sem][section][row] = dict()
			self.section_fixed_slots[sem][section][row][column] = item.text()


	def next_btn_event(self):
		if self.FirstWindow.isVisible():
			self.FirstWindow.hide()
			self.SecondWindow.show()
			self.populate_second_window()
		elif self.SecondWindow.isVisible():
			self.SecondWindow.hide()
			self.ThirdWindow.show()
		elif self.ThirdWindow.isVisible():
			self.ThirdWindow.hide()
			self.FourthWindow.show()
			for faculty in self.faculty_list_value:
				self.ui4.faculty_combobox.addItem(faculty.name)
			self.ui4.faculty_combobox.setCurrentIndex(-1)
		elif self.FourthWindow.isVisible():
			self.FourthWindow.hide()
			self.FifthWindow.show()
			for faculty in self.faculty_list_value:
				self.ui5.faculty_combobox.addItem(faculty.name)
			self.ui5.faculty_combobox.setCurrentIndex(-1)
		elif self.FifthWindow.isVisible():
			sys.exit(app.exec_())

	def back_btn_event(self):
		if self.SecondWindow.isVisible():
			self.SecondWindow.hide()
			self.FirstWindow.show()
		elif self.ThirdWindow.isVisible():
			self.ThirdWindow.hide()
			self.SecondWindow.show()
		elif self.FourthWindow.isVisible():
			self.FourthWindow.hide()
			self.ThirdWindow.show()
		elif self.FifthWindow.isVisible():
			self.FifthWindow.hide()
			self.FourthWindow.show()
		
	def filemenuevent(self, option):
		option = option.text()
		print(option)
		if option == "Exit":
			sys.exit(app.exec_())
		elif option == "Save":
			dialog = QtWidgets.QFileDialog(caption = "Choose save file")
			dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
			if dialog.exec_():
				fname = dialog.selectedFiles()[0]
				print(fname)
				self.save_state(fname)
				self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Success', 'Saved to ' + fname)
			pass
		elif option == "Load":
			dialog = QtWidgets.QFileDialog(caption = "Choose file to load")
			dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
			if dialog.exec_():
				fname = dialog.selectedFiles()[0]
				print(fname)
				self.load_state(fname)
				self.systemtray_icon.show()
				self.systemtray_icon.showMessage('Success', 'Loaded from ' + fname)
				self.populate_second_window()
				self.reset_first_window()
			pass

	def save_state(self, fname):
		file = open(fname, "wb")
		state = (self.faculty_list_value,
			     self.subjects,
			     self.subs,
			     self.num_sections,
			     self.sections,
			     self.subjects_assigned,
			     self.faculty_subjects,
			     self.section_fixed_slots,
			     self.faculty_fixed_slots)
		pickle.dump(state, file)
		file.close()
		pass

	def load_state(self, fname):
		file = open(fname, "rb")
		state = pickle.load(file)
		self.faculty_list_value, \
	    self.subjects, \
	    self.subs, \
	    self.num_sections, \
	    self.sections, \
	    self.subjects_assigned, \
	    self.faculty_subjects, \
	    self.section_fixed_slots, \
	    self.faculty_fixed_slots = state
		file.close()
		pass

	

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName('TimeTable Scheduler')
    main = ParentWindow()
    #main.show()
    sys.exit(app.exec_())


