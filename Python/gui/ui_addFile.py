# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddFile.ui'
#
# Created: Tue Sep 20 11:42:40 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_addFileDialog(object):
    def setupUi(self, addFileDialog):
        addFileDialog.setObjectName(_fromUtf8("addFileDialog"))
        addFileDialog.resize(400, 227)
        self.buttonBox = QtGui.QDialogButtonBox(addFileDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 170, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.headerToIncludeTextEdit = QtGui.QTextEdit(addFileDialog)
        self.headerToIncludeTextEdit.setGeometry(QtCore.QRect(20, 120, 271, 31))
        self.headerToIncludeTextEdit.setObjectName(_fromUtf8("headerToIncludeTextEdit"))
        self.fileNameTextEdit = QtGui.QTextEdit(addFileDialog)
        self.fileNameTextEdit.setGeometry(QtCore.QRect(20, 50, 271, 31))
        self.fileNameTextEdit.setObjectName(_fromUtf8("fileNameTextEdit"))
        self.selectFileButton = QtGui.QPushButton(addFileDialog)
        self.selectFileButton.setGeometry(QtCore.QRect(300, 60, 51, 23))
        self.selectFileButton.setObjectName(_fromUtf8("selectFileButton"))
        self.headerToIncludeLabel = QtGui.QLabel(addFileDialog)
        self.headerToIncludeLabel.setGeometry(QtCore.QRect(10, 100, 241, 16))
        self.headerToIncludeLabel.setObjectName(_fromUtf8("headerToIncludeLabel"))
        self.label_2 = QtGui.QLabel(addFileDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(addFileDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), addFileDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), addFileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(addFileDialog)

    def retranslateUi(self, addFileDialog):
        addFileDialog.setWindowTitle(QtGui.QApplication.translate("addFileDialog", "Agregar archivo", None, QtGui.QApplication.UnicodeUTF8))
        self.selectFileButton.setText(QtGui.QApplication.translate("addFileDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.headerToIncludeLabel.setText(QtGui.QApplication.translate("addFileDialog", "Header a incluir (ejemplo: myClasses/myClass.h):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("addFileDialog", "Archivo:", None, QtGui.QApplication.UnicodeUTF8))

