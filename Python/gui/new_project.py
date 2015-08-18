#!/usr/bin/env python
# -*- coding: latin-1 -*-

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
Window to add/edit a project.
'''
from PyQt4.QtCore import pyqtSignature, QString, Qt, QVariant, SIGNAL, SLOT
from PyQt4.QtGui import *
from ui_newProject import Ui_newProjectDialog
import sys
import os
import shutil
import config
import project
import parse_project
import file_utils


from bug_reproducer_assistant.source_code_parser import ProgramExecution
from bug_reproducer_assistant.source_code_parser import SourceCodeParser

class NewProjectWindow(QDialog, Ui_newProjectDialog):
    '''
    PyQt dialog to add or edit a project.
    '''
    ##
    # @param self The NewProjectWindow to construct.
    # @param parent Optional parent window.
    # @param projectToEdit In edition mode, project to edit. In "New" mode, None.
    def __init__(self, parent = None, projectToEdit = None):
        '''
        Constructor.
        '''
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.projectToEdit_ = projectToEdit        
        self.createActions()
        self.loadControls()

    ##
    # @param self The NewProjectWindow.
    def isEditMode_(self):
        '''
        Is "edition mode", i.e.: the project already exists and its properties are changed by the user.
        '''
        return self.projectToEdit_ is not None

    ##
    # @param self The NewProjectWindow.
    # @param enable If True, enable the controls. Else, disable them.
    def enableVisualStudioDependentControls(self, enable = True):
        '''
        Enable controls dependent on Visual Studio.
        '''
        self.solutionEditBox.setEnabled(enable)
        self.solutionSelectionButton.setEnabled(enable)
        self.compilingCommandEditBox.setEnabled(enable)
        self.cppProjectEditBox.setEnabled(enable)
        self.cppProjectSelectionButton.setEnabled(enable)

    ##
    # @param self The NewProjectWindow.
    # @param enable If True, enable the controls. Else, disable them.
    def enableLanguageDependentControls(self, enable = True):
        '''
        Enable controls related to the programming language.
        '''
        if self.isEditMode_():
            #Language and main file are immutable, because they're
            #the core of the project annotations.
            #If user wants to change them,
            #she should create another project.
            self.languageComboBox.setEnabled(False)
            self.mainFileEditBox.setEnabled(False)
        else:
            myConfig = config.instance()
            self.mainFileEditBox.setEnabled(enable)
            self.mainFileSelectionButton.setEnabled(enable)
            language = self.getSelectedLanguage_()
            LANG = ProgramExecution.Languages
            exeCommand = myConfig.cpp_defaultExeCommand if language == LANG.C_PLUS_PLUS else myConfig.python_defaultExeCommand  
            self.exeCommandTextEdit.setText(exeCommand)

        self.mainFunctionComboBox.setEnabled(enable)
        
        if self.getSelectedLanguage_() == ProgramExecution.Languages.C_PLUS_PLUS:
            self.enableVisualStudioDependentControls(enable)
        else:
            self.enableVisualStudioDependentControls(enable = False)

    ##
    # @param self The NewProjectWindow.
    def setDefaultsToLanguageDependentControls(self):
        '''
        Set default values for controls related to the programming language.
        '''
        if self.isEditMode_():
            mainFile = self.projectToEdit_.getMainFile()
            self.mainFileEditBox.setText(mainFile)
            self.loadMainFunctionComboBox_() 
        else:
            lang = self.getSelectedLanguage_()
            conf = config.instance()
            mainFile = conf.cpp_defaultRootFolder if lang == ProgramExecution.Languages.C_PLUS_PLUS else conf.python_defaultRootFolder
            self.mainFileEditBox.setText(mainFile)
        
        self.setDefaultsToVisualStudioDependentControls()

    ##
    # @param self The NewProjectWindow.
    def setDefaultsToVisualStudioDependentControls(self):
        '''
        Set default values for VS-related controls.
        For C++ projects, get them from the configuration.
        For Python, set null values (the controls are disabled anyway).
        '''
        self.cppProjectEditBox.setText("")
        lang = self.getSelectedLanguage_()
        
        if self.isEditMode_():
            solutionFile = self.projectToEdit_.getSolutionFile()
            compilingCommand = self.projectToEdit_.getCompilingCommand()
            cppProject = self.projectToEdit_.getCppProject()
        else:
            #No Python, but during loading time it may not be set
            if lang == ProgramExecution.Languages.C_PLUS_PLUS:
                myConfig = config.instance()
                solutionFile = myConfig.cpp_defaultRootFolder
                compilingCommand = myConfig.defaultCompilingCommand
                cppProject = myConfig.cpp_defaultRootFolder
            else:
                solutionFile = ""
                compilingCommand = ""
                cppProject = ""

        self.solutionEditBox.setText(solutionFile)
        self.compilingCommandEditBox.setText(compilingCommand)
        self.cppProjectEditBox.setText(cppProject)

    ##
    # @param self The NewProjectWindow.        
    def createActions(self):
        '''
        Create PyQt actions.
        '''
        self.connect(self.languageComboBox, SIGNAL("currentIndexChanged(int)"),self, SLOT("selectLanguage()"))
        self.connect(self.mainFileSelectionButton, SIGNAL("clicked()"),self, SLOT("selectMainFile()"))
        self.connect(self.projectsLocationSelectionButton, SIGNAL("clicked()"),self, SLOT("selectProjectsLocation()"))
        self.connect(self.solutionSelectionButton, SIGNAL("clicked()"),self, SLOT("selectSolution()"))
        self.connect(self.cppProjectSelectionButton, SIGNAL("clicked()"),self, SLOT("selectCppProject()"))

    ##
    # @param self The NewProjectWindow.        
    def loadControls(self):
        '''
        Initial load of this window's controls.
        '''
        self.enableVisualStudioDependentControls(enable = False)
        self.enableLanguageDependentControls(enable = False)
        if self.isEditMode_():
            projectName = self.projectToEdit_.getName() 
            projectsLocation = self.projectToEdit_.getFolder() 
            exeCommand = self.projectToEdit_.getExeCommand()
            language = self.projectToEdit_.getLanguage()
        else:
            myConfig = config.instance()
            projectName = ""
            projectsLocation = myConfig.getProjectsFolder()
            language = myConfig.defaultLanguage
            LANG = ProgramExecution.Languages
            exeCommand = myConfig.cpp_defaultExeCommand if language == LANG.C_PLUS_PLUS else myConfig.python_defaultExeCommand  
            
        self.projectNameTextEdit.setText(projectName)
        if self.isEditMode_():
            self.projectNameTextEdit.setEnabled(False)
        self.projectsLocationEditBox.setText(projectsLocation)
        self.exeCommandTextEdit.setText(exeCommand)

        languageIndex = 0 if not language else self.languageComboBox.findText(language)
        self.languageComboBox.setCurrentIndex(languageIndex)
        if languageIndex >= 0:
            self.languageHasBeenSelected_()          

    ##
    # @param self The NewProjectWindow.
    # @return The selected programming language.
    def getSelectedLanguage_(self):
        '''
        Get the selected programming language.
        '''
        return str(self.languageComboBox.currentText())

    ##
    # @param self The NewProjectWindow.
    # @return True if the data is valid.
    def validateProject_(self):
        '''
        Validate project data selected by the user.
        '''
        theProjectsManager = project.projectsManagerInstance()
        name = str(self.projectNameTextEdit.toPlainText())
        
        if not self.isEditMode_() and theProjectsManager.existsProject(name):
            QMessageBox.about(self, 'ERROR','El nombre de proyecto ya está siendo usado. Por favor, escoja uno diferente.')
            self.projectNameTextEdit.setFocus()
            return False

        folder = str(self.projectsLocationEditBox.toPlainText())
        if not os.path.exists(folder):
            QMessageBox.about(self, 'ERROR','La ruta del proyecto es inválida. Por favor, seleccione una correcta.')
            self.projectsLocationEditBox.setFocus()
            return False

        if self.getSelectedLanguage_() == ProgramExecution.Languages.C_PLUS_PLUS:
            solutionFile = str(self.solutionEditBox.toPlainText())
            if not self.validateSolution_(solutionFile, warnToUser = True):
                return False
    
            cppProject = str(self.cppProjectEditBox.toPlainText())
            if not self.validateCppProject_(cppProject, warnToUser = True):
                return False

        mainFile = str(self.mainFileEditBox.toPlainText())
        if not self.validateMainFile_(mainFile, warnToUser = True):
            return False
            
        return True

    ##
    # @param self The NewProjectWindow.
    # @param mainFile Main program file to validate.
    # @param warnToUser If True, inform any possible errors to the user.
    # @return True if the main file is valid.
    def validateMainFile_(self, mainFile, warnToUser = False):
        '''
        Validate main file selected by the user.
        '''
        if not os.path.exists(mainFile):
            if warnToUser:
                QMessageBox.about(self, 'ERROR','La ruta del archivo main del proyecto es inválida. Por favor, seleccione una correcta.')
                self.mainFileSelectionButton.setFocus()
            return False
        else:
            language = self.getSelectedLanguage_()
            LANG = ProgramExecution.Languages
            extensions = ['.c', '.cpp'] if language == LANG.C_PLUS_PLUS else ['.py']
            validExtension = False
            for ext in extensions:
                if mainFile.lower().endswith(ext):
                    validExtension = True
                    break
            if not validExtension:
                if warnToUser:
                    QMessageBox.about(self, 'ERROR', 'El archivo main no tiene una extensión correcta. Por favor, seleccione un archivo correcto.')
                    self.mainFileSelectionButton.setFocus()
                return False
        return True

    ##
    # @param self The NewProjectWindow.
    # @param selectionButton Selection button (where to focus in case of error).
    # @param filePath Path for the file to validate.
    # @param extensions Valid file extensions to validate.
    # @param noPathMessage Error message to the user when the path is invalid (for warnUser = True).
    # @param badExtensionMessage Error message to the user when the file extension is invalid (for warnUser = True).
    # @param warnToUser If True, inform any possible errors to the user.
    # @return True if the file is valid.
    def validateFile_(self, selectionButton, filePath, extensions, noPathMessage, badExtensionMessage, warnToUser):
        '''
        Generic function to a file selected by the user
        (call it with different parameters according to the type of file to validate).
        '''        
        if not os.path.exists(filePath):
            if warnToUser:
                QMessageBox.about(self, 'ERROR', noPathMessage)
                selectionButton.setFocus()
            return False
        else:
            extensionOk = False
            singleExtensions = extensions.split()
            for extension in singleExtensions:
                ext = extension.strip()
                dotIndex = ext.rfind('.')
                ending = ext if dotIndex == -1 else ext[dotIndex:]
                if filePath.lower().endswith(ending):
                    extensionOk = True
                    break
            if not extensionOk:
                if warnToUser:
                    QMessageBox.about(self, 'ERROR', badExtensionMessage)
                    selectionButton.setFocus()
                return False
        return True

    ##
    # @param self The NewProjectWindow
    # @param solutionFile Visual Stuido solution file to validate.
    # @param warnToUser If True, inform any possible errors to the user.
    # @return True if the Visual Studio solution is valid.
    def validateSolution_(self, solutionFile, warnToUser = True):
        '''
        Validate Visual Studio solution selected by the user.
        '''
        noPathMessage = 'La ruta de la solucion del proyecto es invalida. Por favor, seleccione una correcta.'
        badExtensionMessage = 'El archivo de la solucion no tiene una extension correcta (.sln). Por favor, seleccione una solucion valida.'
        return self.validateFile_(self.solutionSelectionButton, solutionFile, ".sln", noPathMessage, badExtensionMessage, warnToUser)

    ##
    # @param self The NewProjectWindow.
    # @param projectFile Visual Studio project path.
    # @param warnToUser If True, inform any possible errors to the user.
    # @return True if the Visual Studio project is valid.
    def validateCppProject_(self, projectFile, warnToUser = True):
        '''
        Validate Visual Studio project selected by the user.
        '''
        noPathMessage = 'La ruta del proyecto C++ es invalida. Por favor, seleccione una correcta.'
        projectExtensions = config.instance().projectExtensions
        badExtensionMessage = 'El archivo de la solucion no tiene una extension correcta (' + projectExtensions + '). Por favor, seleccione una solucion valida.'
        return self.validateFile_(self.cppProjectSelectionButton, projectFile, projectExtensions, noPathMessage, badExtensionMessage, warnToUser)

    ##
    # @param self The NewProjectWindow.
    def languageHasBeenSelected_(self):
        '''
        Call this function immediately after the language has changed.
        It fires other helper functions for language-dependent controls.
        '''
        self.enableLanguageDependentControls()
        self.setDefaultsToLanguageDependentControls()

    ##
    # @param self The NewProjectWindow.
    def loadMainFunctionComboBox_(self):
        '''
        Load combo box for main function.
        It uses a SourceCodeParser instance to get all the possible global functions.
        '''
        language = self.getSelectedLanguage_()
        self.mainFunctionComboBox.clear()
        mainFile = str(self.mainFileEditBox.toPlainText())
        if self.validateMainFile_(mainFile, warnToUser = False):
            mySourceCodeParser = SourceCodeParser(language, mainFile)
            _, functions = mySourceCodeParser.getAllClassesAndFunctions(mainFile)
            
            for funcName in functions:
                self.mainFunctionComboBox.addItem(funcName)
        
        if self.isEditMode_():
            mainFunctionIndex = self.mainFunctionComboBox.findText(self.projectToEdit_.getMainFunction())
            self.mainFunctionComboBox.setCurrentIndex(mainFunctionIndex)

    ##
    # @param self The NewProjectWindow.
    # @param cppProject Visual Studio project path.
    def addBraCustomInfoToCppProject_(self, cppProject):
        '''
        Add custom information to the Visual Studio project (additional libraries, preprocessor definitions, etc.)
        for the annotations to compile.
        It creates a backup to be restored when the "Bug-reproducer Assistant" project is removed. 
        '''
        cppProjectBkp = project.getCppProjectFileBackup(cppProject)
        shutil.copy(cppProject, cppProjectBkp)
        
        installationFolder = config.installationConfig().getInstallationFolder()

        additionalDependencies = ['bug_reproducer_assistant.lib', 'jsoncpp.lib']
        preprocessorDefinitions = ['BUG_REPRODUCER_ASSISTANT_ENABLED']
        BOOST_LIB_FOLDER = config.instance().boostLibraryFolder
        LIBRARIES_LIB_PREFIX = os.path.join(installationFolder, 'C++', 'libs')
        
        additionalLibraryDirectoriesDebug = [BOOST_LIB_FOLDER, os.path.join(LIBRARIES_LIB_PREFIX, 'Debug')] 
        additionalLibraryDirectoriesRelease = [BOOST_LIB_FOLDER, os.path.join(LIBRARIES_LIB_PREFIX, 'Release')]
        
        additionalIncludeDirectories = [config.instance().boostIncludeFolder, os.path.join(installationFolder, 'C++', 'include')]
        
        myBraCustomProjectInfo = parse_project.BraCustomProjectInfo(additionalDependencies, preprocessorDefinitions, additionalLibraryDirectoriesDebug, additionalLibraryDirectoriesRelease, additionalIncludeDirectories)

        myProjectParser = parse_project.ProjectParser(cppProjectBkp, cppProject, 'vcxproj', myBraCustomProjectInfo)
        myProjectParser.parseProject()
    
    ## SLOTS
    @pyqtSignature("")
    ##
    # @param self The NewProjectWindow.    
    def accept(self):
        '''
        User accept. If data is valid, store the project with the help of the ProjectManager.  
        '''
        ok = self.validateProject_()
        if not ok:
            return
        
        theProjectsManager = project.projectsManagerInstance()
        name = str(self.projectNameTextEdit.toPlainText())
        projectsFolder = str(self.projectsLocationEditBox.toPlainText())
        folder = os.path.join(projectsFolder, name)
        language = self.getSelectedLanguage_()
        solutionFile = str(self.solutionEditBox.toPlainText())
        cppProject = str(self.cppProjectEditBox.toPlainText())
        mainFile = str(self.mainFileEditBox.toPlainText())
        mainFunction = str(self.mainFunctionComboBox.currentText())
        compilingCommand = str(self.compilingCommandEditBox.toPlainText())
        exeCommand = str(self.exeCommandTextEdit.toPlainText())
        
        aProject = project.Project(name, folder, language, solutionFile, mainFile, mainFunction, exeCommand, [], cppProject, compilingCommand)
        #Annotate main file before adding it to the tree
        
        if self.isEditMode_():
            #If main function changed, unannotate previous main function
            previousMainFunction = self.projectToEdit_.getMainFunction()
            if mainFunction != previousMainFunction:
                mySourceCodeParser = SourceCodeParser(language, mainFile, previousMainFunction)
                mySourceCodeParser.unAnnotateMainFile()
        
        mySourceCodeParser = SourceCodeParser(language, mainFile, mainFunction)
        mainBackupFileName = mainFile + ".bkp"
        shutil.copyfile(mainFile, mainBackupFileName)
            
        dumpFileName = os.path.join(aProject.getExecutionsFolder(), name + ".json")
        mySourceCodeParser.annotateMainFile(dumpFileName)
        
        if language == ProgramExecution.Languages.C_PLUS_PLUS:
            self.addBraCustomInfoToCppProject_(cppProject)

        theProjectsManager.storeProject(aProject)
        theProjectsManager.setCurrentProjectName(aProject.getName())
        QDialog.accept(self)
        
    @pyqtSignature("")
    ##
    # @param self The NewProjectWindow.    
    def reject(self):
        '''
        User has cancelled.
        '''
        QDialog.reject(self)

    @pyqtSignature("")
    ##
    # @param self The NewProjectWindow.
    def selectProjectsLocation(self):
        '''
        User selects the project location in disk.
        '''
        selectedFolder = QFileDialog.getExistingDirectory(self, 'Seleccione directorio de proyectos', str(self.projectsLocationEditBox.toPlainText()))
        if selectedFolder:
            self.projectsLocationEditBox.setText(selectedFolder)
        
    @pyqtSignature("")
    ##
    # @param self The NewProjectWindow.    
    def selectCppProject(self):
        '''
        User selects the Visual Studio project.
        '''
        projectExtensions = config.instance().projectExtensions
        selectedFile = QFileDialog.getOpenFileName(self, 'Seleccione el proyecto de Visual Studio', str(self.cppProjectEditBox.toPlainText()), projectExtensions)
        if selectedFile:
            self.cppProjectEditBox.setText(selectedFile)

    @pyqtSignature("")
    ##
    # @param self The NewProjectWindow.    
    def selectSolution(self):
        '''
        User selects the Visual Studio solution.
        '''
        solutionExtensions = config.instance().solutionExtensions
        selectedFile = QFileDialog.getOpenFileName(self, 'Seleccione la solucion de Visual Studio', str(self.solutionEditBox.toPlainText()), solutionExtensions)
        if selectedFile:
            self.solutionEditBox.setText(selectedFile)

    @pyqtSignature("")
    ##
    # @param self The NewProjectWindow.
    def selectLanguage(self):
        '''
        User selects the programming language.
        '''
        self.languageHasBeenSelected_()
        
    @pyqtSignature("")
    ##
    # @param self The NewProjectWindow.    
    def selectMainFile(self):
        '''
        User selects the main file.
        '''
        language = self.getSelectedLanguage_()
        LANG = ProgramExecution.Languages
        extension = '*.c;*.cpp' if language == LANG.C_PLUS_PLUS else '*.py'
        selectedFile = QFileDialog.getOpenFileName(self, 'Seleccione el archivo main del proyecto', str(self.mainFileEditBox.toPlainText()), extension)
        if selectedFile:  
            self.mainFileEditBox.setText(selectedFile)
            self.loadMainFunctionComboBox_()