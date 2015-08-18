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
Bug-reproducer Assistant project. It allows the user to map
in the GUI a program and its source files as a logical unit.
Each project has its own files list, program executions and equivalent programs.
'''
from __future__ import with_statement
import ctypes
import os
import sys
import simplejson as json
import shutil
import config
from file_utils import createFolderIfNotExists
from file_utils import removeFolder

from bug_reproducer_assistant.call_graph import ProgramExecution
from bug_reproducer_assistant.source_code_parser import SourceCodeParser

##
# @param cppProjectFile A C++ Visual Studio project.
# @return The backup filename for the C++ project.
def getCppProjectFileBackup(cppProjectFile):
    '''
    Gets the backup filename for the C++ project. It may be used to restore
    the original c++ project once the "Bug-reproducer Assistant" project is removed.
    '''
    return cppProjectFile + '.brabkp'

class Project:
    '''
    Bug-reproducer Assistant project: there is one per program
    to analize.
    '''
    ##
    # @param self The Project instance to construct.
    # @param name Project name.
    # @param folder Folder where the project data is stored.
    # @param language The program's programming language.
    # @param solutionFile Visual Studio solution file.
    # @param mainFile Program's main file.
    # @param mainFunction Program's main function.
    # @param exeCommand Command to execute the program.
    # @param treeFiles Source files displayed in the annotations tree.
    # @param cppProject Visual Studio C++ project.
    # @param compilingCommand Command to compile the program.
    def __init__(self, name, folder, language, solutionFile, mainFile, mainFunction, exeCommand="", treeFiles=[], cppProject="", compilingCommand=""):
        '''
        Constructor.
        '''
        self.name_ = name
        self.folder_ = folder
        self.language_ = language
        self.solutionFile_ = solutionFile
        self.mainFile_ = mainFile
        self.mainFunction_ = mainFunction
        self.exeCommand_ = exeCommand
        self.treeFiles_ = treeFiles
        self.compilingCommand_ = compilingCommand
        self.cppProject_ = cppProject

    ##
    # @param self The Project instance.    
    # @return The project name.
    def getName(self):
        '''
        Get the project name.
        '''
        return self.name_

    ##
    # @param self The Project instance.    
    # @return The Visual Studio solution file.
    def getSolutionFile(self):
        '''
        Get the Visual Studio solution file.
        '''
        return self.solutionFile_

    ##
    ##
    # @param self The Project instance.     
    # @return The folder where the project data is stored.
    def getFolder(self):
        '''
        Get the folder where the project data is stored.
        '''
        return self.folder_

    ##
    # @param self The Project instance.     
    # @return the folder where the program executions are stored.
    def getExecutionsFolder(self):
        '''
        Get the folder where the program executions
        (and their equivalent programs) are stored.
        '''
        return os.path.join(self.folder_, "Executions")

    ##
    # @param self The Project instance.
    # @return The program's programming language.
    def getLanguage(self):
        '''
        Get the program's programming language.
        '''
        return self.language_

    ##
    # @param self The Project instance.
    # @return The Visual Studio C++ project.
    def getCppProject(self):
        '''
        Get the Visual Studio C++ project.
        '''
        return self.cppProject_

    ##
    # @param self The Project instance.
    # @return The program's main file.
    def getMainFile(self):
        '''
        Get the program's main file.
        '''
        return self.mainFile_

    ##
    # @param self The Project instance.
    # @return The program's main function.
    def getMainFunction(self):
        '''
        Get the program's main function.
        '''
        return self.mainFunction_

    ##
    # @param self The Project instance.
    # @return The command to compile the program.
    def getCompilingCommand(self):
        '''
        Get the command to compile the program.
        '''
        return self.compilingCommand_

    ##
    # @param self The Project instance.
    # @return The command to execute the program.
    def getExeCommand(self):
        '''
        Get the command to execute the program.
        '''
        return self.exeCommand_

    # @param Source files displayed in the annotations tree.

    ##
    # @param self The Project instance.
    # @param treeFile A source file displayed in the annotations tree.
    def addTreeFile(self, treeFile):
        '''
        Add a source file displayed in the annotations tree.
        '''
        self.treeFiles_.append(treeFile)

    ##
    # @param self The Project instance.
    # @return The source files displayed in the annotations tree.
    def getTreeFiles(self):
        '''
        Get the source files displayed in the annotations tree.
        '''
        return self.treeFiles_

class ProjectSerializer:
    '''
    It loads/stores all the projects in disk, for persistence between runnings.
    '''
    NAME = 'name'
    LOCATION = 'location'
    LANGUAGE = 'language'
    SOLUTION_FILE = 'solutionFile'
    MAIN_FILE = 'mainFile'
    MAIN_FUNCTION = 'mainFunction'
    EXE_COMMAND = 'exeCommand'
    TREE_FILES = 'treeFiles'
    COMPILING_COMMAND = 'compilingCommand'
    CPP_PROJECT = 'cppProject'
    FILE_TO_ANNOTATE = 'fileToAnnotate'
    HEADER_TO_INCLUDE = 'headerToInclude'
    PROJECT_SETTINGS_FILE_NAME = 'projectSettings.json'
    INDEX_FILE_NAME = 'projects.json'
    INDENT = 4
    
    @staticmethod
    ##
    # @return All the loaded projects.
    def loadProjectsList():
        '''
        Load the projects from disk into memory.
        '''
        ##
        # @param projectMap A project represented as a map, to ease Json-serialization.
        # @return The source files to be displayed in the annotations tree.
        def loadTreeFiles(projectMap):
            '''
            Load the source files to be displayed in the annotations tree.
            '''
            treeFiles = []
            jsonTreeFiles = projectMap[ProjectSerializer.TREE_FILES]
            for jsonTreeFile in jsonTreeFiles:
                fileToAnnotate = jsonTreeFile[ProjectSerializer.FILE_TO_ANNOTATE]
                headerToInclude = jsonTreeFile[ProjectSerializer.HEADER_TO_INCLUDE]
                myTreeFile = fileToAnnotate, headerToInclude
                treeFiles.append(myTreeFile)
            return treeFiles
            
        projects = {}
        #First, get all projects information
        dataFolder = config.installationConfig().getDataFolder()
        indexFilePath = os.path.join(dataFolder, ProjectSerializer.INDEX_FILE_NAME)
        
        if os.path.exists(indexFilePath):
            with open(indexFilePath, 'r') as fp:
                projectsIndexMap = json.load(fp)
            
            for projectName, projectFolder in projectsIndexMap.items():
                
                projectConfigPath = os.path.join(projectFolder, ProjectSerializer.PROJECT_SETTINGS_FILE_NAME)
                with open(projectConfigPath, 'r') as fp:
                    projectMap = json.load(fp)
    
                name = projectMap[ProjectSerializer.NAME]
                folder = projectMap[ProjectSerializer.LOCATION]
                language = projectMap[ProjectSerializer.LANGUAGE]
                solutionFile = projectMap[ProjectSerializer.SOLUTION_FILE]
                mainFile = projectMap[ProjectSerializer.MAIN_FILE]
                mainFunction = projectMap[ProjectSerializer.MAIN_FUNCTION]
                exeCommand = projectMap[ProjectSerializer.EXE_COMMAND]
                treeFiles = loadTreeFiles(projectMap)
                compilingCommand = projectMap[ProjectSerializer.COMPILING_COMMAND]
                cppProject = projectMap[ProjectSerializer.CPP_PROJECT]
               
                if projectName != name:
                    raise RuntimeError('Inconsistency between project names: "' + projectName + '", "' + name + '". Check configuration folders.')

                aProject = Project(name, folder, language, solutionFile, mainFile, mainFunction, exeCommand, treeFiles, cppProject, compilingCommand)
                projects[name] = aProject
        return projects

    @staticmethod
    ##
    # @param allProjects All the projects to store.
    def saveProjectsList(allProjects):
        '''
        Store all the projects from memory into disk.
        '''
        def saveTreeFiles(treeFiles):
            jsonTreeFiles = []
            for myTreeFile in treeFiles:
                jsonTreeFile = {}
                jsonTreeFile[ProjectSerializer.FILE_TO_ANNOTATE] = myTreeFile[0]
                jsonTreeFile[ProjectSerializer.HEADER_TO_INCLUDE] = myTreeFile[1]
                jsonTreeFiles.append(jsonTreeFile)
            return jsonTreeFiles
        
        #First, save in all projects information
        dataFolder = config.installationConfig().getDataFolder()
        indexFilePath = os.path.join(dataFolder, ProjectSerializer.INDEX_FILE_NAME)
        
        projectsIndexMap = {}
        for projectName, aProject in allProjects.items():
            projectsIndexMap[projectName] = aProject.getFolder()
            #Now, save current project
            projectMap = {}
            projectMap[ProjectSerializer.NAME] = aProject.getName()
            projectMap[ProjectSerializer.LOCATION] = aProject.getFolder()
            projectMap[ProjectSerializer.LANGUAGE] = aProject.getLanguage()
            projectMap[ProjectSerializer.SOLUTION_FILE] = aProject.getSolutionFile()
            projectMap[ProjectSerializer.MAIN_FILE] = aProject.getMainFile()
            projectMap[ProjectSerializer.MAIN_FUNCTION] = aProject.getMainFunction()
            projectMap[ProjectSerializer.EXE_COMMAND] = aProject.getExeCommand()
            projectMap[ProjectSerializer.TREE_FILES] = saveTreeFiles(aProject.getTreeFiles())
            projectMap[ProjectSerializer.COMPILING_COMMAND] = aProject.getCompilingCommand()                        
            projectMap[ProjectSerializer.CPP_PROJECT] = aProject.getCppProject()
            
            projectFolder = aProject.getFolder()
            createFolderIfNotExists(projectFolder)
            executionsFolder = aProject.getExecutionsFolder()
            createFolderIfNotExists(executionsFolder)

            projectConfigPath = os.path.join(projectFolder, ProjectSerializer.PROJECT_SETTINGS_FILE_NAME)
            
            with open(projectConfigPath, 'w') as fp:
                json.dump(projectMap, fp, sort_keys=True, indent=ProjectSerializer.INDENT)
                
        with open(indexFilePath, 'w') as fp:
            json.dump(projectsIndexMap, fp, sort_keys=True, indent=ProjectSerializer.INDENT)

class ProjectsManager:
    '''
    It manages projects. Takes care of loading/storing them
    in memory as well as in disk, for persinstency.
    '''
    ##
    # @param self The ProjectsManager instance to construct.
    def __init__(self):
        '''
        Constructor.
        '''
        self.currentProjectName_ = None
        self.projects_ = ProjectSerializer.loadProjectsList()

    ##
    # @param self The ProjectsManager instance to construct.
    def clearAllProjects(self):
        '''
        Remove all projects.
        
        WARNING: this will erase the contents in memory, but later it will
        remove the project's files (including the equivalent programs) from disk.
        Make sure to backup any important files from your projects before calling this method.
        '''
        self.projects_ = {}
        self.currentProjectName_ = None

    ##
    # @param self The ProjectsManager instance to construct.
    def storeAllProjects(self):
        '''
        Store all projects in disk.
        '''
        ProjectSerializer.saveProjectsList(self.projects_)

    ##
    # @param self The ProjectsManager instance to construct.
    # @param aProject The project to store.
    def storeProject(self, aProject):
        '''
        Store a project (in memory as well as disk).
        '''
        self.projects_[aProject.getName()] = aProject
        ProjectSerializer.saveProjectsList(self.projects_)

    ##
    # @param self The ProjectsManager instance to construct.
    # @param projectName Name of the project to remove.
    def removeProject(self, projectName):
        '''
        Remove a project.
        '''
        if projectName == self.currentProjectName_:
            self.currentProjectName_ = None
        theProject = self.projects_[projectName]
        #Unannotate Files
        theLanguage = theProject.getLanguage()
        treeFiles = theProject.getTreeFiles()
        mainFile = theProject.getMainFile()
        mainFunction = theProject.getMainFunction()
        aSourceCodeParser = SourceCodeParser(theLanguage, mainFile, mainFunction)
        if theLanguage == ProgramExecution.Languages.C_PLUS_PLUS:
            for sourceFile, _ in treeFiles:
                #Unannotate file
                sourceFileTmp = sourceFile + '.tmp'
                shutil.copy(sourceFile, sourceFileTmp)
                try:
                    aSourceCodeParser.unAnnotateCppFile(sourceFile, sourceFileTmp)
                    shutil.copy(sourceFileTmp, sourceFile)
                finally:
                    if os.path.exists(sourceFileTmp):
                        os.remove(sourceFileTmp)
        aSourceCodeParser.unAnnotateMainFile()
        
        cppProject = theProject.getCppProject()
        cppProjectBkp = getCppProjectFileBackup(cppProject)
        if os.path.exists(cppProjectBkp):
            shutil.copy(cppProjectBkp, cppProject)
            os.remove(cppProjectBkp)
                        
        projectFolder = theProject.getFolder()
        removeFolder(projectFolder)
        del self.projects_[projectName]
        ProjectSerializer.saveProjectsList(self.projects_)

    ##
    # @param self The ProjectsManager instance to construct.
    # @param projectName The project name to search.
    def existsProject(self, projectName):
        '''
        Tell whether or not a project exists, looking for its name.
        '''
        return self.projects_.has_key(projectName)

    ##
    # @param self The ProjectsManager instance to construct.
    # @param projectName The current project's name to set.
    def setCurrentProjectName(self, projectName):
        '''
        Set the current project's name.
        '''
        if projectName:
            assert self.existsProject(projectName)
        self.currentProjectName_ = projectName

    ##
    # @param self The ProjectsManager instance to construct.
    # @return The current project's name.
    def getCurrentProjectName(self):
        '''
        Get the current project's name.
        '''
        return self.currentProjectName_

    ##
    # @param self The ProjectsManager instance to construct.
    # @param projectName The project's name to look for.
    # @return The project whose name equals projectName.
    def getProject(self, projectName):
        '''
        Get a project, searching by name.
        '''
        assert self.existsProject(projectName)
        return self.projects_[projectName]

    ##
    # @param self The ProjectsManager instance to construct.
    # @return All projects list.
    def getAllProjects(self):
        '''
        Get all projects list.
        '''
        return self.projects_

projectsManagerInstance_ = ProjectsManager()

##
# @return: The ONLY ProjectsManager instance.
def projectsManagerInstance():
    '''
    Return the ONLY ProjectsManager instance (Singleton Pattern). 
    '''
    return projectsManagerInstance_
