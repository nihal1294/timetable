#Copyright (C)  2017  Nihal Rao I, Sanjan S Poojari, Shishir Upadhya

from PyQt5 import QtCore, QtGui, QtWidgets
import lightstyle

class Ui_licenseWindow(object):
    def setupUi(self, licenseWindow):
        licenseWindow.setObjectName("licenseWindow")
        licenseWindow.setEnabled(True)
        licenseWindow.resize(950, 650)
        licenseWindow.setStyleSheet(lightstyle.css.replace('bgwlogo.png', 'img14.jpg'))
        licenseWindow.setWindowIcon(QtGui.QIcon('icons/favicon.ico'))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(licenseWindow.sizePolicy().hasHeightForWidth())
        licenseWindow.setSizePolicy(sizePolicy)
        licenseWindow.setMinimumSize(QtCore.QSize(950, 650))
        licenseWindow.setMaximumSize(QtCore.QSize(950, 650))
        licenseWindow.setSizeGripEnabled(False)
        licenseWindow.setModal(False)
        self.gridLayoutWidget = QtWidgets.QWidget(licenseWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 931, 631))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(5, 0, 5, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.logoLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.logoLabel.setText("")
        self.logoLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.logoLabel.setObjectName("logoLabel")
        self.gridLayout.addWidget(self.logoLabel, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.licenseBtn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.licenseBtn.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.licenseBtn.setFont(font)
        self.licenseBtn.setObjectName("licenseBtn")
        self.horizontalLayout.addWidget(self.licenseBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeBtn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.closeBtn.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.closeBtn.setFont(font)
        self.closeBtn.setObjectName("closeBtn")
        self.horizontalLayout.addWidget(self.closeBtn)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 3)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 4, 0, 1, 3)
        self.scrollArea = QtWidgets.QScrollArea(self.gridLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 919, 521))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 891, 501))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 219))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.label_2.setObjectName("label_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 3, 0, 1, 3)

        self.retranslateUi(licenseWindow)
        QtCore.QMetaObject.connectSlotsByName(licenseWindow)

    def retranslateUi(self, licenseWindow):
        _translate = QtCore.QCoreApplication.translate
        licenseWindow.setWindowTitle(_translate("licenseWindow", "License"))
        self.licenseBtn.setText(_translate("licenseWindow", "License"))
        self.closeBtn.setText(_translate("licenseWindow", "Close"))
        self.label.setText(_translate("licenseWindow", "🆃🅸🅼🅴🆃🅰🅱🅻🅴 🅶🅴🅽🅴🆁🅰🆃🅾🆁"))
        self.label_2.setText(_translate("licenseWindow", "𝗟𝗶𝗰𝗲𝗻𝘀𝗲:\n"
"\n"
"𝗧𝗶𝗺𝗲𝘁𝗮𝗯𝗹𝗲 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗼𝗿, 𝗮 𝘀𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝘁𝗼 𝗽𝗿𝗼𝗱𝘂𝗰𝗲 𝘁𝗶𝗺𝗲𝘁𝗮𝗯𝗹𝗲𝘀 𝗶𝗻 𝗮 𝘂𝗻𝗶𝘃𝗲𝗿𝘀𝗶𝘁𝘆\n"
" 𝗖𝗼𝗽𝘆𝗿𝗶𝗴𝗵𝘁 (𝗖) 𝟮𝟬𝟭𝟳 𝗡𝗶𝗵𝗮𝗹 𝗥𝗮𝗼 𝗜, 𝗦𝗮𝗻𝗷𝗮𝗻 𝗦 𝗣𝗼𝗼𝗷𝗮𝗿𝗶, 𝗦𝗵𝗶𝘀𝗵𝗶𝗿 𝗨𝗽𝗮𝗱𝗵𝘆𝗮\n"
"\n"
"This program is free software: you can redistribute it and/or modify it under the terms\n"
"of the 𝗚𝗡𝗨 𝗚𝗲𝗻𝗲𝗿𝗮𝗹 𝗣𝘂𝗯𝗹𝗶𝗰 𝗟𝗶𝗰𝗲𝗻𝘀𝗲 as published by the 𝗙𝗿𝗲𝗲 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲 𝗙𝗼𝘂𝗻𝗱𝗮𝘁𝗶𝗼𝗻,\n"
"either version 3 of the License, or (at your option) any later version.\n"
"\n"
"This program is distributed in the hope that it will be useful, but 𝗪𝗜𝗧𝗛𝗢𝗨𝗧 𝗔𝗡𝗬\n"
"𝗪𝗔𝗥𝗥𝗔𝗡𝗧𝗬; without even the implied warranty of 𝗠𝗘𝗥𝗖𝗛𝗔𝗡𝗧𝗔𝗕𝗜𝗟𝗜𝗧𝗬 or 𝗙𝗜𝗧𝗡𝗘𝗦𝗦 𝗙𝗢𝗥\n"
"𝗔 𝗣𝗔𝗥𝗧𝗜𝗖𝗨𝗟𝗔𝗥 𝗣𝗨𝗥𝗣𝗢𝗦𝗘. See the 𝗚𝗡𝗨 𝗚𝗲𝗻𝗲𝗿𝗮𝗹 𝗣𝘂𝗯𝗹𝗶𝗰 𝗟𝗶𝗰𝗲𝗻𝘀𝗲 for more details.\n"
"\n"
"Click on the \"𝗟𝗶𝗰𝗲𝗻𝘀𝗲\" button to view a copy of the 𝗚𝗡𝗨 𝗚𝗲𝗻𝗲𝗿𝗮𝗹 𝗣𝘂𝗯𝗹𝗶𝗰 𝗟𝗶𝗰𝗲𝗻𝘀𝗲\n"
"distributed along with this program. If not, see 𝗵𝘁𝘁𝗽𝘀://𝘄𝘄𝘄.𝗴𝗻𝘂.𝗼𝗿𝗴/𝗹𝗶𝗰𝗲𝗻𝘀𝗲𝘀/\n"
"\n"
"To get in touch with the developers, ping us on Twitter, @𝗻𝗶𝗵𝗮𝗹𝟭𝟮𝟵𝟰 or\n"
"@𝗦𝗮𝗻𝗷𝗮𝗻𝟵𝟱 or @𝘀𝘂𝗼𝗱𝗲𝘁𝗵"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    licenseWindow = QtWidgets.QDialog()
    ui = Ui_licenseWindow()
    ui.setupUi(licenseWindow)
    licenseWindow.show()
    sys.exit(app.exec_())

