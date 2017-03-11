import random
from data import *
#ui modules
import sys
from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow



def generate(subjects, name, faculty): # subjects is a list of tuples (name, hours/week, teacher)
    tt = empty_timetable()
    for subject in subjects:
        for i in range(subject[1]):
            while True:
                random_day = random.choice(('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'))
                random_time = random.randint(1, 8)
                if random_day == 'saturday':
                    random_time = random.randint(1, 4)
                if tt[random_day][random_time] == '': # time slot hasn't been allocated
                    tt[random_day][random_time] = subject
                    faculty[subject[2]][random_day][random_time] = (name, subject)
                    break
    return tt

def print_timetable(tt, name, style = 'section'):
    print(('%-15s ' * 9) % (name, '9:00-9:55', '9:55-10:50', '11:10-12:05', '12:05-1:00', '1:00-1:55', '1:55-2:50', '2:50-3:40', '3:40-4:30'))
    for day in tt:
        print('%-15s' % day, end = ' ')
        for timeslot in tt[day]:
            if tt[day][timeslot] == '':
                print('%-15s' % '-', end = ' ')
            else:

                if style == 'section':
                    print('%-15s' % tt[day][timeslot][3], end = ' ')
                else:
                    section = tt[day][timeslot][0]
                    subject = tt[day][timeslot][1][3]
                    print('%-15s' % (subject + ' (' + section + ')') , end = ' ')
        print()
    print()



foura = generate(subjects['4A'], '4A', faculty)
fourb = generate(subjects['4B'], '4B', faculty)
fourc = generate(subjects['4C'], '4C', faculty)
fourd = generate(subjects['4D'], '4D', faculty)

sixa = generate(subjects['6A'], '6A', faculty)
sixb = generate(subjects['6B'], '6B', faculty)
sixc = generate(subjects['6C'], '6C', faculty)
sixd = generate(subjects['6D'], '6D', faculty)

eighta = generate(subjects['8A'], '8A', faculty)
eightb = generate(subjects['8B'], '8B', faculty)
eightc = generate(subjects['8C'], '8C', faculty)
eightd = generate(subjects['8D'], '8D', faculty)


print_timetable(foura, 'IV A')
print_timetable(fourb, 'IV B')
print_timetable(fourc, 'IV C')
print_timetable(fourd, 'IV D')

print()

print_timetable(sixa, 'VI A')
print_timetable(sixb, 'VI B')
print_timetable(sixc, 'VI C')
print_timetable(sixd, 'VI D')

print()

print_timetable(eighta, 'VIII A')
print_timetable(eightb, 'VIII B')
print_timetable(eightc, 'VIII C')
print_timetable(eightd, 'VIII D')

print()

print_timetable(faculty['Mr. Ramesha Shettigar'], 'Mr. Ramesha', style = 'staff')


#ui methods
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.closeButton.clicked.connect(self.close)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())	