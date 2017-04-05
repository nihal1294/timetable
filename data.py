from collections import OrderedDict

class timetable(OrderedDict):
    def __init__(self, name, fixedslots = False):
        self.name = name
        self.final = OrderedDict()
        for day in 'monday', 'tuesday', 'wednesday', 'thursday', 'friday':
            self[day] = OrderedDict({1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''})
            self.final[day] = OrderedDict({1: fixedslots, 2: fixedslots, 3: fixedslots, 4: fixedslots, 5: fixedslots, 6: fixedslots, 7: fixedslots, 8: fixedslots})
        self['saturday'] = {1: '', 2: '', 3: '', 4: ''}
        self.final['saturday'] = OrderedDict({1: fixedslots, 2: fixedslots, 3: fixedslots, 4: fixedslots})

    def calc_flexibility(self):
      flexibility = 0
      for day in 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday':
        for timeslot in self[day]:
          if self.final[day][timeslot] == False:
            flexibility += 1
      self.flexibility = flexibility/100.0

faculty = { 'Mr. Venugopala P S': timetable('Mr. Venugopala P S'),
    'Mr. Ravi B': timetable('Mr. Ravi B'),
    'Mr. Radhakrishna Dodmane': timetable('Mr. Radhakrishna Dodmane'),
    'Mr. Pradeep Nazareth': timetable('Mr. Pradeep Nazareth'),
    'Mr. Sannidhan M S': timetable('Mr. Sannidhan M S'),
    'Mr. Roshan Fernandes': timetable('Mr. Roshan Fernandes'),
    'Dr. Uday Kumar Shenoy': timetable('Dr. Uday Kumar Shenoy'),
    'Mr. Raghunandan K R': timetable('Mr. Raghunandan K R'),
    'Mrs. Shabari Shedthi B': timetable('Mrs. Shabari Shedthi B'),
    'Mrs. Asmitha Poojari': timetable('Mrs. Asmitha Poojari'),
    'Dr. K R Uday Kumar Reddy': timetable('Dr. K R Uday Kumar Reddy'),
    'Mrs. Sharada Uday Shenoy': timetable('Mrs. Sharada Uday Shenoy'),
    'Mr. Raju K': timetable('Mr. Raju K'),
    'Mr. Ranjan Kumar H S': timetable('Mr. Ranjan Kumar H S'),
    'Mrs. Pallavi K N': timetable('Mrs. Pallavi K N'),
    'Mr. Ramesha Shettigar': timetable('Mr. Ramesha Shettigar'),
    'Mr. Krishna Prasad Rao': timetable('Mr. Krishna Prasad Rao'),
    'Mrs. Sarika Hegde': timetable('Mrs. Sarika Hegde'),
    'Mrs. Savitha Shetty': timetable('Mrs. Savitha Shetty'),
    'Dr. D K Sreekantha': timetable('Dr. D K Sreekantha'),
    'Mrs. Jyothi Shetty': timetable('Mrs. Jyothi Shetty'),
    'Mr. Sudeepa K B': timetable('Mr. Sudeepa K B'),
    'Mr. Pradeep Kanchan': timetable('Mr. Pradeep Kanchan'),
    'Mr. Vijay Murari T': timetable('Mr. Vijay Murari T'),
    'Dr. Mohammed Javed': timetable('Dr. Mohammed Javed'),
    'Mr. Chandra Naik': timetable('Mr. Chandra Naik'),
    'Mrs. Anisha P Rodrigues': timetable('Mrs. Anisha P Rodrigues'),
    'Mr. K R Raghunandan': timetable('Mr. K R Raghunandan'),
    'Mrs. Minu P Abraham': timetable('Mrs. Minu P Abraham'),
    'Mr. Sampath Kini': timetable('Mr. Sampath Kini'),
    'Mr. Mahesh Kini': timetable('Mr. Mahesh Kini'),
    'Mr. H R Manjunath Prasad': timetable('Mr. H R Manjunath Prasad'),
    'Mr. Naveen Chandavarkar': timetable('Mr. Naveen Chandavarkar'),
    'Mr. Pawan Hegde': timetable('Mr. Pawan Hegde'),
    'Mrs. Keerthana B C': timetable('Mrs. Keerthana B C'),
    'Mr. Sunil Kumar Aithal': timetable('Mr. Sunil Kumar Aithal'),
    'Mr. Shashank Shetty': timetable('Mr. Shashank Shetty'),
    'Mr. Puneeth R P': timetable('Mr. Puneeth R P'),
    'Mrs. Shilpa M K': timetable('Mrs. Shilpa M K'),
    "Mrs. Divya Jennifer D'Souza": timetable("Mrs. Divya Jennifer D'Souza"),
    'Mrs. Rajalaxmi Hegde': timetable('Mrs. Rajalaxmi Hegde'),
    'Mr. Sandeep Hegde': timetable('Mr. Sandeep Hegde'),
    'Ms. Swathi Pai M': timetable('Ms. Swathi Pai M'),
    'Ms. Ankitha A Nayak': timetable('Ms. Ankitha A Nayak'),
    'Ms. Rajashree': timetable('Ms. Rajashree'),

    # maths 
    'Ms. Smitha G V': timetable('Ms. Smitha G V', fixedslots = True),
    'Dr. Shashirekha B Rai': timetable('Dr. Shashirekha B Rai', fixedslots = True),
    'Ms. Anitha D Bayar': timetable('Ms. Anitha D Bayar', fixedslots = True),
    "Ms. Apoorva D'Souza": timetable("Ms. Apoorva D'Souza", fixedslots = True),
    #humanities
    'Mr. Rama Krishna': timetable('Mr. Rama Krishna'),
    'Humanities': timetable('', fixedslots = True),
    
    '': timetable('')
}


subjects = {'4A': (
                   ('Probability Theory and Numberical Methods', 0, 'Ms. Smitha G V', 'Maths'),
                   ('Design & Analysis of Algorithms', 4, 'Mr. Venugopala P S', 'DAA'),
                   ('Finite Automata & Formal languages', 4, 'Mr. Ravi B', 'FAFL'),
                   ('Data Communications', 4, 'Mr. Radhakrishna Dodmane', 'DC'),
                   ('Computer Organization & Architecture', 4, 'Mr. Pradeep Nazareth', 'CO'),
                   ('Unix Programming', 4, 'Mr. Sannidhan M S', 'Unix'),
                   ('', 0, ('Mr. Venugopala P S', 'Mr. Sannidhan M S'), 'DAA/Unix Lab'),
                   ('', 0, 'Humanities', 'ESC')
                   ),
             '4B': (
                   ('Probability Theory and Numberical Methods', 0, 'Dr. Shashirekha B Rai', 'Maths'),
                   ('Design & Analysis of Algorithms', 4, 'Mr. Roshan Fernandes', 'DAA'),
                   ('Finite Automata & Formal languages', 4, 'Mr. Radhakrishna Dodmane', 'FAFL'),
                   ('Data Communications', 4, 'Dr. Uday Kumar Shenoy', 'DC'),
                   ('Computer Organization & Architecture', 4, 'Mr. Raghunandan K R', 'CO'),
                   ('Unix Programming', 4, 'Mrs. Shabari Shedthi B', 'Unix'),
                   ('', 0, ('Mrs. Shabari Shedthi B', 'Mr. Roshan Fernandes'), 'DAA/Unix Lab'),
                   ('', 0, 'Humanities', 'ESC')
                   ),
             '4C': (
                   ('Probability Theory and Numberical Methods', 0, 'Ms. Anitha D Bayar', 'Maths'),
                   ('Design & Analysis of Algorithms', 4, 'Mrs. Asmitha Poojari', 'DAA'),
                   ('Finite Automata & Formal languages', 4, 'Dr. K R Uday Kumar Reddy', 'FAFL'),
                   ('Data Communications', 4, 'Mrs. Sharada Uday Shenoy', 'DC'),
                   ('Computer Organization & Architecture', 4, 'Mr. Raju K', 'CO'),
                   ('Unix Programming', 4, 'Mr. Ranjan Kumar H S', 'Unix'),
                   ('', 0, ('Mrs. Asmitha Poojari', 'Mr. Ranjan Kumar H S'), 'DAA/Unix Lab'),
                   ('', 0, 'Humanities', 'ESC')
                   ),
             '4D': (
                   ('Probability Theory and Numberical Methods', 0, "Ms. Apoorva D'Souza", 'Maths'),
                   ('Design & Analysis of Algorithms', 4, 'Mrs. Pallavi K N', 'DAA'),
                   ('Finite Automata & Formal languages', 4, 'Mr. Ramesha Shettigar', 'FAFL'),
                   ('Data Communications', 4, 'Mr. Krishna Prasad Rao', 'DC'),
                   ('Computer Organization & Architecture', 4, 'Mrs. Sarika Hegde', 'CO'),
                   ('Unix Programming', 4, 'Mrs. Savitha Shetty', 'Unix'),
                   ('', 0, ('Mrs. Pallavi K N', 'Mrs. Savitha Shetty'), 'DAA/Unix Lab'),
                   ('', 0, 'Humanities', 'ESC')
                   ),
             '6A': (
                    ('', 4, 'Mrs. Shilpa M K', 'CG'),
                    ('', 4, 'Mr. Sudeepa K B', 'CN'),
                    ('', 4, 'Mr. Sandeep Hegde', 'JIT'),
                    ('', 3, 'Mr. Pradeep Nazareth', 'ST'),
                    ('', 0, 'Mr. Roshan Fernandes', 'CCIM'),
                    ('', 0, 'Mr. Ravi B', 'MC'),
                    ('', 1, 'Mr. Krishna Prasad Rao', 'ESD'),
                    ('', 0, ('Mrs. Shilpa M K', 'Mr. Sudeepa K B'), 'CG/CN Lab'),
                    ('', 0, ('Mr. Sandeep Hegde',), 'JIT Lab')
                    ),
            '6B': (
                    ('', 4, 'Mr. Sannidhan M S', 'CG'),
                    ('', 4, 'Mr. Chandra Naik', 'CN'),
                    ('', 4, 'Mr. Ramesha Shettigar', 'JIT'),
                    ('', 3, 'Mrs. Rajalaxmi Hegde', 'ST'),
                    ('', 0, 'Mrs. Minu P Abraham', 'CCIM'),
                    ('', 0, 'Dr. Uday Kumar Shenoy', 'MC'),
                    ('', 1, 'Mr. Sunil Kumar Aithal', 'ESD'),
                    ('', 0, ('Mr. Sannidhan M S', 'Mr. Chandra Naik'), 'CG/CN Lab'),
                    ('', 0, ('Mr. Ramesha Shettigar',), 'JIT Lab')
                    ),
            '6C': (
                    ('', 4, 'Mr. Pawan Hegde', 'CG'),
                    ('', 4, 'Mr. Vijay Murari T', 'CN'),
                    ('', 4, 'Mr. Mahesh Kini', 'JIT'),
                    ('', 3, 'Mrs. Shabari Shedthi B', 'ST'),
                    ('', 0, 'Mr. Venugopala P S', 'CCIM'),
                    ('', 0, 'Mrs. Sharada Uday Shenoy', 'MC'),
                    ('', 1, 'Mr. Sunil Kumar Aithal', 'ESD'),
                    ('', 0, ('Mr. Pawan Hegde', 'Mr. Vijay Murari T'), 'CG/CN Lab'),
                    ('', 0, ('Mr. Mahesh Kini',), 'JIT Lab')
                    ),
            '6D': (
                    ('', 4, 'Mrs. Jyothi Shetty', 'CG'),
                    ('', 4, 'Mr. Chandra Naik', 'CN'),
                    ('', 4, 'Mr. Sampath Kini', 'JIT'),
                    ('', 3, 'Dr. D K Sreekantha', 'ST'),
                    ('', 0, 'Mr. Pawan Hegde', 'CCIM'),
                    ('', 0, 'Mrs. Sharada Uday Shenoy', 'MC'),
                    ('', 1, 'Mrs. Shilpa M K', 'ESD'),
                    ('', 0, ('Mrs. Jyothi Shetty', 'Mr. Chandra Naik'), 'CG/CN Lab'),
                    ('', 0, ('Mr. Sampath Kini',), 'JIT Lab')
                    ),
            '8A': (
                    ('', 3, 'Mr. Rama Krishna', 'EM'),
                    ('', 3, 'Dr. Mohammed Javed', 'BA'),
                    ('', 3, 'Mr. Naveen Chandavarkar', 'BAI'),
                    ('', 3, '', 'OE'),
                    ),
            '8B': (
                    ('', 3, 'Mr. Rama Krishna', 'EM'),
                    ('', 3, 'Mrs. Anisha P Rodrigues', 'BA'),
                    ('', 3, 'Mr. Sunil Kumar Aithal', 'BAI'),
                    ('', 3, '', 'OE'),
                    ),
            '8C': (
                    ('', 3, 'Mr. Rama Krishna', 'EM'),
                    ('', 3, 'Mrs. Pallavi K N', 'IOT'),
                    ('', 3, "Mrs. Divya Jennifer D'Souza", 'SIC'),
                    ('', 3, '', 'OE'),
                    ),
            '8D': (
                    ('', 3, 'Mr. Rama Krishna', 'EM'),
                    ('', 3, 'Mrs. Asmitha Poojari', 'IOT'),
                    ('', 3, 'Mr. Vijay Murari T', 'SIC'),
                    ('', 3, '', 'OE'),
                    )
}