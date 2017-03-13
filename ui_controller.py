from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
from PyQt5 import Qt
from collections import OrderedDict
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
#import notification

from window import Ui_window
from window2 import Ui_window2
from window3 import Ui_window3
from window4 import Ui_window4
from window5 import Ui_window5

#new singular class implementing QStackedLayout
class ParentWindow(QMainWindow):

	def __init__(self, parent = None):
		super(ParentWindow,self).__init__(parent)
		self.central_window = QWidget()
		self.layered_windows = QStackedLayout()

		#code to resize the main window ...does NOT resize the widgets !
		screen_width = QDesktopWidget().screenGeometry().width()
		screen_height = QDesktopWidget().screenGeometry().height()
		print('current screen res: ',screen_width, screen_height)
		self.adjusted_width = (screen_width/1366)
		self.adjusted_height = (screen_height/768)
		print('resize ratio: ',self.adjusted_width, self.adjusted_height)

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
		self.resize(916*self.adjusted_width, 460*self.adjusted_height)
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
		self.ui.removeBtn.clicked.connect(self.remove_btn_event)
		self.ui.nextBtn.clicked.connect(self.next_btn_event)
		self.ui.sections_spinbox.valueChanged.connect(self.section_spinbox_event)
		self.ui.inputType_combobox.addItem("Faculty")
		self.ui.inputType_combobox.addItem("Subjects")
		self.ui.inputType_combobox.setCurrentIndex(-1)
		self.ui.inputType_combobox.activated[str].connect(self.inputType_combobox_event)
		self.ui.semester_combobox.activated[str].connect(self.semester_combobox_event)
		self.sem_list = ['III', 'IV', 'V', 'VI', 'VII', 'VIII']
		for sem in self.sem_list:
			self.ui.semester_combobox.addItem(sem)
		self.ui.semester_combobox.setCurrentIndex(-1)
		self.faculty_list_value = []
		self.subjects = OrderedDict()
		self.num_sections = dict()
		for sem in self.sem_list:
			self.subjects[sem] = []
			self.num_sections[sem] = 0
		self.sections = 0
		self.inputType = ""
		self.text = ""
		self.sem = ""
		self.lab = 0
		self.credits = 1
		self.titles_list = ['Mr.', 'Ms.', 'Mrs.', 'Dr.', 'Prof.' ]
		for value in self.titles_list:
			self.ui.title_combobox.addItem(value)
		self.systemtray_icon = Qt.QSystemTrayIcon(Qt.QIcon('E:\The Usual\WaRbxZN.png'))

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
		self.ui3.subject_table.cellClicked.connect(self.cellClick_event)
		for sem in self.sem_list:
			self.ui3.semester_combobox.addItem(sem)
		self.ui3.semester_combobox.setCurrentIndex(-1)

		#table widget events
		'''slotType = self.ui3.slotType_combobox.currentText()
		cellrow = self.ui3.subject_table.currentRow()
		cellcolumn = self.ui3.subject_table.currentColumn()
		
		#if self.ui3.subject_table.itemPressed():
		self.ui3.subject_table.setItem(cellrow,cellcolumn,slotType)
		cellitem = self.ui3.subject_table.takeItem()
		print(cellitem)'''





	def setup_fourth_window(self):
		#FOURTH WINDOW - Faculty Constraints
		self.FourthWindow = QMainWindow()
		self.ui4 = Ui_window4()
		self.ui4.setupUi(self.FourthWindow)

		self.ui4.generateBtn.clicked.connect(self.next_btn_event)	
		self.ui4.backBtn.clicked.connect(self.back_btn_event)
		for faculty in self.faculty_list_value:
			self.ui4.faculty_combobox.addItem(faculty)
		self.ui4.faculty_combobox.setCurrentIndex(-1)

	def setup_fifth_window(self):
		#FIFTH WINDOW - Generated timetable
		self.FifthWindow = QMainWindow()
		self.ui5 = Ui_window5()
		self.ui5.setupUi(self.FifthWindow)

		#self.ui5.finishBtn.clicked.connect(self.next_btn_event)
		self.ui5.backBtn.clicked.connect(self.back_btn_event)
		self.ui5.inputType_combobox.activated[str].connect(self.inputType_combobox_event)
		self.ui5.faculty_combobox.setEnabled(False)
		self.ui5.inputType_combobox.addItem('Students')
		self.ui5.inputType_combobox.addItem('Faculty')
		for sem in self.sem_list:
			self.ui5.semester_combobox.addItem(sem)
		self.ui5.semester_combobox.setCurrentIndex(-1)
		for sec in map(str,range(self.sections)):	#make this work...im not sure how to.
			self.ui5.section_combobox.addItem(sec)
		self.ui5.section_combobox.setCurrentIndex(-1)
		for faculty in self.faculty_list_value:
			self.ui5.faculty_combobox.addItem(faculty)
		self.ui5.faculty_combobox.setCurrentIndex(-1)




	#nihal mods ----------
	# first form functions
	def inputType_combobox_event(self):    #function for input type combobox in first form
		if self.FirstWindow.isVisible():
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
				self.ui.input_textbox.returnPressed.connect(self.ui.addBtn.click)
				self.ui.subject_short_input.setEnabled(False)
				self.ui.input_list.clear()
				for values in self.faculty_list_value:
					self.ui.input_list.addItem(values)
			else: # input type subjects
				self.ui.semester_combobox.setEnabled(True)
				self.ui.sections_spinbox.setEnabled(True)
				self.ui.input_textbox.setEnabled(True)
				self.ui.lab_checkbox.setEnabled(True)
				self.ui.credits_spinbox.setEnabled(True)
				self.ui.title_combobox.setEnabled(False)
				self.ui.subject_short_input.setEnabled(True)
				self.ui.lab_checkbox.setEnabled(True)
				self.ui.credits_spinbox.setEnabled(True)
				#self.ui.input_textbox.returnPressed.
				self.ui.subject_short_input.returnPressed.connect(self.ui.addBtn.click)
				self.ui.input_list.clear()
				if self.sem in self.subjects:
					for subject in self.subjects[self.sem]:
						self.ui.input_list.addItem(subject)

		#	sanjan mods - same method is used for fifth window. Do This in other combobox for other windows
		if self.FifthWindow.isVisible():
			self.inputType = self.ui5.inputType_combobox.currentText()
			print(self.inputType)
			if self.inputType == "Faculty":
				self.ui5.semester_combobox.setEnabled(False)
				self.ui5.section_combobox.setEnabled(False)
				self.ui5.faculty_combobox.setEnabled(True)

			else:
				self.ui5.semester_combobox.setEnabled(True)
				self.ui5.section_combobox.setEnabled(True)
				self.ui5.faculty_combobox.setEnabled(False)



	def semester_combobox_event(self):   #function for semester combobox
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
			for subject in self.subjects[self.sem]:
				self.ui.input_list.addItem(subject)

	def section_spinbox_event(self):    #function for sections spinbox
		if self.sem != '':
			self.num_sections[self.sem] = self.ui.sections_spinbox.value()  #saves the number of sections when "add" button is clicked
			print(self.sem, self.num_sections[self.sem])


	def add_btn_event(self):   #function for add button
		#print(dir(self.ui.input_textbox))
		self.text = self.ui.input_textbox.text()
		if self.text != '':
			if self.inputType == "Subjects":
				short_sub = self.ui.subject_short_input.text()
				if short_sub != '':
					t = self.text + " - " + short_sub
					self.ui.input_list.addItem(t)
					self.subjects[self.sem].append(t)
				else:
					#notification.Notify("Please enter the subject short form.")
					self.systemtray_icon.show()
					self.systemtray_icon.showMessage('Input', 'Please enter the subject short form.')
			else: # input type is Faculty
				self.title = self.ui.title_combobox.currentText()
				t = self.title + " " + self.text
				self.faculty_list_value.append(t)
				self.ui.input_list.addItem(t)
		else:
			self.systemtray_icon.show()
			if self.inputType == "Subjects":
				#notification.Notify("Please enter the subject name.")
				self.systemtray_icon.showMessage('Input', 'Please enter the subject name.')
			else:
				#notification.Notify("Please enter the faculty name.")
				self.systemtray_icon.showMessage('Input', 'Please enter the faculty name.')
		self.ui.input_list.sortItems()
		self.ui.subject_short_input.clear()
		self.ui.input_textbox.clear()
		self.ui.input_textbox.setFocus()
		
		print('faculty list: ', self.faculty_list_value)
		print('subjects list: ', self.subjects)


	def remove_btn_event(self):    #function for remove button
		row = self.ui.input_list.selectedItems()
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
						self.subjects[self.sem].remove(x.text())
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
		for name in self.faculty_list_value:
			self.ui2.faculty_combobox.addItem(name)
		for sem in self.sem_list:
			self.ui2.semester_combobox.addItem(sem)
		self.ui2.faculty_combobox.setCurrentIndex(-1)
		self.ui2.semester_combobox.setCurrentIndex(-1)

		self.sections = dict()
		for sem in self.sem_list:
			self.sections[sem] = list(map(chr, range(65, 65+26)))[:self.num_sections[sem]]

		self.subjects_assigned = dict() # this dict will be like {'III': {'A': [subjects], 'B': [subjects]}, 'IV': {} ..etc}
		for sem in self.sem_list:
			self.subjects_assigned[sem] = dict()
			for section in self.sections[sem]: 
				self.subjects_assigned[sem][section] = []

		self.faculty_subjects = dict() # stores subjects assigned to each faculty
		for faculty in self.faculty_list_value:
			self.faculty_subjects[faculty] = []
		print(self.subjects_assigned)
		

	def semester_combobox2_event(self): # semester combobox in second form
		self.sem = self.ui2.semester_combobox.currentText()
		self.ui2.subject_combobox.clear()
		for subject in self.subjects[self.sem]:
			self.ui2.subject_combobox.addItem(subject)
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
			for subject in self.subjects_assigned[sem][section]:
				self.ui2.assigned_list.addItem(subject)
		pass

	def faculty_combobox2_event(self):
		faculty = self.ui2.faculty_combobox.currentText()
		self.ui2.assigned_list.clear()
		for subject in self.faculty_subjects[faculty]:
			self.ui2.assigned_list.addItem(subject)
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
		subject = self.ui2.subject_combobox.currentText()
		if subject == '':
			self.systemtray_icon.show()
			self.systemtray_icon.showMessage('Input', 'Please select a subject')
			return

		sub = subject + ' - ' + faculty
		self.subjects_assigned[sem][section].append(sub)
		self.faculty_subjects[faculty].append(subject + ' - ' + sem + ' - ' + section)
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
					subject = x[0] + ' - ' + x[1]
					faculty = x[2]
					section = self.ui2.section_combobox.currentText()
					sem = self.ui2.semester_combobox.currentText()
					self.subjects_assigned[sem][section].remove(subject + ' - ' + faculty)
					self.faculty_subjects[faculty].remove(subject + ' - ' + sem + ' - ' + section)
					pass
				else: # deleting from faculty view
					subject = x[0] + ' - ' + x[1]
					sem = x[2]
					section = x[3]
					faculty = self.ui2.faculty_combobox.currentText()
					self.subjects_assigned[sem][section].remove(subject + ' - ' + faculty)
					self.faculty_subjects[faculty].remove(subject + ' - ' + sem + ' - ' + section)
					pass
		pass

	#third form functions
	def semester_combobox3_event(self):
		self.ui3.subject_table.clearContents()
		self.sem = self.ui3.semester_combobox.currentText()
		self.ui3.slotType_combobox.clear()
		for subject in self.subjects[self.sem]:
			self.ui3.slotType_combobox.addItem(subject)
		self.ui3.section_combobox.clear()
		for section in self.sections[self.sem]:
			self.ui3.section_combobox.addItem(section)


	def section_combobox3_event(self):
		self.ui3.subject_table.clearContents()


	def slotType_combobox3_event(self):
		self.slot = self.ui3.slotType_combobox.currentText()


	def cellClick_event(self, row, column):
		#row = self.ui3.subject_table.currentRow()
		#column = self.ui3.subject_table.currentColumn()
		self.slot = self.ui3.slotType_combobox.currentText()
		print (str(row), str(column))
		item = QtWidgets.QTableWidgetItem()
		item.setText(str(self.slot))
		self.ui3.subject_table.setItem(row, column, item)
		#print(dir(self.ui3.subject_table))
		#self.ui3.subject_table.setText(row, column, self.slot)



	#sanjan mods ------------------------

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
		elif self.FourthWindow.isVisible():
			self.FourthWindow.hide()
			self.FifthWindow.show()
		elif self.FifthWindow.isVisible():
			self.close()

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
		


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName('TimeTable Scheduler')
    main = ParentWindow()
    main.show()
    sys.exit(app.exec_())


'''

faculty - subject - section assignments should persist when moving between windows
show a message indicaating which list of assignments you are showing eg faculty or section

'''