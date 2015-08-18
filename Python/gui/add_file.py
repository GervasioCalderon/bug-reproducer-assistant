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
Window to add a file to the current project.
'''
import os
import sys

from PyQt4.QtCore import pyqtSignature, QString, Qt, QVariant, SIGNAL, SLOT
from PyQt4.QtGui import *
from ui_addFile import Ui_addFileDialog
import os
import config
import project
from file_utils import normalizePathSeparators
from bug_reproducer_assistant.call_graph import ProgramExecution

##
# @param fileName Source code file name.
# @param language The program's programming language.
# @return Whether or not the file has a valid source code extension, according to the language.
def _validateExtension(fileName, language):
    '''
    Validate file extension to be an accepted source format.
    '''
    assert language in (ProgramExecution.Languages.C_PLUS_PLUS, ProgramExecution.Languages.PYTHON)
    if language == ProgramExecution.Languages.C_PLUS_PLUS:
        return fileName.endswith('.h')
    else:
        return fileName.endswith('.py')

##
# @param language The program's programming language.
# @return the extension filter, based on the language.
def _getSourceFileFilter(language):
    '''
    Return the extension filter, based on the language.
    '''
    LANG = ProgramExecution.Languages
    return '*.h' if language == LANG.C_PLUS_PLUS else '*.py'


class AddFileWindow(QDialog, Ui_addFileDialog):
    '''
    PyQt Window to add a file to the project.
    '''
    ##
    # @param self The AddFileWindow to construct.
    # @param parent Optional parent window.
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        theProjectsManager = project.projectsManagerInstance()
        self.currentProject_ = theProjectsManager.getProject(theProjectsManager.getCurrentProjectName())
        self.userHasEditedHeader_ = False

        self.selectedHeaderToInclude_ = ""
        self.selectedFileName_ = ""
        self.setupUi(self)
        self.createActions()
        self.loadControls()

    ##
    # @param self The AddFileWindow.
    def createActions(self):
        '''
        Create PyQt actions.
        '''
        self.connect(self.selectFileButton, SIGNAL("clicked()"),self, SLOT("selectFile()"))

    ##
    # @param self The AddFileWindow.
    def loadControls(self):
        '''
        Initial load of this window's controls.
        '''
        defaultPath = self.getDefaultSourcesFolder_()

        self.headerToIncludeTextEdit.setText("")
        if self.currentProject_.getLanguage() == ProgramExecution.Languages.C_PLUS_PLUS:
            self.headerToIncludeLabel.setText("Header a incluir (ejemplo: myClasses/myClass.h):")
        else:
            self.headerToIncludeLabel.setText("Import a incluir (ejemplo: myClasses.myClass):")
        self.fileNameTextEdit.setText(defaultPath)

    ##
    # @param self The AddFileWindow.
    # @return The selected "header to include".
    def getSelectedHeaderToInclude(self):
        '''
        Get the "header to include" selected by the user.
        '''
        return self.selectedHeaderToInclude_

    ##
    # @param self The AddFileWindow.
    # @return The file name "header to include".
    def getSelectedFileName(self):
        '''
        Get the file name selected by the user.
        '''
        return self.selectedFileName_

    ##
    # @param self The AddFileWindow.
    # @return The default folder for source files.
    def getDefaultSourcesFolder_(self):
        '''
        Return The default folder for source files.
        '''
        return os.path.dirname(self.currentProject_.getMainFile())
    
    ##
    # @param self The AddFileWindow.
    # @return True if the data is valid.
    def validateFileData_(self):
        '''
        Validate file data selected by the user.
        '''
        headerToInclude = str(self.headerToIncludeTextEdit.toPlainText())
        fileName = str(self.fileNameTextEdit.toPlainText())
        language = self.currentProject_.getLanguage()
        
        if not headerToInclude:
            QMessageBox.about(self, 'ERROR','Debe seleccionar un header para incluir.')
            self.headerToIncludeTextEdit.setFocus()
            return False
        if not os.path.exists(fileName):
            QMessageBox.about(self, 'ERROR','La ruta del archivo es invalida. Por favor, seleccione una correcta.')
            self.fileNameTextEdit.setFocus()
            return False
        if not _validateExtension(fileName, language):
            QMessageBox.about(self, 'ERROR','No es un archivo fuente ' + language + '.')
            self.fileNameTextEdit.setFocus()
            return False

        return True

    ## SLOTS
    @pyqtSignature("")
    ##
    # @param self The AddFileWindow.
    def accept(self):
        '''
        User accept. If data is valid, set file name and "header to include" to be consulted.
        '''
        ok = self.validateFileData_()
        if not ok:
            return

        self.selectedHeaderToInclude_ = str(self.headerToIncludeTextEdit.toPlainText())
        self.selectedFileName_ = str(self.fileNameTextEdit.toPlainText())
        QDialog.accept(self)

    @pyqtSignature("")
    ##
    # @param self The AddFileWindow. 
    def reject(self):
        '''
        User has cancelled.
        '''
        QDialog.reject(self)

    @pyqtSignature("")
    ##
    # @param self The AddFileWindow.
    def selectFile(self):
        '''
        User has selected "Select File" button.
        Open a file dialog, filtering according to the source extension.
        '''
        myConfig = config.instance()
        language = self.currentProject_.getLanguage()
        selectedFile = QFileDialog.getOpenFileName(self, 'Seleccione archivo fuente', str(self.fileNameTextEdit.toPlainText()), _getSourceFileFilter(language))
        if selectedFile:
            self.fileNameTextEdit.setText(selectedFile)
        
        #TODO GERVA: capturar evento de editar texto
        #y setear True userHasEditedHeader
        if not self.userHasEditedHeader_:
            defaultPath = self.getDefaultSourcesFolder_()
            fileName = str(self.fileNameTextEdit.toPlainText())
            
            #Normalize paths, to format the path to include
            defaultPath = normalizePathSeparators(defaultPath)
            fileName = normalizePathSeparators(fileName)
            if fileName.startswith(defaultPath):
                headerToInclude = fileName[len(defaultPath):]
                if headerToInclude.startswith('/'):
                    headerToInclude = headerToInclude[1:]
                if language == ProgramExecution.Languages.PYTHON:
                    #Get rid of extension
                    dotIndex = headerToInclude.rfind('.')
                    if dotIndex >= 0:
                        headerToInclude = headerToInclude[:dotIndex]
                    headerToInclude = headerToInclude.replace('/', '.')
                self.headerToIncludeTextEdit.setText(headerToInclude)