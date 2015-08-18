# This file is part of Bug-reproducer Assistant
# The tool has been designed and developed by Gervasio Andres Calderon Fernandez, of Core Security Technologies
# 
# Copyright (c) 2011, Core Security Technologies
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE 
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
Configuration window. 
'''
from PyQt4.QtCore import pyqtSignature, QString, Qt, QVariant, SIGNAL, SLOT
from PyQt4.QtGui import *
import os
from ui_options import Ui_optionsDialog
import config

class OptionsWindow(QDialog, Ui_optionsDialog):
    '''
    PyQt configuration window.
    '''
    ##
    # @param self The OptionsWindow instance to construct.
    # @param parent Optional parent window.
    def __init__(self, parent = None):
        '''
        Constructor.
        '''
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.createActions()
        self.loadControls()

    ##
    # @param self The OptionsWindow.
    def createActions(self):
        '''
        Create PyQt actions.
        '''
        self.connect(self.cpp_defaultRootFolderSelectionButton, SIGNAL("clicked()"),self, SLOT("select_cpp_defaultRootFolder()"))
        self.connect(self.python_defaultRootFolderSelectionButton, SIGNAL("clicked()"),self, SLOT("select_python_defaultRootFolder()"))
        self.connect(self.visualStudioExeSelectionButton, SIGNAL("clicked()"),self, SLOT("selectVisualStudioExe()"))
        self.connect(self.boostIncludeFolderSelectionButton, SIGNAL("clicked()"),self, SLOT("selectBoostIncludeFolder()"))
        self.connect(self.boostLibraryFolderSelectionButton, SIGNAL("clicked()"),self, SLOT("selectBoostLibraryFolder()"))

    ##
    # @param self The OptionsWindow.
    def loadControls(self):
        '''
        Initial load of this window's controls.
        '''
        myConfig = config.instance()
        languageIndex = 0 if not myConfig.defaultLanguage else self.defaultLanguageComboBox.findText(myConfig.defaultLanguage) 
        self.defaultLanguageComboBox.setCurrentIndex(0)
        self.cpp_defaultRootFolderEditBox.setText(myConfig.cpp_defaultRootFolder)
        self.python_defaultRootFolderEditBox.setText(myConfig.python_defaultRootFolder)
        self.defaultCompilingCommandEditBox.setText(myConfig.defaultCompilingCommand)
        self.cpp_defaultExeCommandEditBox.setText(myConfig.cpp_defaultExeCommand)
        self.python_defaultExeCommandEditBox.setText(myConfig.python_defaultExeCommand)
        #Boost
        self.boostIncludeFolderEditBox.setText(myConfig.boostIncludeFolder)
        self.boostLibraryFolderEditBox.setText(myConfig.boostLibraryFolder)
        #Visual Studio controls
        self.visualStudioExeEditBox.setText(myConfig.visualStudioExe)
        self.solutionExtensionsEditBox.setText(myConfig.solutionExtensions)
        self.projectExtensionsEditBox.setText(myConfig.projectExtensions)

    ##
    # @param self The OptionsWindow.
    def validateOptions_(self):
        '''
        Validate data selected by the user.
        '''
        cppFolder = str(self.cpp_defaultRootFolderEditBox.toPlainText())
        if cppFolder and not os.path.exists(cppFolder):
            QMessageBox.about(self, 'ERROR','La ruta del directorio raiz de fuentes C++ es invalida. Por favor, seleccione una correcta.')
            self.cpp_defaultRootFolderEditBox.setFocus()
            return False
        pythonFolder = str(self.python_defaultRootFolderEditBox.toPlainText())
        if pythonFolder and not os.path.exists(pythonFolder):
            QMessageBox.about(self, 'ERROR','La ruta del directorio raiz de scripts Python es invalida. Por favor, seleccione una correcta.')
            self.python_defaultRootFolderEditBox.setFocus()
            return False
        boostIncludeFolder = str(self.boostIncludeFolderEditBox.toPlainText())
        if not boostIncludeFolder:
            QMessageBox.about(self, 'ERROR','Debe seleccionar un directorio de INCLUDE (.hpp) de Boost')
            self.boostIncludeFolderSelectionButton.setFocus()
            return False
        if not os.path.exists(boostIncludeFolder):
            QMessageBox.about(self, 'ERROR','La ruta del directorio de INCLUDE (.hpp) de Boost es invalida. Por favor, seleccione una correcta.')
            self.boostIncludeFolderSelectionButton.setFocus()
            return False
        boostLibraryFolder = str(self.boostIncludeFolderEditBox.toPlainText())
        if not boostLibraryFolder:
            QMessageBox.about(self, 'ERROR','Debe seleccionar un directorio de LIBRARIES (.lib) de Boost')
            self.boostIncludeFolderSelectionButton.setFocus()
            return False
        if not os.path.exists(boostLibraryFolder):
            QMessageBox.about(self, 'ERROR','La ruta del directorio de LIBRARIES (.lib) de Boost es invalida. Por favor, seleccione una correcta.')
            self.boostLibraryFolderSelectionButton.setFocus()
            return False
        return True

    ## SLOTS
    @pyqtSignature("")
    ##
    # @param self The OptionsWindow.
    def accept(self):
        '''
        User accept. If data is valid, save the options with the help of config.ConfigSerializer.
        '''
        ok = self.validateOptions_()
        if not ok:
            return
        myConfig = config.instance()
        myConfig.defaultLanguage = str(self.defaultLanguageComboBox.currentText())
        #C++
        myConfig.cpp_defaultRootFolder = str(self.cpp_defaultRootFolderEditBox.toPlainText())
        myConfig.defaultCompilingCommand = str(self.defaultCompilingCommandEditBox.toPlainText())
        myConfig.cpp_defaultExeCommand = str(self.cpp_defaultExeCommandEditBox.toPlainText())        
        #Visual Studio
        myConfig.visualStudioExe = str(self.visualStudioExeEditBox.toPlainText())
        myConfig.solutionExtensions = str(self.solutionExtensionsEditBox.toPlainText())
        myConfig.projectExtensions = str(self.projectExtensionsEditBox.toPlainText())        
        #Boost
        myConfig.boostIncludeFolder = str(self.boostIncludeFolderEditBox.toPlainText())
        myConfig.boostLibraryFolder = str(self.boostLibraryFolderEditBox.toPlainText())
        #Python
        myConfig.python_defaultRootFolder = str(self.python_defaultRootFolderEditBox.toPlainText())        
        myConfig.python_defaultExeCommand = str(self.python_defaultExeCommandEditBox.toPlainText())
            
        config.ConfigSerializer.saveConfig()
        QDialog.accept(self)
        
    @pyqtSignature("")
    ##
    # @param self The OptionsWindow.
    def reject(self):
        '''
        User has cancelled.
        '''
        QDialog.reject(self)
        

    @pyqtSignature("")
    ##
    # @param self The OptionsWindow.
    def select_cpp_defaultRootFolder(self):
        '''
        User selects the default folder for C++ sources.
        '''
        selectedFolder = QFileDialog.getExistingDirectory(self, 'Seleccione el directorio raiz de fuentes C++', str(self.cpp_defaultRootFolderEditBox.toPlainText()))
        if selectedFolder:
            self.cpp_defaultRootFolderEditBox.setText(selectedFolder)
        
    @pyqtSignature("")
    ##
    # @param self The OptionsWindow.    
    def select_python_defaultRootFolder(self):
        '''
        User selects Python default root folder.
        '''
        selectedFolder = QFileDialog.getExistingDirectory(self, 'Seleccione el directorio raiz de scripts Python', str(self.python_defaultRootFolderEditBox.toPlainText()))
        if selectedFolder:
            self.python_defaultRootFolderEditBox.setText(selectedFolder)

    @pyqtSignature("")
    ##
    # @param self The OptionsWindow.
    def selectVisualStudioExe(self):
        '''
        User selects Visual Studio executable path.
        '''
        selectedFile = QFileDialog.getOpenFileName(self, 'Seleccione el ejecutable de Visual Studio', str(self.visualStudioExeEditBox.toPlainText()), '*.exe')
        if selectedFile:
            self.visualStudioExeEditBox.setText(selectedFile)

    @pyqtSignature("")
    ##
    # @param self The OptionsWindow.    
    def selectBoostIncludeFolder(self):
        '''
        User selects Boost include folder.
        '''
        selectedFolder = QFileDialog.getExistingDirectory(self, 'Seleccione el directorio de INCLUDE (.hpp) de Boost', str(self.boostIncludeFolderEditBox.toPlainText()))
        if selectedFolder:
            self.boostIncludeFolderEditBox.setText(selectedFolder)

    @pyqtSignature("")
    ##
    # @param self The OptionsWindow.    
    def selectBoostLibraryFolder(self):
        '''
        User selects Boost library folder.
        '''
        selectedFolder = QFileDialog.getExistingDirectory(self, 'Seleccione el directorio de LIBRARIES (.lib) de Boost', str(self.boostLibraryFolderEditBox.toPlainText()))
        if selectedFolder:
            self.boostLibraryFolderEditBox.setText(selectedFolder)
   