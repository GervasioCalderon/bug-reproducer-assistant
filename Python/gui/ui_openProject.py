# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OpenProject.ui'
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

class Ui_openProjectDialog(object):
    def setupUi(self, openProjectDialog):
        openProjectDialog.setObjectName(_fromUtf8("openProjectDialog"))
        openProjectDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        openProjectDialog.resize(400, 300)
        self.confirmationButtonBox = QtGui.QDialogButtonBox(openProjectDialog)
        self.confirmationButtonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.confirmationButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.confirmationButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Open)
        self.confirmationButtonBox.setObjectName(_fromUtf8("confirmationButtonBox"))
        self.removeProjectButton = QtGui.QPushButton(openProjectDialog)
        self.removeProjectButton.setGeometry(QtCore.QRect(300, 30, 75, 23))
        self.removeProjectButton.setObjectName(_fromUtf8("removeProjectButton"))
        self.projectsListWidget = QtGui.QListWidget(openProjectDialog)
        self.projectsListWidget.setGeometry(QtCore.QRect(20, 20, 256, 192))
        self.projectsListWidget.setObjectName(_fromUtf8("projectsListWidget"))

        self.retranslateUi(openProjectDialog)
        QtCore.QObject.connect(self.confirmationButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), openProjectDialog.accept)
        QtCore.QObject.connect(self.confirmationButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), openProjectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(openProjectDialog)

    def retranslateUi(self, openProjectDialog):
        openProjectDialog.setWindowTitle(QtGui.QApplication.translate("openProjectDialog", "Abrir proyecto", None, QtGui.QApplication.UnicodeUTF8))
        self.removeProjectButton.setText(QtGui.QApplication.translate("openProjectDialog", "Eliminar", None, QtGui.QApplication.UnicodeUTF8))

