# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Options.ui'
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

class Ui_optionsDialog(object):
    def setupUi(self, optionsDialog):
        optionsDialog.setObjectName(_fromUtf8("optionsDialog"))
        optionsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        optionsDialog.resize(534, 664)
        self.confirmationButtonBox = QtGui.QDialogButtonBox(optionsDialog)
        self.confirmationButtonBox.setGeometry(QtCore.QRect(120, 630, 341, 32))
        self.confirmationButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.confirmationButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.confirmationButtonBox.setObjectName(_fromUtf8("confirmationButtonBox"))
        self.label_2 = QtGui.QLabel(optionsDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 91, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.defaultLanguageComboBox = QtGui.QComboBox(optionsDialog)
        self.defaultLanguageComboBox.setGeometry(QtCore.QRect(20, 30, 191, 22))
        self.defaultLanguageComboBox.setObjectName(_fromUtf8("defaultLanguageComboBox"))
        self.defaultLanguageComboBox.addItem(_fromUtf8(""))
        self.defaultLanguageComboBox.addItem(_fromUtf8(""))
        self.tabWidget = QtGui.QTabWidget(optionsDialog)
        self.tabWidget.setGeometry(QtCore.QRect(20, 60, 471, 571))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.cppTab = QtGui.QWidget()
        self.cppTab.setObjectName(_fromUtf8("cppTab"))
        self.label = QtGui.QLabel(self.cppTab)
        self.label.setGeometry(QtCore.QRect(10, 10, 151, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_4 = QtGui.QLabel(self.cppTab)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 271, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.cpp_defaultExeCommandEditBox = QtGui.QTextEdit(self.cppTab)
        self.cpp_defaultExeCommandEditBox.setGeometry(QtCore.QRect(20, 140, 381, 31))
        self.cpp_defaultExeCommandEditBox.setObjectName(_fromUtf8("cpp_defaultExeCommandEditBox"))
        self.cpp_defaultRootFolderEditBox = QtGui.QTextEdit(self.cppTab)
        self.cpp_defaultRootFolderEditBox.setGeometry(QtCore.QRect(20, 30, 381, 31))
        self.cpp_defaultRootFolderEditBox.setObjectName(_fromUtf8("cpp_defaultRootFolderEditBox"))
        self.label_5 = QtGui.QLabel(self.cppTab)
        self.label_5.setGeometry(QtCore.QRect(10, 120, 231, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.defaultCompilingCommandEditBox = QtGui.QTextEdit(self.cppTab)
        self.defaultCompilingCommandEditBox.setGeometry(QtCore.QRect(20, 90, 381, 31))
        self.defaultCompilingCommandEditBox.setObjectName(_fromUtf8("defaultCompilingCommandEditBox"))
        self.cpp_defaultRootFolderSelectionButton = QtGui.QPushButton(self.cppTab)
        self.cpp_defaultRootFolderSelectionButton.setGeometry(QtCore.QRect(410, 30, 21, 23))
        self.cpp_defaultRootFolderSelectionButton.setObjectName(_fromUtf8("cpp_defaultRootFolderSelectionButton"))
        self.frame = QtGui.QFrame(self.cppTab)
        self.frame.setGeometry(QtCore.QRect(20, 330, 361, 211))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.projectExtensionsEditBox = QtGui.QTextEdit(self.frame)
        self.projectExtensionsEditBox.setGeometry(QtCore.QRect(10, 160, 301, 31))
        self.projectExtensionsEditBox.setObjectName(_fromUtf8("projectExtensionsEditBox"))
        self.label_9 = QtGui.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(10, 10, 151, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.visualStudioExeSelectionButton = QtGui.QPushButton(self.frame)
        self.visualStudioExeSelectionButton.setGeometry(QtCore.QRect(320, 30, 21, 23))
        self.visualStudioExeSelectionButton.setObjectName(_fromUtf8("visualStudioExeSelectionButton"))
        self.visualStudioExeEditBox = QtGui.QTextEdit(self.frame)
        self.visualStudioExeEditBox.setGeometry(QtCore.QRect(10, 30, 301, 31))
        self.visualStudioExeEditBox.setObjectName(_fromUtf8("visualStudioExeEditBox"))
        self.label_8 = QtGui.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(10, 70, 271, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_10 = QtGui.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(10, 130, 131, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.solutionExtensionsEditBox = QtGui.QTextEdit(self.frame)
        self.solutionExtensionsEditBox.setGeometry(QtCore.QRect(10, 90, 301, 31))
        self.solutionExtensionsEditBox.setObjectName(_fromUtf8("solutionExtensionsEditBox"))
        self.label_7 = QtGui.QLabel(self.cppTab)
        self.label_7.setGeometry(QtCore.QRect(10, 310, 161, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.boostIncludeFolderSelectionButton = QtGui.QPushButton(self.cppTab)
        self.boostIncludeFolderSelectionButton.setGeometry(QtCore.QRect(410, 210, 21, 23))
        self.boostIncludeFolderSelectionButton.setObjectName(_fromUtf8("boostIncludeFolderSelectionButton"))
        self.boostLibraryFolderSelectionButton = QtGui.QPushButton(self.cppTab)
        self.boostLibraryFolderSelectionButton.setGeometry(QtCore.QRect(410, 270, 21, 23))
        self.boostLibraryFolderSelectionButton.setObjectName(_fromUtf8("boostLibraryFolderSelectionButton"))
        self.boostIncludeFolderEditBox = QtGui.QTextEdit(self.cppTab)
        self.boostIncludeFolderEditBox.setGeometry(QtCore.QRect(20, 210, 381, 31))
        self.boostIncludeFolderEditBox.setObjectName(_fromUtf8("boostIncludeFolderEditBox"))
        self.boostLibraryFolderEditBox = QtGui.QTextEdit(self.cppTab)
        self.boostLibraryFolderEditBox.setGeometry(QtCore.QRect(20, 270, 381, 31))
        self.boostLibraryFolderEditBox.setObjectName(_fromUtf8("boostLibraryFolderEditBox"))
        self.label_11 = QtGui.QLabel(self.cppTab)
        self.label_11.setGeometry(QtCore.QRect(20, 190, 141, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(self.cppTab)
        self.label_12.setGeometry(QtCore.QRect(20, 250, 171, 16))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(self.cppTab)
        self.label_13.setGeometry(QtCore.QRect(10, 180, 46, 13))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.tabWidget.addTab(self.cppTab, _fromUtf8(""))
        self.pythonTab = QtGui.QWidget()
        self.pythonTab.setObjectName(_fromUtf8("pythonTab"))
        self.label_6 = QtGui.QLabel(self.pythonTab)
        self.label_6.setGeometry(QtCore.QRect(10, 80, 231, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_3 = QtGui.QLabel(self.pythonTab)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 151, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.python_defaultRootFolderEditBox = QtGui.QTextEdit(self.pythonTab)
        self.python_defaultRootFolderEditBox.setGeometry(QtCore.QRect(20, 30, 381, 31))
        self.python_defaultRootFolderEditBox.setObjectName(_fromUtf8("python_defaultRootFolderEditBox"))
        self.python_defaultExeCommandEditBox = QtGui.QTextEdit(self.pythonTab)
        self.python_defaultExeCommandEditBox.setGeometry(QtCore.QRect(20, 100, 381, 31))
        self.python_defaultExeCommandEditBox.setObjectName(_fromUtf8("python_defaultExeCommandEditBox"))
        self.python_defaultRootFolderSelectionButton = QtGui.QPushButton(self.pythonTab)
        self.python_defaultRootFolderSelectionButton.setGeometry(QtCore.QRect(410, 30, 21, 23))
        self.python_defaultRootFolderSelectionButton.setObjectName(_fromUtf8("python_defaultRootFolderSelectionButton"))
        self.tabWidget.addTab(self.pythonTab, _fromUtf8(""))

        self.retranslateUi(optionsDialog)
        self.defaultLanguageComboBox.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.confirmationButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), optionsDialog.accept)
        QtCore.QObject.connect(self.confirmationButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), optionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(optionsDialog)

    def retranslateUi(self, optionsDialog):
        optionsDialog.setWindowTitle(QtGui.QApplication.translate("optionsDialog", "Opciones", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("optionsDialog", "Lenguaje default:", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultLanguageComboBox.setItemText(0, QtGui.QApplication.translate("optionsDialog", "C++", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultLanguageComboBox.setItemText(1, QtGui.QApplication.translate("optionsDialog", "Python", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("optionsDialog", "Raíz de los fuentes (default):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("optionsDialog", "Comando para compilar -BUILD- el programa (default):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("optionsDialog", "Comando para EJECUTAR el programa (default):", None, QtGui.QApplication.UnicodeUTF8))
        self.cpp_defaultRootFolderSelectionButton.setText(QtGui.QApplication.translate("optionsDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("optionsDialog", "Exe de Visual Studio:", None, QtGui.QApplication.UnicodeUTF8))
        self.visualStudioExeSelectionButton.setText(QtGui.QApplication.translate("optionsDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("optionsDialog", "Extensiones de solución:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("optionsDialog", "Extensiones de proyecto:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("optionsDialog", "Configuracion de Visual Studio:", None, QtGui.QApplication.UnicodeUTF8))
        self.boostIncludeFolderSelectionButton.setText(QtGui.QApplication.translate("optionsDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.boostLibraryFolderSelectionButton.setText(QtGui.QApplication.translate("optionsDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("optionsDialog", "Carpeta INCLUDE de boost:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("optionsDialog", "Carpeta de LIBRARIES de boost:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("optionsDialog", "Boost:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.cppTab), QtGui.QApplication.translate("optionsDialog", "C++", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("optionsDialog", "Comando para EJECUTAR el programa (default):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("optionsDialog", "Raíz de los fuentes (default):", None, QtGui.QApplication.UnicodeUTF8))
        self.python_defaultRootFolderSelectionButton.setText(QtGui.QApplication.translate("optionsDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pythonTab), QtGui.QApplication.translate("optionsDialog", "Python", None, QtGui.QApplication.UnicodeUTF8))
