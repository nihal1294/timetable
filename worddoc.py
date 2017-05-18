'''

xml paths:
section timetable:
1st table:
t = root[0][6]
r1 = t[3]
u11 = r1[1] 
u11_text = c11[1][1][1].text
u12 = r1[2] etc
r2 = t[4] etc

2nd table:
t = root[0][10]
regular subjects:
r1 = t[3]
c11 = r1[1]
c11_text = c11[1][1][1].text
lab subjects:
row = t[5]
l1: r1[1]
l111: r1[2]
l112: r1[3]
l121: t[6][2]
l122: t[6][3]

section:
root[0][3][18][1].text - replace


personal timetable:
staff name: root[0][5][2][1].text
room no: 
r1: root[0][8]- p
	root[0][8][4][1].text
table: t = root[0][9]
r1 = t[3]
c11 = r1[2]
teaching workload:
w1: root[0][27][2][1].text - replace
w2: root[0][28][5][1].text
w3: root[0][29][3][1].text
'''

import xml.etree.ElementTree as ET
import zipfile
import os
import copy

day_row_num = {
	'monday': 0,
	'tuesday': 1,
	'wednesday': 2,
	'thursday': 3,
	'friday': 4,
	'saturday': 5
}

def print_faculty_wordxml(tt, faculty_subjects, subs):
	tree = ET.parse('template2.xml')
	root = tree.getroot()
	root[0][5][2][1].text = tt.name # name
	t = root[0][9] # table
	w1 = root[0][27][2][1] # teaching workloads
	w2 = root[0][28][5][1]
	w3 = root[0][29][3][1]
	
	reg_subs = []
	for f_s in faculty_subjects:
		sub, short_sub, sec = f_s.split(' - ')
		sub = subs[short_sub]
		if sub.lab == False:
			reg_subs.append((short_sub, sec))
	if len(reg_subs) > 0:
		r = root[0][8]
		r[4][1].text = '{} - {} - '.format(reg_subs[0][0], reg_subs[0][1])
		next_sub = 9
		for short_sub, sec in reg_subs[1:]:
			p = copy.deepcopy(r)
			p[4][1].text = '{} - {} - '.format(short_sub, sec)
			root[0].insert(next_sub, p)
	
	theory_units = 0
	lab_units = 0
	for day in tt:
		for timeslot in tt[day]:
			sub = tt[day][timeslot]
			if sub == '':
				sub = ' '
			else:
				sub = tt[day][timeslot][1][3]
				if subs[sub].lab == True:
					lab_units += 1
				else:
					theory_units += 2
			r = day_row_num[day] + 3
			c = timeslot + 1
			t[r][c][1][1][1].text = sub
			
	w1.text = w1.text.replace('w1', str(theory_units + lab_units))
	w2.text = str(theory_units)
	w3.text = str(lab_units)

	return ET.tostring(root)

def print_section_wordxml(tt, subjects_assigned, subs, faculty):
	tree = ET.parse('template.xml')
	root = tree.getroot()
	t1 = root[0][6]

	for day in tt:
		for timeslot in tt[day]:
			sub = tt[day][timeslot]
			if sub == '':
				sub = ' '
			else:
				sub = sub[3]
			r = day_row_num[day] +3
			c = timeslot +1
			t1[r][c][1][1][1].text = sub
			

	root[0][3][18][1].text = root[0][3][18][1].text.replace('s00', tt.name)	

	regular_subs = []
	labs = []
	for fac in subjects_assigned:
		sub_name, short_sub, fac = fac.split(' - ')
		sub = subs[short_sub]
		if sub.lab == True:
			lab = sub_name.split('|')
			fac = fac.split(', ')
			for i, lname in enumerate(lab):
				if lname.endswith(' Lab') == False:
					lname = lname + ' Lab'
				initials = ''.join(map(lambda x: x[0].upper(), fac[i].split(' ')))
				labs.append((lname, initials))
		else:
			regular_subs.append((sub_name, sub.subcode, str(faculty[faculty.index(fac)])))

	t2 = root[0][10]
	r = t2[3]
	labrow1 = t2[5]
	labrow2 = t2[6]
	r[1][1][1][1].text = regular_subs[0][1] # subject code
	r[2][1][1][1].text = regular_subs[0][0] # sub expansion
	r[3][1][1][1].text = regular_subs[0][2] # faculty
	t2_nextrow = 4
	for sub_name, subcode, faculty in regular_subs[1:]:
		r = copy.deepcopy(t2[3])
		r[1][1][1][1].text = subcode
		r[2][1][1][1].text = sub_name
		r[3][1][1][1].text = faculty
		t2.insert(t2_nextrow, r)
		t2_nextrow += 1

	if len(labs) > 0:
		r = labrow1
		sec = tt.name.split(' ')[1]
		r[1][1][1][1].text = labs[0][0]
		r[2][1][1][1].text = sec + '1'
		r[3][1][1][1].text = labs[0][1]
		r = labrow2
		r[2][1][1][1].text = sec + '2'
		r[3][1][1][1].text = labs[0][1]
		for labname, initials in labs[1:]:
			r = copy.deepcopy(labrow1)
			r[1][1][1][1].text = labname
			r[2][1][1][1].text = sec + '1'
			r[3][1][1][1].text = initials
			t2.append(r)
			r = copy.deepcopy(labrow2)
			r[2][1][1][1].text = sec + '2'
			r[3][1][1][1].text = initials
			t2.append(r)

	return ET.tostring(root)

def make_docx(tt, subjects_assigned, subs, filename, tt_type, faculty = None):
	if tt_type == 'section':
		xml_string = print_section_wordxml(tt, subjects_assigned, subs, faculty)
	else:
		xml_string = print_faculty_wordxml(tt, subjects_assigned, subs)
	with open(os.path.join('template', 'word', 'document.xml'), 'wb') as f:
		f.write(xml_string)
	file_paths = []
	os.chdir('template')
	for file in os.listdir():
		if os.path.isdir(file):
			for root, dirs, files in os.walk(file):
				for file in files:
					file_paths.append(os.path.join(root, file))
		else:
			file_paths.append(file)

	with zipfile.ZipFile(os.path.join('..', filename), 'w') as zf:
		for file in file_paths:
			zf.write(file)

	os.chdir('..')