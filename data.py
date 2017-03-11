from collections import OrderedDict

def empty_timetable():
    tt = OrderedDict()
    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
        tt[day] = {1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: ''}
    tt['saturday'] = {1: '', 2: '', 3: '', 4: ''}
    return tt

faculty = { 'Mr. Venugopala P S': empty_timetable(),
    'Mr. Ravi B': empty_timetable(),
    'Mr. Radhakrishna Dodmane': empty_timetable(),
    'Mr. Pradeep Nazareth': empty_timetable(),
    'Mr. Sannidhan M S': empty_timetable(),
    'Mr. Roshan Fernandes': empty_timetable(),
    'Dr. Uday Kumar Shenoy': empty_timetable(),
    'Mr. Raghunandan K R': empty_timetable(),
    'Mrs. Shabari Shedthi B': empty_timetable(),
    'Mrs. Asmitha Poojari': empty_timetable(),
    'Dr. K R Uday Kumar Reddy': empty_timetable(),
    'Mrs. Sharada Uday Shenoy': empty_timetable(),
    'Mr. Raju K': empty_timetable(),
    'Mr. Ranjan Kumar H S': empty_timetable(),
    'Mrs. Pallavi K N': empty_timetable(),
    'Mr. Ramesha Shettigar': empty_timetable(),
    'Mr. Krishna Prasad Rao': empty_timetable(),
    'Mrs. Sarika Hegde': empty_timetable(),
    'Mrs. Savitha Shetty': empty_timetable(),
    'Dr. D K Sreekantha': empty_timetable(),
    'Mrs. Jyothi Shetty': empty_timetable(),
    'Mr. Sudeepa K B': empty_timetable(),
    'Mr. Pradeep Kanchan': empty_timetable(),
    'Mr. Vijay Murari T': empty_timetable(),
    'Dr. Mohammed Javed': empty_timetable(),
    'Mr. Chandra Naik': empty_timetable(),
    'Mrs. Anisha P Rodrigues': empty_timetable(),
    'Mr. K R Raghunandan': empty_timetable(),
    'Mrs. Minu P Abraham': empty_timetable(),
    'Mr. Sampath Kini': empty_timetable(),
    'Mr. Mahesh Kini': empty_timetable(),
    'Mr. H R Manjunath Prasad': empty_timetable(),
    'Mr. Naveen Chandavarkar': empty_timetable(),
    'Mr. Pawan Hegde': empty_timetable(),
    'Mrs. Keerthana B C': empty_timetable(),
    'Mr. Sunil Kumar Aithal': empty_timetable(),
    'Mr. Shashank Shetty': empty_timetable(),
    'Mr. Puneeth R P': empty_timetable(),
    'Mrs. Shilpa M K': empty_timetable(),
    "Mrs. Divya Jennifer D'Souza": empty_timetable(),
    'Mrs. Rajalaxmi Hegde': empty_timetable(),
    'Mr. Sandeep Hegde': empty_timetable(),
    'Ms. Swathi Pai M': empty_timetable(),
    'Ms. Ankitha A Nayak': empty_timetable(),
    'Ms. Rajashree': empty_timetable(),

    # maths 
    'Ms. Smitha G V': empty_timetable(),
    'Dr. Shashirekha B Rai': empty_timetable(),
    'Ms. Anitha D Bayar': empty_timetable(),
    "Ms. Apoorva D'Souza": empty_timetable(),
    #humanities
    'Mr. Rama Krishna': empty_timetable(),

    '': empty_timetable()
}


subjects = {'4A': (
                   ('Probability Theory and Numberical Methods', 4, 'Ms. Smitha G V', 'Maths'),
                   ('Design & Analysis of Algorithms', 4, 'Mr. Venugopala P S', 'DAA'),
                   ('Finite Automata & Formal languages', 4, 'Mr. Ravi B', 'FAFL'),
                   ('Data Communications', 4, 'Mr. Radhakrishna Dodmane', 'DC'),
                   ('Computer Organization & Architecture', 4, 'Mr. Pradeep Nazareth', 'CO'),
                   ('Unix Programming', 4, 'Mr. Sannidhan M S', 'Unix')
                   ),
             '4B': (
                   ('Probability Theory and Numberical Methods', 4, 'Dr. Shashirekha B Rai', 'Maths'),
                   ('Design & Analysis of Algorithms', 4, 'Mr. Roshan Fernandes', 'DAA'),
                   ('Finite Automata & Formal languages', 4, 'Mr. Radhakrishna Dodmane', 'FAFL'),
                   ('Data Communications', 4, 'Dr. Uday Kumar Shenoy', 'DC'),
                   ('Computer Organization & Architecture', 4, 'Mr. Raghunandan K R', 'CO'),
                   ('Unix Programming', 4, 'Mrs. Shabari Shedthi B', 'Unix')
                   ),
             '4C': (
                   ('Probability Theory and Numberical Methods', 4, 'Ms. Anitha D Bayar', 'Maths'),
                   ('Design & Analysis of Algorithms', 4, 'Mrs. Asmitha Poojari', 'DAA'),
                   ('Finite Automata & Formal languages', 4, 'Dr. K R Uday Kumar Reddy', 'FAFL'),
                   ('Data Communications', 4, 'Mrs. Sharada Uday Shenoy', 'DC'),
                   ('Computer Organization & Architecture', 4, 'Mr. Raju K', 'CO'),
                   ('Unix Programming', 4, 'Mr. Ranjan Kumar H S', 'Unix')
                   ),
             '4D': (
                   ('Probability Theory and Numberical Methods', 4, "Ms. Apoorva D'Souza", 'Maths'),
                   ('Design & Analysis of Algorithms', 4, 'Mrs. Pallavi K N', 'DAA'),
                   ('Finite Automata & Formal languages', 4, 'Mr. Ramesha Shettigar', 'FAFL'),
                   ('Data Communications', 4, 'Mr. Krishna Prasad Rao', 'DC'),
                   ('Computer Organization & Architecture', 4, 'Mrs. Sarika Hegde', 'CO'),
                   ('Unix Programming', 4, 'Mrs. Savitha Shetty', 'Unix')
                   ),
             '6A': (
                    ('', 4, 'Mrs. Shilpa M K', 'CG'),
                    ('', 4, 'Mr. Sudeepa K B', 'CN'),
                    ('', 4, 'Mr. Sandeep Hegde', 'JIT'),
                    ('', 3, 'Mr. Pradeep Nazareth', 'ST'),
                    ('', 3, 'Mr. Roshan Fernandes', 'CCIM'),
                    ('', 3, 'Mr. Ravi B', 'MC'),
                    ('', 1, 'Mr. Krishna Prasad Rao', 'ESD'),
                    ),
            '6B': (
                    ('', 4, 'Mr. Sannidhan M S', 'CG'),
                    ('', 4, 'Mr. Chandra Naik', 'CN'),
                    ('', 4, 'Mr. Ramesha Shettigar', 'JIT'),
                    ('', 3, 'Mrs. Rajalaxmi Hegde', 'ST'),
                    ('', 3, 'Mrs. Minu P Abraham', 'CCIM'),
                    ('', 3, 'Dr. Uday Kumar Shenoy', 'MC'),
                    ('', 1, 'Mr. Sunil Kumar Aithal', 'ESD'),
                    ),
            '6C': (
                    ('', 4, 'Mr. Pawan Hegde', 'CG'),
                    ('', 4, 'Mr. Vijay Murari T', 'CN'),
                    ('', 4, 'Mr. Mahesh Kini', 'JIT'),
                    ('', 3, 'Mrs. Shabari Shedthi B', 'ST'),
                    ('', 3, 'Mr. Venugopala P S', 'CCIM'),
                    ('', 3, 'Mrs. Sharada Uday Shenoy', 'MC'),
                    ('', 1, 'Mr. Sunil Kumar Aithal', 'ESD'),
                    ),
            '6D': (
                    ('', 4, 'Mrs. Jyothi Shetty', 'CG'),
                    ('', 4, 'Mr. Chandra Naik', 'CN'),
                    ('', 4, 'Mr. Sampath Kini', 'JIT'),
                    ('', 3, 'Dr. D K Sreekantha', 'ST'),
                    ('', 3, 'Mr. Pawan Hegde', 'CCIM'),
                    ('', 3, 'Mrs. Sharada Uday Shenoy', 'MC'),
                    ('', 1, 'Mrs. Shilpa M K', 'ESD'),
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
