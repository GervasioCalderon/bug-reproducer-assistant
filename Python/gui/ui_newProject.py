# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewProject.ui'
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

class Ui_newProjectDialog(object):
    def setupUi(self, newProjectDialog):
        newProjectDialog.setObjectName(_fromUtf8("newProjectDialog"))
        newProjectDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        newProjectDialog.resize(437, 646)
        self.languageComboBox = QtGui.QComboBox(newProjectDialog)
        self.languageComboBox.setGeometry(QtCore.QRect(40, 150, 191, 22))
        self.languageComboBox.setObjectName(_fromUtf8("languageComboBox"))
        self.languageComboBox.addItem(_fromUtf8(""))
        self.languageComboBox.addItem(_fromUtf8(""))
        self.label_2 = QtGui.QLabel(newProjectDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 130, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.projectNameTextEdit = QtGui.QTextEdit(newProjectDialog)
        self.projectNameTextEdit.setGeometry(QtCore.QRect(40, 30, 241, 31))
        self.projectNameTextEdit.setObjectName(_fromUtf8("projectNameTextEdit"))
        self.label_3 = QtGui.QLabel(newProjectDialog)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.projectsLocationEditBox = QtGui.QTextEdit(newProjectDialog)
        self.projectsLocationEditBox.setGeometry(QtCore.QRect(40, 90, 241, 31))
        self.projectsLocationEditBox.setObjectName(_fromUtf8("projectsLocationEditBox"))
        self.label_4 = QtGui.QLabel(newProjectDialog)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 71, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.projectsLocationSelectionButton = QtGui.QPushButton(newProjectDialog)
        self.projectsLocationSelectionButton.setGeometry(QtCore.QRect(290, 100, 21, 23))
        self.projectsLocationSelectionButton.setObjectName(_fromUtf8("projectsLocationSelectionButton"))
        self.exeCommandTextEdit = QtGui.QTextEdit(newProjectDialog)
        self.exeCommandTextEdit.setGeometry(QtCore.QRect(50, 330, 311, 31))
        self.exeCommandTextEdit.setObjectName(_fromUtf8("exeCommandTextEdit"))
        self.label_5 = QtGui.QLabel(newProjectDialog)
        self.label_5.setGeometry(QtCore.QRect(10, 310, 201, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(newProjectDialog)
        self.label_6.setGeometry(QtCore.QRect(10, 190, 71, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.mainFileEditBox = QtGui.QTextEdit(newProjectDialog)
        self.mainFileEditBox.setGeometry(QtCore.QRect(40, 210, 241, 31))
        self.mainFileEditBox.setReadOnly(True)
        self.mainFileEditBox.setObjectName(_fromUtf8("mainFileEditBox"))
        self.mainFileSelectionButton = QtGui.QPushButton(newProjectDialog)
        self.mainFileSelectionButton.setGeometry(QtCore.QRect(290, 210, 21, 23))
        self.mainFileSelectionButton.setObjectName(_fromUtf8("mainFileSelectionButton"))
        self.label_7 = QtGui.QLabel(newProjectDialog)
        self.label_7.setGeometry(QtCore.QRect(10, 250, 81, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.mainFunctionComboBox = QtGui.QComboBox(newProjectDialog)
        self.mainFunctionComboBox.setGeometry(QtCore.QRect(40, 270, 261, 22))
        self.mainFunctionComboBox.setObjectName(_fromUtf8("mainFunctionComboBox"))
        self.frame = QtGui.QFrame(newProjectDialog)
        self.frame.setGeometry(QtCore.QRect(20, 390, 391, 191))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.solutionEditBox = QtGui.QTextEdit(self.frame)
        self.solutionEditBox.setGeometry(QtCore.QRect(10, 30, 311, 31))
        self.solutionEditBox.setObjectName(_fromUtf8("solutionEditBox"))
        self.cppProjectEditBox = QtGui.QTextEdit(self.frame)
        self.cppProjectEditBox.setGeometry(QtCore.QRect(10, 90, 311, 31))
        self.cppProjectEditBox.setObjectName(_fromUtf8("cppProjectEditBox"))
        self.compilingCommandEditBox = QtGui.QTextEdit(self.frame)
        self.compilingCommandEditBox.setGeometry(QtCore.QRect(10, 150, 311, 31))
        self.compilingCommandEditBox.setObjectName(_fromUtf8("compilingCommandEditBox"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_8 = QtGui.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(10, 130, 221, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(10, 70, 46, 13))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.solutionSelectionButton = QtGui.QPushButton(self.frame)
        self.solutionSelectionButton.setGeometry(QtCore.QRect(330, 30, 21, 23))
        self.solutionSelectionButton.setObjectName(_fromUtf8("solutionSelectionButton"))
        self.cppProjectSelectionButton = QtGui.QPushButton(self.frame)
        self.cppProjectSelectionButton.setGeometry(QtCore.QRect(330, 100, 21, 23))
        self.cppProjectSelectionButton.setObjectName(_fromUtf8("cppProjectSelectionButton"))
        self.label_10 = QtGui.QLabel(newProjectDialog)
        self.label_10.setGeometry(QtCore.QRect(20, 370, 191, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.confirmationButtonBox = QtGui.QDialogButtonBox(newProjectDialog)
        self.confirmationButtonBox.setGeometry(QtCore.QRect(40, 590, 341, 32))
        self.confirmationButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.confirmationButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.confirmationButtonBox.setObjectName(_fromUtf8("confirmationButtonBox"))

        self.retranslateUi(newProjectDialog)
        QtCore.QObject.connect(self.confirmationButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), newProjectDialog.accept)
        QtCore.QObject.connect(self.confirmationButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), newProjectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(newProjectDialog)

    def retranslateUi(self, newProjectDialog):
        newProjectDialog.setWindowTitle(QtGui.QApplication.translate("newProjectDialog", "Nuevo Proyecto", None, QtGui.QApplication.UnicodeUTF8))
        self.languageComboBox.setItemText(0, QtGui.QApplication.translate("newProjectDialog", "C++", None, QtGui.QApplication.UnicodeUTF8))
        self.languageComboBox.setItemText(1, QtGui.QApplication.translate("newProjectDialog", "Python", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("newProjectDialog", "Lenguaje:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("newProjectDialog", "Nombre:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("newProjectDialog", "Ubicación:", None, QtGui.QApplication.UnicodeUTF8))
        self.projectsLocationSelectionButton.setText(QtGui.QApplication.translate("newProjectDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("newProjectDialog", "Comando para EJECUTAR el programa:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("newProjectDialog", "Archivo MAIN:", None, QtGui.QApplication.UnicodeUTF8))
        self.mainFileSelectionButton.setText(QtGui.QApplication.translate("newProjectDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("newProjectDialog", "Función main(): ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("newProjectDialog", "Solución:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("newProjectDialog", "Comando para compilar (BUILD) el programa:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("newProjectDialog", "Proyecto:", None, QtGui.QApplication.UnicodeUTF8))
        self.solutionSelectionButton.setText(QtGui.QApplication.translate("newProjectDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.cppProjectSelectionButton.setText(QtGui.QApplication.translate("newProjectDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("newProjectDialog", "Configuracion Visual Studio (sólo C++)", None, QtGui.QApplication.UnicodeUTF8))

