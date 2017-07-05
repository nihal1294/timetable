# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_window.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import lightstyle

class Ui_aboutWindow(object):
    def setupUi(self, aboutWindow):
        aboutWindow.setObjectName("aboutWindow")
        aboutWindow.resize(800, 450)
        aboutWindow.setStyleSheet(lightstyle.css.replace('bgwlogo.png', 'img13.png'))
        aboutWindow.setWindowIcon(QtGui.QIcon('icons/favicon.ico'))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(aboutWindow.sizePolicy().hasHeightForWidth())
        aboutWindow.setSizePolicy(sizePolicy)
        aboutWindow.setMinimumSize(QtCore.QSize(800, 450))
        aboutWindow.setMaximumSize(QtCore.QSize(800, 450))
        self.gridLayoutWidget = QtWidgets.QWidget(aboutWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 441))
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 789, 331))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setGeometry(QtCore.QRect(50, 0, 671, 331))
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
        self.label_2.setObjectName("label_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 3, 0, 1, 3)

        self.retranslateUi(aboutWindow)
        QtCore.QMetaObject.connectSlotsByName(aboutWindow)

    def retranslateUi(self, aboutWindow):
        _translate = QtCore.QCoreApplication.translate
        aboutWindow.setWindowTitle(_translate("aboutWindow", "About"))
        self.closeBtn.setText(_translate("aboutWindow", "Close"))
        self.label.setText(_translate("aboutWindow", "🆃🅸🅼🅴🆃🅰🅱🅻🅴 🅶🅴🅽🅴🆁🅰🆃🅾🆁"))
        self.label_2.setText(_translate("aboutWindow", "𝑫𝒆𝒗𝒆𝒍𝒐𝒑𝒆𝒅 𝑩𝒚:\n"
"🅽🅸🅷🅰🅻 🆁🅰🅾 🅸\n"
"🆂🅰🅽🅹🅰🅽 🆂 🅿🅾🅾🅹🅰🆁🅸\n"
"🆂🅷🅸🆂🅷🅸🆁 🆄🅿🅰🅳🅷🆈🅰\n"
"\n"
"𝑼𝒏𝒅𝒆𝒓 𝒕𝒉𝒆 𝑮𝒖𝒊𝒅𝒂𝒏𝒄𝒆 𝒐𝒇:\n"
"🅼🆁. 🆁🅰🅼🅴🆂🅷🅰 🆂🅷🅴🆃🆃🅸🅶🅰🆁\n"
"𝗔𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 𝗣𝗿𝗼𝗳𝗲𝘀𝘀𝗼𝗿\n"
"𝗗𝗲𝗽𝗮𝗿𝘁𝗺𝗲𝗻𝘁 𝗼𝗳 𝗖𝗼𝗺𝗽𝘂𝘁𝗲𝗿 𝗦𝗰𝗶𝗲𝗻𝗰𝗲 & 𝗘𝗻𝗴𝗶𝗻𝗲𝗲𝗿𝗶𝗻𝗴\n"
"\n"
#"𝑭𝒐𝒓:\n"
"𝗡𝗠𝗔𝗠 𝗜𝗻𝘀𝘁𝗶𝘁𝘂𝘁𝗲 𝗼𝗳 𝗧𝗲𝗰𝗵𝗻𝗼𝗹𝗼𝗴𝘆, 𝗡𝗶𝘁𝘁𝗲"
" 𝟮𝟬𝟭𝟳"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    aboutWindow = QtWidgets.QDialog()
    ui = Ui_aboutWindow()
    ui.setupUi(aboutWindow)
    aboutWindow.show()
    sys.exit(app.exec_())
