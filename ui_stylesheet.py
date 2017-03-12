css = '''
QPushButton{
	background-color: white;
	border: 2px solid gray;
	border-radius:4px;
}

QPushButton:hover{
	border-width:4px;
}

QPushButton:clicked{
	border-width:2px;
	background-color:gray;
}

QLineEdit:clicked{
	border:2px solid blue;
}

#trialwindow, #trialwindow2, #trialwindow3, #trialwindow4, #trialwindow5{
	background-color:white;
}

#addBtn:hover, #assignBtn:hover, #printBtn:hover, #saveBtn:hover{
	border-color:cyan;
}

#removeBtn:hover, #backBtn:hover{
	border-color:red;
}

#nextBtn:hover, #generateBtn:hover, #finishBtn:hover{
	border-color:green;
}

'''