
#from PyQt5 import QtWidgets, QtCore

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
from PyQt5 import Qt

import sys
#import notification

from window import Ui_window
from window2 import Ui_window2
from window3 import Ui_window3
from window4 import Ui_window4
from window5 import Ui_window5

from trialwindow import Ui_trialwindow
from trialwindow2 import Ui_trialwindow2
from trialwindow3 import Ui_trialwindow3
from trialwindow4 import Ui_trialwindow4
from trialwindow5 import Ui_trialwindow5


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
		self.subject_list_value = []
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

		self.ui2.nextBtn.clicked.connect(self.next_btn_event)
		self.ui2.backBtn.clicked.connect(self.back_btn_event)

	def setup_third_window(self):
		#THIRD WINDOW - Subject Constraints
		self.ThirdWindow = QMainWindow()
		self.ui3 = Ui_window3()
		self.ui3.setupUi(self.ThirdWindow)

		self.ui3.nextBtn.clicked.connect(self.next_btn_event)
		self.ui3.backBtn.clicked.connect(self.back_btn_event)
		for sem in self.sem_list:
			self.ui3.semester_combobox.addItem(sem)
		self.ui3.semester_combobox.setCurrentIndex(-1)
		for sec in map(str,range(self.sections)):	#make this work...im not sure how to.
			self.ui3.section_combobox.addItem(sec)
			print(sec)
		self.ui3.section_combobox.setCurrentIndex(-1)
		for slot in ['Maths','ESC','DAA/UNIX Lab','CG/CN Lab','CCIM/MBD','MCC/MCAP','EM','Project Lab']:
			self.ui3.slotType_combobox.addItem(slot)
		self.ui3.slotType_combobox.setCurrentIndex(-1)

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

	def inputType_combobox_event(self):    #function for input type combobox
		if self.FirstWindow.isVisible():
			self.inputType = self.ui.inputType_combobox.currentText()
			print(self.inputType)
			#print(dir(self.ui.inputType_combobox))
			if self.inputType == "Faculty":
				self.ui.semester_combobox.setEnabled(False)
				self.ui.sections_spinbox.setEnabled(False)
				self.ui.title_combobox.setEnabled(True)
				self.ui.input_textbox.setEnabled(True)
				self.ui.input_textbox.returnPressed.connect(self.ui.addBtn.click)
				self.ui.subject_short_input.setEnabled(False)
				self.ui.input_list.clear()
				for values in self.faculty_list_value:
					self.ui.input_list.addItem(values)
			else:
				self.ui.semester_combobox.setEnabled(True)
				self.ui.sections_spinbox.setEnabled(True)
				self.ui.input_textbox.setEnabled(True)
				self.ui.title_combobox.setEnabled(False)
				self.ui.subject_short_input.setEnabled(True)
				self.ui.lab_checkbox.setEnabled(True)
				self.ui.credits_spinbox.setEnabled(True)
				#self.ui.input_textbox.returnPressed.
				self.ui.subject_short_input.returnPressed.connect(self.ui.addBtn.click)
				self.ui.input_list.clear()
				for values in self.subject_list_value:
					self.ui.input_list.addItem(values)

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
		self.sem = self.ui.semester_combobox.currentText()
		print(self.sem)

	def section_spinbox_event(self):    #function for sections spinbox
		self.sections = self.ui.sections_spinbox.value()  #saves the number of sections when "add" button is clicked
		print(self.sections)


	def add_btn_event(self):   #function for add button
		#print(dir(self.ui.input_textbox))
		self.text = self.ui.input_textbox.text()
		if self.text != '':
			if self.inputType == "Subjects":
				short_sub = self.ui.subject_short_input.text()
				if short_sub != '':
					t = self.text + " - " + short_sub
					self.subject_list_value.append(t)
					self.ui.input_list.addItem(t)
				else:
					#notification.Notify("Please enter the subject short form.")
					self.systemtray_icon.show()
					self.systemtray_icon.showMessage('Input', 'Please enter the subject short form.')
			else:
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
		print('subjects list: ', self.subject_list_value)


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
						self.subject_list_value.remove(x.text())
					else:
						self.systemtray_icon.show()
						self.systemtray_icon.showMessage('Faculty', x.text() + ' removed from the faculty list')
						self.faculty_list_value.remove(x.text())
				except ValueError:
					pass
			self.ui.input_list.clearSelection()
			self.ui.input_list.repaint()

		print('faculty list: ', self.faculty_list_value)
		print('subjects list: ', self.subject_list_value)


	#sanjan mods ------------------------

	def next_btn_event(self):
		if self.FirstWindow.isVisible():
			self.FirstWindow.hide()
			self.SecondWindow.show()
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
