import random
from data import *
from collections import deque
import sys

'''
def getfreeslots1(tt):
	freeslots = []
	nonfinalslots = []
	for day in tt:
		for timeslot in tt[day]:
			if tt[day][timeslot] == '' and tt.final[day][timeslot] != True: # time slot is free
				freeslots.append((day, timeslot))
			elif tt.final[day][timeslot] != True:
				nonfinalslots.append((day, timeslot))
	return freeslots, nonfinalslots

def getfreeslots2(tt):
	freeslots = []
	nonfinalslots = []
	for timeslot in range(1, 8+1):
		for day in tt:
			if timeslot in tt[day]:
				if tt[day][timeslot] == '' and tt.final[day][timeslot] != True: # time slot is free
					freeslots.append((day, timeslot))
				elif tt.final[day][timeslot] != True:
					nonfinalslots.append((day, timeslot))
	return freeslots, nonfinalslots
'''

day_row_num = {
	'monday': 0,
	'tuesday': 1,
	'wednesday': 2,
	'thursday': 3,
	'friday': 4,
	'saturday': 5
}

def getfreeslots(tt):
	freeslots = []
	nonfinalslots = []
	for day in tt:
		for timeslot in range(1, 6+1):
			if timeslot in tt[day]:
				if tt[day][timeslot] == '' and tt.final[day][timeslot] != True: # time slot is free
					freeslots.append((day, timeslot))
				elif tt.final[day][timeslot] != True:
					nonfinalslots.append((day, timeslot))
	for day in tt:
		for timeslot in range(7, 8+1):
			if timeslot in tt[day]:
				if tt[day][timeslot] == '' and tt.final[day][timeslot] != True: # time slot is free
					freeslots.append((day, timeslot))
				elif tt.final[day][timeslot] != True:
					nonfinalslots.append((day, timeslot))
	return freeslots, nonfinalslots

def getnumhours(tt, subject, day):
	# return the number of hours of subject on a given day, and a list of those hours
	num = 0
	hours = []
	for timeslot in tt[day]:
		if tt[day][timeslot] != '' and subject[2] == tt[day][timeslot][2] and subject[3] == tt[day][timeslot][3]:
			num += 1
			hours.append(timeslot)
	return num, hours
	


def generate(tt, subjects, faculty): # subjects is a list of tuples (name, hours/week, teacher, short name); faculty is a dict
	remaining_hours = [i[1] for i in subjects]
	freeslots, _ = getfreeslots(tt)
	for _ in range(max(remaining_hours)): # repeat for as many times as the max credits 
		for i in range(len(subjects)): # iterate through all subjects, allot 1 hour for each subject
	#        print(tt.name, subject)
			if remaining_hours[i] > 0:
				subject = subjects[i]
				for day, time in freeslots:
					if faculty[subject[2]].final[day][time] != True and getnumhours(tt, subject, day)[0] < 1: # if teacher slot is not finalized and subject isnt already there that day
						tt[day][time] = subject
						faculty[subject[2]][day][time] = (tt.name, subject)
						remaining_hours[i] -= 1
						freeslots.remove((day, time))
						break
				else:
					'''
					print("no free slots for ", tt.name, subject)
					print_timetable(tt)
					print_timetable(faculty[subject[2]], style = 'staff')
					sys.exit()
					'''
					print("no free slots for ", tt.name, subject)
					dayclash.append((tt, subject))
	return tt

def print_timetable(tt, style = 'section', name = ''):
	if name == '':
		name = tt.name
	print(('%-20s ' * 9) % (name, '9:00-9:55', '9:55-10:50', '11:10-12:05', '12:05-1:00', '1:00-1:55', '1:55-2:50', '2:50-3:40', '3:40-4:30'))
	for day in tt:
		print('%-20s' % day, end = ' ')
		for timeslot in tt[day]:
			if tt[day][timeslot] == '':
				print('%-20s' % '-', end = ' ')
			else:

				if style == 'section':
					print('%-20s' % tt[day][timeslot][3], end = ' ')
				else:
					section = tt[day][timeslot][0]
					subject = tt[day][timeslot][1][3]
					print('%-20s' % (subject + ' (' + section + ')') , end = ' ')
		print()
	print()

def rehabilitate(day, section, subject, faculty):
	teacher = faculty[subject[2]]
	for timeslot in teacher[day]:
		if teacher[day][timeslot] == '' and teacher.final[day][timeslot] != True and getnumhours(section, subject, day)[0] < 1: # teacher is available
			if section.final[day][timeslot] != True: # time slot for that section is not finalized
				clashing_subject = section[day][timeslot]
				if clashing_subject != '': # whatever subject has been allotted, move it to clash
					clash.append((section, clashing_subject))
					clashing_teacher = clashing_subject[2]
					print(clashing_teacher)
					faculty[clashing_teacher][day][timeslot] = ''
				section.final[day][timeslot] = True # finalize the lecture by moving the new subject into the time slot
				section[day][timeslot] = subject
				teacher[day][timeslot] = (section.name, subject)
				teacher.final[day][timeslot] = True
				return
	else: # teacher has no free time slots where the lecture can be scheduled, on that day
		dayclash.append((section, subject))

def adjust_clash(timetables, faculty):
	for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
#        print(day)

		n_dayclash = len(dayclash)
		for i in range(n_dayclash):
			dayclash_ele = dayclash.popleft()
			rehabilitate(day, dayclash_ele[0], dayclash_ele[1], faculty)
		
		timeslots = 8 if day != 'saturday' else 4
		for timeslot in range(1, timeslots+1):
#            print(timeslot)
			for sem in timetables:
				for section in timetables[sem]:
					section = timetables[sem][section]
					if section[day][timeslot] != '' and section.final[day][timeslot] == False: # if lecture has not been finalized
						subject = section[day][timeslot]
						teacher = faculty[subject[2]]
						numhours, hours = getnumhours(section, subject, day)
						
						try:
							if teacher[day][timeslot] == '' and teacher.final[day][timeslot] != True:
								teacher[day][timeslot] = (section.name, subject)
								section.final[day][timeslot] = True
								teacher.final[day][timeslot] = True
							elif teacher[day][timeslot] != '' and (teacher[day][timeslot][0] != section.name or teacher[day][timeslot][1] != subject): # teacher is not available, there is a clash
								# teacher is not available
								# what if teacher takes 2 subjects for same section? 2nd condition takes care of this
								section[day][timeslot] = ''
								rehabilitate(day, section, subject, faculty)
							else: # if teacher is available, finalize the lecture 
								section.final[day][timeslot] = True
								teacher.final[day][timeslot] = True
						except Exception as e:
							print(section.name, subject, day, timeslot, faculty[subject[2]][day][timeslot])
							print_timetable(faculty[subject[2]], style = 'staff')
							print_timetable(section)
							raise 
		while len(clash) > 0:
			clash_ele = clash.popleft()
			rehabilitate(day, clash_ele[0], clash_ele[1], faculty)
		

def finalize_lab(section, day, time, subject):
	global faculty
	for i in range(time, time+3): # finalize 3 hours
		section[day][i] = subject
		section.final[day][i] = True
		for teacher in subject[2]:
			faculty[teacher][day][i] = (section.name, subject)
			faculty[teacher].final[day][i] = True

def finalize_theory(section, day, time, subject, hours = 1):
	global faculty
	for i in range(time, time+hours):
		section[day][i] = subject
		section.final[day][i] = True
		teacher = subject[2]
		faculty[teacher][day][i] = (section.name, subject)
		faculty[teacher].final[day][i] = True

def free_faculty(teacher, time, day = 'all'):
	if day == 'all':
		for day in 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday':
			if time == 'all':
				for i in range(1, 8+1):
					if i in teacher.final[day]:
						teacher.final[day][i] = True
			else:
				teacher.final[day][time] = True
	else:
		if time == 'all':
			for i in range(1, 8+1):
				if i in teacher.final[day]:
					teacher.final[day][i] = True
		else:
			teacher.final[day][time] = True

def produce_timetable(ui):
	global faculty
	global subjects
	global dayclash
	global clash
	dayclash = deque()
	clash = deque()

	faculty = dict()
	for member in ui.faculty_list_value:
		faculty[member] = timetable(member)
	subjects = dict()
	subjects_ref = dict()
	timetables = dict()
	for sem in ui.num_sections:
		if ui.num_sections[sem] > 0:
			subjects[sem] = dict()
			subjects_ref[sem] = dict()
			timetables[sem] = dict()
			for section in ui.sections[sem]:
				subjects[sem][section] = []
				subjects_ref[sem][section] = dict()
				timetables[sem][section] = timetable(sem + ' ' + section)
	for sem in ui.subjects_assigned:
		for section in ui.subjects_assigned[sem]:
			for sub in ui.subjects_assigned[sem][section]:
				sub_long, sub_short, staff = sub.split(' - ')
				print(sub_long, sub_short, staff)
				print(ui.subs)
				sub = ui.subs[sem][sub_short]
				s = [sub_long, sub.credits, staff, sub_short]
				subjects[sem][section].append(s)
				subjects_ref[sem][section][sub_short] = s
	print(subjects)
	for sem in ui.section_fixed_slots:
		for section in ui.section_fixed_slots[sem]:
			for row in ui.section_fixed_slots[sem][section]:
				for col in ui.section_fixed_slots[sem][section][row]:
					sub_short = ui.section_fixed_slots[sem][section][row][col]
					day = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')[row]
					hour = col+1
					if sub_short == '-':
						timetables[sem][section].final[day][hour] = True
					else:
						sub = subjects_ref[sem][section][sub_short]
						print(sub, row, col)
						if ui.subs[sem][sub_short].lab == True:
							#finalize_lab(timetables[sem][section], day, hour, sub)
							finalize_theory(timetables[sem][section], day, hour, sub)
						else:
							finalize_theory(timetables[sem][section], day, hour, sub)
			print_timetable(timetables[sem][section])
	for staff in ui.faculty_fixed_slots:
		for row in ui.faculty_fixed_slots[staff]:
			for column in ui.faculty_fixed_slots[staff][row]:
				day = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')[row]
				hour = column+1
				free_faculty(faculty[staff], hour, day)
	print('...generating...')
	for sem in timetables:
		for section in timetables[sem]:
			generate(timetables[sem][section], subjects[sem][section], faculty)
			print_timetable(timetables[sem][section])
	print_timetable(faculty[''], style = 'staff')
	print('...adjusting clashes...')
	adjust_clash(timetables, faculty)
	for sem in timetables:
		for section in timetables[sem]:
			print_timetable(timetables[sem][section])
	return timetables, faculty

if __name__ == '__main__':

	dayclash = deque()
	clash = deque()

	foura = timetable('4A')
	fourb = timetable('4B')
	fourc = timetable('4C')
	fourd = timetable('4D')
	sixa = timetable('6A')
	sixb = timetable('6B')
	sixc = timetable('6C')
	sixd = timetable('6D')
	eighta = timetable('8A')
	eightb = timetable('8B')
	eightc = timetable('8C')
	eightd = timetable('8D')

	# fixed slots
	# maths- A
	finalize_theory(foura, 'monday', 2, subjects['4A'][0])
	finalize_theory(foura, 'tuesday', 6, subjects['4A'][0])
	finalize_theory(foura, 'thursday', 4, subjects['4A'][0])
	finalize_theory(foura, 'saturday', 3, subjects['4A'][0])
	# labs- A
	finalize_lab(foura, 'wednesday', 2, subjects['4A'][6])
	finalize_lab(foura, 'friday', 6, subjects['4A'][6])
	# ESC - A
	finalize_theory(foura, 'monday', 3, subjects['4A'][7], hours=2)

	# maths - B
	finalize_theory(fourb, 'tuesday', 4, subjects['4B'][0])
	finalize_theory(fourb, 'wednesday', 6, subjects['4B'][0])
	finalize_theory(fourb, 'thursday', 1, subjects['4B'][0])
	finalize_theory(fourb, 'saturday', 1, subjects['4B'][0])
	# labs - B
	finalize_lab(fourb, 'monday', 6, subjects['4B'][6])
	finalize_lab(fourb, 'friday', 2, subjects['4B'][6])
	# ESC - B
	finalize_theory(fourb, 'wednesday', 3, subjects['4B'][7], hours=2)

	# maths - C
	finalize_theory(fourc, 'monday', 6, subjects['4C'][0])
	finalize_theory(fourc, 'tuesday', 4, subjects['4C'][0])
	finalize_theory(fourc, 'wednesday', 6, subjects['4C'][0])
	finalize_theory(fourc, 'thursday', 2, subjects['4C'][0])
	# labs - C
	finalize_lab(fourc, 'tuesday', 6, subjects['4C'][6])
	finalize_lab(fourc, 'saturday', 1, subjects['4C'][6])
	# ESC - C
	finalize_theory(fourc, 'wednesday', 7, subjects['4C'][7], hours=2)

	# maths - D
	finalize_theory(fourd, 'monday', 6, subjects['4D'][0])
	finalize_theory(fourd, 'tuesday', 6, subjects['4D'][0])
	finalize_theory(fourd, 'thursday', 3, subjects['4D'][0])
	finalize_theory(fourd, 'friday', 4, subjects['4D'][0])
	# labs - D
	finalize_lab(fourd, 'tuesday', 2, subjects['4D'][6])
	finalize_lab(fourd, 'wednesday', 6, subjects['4D'][6])
	# ESC - D
	finalize_theory(fourd, 'friday', 7, subjects['4D'][7], hours=2)

	# department constraints
	for section in foura, fourb, fourc, fourd, sixa, sixb, sixc, sixd, eighta, eightb, eightc, eightd:
		for day in 'monday', 'tuesday', 'wednesday', 'thursday', 'friday':
			section.final[day][5] = True # lunch break
		section.final['saturday'][4] = True # saturday
		for hour in 6,7,8: # thursday afternoon
			section.final['thursday'][hour] = True

	# faculty constraints
	free_faculty(faculty['Mr. Venugopala P S'], 1)
	free_faculty(faculty['Mr. Radhakrishna Dodmane'], 8)
	free_faculty(faculty['Dr. Uday Kumar Shenoy'], 1)
	free_faculty(faculty['Dr. K R Uday Kumar Reddy'], time = 'all', day = 'saturday')

	# 6th sem lab
	# CG/CN
	finalize_lab(sixa, 'monday', 2, subjects['6A'][7])
	finalize_lab(sixa, 'wednesday', 2, subjects['6A'][7])
	finalize_lab(sixb, 'tuesday', 1, subjects['6B'][7])
	finalize_lab(sixb, 'friday', 1, subjects['6B'][7])
	finalize_lab(sixc, 'tuesday', 6, subjects['6C'][7])
	finalize_lab(sixc, 'friday', 6, subjects['6C'][7])
	finalize_lab(sixd, 'monday', 6, subjects['6D'][7])
	finalize_lab(sixd, 'wednesday', 6, subjects['6D'][7])
	# JIT
	finalize_lab(sixa, 'tuesday', 6, subjects['6A'][8])
	finalize_lab(sixa, 'friday', 6, subjects['6A'][8])
	finalize_lab(sixb, 'monday', 6, subjects['6B'][8])
	finalize_lab(sixb, 'wednesday', 6, subjects['6B'][8])
	finalize_lab(sixc, 'monday', 1, subjects['6C'][8])
	finalize_lab(sixc, 'wednesday', 1, subjects['6C'][8])
	finalize_lab(sixd, 'tuesday', 1, subjects['6D'][8])
	finalize_lab(sixd, 'friday', 1, subjects['6D'][8])

	# 6th sem OE
	# CCIM/MBD
	finalize_theory(sixa, 'tuesday', 4, subjects['6A'][4])
	finalize_theory(sixa, 'thursday', 2, subjects['6A'][4])
	finalize_theory(sixa, 'saturday', 2, subjects['6A'][4])
	finalize_theory(sixb, 'tuesday', 4, subjects['6B'][4])
	finalize_theory(sixb, 'thursday', 2, subjects['6B'][4])
	finalize_theory(sixb, 'saturday', 2, subjects['6B'][4])
	finalize_theory(sixc, 'tuesday', 4, subjects['6C'][4])
	finalize_theory(sixc, 'thursday', 2, subjects['6C'][4])
	finalize_theory(sixc, 'saturday', 2, subjects['6C'][4])
	finalize_theory(sixd, 'tuesday', 4, subjects['6D'][4])
	finalize_theory(sixd, 'thursday', 2, subjects['6D'][4])
	finalize_theory(sixd, 'saturday', 2, subjects['6D'][4])

	# MCC/MCAP
	finalize_theory(sixa, 'thursday', 3, subjects['6A'][5])
	finalize_theory(sixa, 'friday', 4, subjects['6A'][5])
	finalize_theory(sixa, 'saturday', 1, subjects['6A'][5])
	finalize_theory(sixb, 'thursday', 3, subjects['6B'][5])
	finalize_theory(sixb, 'friday', 4, subjects['6B'][5])
	finalize_theory(sixb, 'saturday', 1, subjects['6B'][5])
	finalize_theory(sixc, 'thursday', 3, subjects['6C'][5])
	finalize_theory(sixc, 'friday', 4, subjects['6C'][5])
	finalize_theory(sixc, 'saturday', 1, subjects['6C'][5])
	finalize_theory(sixd, 'thursday', 3, subjects['6D'][5])
	finalize_theory(sixd, 'friday', 4, subjects['6D'][5])
	finalize_theory(sixd, 'saturday', 1, subjects['6D'][5])

	print_timetable(foura)
	print_timetable(fourb)
	print_timetable(fourc)
	print_timetable(fourd)

	print('... generating ...')
	generate(foura, subjects['4A'], faculty)
	generate(fourb, subjects['4B'], faculty)
	generate(fourc, subjects['4C'], faculty)
	generate(fourd, subjects['4D'], faculty)

	generate(sixa, subjects['6A'], faculty)
	generate(sixb, subjects['6B'], faculty)
	generate(sixc, subjects['6C'], faculty)
	generate(sixd, subjects['6D'], faculty)

	generate(eighta, subjects['8A'], faculty)
	generate(eightb, subjects['8B'], faculty)
	generate(eightc, subjects['8C'], faculty)
	generate(eightd, subjects['8D'], faculty)

	print_timetable(foura)
	print_timetable(fourb)
	print_timetable(fourc)
	print_timetable(fourd)
	print_timetable(eighta)
	print_timetable(eightb)
	print_timetable(eightc)
	print_timetable(eightd)
	print_timetable(faculty[''], style='staff')
	'''
	print_timetable(sixa)
	print_timetable(sixb)
	print_timetable(sixc)
	print_timetable(sixd)
	'''
	print('... adjusting clashes ...')
	timetables = OrderedDict({
		'IV': OrderedDict({
			'A': foura,
			'B': fourb,
			'C': fourc,
			'D': fourd
		}),
		'VI': OrderedDict({
			'A': sixa,
			'B': sixb,
			'C': sixc,
			'D': sixd
		}),
		'VIII': OrderedDict({
			'A': eighta,
			'B': eightb,
			'C': eightc,
			'D': eightd
		})
	})
	adjust_clash(timetables, faculty=faculty)
	adjust_clash(timetables, faculty=faculty)

	print_timetable(foura)
	print_timetable(fourb)
	print_timetable(fourc)
	print_timetable(fourd)
	print_timetable(sixa)
	print_timetable(sixb)
	print_timetable(sixc)
	print_timetable(sixd)

	print('... faculty timetable ...')
	print_timetable(faculty['Mr. Venugopala P S'], style = 'staff', name = 'Mr. Venugopal')
	print_timetable(faculty['Mr. Ramesha Shettigar'], style = 'staff', name = 'Mr. RS')
	#print_timetable(faculty['Dr. K R Uday Kumar Reddy'], style = 'staff', name = 'Mr. HOD')

	def print_dayclash():
		global dayclash
		for item in dayclash:
			print(item[0].name, item[1])
	print_dayclash()
	'''
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

	print_timetable(faculty['Mr. Ramesha Shettigar'], style = 'staff')
	'''