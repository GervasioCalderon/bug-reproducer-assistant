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
Bug-reproducer Assistant main window.
'''
from __future__ import with_statement
import subprocess
import tempfile

import glob
import os

from PyQt4.QtCore import pyqtSignature, QString, Qt, QVariant, SIGNAL, SLOT
from PyQt4.QtGui import *
from bug_reproducer_assistant.code_generator import CodeGenerator
from bug_reproducer_assistant.code_generator import GeneratedSourceType
from bug_reproducer_assistant.call_graph import ProgramExecution
import config
import project
import file_utils
from options import OptionsWindow
from new_project import NewProjectWindow
from open_project import OpenProjectWindow
from add_file import AddFileWindow
from annotations_tree import TreeItemType
from annotations_tree import FileTreeItem
from annotations_tree import FunctionTreeItem
from annotations_tree import ClassTreeItem
from annotations_tree_widget import AnnotationsTreeWidgetItem
from executions_tree_widget import ExecutionsTreeWidgetItem
from annotations_tree_widget import getCheckedStateFromAnnotation
from ui_mainwindow import Ui_BugReproducerAssistant

##
# @return A temporary path for a Batch file.
def getAuxBatFilePath():
    '''
    Get a temporary path for a Batch file (to run the commands).
    '''
    return os.path.join(tempfile.gettempdir(), 'BRA_auxCommand.bat')

OUTPUT_WINDOW_PROMPT = ">>"

##
# @param language The current project's programming language.
# @return The file extension for this programming language.
def getExtensionByLanguage(language):
    '''
    Get file extension according to the programming language.
    '''
    return '.py' if language == ProgramExecution.Languages.PYTHON else '.cpp'

##
# @param executionPath Equivalente program's path.
# @param language The current project's programming language.
# @return the path for the equivalent program related to a program execution.
def getEquivalentProgramPathFromExecution(executionPath, language):
    '''
    Get the path for the equivalent program related to a program execution (Json database).
    '''
    return executionPath[:executionPath.rfind('.')] + getExtensionByLanguage(language)

##
# @param fileType This item file type (see ExecutionsTreeWidgetItem.FileType).
# @param filePath Path of the represented file.
# @return A new item for the executions tree.
def createExecutionsTreeWidgetItem(fileType, filePath):
    '''
    Create an item for the executions tree.
    '''
    fileName = os.path.basename(filePath)
    myTreeItem = ExecutionsTreeWidgetItem(fileType, filePath)
    myFont = myTreeItem.font(0)
    myFont.setBold(True)
    myTreeItem.setFont(0, myFont)
    myTreeItem.setText(0, fileName)
    myTreeItem.setCheckState(0, Qt.Unchecked)
    return myTreeItem

class MainWindow(QMainWindow, Ui_BugReproducerAssistant):
    '''
    PyQt main Window for Bug-reproducer Assistant program.
    '''
    ##
    # @param self The MainWindow to construct.
    # @param parent Optional parent window.    
    def __init__(self, parent = None):
        '''
        Constructor.
        '''
        self.folderNumber = 0
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.connect(self.actionExit, SIGNAL("triggered()"),qApp, SLOT("quit()"))
        self.createActions()
        self.outputStr_ = OUTPUT_WINDOW_PROMPT
        self.loadControls()
        #self.setWindowIcon(QIcon(r'images\icon.jpg'))
        config.ConfigSerializer.loadConfig()
        self.currentProject = None
        project.ProjectSerializer.loadProjectsList()
        if config.installationConfig().getIsFirstUse():
            config.installationConfig().setIsFirstUse(0)
            self.options()

    ##
    # @param self The MainWindow.
    def createActions(self):
        '''
        Create PyQt actions.
        '''
        self.connect(self.actionNewProject, SIGNAL("triggered()"),self, SLOT("newProject()"))
        self.connect(self.actionOpenProject, SIGNAL("triggered()"),self, SLOT("openProject()"))
        self.connect(self.actionEditProject, SIGNAL("triggered()"),self, SLOT("editProject()"))
        self.connect(self.actionCloseProject, SIGNAL("triggered()"),self, SLOT("closeProject()"))
        self.connect(self.actionOptions, SIGNAL("triggered()"),self, SLOT("options()"))
        self.connect(self.actionBraHelp, SIGNAL("triggered()"),self, SLOT("braHelp()"))
        self.connect(self.actionAbout, SIGNAL("triggered()"),self, SLOT("about()"))
        self.connect(self.newProjectButton, SIGNAL("clicked()"), self, SLOT("newProject()"))
        self.connect(self.openProjectButton, SIGNAL("clicked()"), self, SLOT("openProject()"))
        self.connect(self.editProjectButton, SIGNAL("clicked()"), self, SLOT("editProject()"))        
        self.connect(self.closeProjectButton, SIGNAL("clicked()"), self, SLOT("closeProject()"))
        self.connect(self.refreshProjectButton, SIGNAL("clicked()"), self, SLOT("refreshProject()"))
        self.connect(self.addFileButton, SIGNAL("clicked()"), self, SLOT("addFile()"))
        self.connect(self.projectExplorerTreeWidget, SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self, SLOT("changeAnnotationState(QTreeWidgetItem*, int)"))
        self.connect(self.compileProgramButton, SIGNAL("clicked()"),self, SLOT("compileProgram()"))
        self.connect(self.executeProgramButton, SIGNAL("clicked()"),self, SLOT("executeProgram()"))
        self.connect(self.generateEquivalentProgramButton, SIGNAL("clicked()"),self, SLOT("generateEquivalentProgram()"))
        self.connect(self.clearOutputButton, SIGNAL("clicked()"),self, SLOT("clearOutputWindow()"))
        #Executions Tab
        self.connect(self.executionsExplorerTreeWidget, SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self, SLOT("selectProgramExecutionItem(QTreeWidgetItem*, int)"))
        
    ##
    # @param self The MainWindow.
    def loadControls(self):
        '''
        Initial load of this window's controls.
        '''
        #Hide Project-related controls
        self.setVisibleProjectWidgets(False)

        self.refreshOutputWindow()

    ##
    # @param self The MainWindow.
    # @param enable If True, enable the controls. Else, disable them.
    def enableEditProjectControls(self, enable = True):
        '''
        Enable controls to edit current project.
        '''
        self.actionEditProject.setEnabled(enable)
        self.editProjectButton.setEnabled(enable)

    ##
    # @param self The MainWindow.
    # @param enable If True, enable the controls. Else, disable them.
    def setVisibleProjectWidgets(self, enable = True):
        '''
        Set/unset ALL controls visibility (for initial loading or immediately after closing a project). 
        '''
        self.enableEditProjectControls(enable)
        self.explorersTab.setVisible(enable)
        self.codeTextEdit.setVisible(enable)
        self.refreshProjectButton.setVisible(enable)

    ##
    # @param self The MainWindow.
    def refreshExecutionsTree(self):
        '''
        Refresh executions tree (some new executions databases may be found in disk,
        if the program has been run outside "Bug-reproducer Assistant").
        '''
        self.executionsExplorerTreeWidget.clear()
        self.compileProgramButton.setEnabled(self.currentProject.getLanguage() == ProgramExecution.Languages.C_PLUS_PLUS)
        self.unitTestRadioButton.setEnabled(self.currentProject.getLanguage() == ProgramExecution.Languages.PYTHON)
        if self.currentProject.getLanguage() == ProgramExecution.Languages.C_PLUS_PLUS:
            self.unitTestRadioButton.setChecked(False)
        self.generateEquivalentProgramButton.setEnabled(False)
        #TODO GERVA: por ahora solo cargo el main
        #despues guardo el resto de los archivos
        executionsFolder = self.currentProject.getExecutionsFolder()
        jsonFilesFilter = os.path.join(executionsFolder, "*.json")
        jsonFiles = glob.glob(jsonFilesFilter)
        for jsonFilePath in jsonFiles:
            jsonFileTreeItem = createExecutionsTreeWidgetItem(ExecutionsTreeWidgetItem.FileType.EXECUTION, jsonFilePath)
            ret = self.executionsExplorerTreeWidget.addTopLevelItem(jsonFileTreeItem)
            equivProgramPath = getEquivalentProgramPathFromExecution(jsonFilePath, self.currentProject.getLanguage())
            if os.path.exists(equivProgramPath):
                equivProgramTreeItem = createExecutionsTreeWidgetItem(ExecutionsTreeWidgetItem.FileType.EQUIV_PROGRAM, equivProgramPath)
                jsonFileTreeItem.addChild(equivProgramTreeItem)

    ##
    # @param self The MainWindow.
    def loadCurrentProject(self):
        '''
        Load the current project in this window.
        '''
        def loadFilesIntoTree():
            '''
            Load source files in annotations tree.
            '''
            self.projectExplorerTreeWidget.clear()
            #TODO GERVA: por ahora solo cargo el main
            #despues guardo el resto de los archivos
            mainFile = self.currentProject.getMainFile()
            mainFunction = self.currentProject.getMainFunction()
            mainFileCaption = "MAIN: " + mainFile
            
            myFileTreeItem = FileTreeItem(mainFile, headerToInclude = '')
            myWidgetItem = AnnotationsTreeWidgetItem(myFileTreeItem, mayAnnotate = False)
            myFont = myWidgetItem.font(0)
            myFont.setBold(True)
            myWidgetItem.setFont(0, myFont)
            myWidgetItem.setText(0, mainFileCaption)
            myWidgetItem.setCheckState(0, Qt.Unchecked)
            self.projectExplorerTreeWidget.addTopLevelItem(myWidgetItem)
            
            myFunctionTreeItem = FunctionTreeItem(mainFile, '', mainFunction)
            myFuncWidgetItem = AnnotationsTreeWidgetItem(myFunctionTreeItem, mayAnnotate = False)
            myFont = myFuncWidgetItem.font(0)
            myFont.setBold(True)
            myFuncWidgetItem.setFont(0, myFont)
            myFuncWidgetItem.setText(0, mainFunction)
            myFuncWidgetItem.setCheckState(0, Qt.Unchecked)
            myWidgetItem.addChild(myFuncWidgetItem)
            
            for fileToAnnotate, headerToInclude in self.currentProject.getTreeFiles():
                self.doAddFile_(fileToAnnotate, headerToInclude, refreshFile = False)
            
            self.refreshFileContents(mainFile)
                
        theProjectsManager = project.projectsManagerInstance()
        currentProjectName = theProjectsManager.getCurrentProjectName()
        if currentProjectName:
            self.currentProject = theProjectsManager.getProject(currentProjectName)
            loadFilesIntoTree()
            self.refreshExecutionsTree()
            self.setVisibleProjectWidgets(True)
        else:
            self.currentProject = None
            self.setVisibleProjectWidgets(False)

    ##
    # @param self The MainWindow.
    def storeCurrentProject(self):
        '''
        Store current project (in the ProjectsManager).
        '''
        theProjectsManager = project.projectsManagerInstance()
        theProjectsManager.storeAllProjects()

    ##
    # @param self The MainWindow.
    # @param fileName File path to display in the File Viewer.
    def refreshFileContents(self, fileName):
        '''
        Refresh a file contents in the File Viewer.
        '''
        with open(fileName, 'r') as f:
            fileContents = f.read()
            self.codeTextEdit.setPlainText(fileContents)

    ##
    # @param self The MainWindow.    
    def refreshOutputWindow(self):
        '''
        Refresh the output window (display the output string backed up in memory).
        '''
        self.outputWindowTextEdit.setPlainText(self.outputStr_)

    ##
    # @param self The MainWindow.
    # @param fileName File name of the source file to add.
    # @param headerToInclude Header to include.
    # @param refreshFile Refresh the file in the File Viewer.
    def doAddFile_(self, fileName, headerToInclude, refreshFile = False):
        '''
        Add a source file to the project.
        '''
        assert fileName and headerToInclude
        theProjectsManager = project.projectsManagerInstance()
        currentProject = theProjectsManager.getProject(theProjectsManager.getCurrentProjectName())
        myFileTreeItem = FileTreeItem(fileName, headerToInclude)
        myWidgetItem = AnnotationsTreeWidgetItem(myFileTreeItem)
        myWidgetItem.setText(0, fileName)
        myWidgetItem.setCheckState(0, Qt.Unchecked)
        self.projectExplorerTreeWidget.addTopLevelItem(myWidgetItem)
        language = currentProject.getLanguage()
        classes, functions = myFileTreeItem.getParser().getAllClassesAndFunctionsAnnotations(fileName, headerToInclude)
        
        for funcName, myAnnotationState in functions:
            myCheckedState = getCheckedStateFromAnnotation(myAnnotationState)
            myFunctionTreeItem = FunctionTreeItem(fileName, headerToInclude, funcName)
            myFuncWidgetItem = AnnotationsTreeWidgetItem(myFunctionTreeItem)
            myFuncWidgetItem.setText(0, funcName)
            myFuncWidgetItem.setCheckState(0, myCheckedState)
            myFuncWidgetItem.setIcon(0, QIcon("./images/code-function.ico"))
            myWidgetItem.addChild(myFuncWidgetItem)

        for className, myAnnotationState in classes:
            myCheckedState = getCheckedStateFromAnnotation(myAnnotationState)
            myClassTreeItem = ClassTreeItem(fileName, headerToInclude, className)
            myClassWidgetItem = AnnotationsTreeWidgetItem(myClassTreeItem)
            myClassWidgetItem.setText(0, className)
            myClassWidgetItem.setCheckState(0, myCheckedState)
            myClassWidgetItem.setIcon(0, QIcon("./images/code-class.ico"))
            myWidgetItem.addChild(myClassWidgetItem)
        
        if refreshFile:
            self.refreshFileContents(fileName)

    ## SLOTS
    @pyqtSignature("")
    ##
    # @param self The MainWindow.
    def newProject(self):
        '''
        User creates a project.
        '''
        myNewProjectWindow = NewProjectWindow(self)
        myNewProjectWindow.exec_()
        self.loadCurrentProject()

    @pyqtSignature("")
    ##
    # @param self The MainWindow.
    def openProject(self):
        '''
        User opens a project.
        '''
        myOpenProjectWindow = OpenProjectWindow(self)
        myOpenProjectWindow.exec_()
        self.loadCurrentProject()

    @pyqtSignature("")
    ##
    # @param self The MainWindow.
    def editProject(self):
        '''
        User changes current project settings.
        '''
        myEditProjectWindow = NewProjectWindow(self, self.currentProject)
        myEditProjectWindow.exec_()
        self.loadCurrentProject()

    @pyqtSignature("")
    ##
    # @param self The MainWindow.
    def closeProject(self):
        '''
        User closes the current project.
        Inform to the ProjectsManager that the current project is null,
        and make invisible the project-related controls.
        '''
        self.storeCurrentProject()
        self.currentProject = None
        theProjectsManager = project.projectsManagerInstance()
        theProjectsManager.setCurrentProjectName(None)
       
        self.setVisibleProjectWidgets(False)

    @pyqtSignature("")
    ##
    # @param self The MainWindow.    
    def options(self):
        '''
        User asks to change configuration.
        Show the OptionsWindow.
        '''
        myOptionsWindow = OptionsWindow(self)
        myOptionsWindow.show()

    @pyqtSignature("")
    ##
    # @param self The MainWindow.    
    def braHelp(self):
        '''
        User asks for help. Display the current version.
        '''
        helpProcess = subprocess.Popen(['explorer', 'Bug Reproducer Assistant Help.pdf'])

    @pyqtSignature("")
    ##
    # @param self The MainWindow.
    def about(self):
        '''
        User asks for information about this program.
        '''
        QMessageBox.about(self, "Acerca de Bug-reproducer Assistant","""                                BUG-REPRODUCER ASSISTANT   

El Bug-reproducer Assistant es una herramienta que extrae comportamiento de código en ejecución (Python o C++), generando un programa equivalente al original pero solamente con las funciones y clases elegidas por el programador.

Esta herramienta ha sido diseñada y desarrollada por Gervasio Andrés Calderón Fernández, de Core Security Technologies.
Por cualquier comentario y/o reporte de bugs, por favor escribir a gerva punto programmer at hotmail dot com.

Un agradecimiento especial al Lic. Aureliano Calvo (CoreLabs researcher, tutor de este proyecto en Core) por sus ideas innovadoras de diseño, y su gran apoyo (¡y paciencia!).
Y al Lic. Andrés Veiga, tutor del proyecto en la FIUBA, por apoyar este proyecto y encauzarlo para que sea completo y fácil de usar a la vez. 

INFORMACIÓN DE LICENCIA

Copyright (c) 2011, Core Security Technologies
All rights reserved.

 Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials
 provided with the distribution.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE 
 USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""")

    @pyqtSignature("")
    ##
    # @param self The MainWindow.
    def refreshProject(self):
        '''
        User refreshes project contents. This may be useful to refresh program executions in the tree,
        when the program is run from outside the BRA GUI.
        '''
        self.loadCurrentProject()
    
    @pyqtSignature("")
    ##
    # @param self The MainWindow.
    def addFile(self):
        '''
        User adds a File. The AddFileWindow is opened.
        '''
        myAddFileWindow = AddFileWindow(self)
        myAddFileWindow.exec_()
        headerToInclude = myAddFileWindow.getSelectedHeaderToInclude()
        fileName = myAddFileWindow.getSelectedFileName()
        if fileName and headerToInclude:
            #else -> user cancelled
            self.doAddFile_(fileName, headerToInclude, refreshFile = True)
            self.currentProject.addTreeFile((fileName, headerToInclude))
            project.projectsManagerInstance().storeAllProjects()

    @pyqtSignature("QTreeWidgetItem*, int")
    ##
    # @param self The MainWindow.
    # @param myItem The selected item.
    # @param index Selected item's index in the tree.
    def changeAnnotationState(self, myItem, index):
        '''
        User clicks an annotation tree item, to change the annotation state.
        '''
        def getFileToDisplay(theTreeItemComposite):
            getTreeItemFile = True
            lang = self.currentProject.getLanguage()
            if lang == ProgramExecution.Languages.PYTHON:
                myItemType = theTreeItemComposite.getTreeItemType()
                if myItemType != TreeItemType.FILE:
                    getTreeItemFile = False
            if getTreeItemFile:
                return theTreeItemComposite.getFileToAnnotate()
            else:
                return self.currentProject.getMainFile()
                
        mayAnnotate = myItem.mayAnnotate()
        if mayAnnotate:
            doAnnotate = myItem.checkState(0) == Qt.Checked
            if doAnnotate:
                myItem.annotate()
            else:
                myItem.unannotate()            
        else:
            myItem.setCheckState(0, Qt.Unchecked)
        filePath = getFileToDisplay(myItem.getTreeItemComposite())
        self.refreshFileContents(filePath)
        
    @pyqtSignature("")
    ##
    # @param self The MainWindow.
    def compileProgram(self):
        '''
        Compile the program.
        '''
        mainFile = self.currentProject.getMainFile()
        compilingCommand = self.currentProject.getCompilingCommand()
        solutionFile = self.currentProject.getSolutionFile()
        cppProjectFile = self.currentProject.getCppProject()
        projectName = self.currentProject.getName()
        compilingCommand = file_utils.replaceTags(compilingCommand, mainFile, projectName, solutionFile, cppProjectFile)
        commandAuxPath = getAuxBatFilePath()
        with open(commandAuxPath, 'w') as commandFile:
            commandFile.write(compilingCommand)
        compilingProcess = subprocess.Popen([commandAuxPath], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        outputStr = compilingProcess.stdout.read()
        self.outputStr_ += '\n'
        self.outputStr_ += outputStr
        self.outputStr_ += OUTPUT_WINDOW_PROMPT
        self.refreshOutputWindow()
    
    @pyqtSignature("")
    ##
    # @param self The MainWindow.
    def executeProgram(self):
        '''
        User executes the program.
        '''
        mainFile = self.currentProject.getMainFile()
        exeCommand = self.currentProject.getExeCommand()
        solutionFile = self.currentProject.getSolutionFile()
        cppProjectFile = self.currentProject.getCppProject()
        projectName = self.currentProject.getName()
        exeCommand = file_utils.replaceTags(exeCommand, mainFile, projectName, solutionFile, cppProjectFile)
        commandAuxPath = getAuxBatFilePath()
        with open(commandAuxPath, 'w') as commandFile:
            commandFile.write(exeCommand)
        compilingProcess = subprocess.Popen([commandAuxPath], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        outputStr = compilingProcess.stdout.read()
        self.outputStr_ += '\n'
        self.outputStr_ += outputStr
        self.outputStr_ += OUTPUT_WINDOW_PROMPT
        self.refreshOutputWindow()
        
        self.refreshExecutionsTree()
        

    @pyqtSignature("")
    ##
    # @param self The MainWindow.
    def generateEquivalentProgram(self):
        '''
        User asks to generate an equivalent program from the selected program execution.
        '''
        FT = ExecutionsTreeWidgetItem.FileType
        currentItem = self.executionsExplorerTreeWidget.currentItem()
        myType = currentItem.getFileType()
        if myType == FT.EXECUTION:
            dumpFileName = currentItem.getFilePath()
            equivProgramPath = getEquivalentProgramPathFromExecution(dumpFileName, self.currentProject.getLanguage())
            with open( dumpFileName, "r") as dumpFileFp:
                with open( equivProgramPath, "w") as equivProgramFp:
                    #Get equivalent program
                    myCodeGenerator = CodeGenerator(dumpFileFp, projectName = self.currentProject.getName())
                    mySourceType = GeneratedSourceType.UNIT_TEST if self.unitTestRadioButton.isChecked() else GeneratedSourceType.MAIN_FILE 
                    myCodeGenerator.generateEquivalentProgram(equivProgramFp, searchLevel = ProgramExecution.MIN_LEVEL, sourceType = mySourceType)
            equivProgramTreeItem = createExecutionsTreeWidgetItem(ExecutionsTreeWidgetItem.FileType.EQUIV_PROGRAM, equivProgramPath)
            currentItem.addChild(equivProgramTreeItem)
            self.refreshFileContents(equivProgramPath)

    @pyqtSignature("")
    ##
    # @param self The MainWindow.
    def clearOutputWindow(self):
        '''
        User clears the output window.
        '''
        self.outputStr_ = OUTPUT_WINDOW_PROMPT
        self.refreshOutputWindow()

    @pyqtSignature("QTreeWidgetItem*, int")
    ##
    # @param self The MainWindow.
    # @param myItem The selected item.
    # @param index Selected item's index in the tree.
    def selectProgramExecutionItem(self, myItem, index):
        '''
        User selects a file in the executions tree. Enable/disable the correspondent controls.
        '''
        myItem.setCheckState(0, Qt.Unchecked)
        filePath = myItem.getFilePath()
        myType = myItem.getFileType()
      
        FT = ExecutionsTreeWidgetItem.FileType
        if myType == FT.EXECUTION:
            equivProgramPath = getEquivalentProgramPathFromExecution(filePath, self.currentProject.getLanguage())
            self.generateEquivalentProgramButton.setEnabled(not os.path.exists(equivProgramPath))
        else:
            assert myType == FT.EQUIV_PROGRAM
            self.generateEquivalentProgramButton.setEnabled(False)
            
        self.refreshFileContents(filePath)

