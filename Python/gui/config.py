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
GUI configuration.
'''
from __future__ import with_statement
import ctypes
import os
import sys
import simplejson as json
import file_utils
import registry_utils

from bug_reproducer_assistant.call_graph import ProgramExecution

##
# @return The folder where the projects will be stored.
def _getProjectsFolder():
    '''
    Get the folder where the projects will be stored.
    '''
    dataFolder = installationConfig().getDataFolder()
    return os.path.join(dataFolder, Config.PROJECTS_FOLDER_NAME)

class InstallationConfig:
    '''
    Configuration for data related to installation.
    '''
    CPP_SUBFOLDER = 'C++'
    PYTHON_SUBFOLDER = 'Python'
    CPP_LIBS_SUBFOLDER = 'libs'
    CPP_INCLUDE_SUBFOLDER = 'include'
    ##
    # @param self The InstallationConfig instance to construct.
    def __init__(self):
        '''
        Constructor.
        '''
        self.installationFolder_ = registry_utils.readInstallPathFromRegistry()
        self.firstUse_ = registry_utils.readFirstUseFromRegistry()
        myDocuments = file_utils.getMyDocumentsFolder()
        self.dataFolder_ = os.path.join(myDocuments, Config.PRODUCT_NAME)
        self.cppFolder_ = os.path.join(self.installationFolder_, InstallationConfig.CPP_SUBFOLDER)
        self.cppIncludeFolder_ = os.path.join(self.cppFolder_, InstallationConfig.CPP_LIBS_SUBFOLDER)
        self.cppLibrariesFolder_ = os.path.join(self.cppFolder_, InstallationConfig.CPP_LIBS_SUBFOLDER)        

    ##
    # @param self The InstallationConfig instance.
    # @return The installation folder.
    def getInstallationFolder(self):
        '''
        Get the installation folder.
        '''
        return self.installationFolder_

    ##
    # @param self The InstallationConfig instance.
    # @return The data folder.
    def getDataFolder(self):
        '''
        Get the data folder (root folder for BRA configuration data).
        '''
        return self.dataFolder_

    ##
    # @param self The InstallationConfig instance.
    # @return Whether or not it is the first time the program is run.
    def getIsFirstUse(self):
        '''
        Tell whether or not it is the first time the program is run.
        '''
        return self.firstUse_

    ##
    # @param self The InstallationConfig instance.
    # @param firstUse If True, it is the first time the program is run.
    def setIsFirstUse(self, firstUse):
        '''
        Set whether or not it is the first time the program is run.
        '''
        self.firstUse_ = firstUse
        registry_utils.writeFirstUseIntoRegistry(firstUse)

    ##
    # @param self The InstallationConfig instance.
    # @return The "Bug-reproducer Assistant" C++ include folder.
    def getCppIncludeFolder(self):
        '''
        Get the "Bug-reproducer Assistant" C++ include folder. 
        '''
        return self.cppIncludeFolder_    

    ##
    # @param self The InstallationConfig instance.
    # @return The "Bug-reproducer Assistant" C++ libraries folder.
    def getCppLibrariesFolder(self):
        '''
        Get the "Bug-reproducer Assistant" C++ libraries folder. 
        '''
        return self.cppLibrariesFolder_

##
# @return Configuration default values.
def getDefaultValues():
    '''
    Get configuration default values.
    '''
    defaultLanguage = ProgramExecution.Languages.C_PLUS_PLUS
    cpp_defaultRootFolder = ''
    python_defaultRootFolder = ''
    defaultCompilingCommand = '"' + file_utils.VISUAL_STUDIO_EXE_MARK + '" "' + file_utils.SOLUTION_PATH_MARK + '" /build'
    cpp_defaultExeCommand = '"' + file_utils.SOLUTION_FOLDER_MARK + "\\Debug\\" + file_utils.CPP_PROJECT_NAME_MARK + '.exe"'
    python_defaultExeCommand = 'python "' + file_utils.MAIN_FILE_MARK + '"'
    boostIncludeFolder = ''
    boostLibraryFolder = ''
    visualStudioExe = r'C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE\VCExpress.exe'
    solutionExtensions = '*.sln'
    projectExtensions = '*.vcxproj'
    
    return defaultLanguage, cpp_defaultRootFolder, python_defaultRootFolder, defaultCompilingCommand, cpp_defaultExeCommand, python_defaultExeCommand, boostIncludeFolder, boostLibraryFolder, visualStudioExe, solutionExtensions, projectExtensions

class Config:
    '''
    Configuration class.
    '''
    PRODUCT_NAME = 'Bug-reproducer Assistant'
    PROJECTS_FOLDER_NAME = 'Projects'
    SETTINGS_FOLDER_NAME = 'Settings'
    
    ##
    # @param self The Config instance to construct.
    def __init__(self):
        self._defaultLanguage, self._cpp_defaultRootFolder, self._python_defaultRootFolder, self._defaultCompilingCommand, self._cpp_defaultExeCommand, self._python_defaultExeCommand, self._boostIncludeFolder, self._boostLibraryFolder, self._visualStudioExe, self._solutionExtensions, self._projectExtensions = getDefaultValues()

    ##
    # @param self The Config instance.
    # @return The projects folder.
    def getProjectsFolder(self):
        '''
        Get the folder where the projects are stored.
        '''
        return _getProjectsFolder()

    ##
    # @param self The Config instance.
    # @return The default language for new projects.
    def getDefaultLanguage(self):
        '''
        Get the default language for new projects.
        '''
        return self._defaultLanguage

    ##
    # @param self The Config instance.
    # @param value The default language for new projects to set.
    def setDefaultLanguage(self, value):
        '''
        Set the default language for new projects.
        '''
        self._defaultLanguage = value

    ##
    # @param self The Config instance.
    # @return The C++ default sources folder.
    def getCppDefaultRootFolder(self):
        '''
        Get the C++ default sources folder.
        '''
        return self._cpp_defaultRootFolder
    
    ##
    # @param self The Config instance.
    # @param value The C++ default sources folder to set.
    def setCppDefaultRootFolder(self, value):
        '''
        Set the C++ default sources folder.
        '''
        self._cpp_defaultRootFolder = value
    
    ##
    # @param self The Config instance.
    # @return The Python default sources folder.
    def getPythonDefaultRootFolder(self):
        '''
        Get the Python default sources folder.
        '''
        return self._python_defaultRootFolder

    ##
    # @param self The Config instance.
    # @param value The Python default sources folder.
    def setPythonDefaultRootFolder(self, value):
        '''
        Set the Python default sources folder.
        '''
        self._python_defaultRootFolder = value

    ##
    # @param self The Config instance.
    # @return The default command to compile the C++ programs.
    def getDefaultCompilingCommand(self):
        '''
        Get the default command to compile the C++ programs.
        '''
        return self._defaultCompilingCommand

    ##
    # @param self The Config instance.
    # @param value The default command to compile the C++ programs.
    def setDefaultCompilingCommand(self, value):
        '''
        Set the default command to compile the C++ programs.
        '''
        self._defaultCompilingCommand = value

    ##
    # @param self The Config instance.
    # @return The default command to execute the C++ programs.
    def getCppDefaultExeCommand(self):
        '''
        Get the default command to execute the C++ programs.
        '''
        return self._cpp_defaultExeCommand

    ##
    # @param self The Config instance.
    # @param value The default command to execute the C++ programs.
    def setCppDefaultExeCommand(self, value):
        '''
        Set the default command to execute the C++ programs.
        '''
        self._cpp_defaultExeCommand = value

    ##
    # @param self The Config instance.
    # @return The default command to execute the Python programs.    
    def getPythonDefaultExeCommand(self):
        '''
        Get the default command to execute the Python programs.
        '''
        return self._python_defaultExeCommand
    
    ##
    # @param self The Config instance.
    # @param value  The default command to execute the Python programs.
    def setPythonDefaultExeCommand(self, value):
        '''
        Set the default command to execute the Python programs.
        '''
        self._python_defaultExeCommand = value
    
    #Boost
        
    ##
    # @param self The Config instance.
    # @return The Boost includes folder.
    def getBoostIncludeFolder(self):
        '''
        Get the Boost includes folder.
        '''
        return self._boostIncludeFolder

    ##
    # @param self The Config instance.
    # @param value The Boost includes folder.
    def setBoostIncludeFolder(self, value):
        '''
        Set the Boost includes folder.
        '''
        self._boostIncludeFolder = value

    ##
    # @param self The Config instance.
    # @return The Boost libraries folder.    
    def getBoostLibraryFolder(self):
        '''
        Get the Boost libraries folder.
        '''
        return self._boostLibraryFolder

    ##
    # @param self The Config instance.
    # @param value The Boost libraries folder.
    def setBoostLibraryFolder(self, value):
        '''
        Set the Boost libraries folder.
        '''
        self._boostLibraryFolder = value
    
    #Visual Studio options
    
    ##
    # @param self The Config instance.
    # @return The Visual Studio executable path (or command).
    def getVisualStudioExe(self):
        '''
        Get the Visual Studio executable path (or command).
        '''
        return self._visualStudioExe
    
    ##
    # @param self The Config instance.
    # @param value The Visual Studio executable path (or command).
    def setVisualStudioExe(self, value):
        '''
        Set the Visual Studio executable path (or command).
        '''
        self._visualStudioExe = value
    
    ##
    # @param self The Config instance.
    # @return The Visual Studio solution valid extensions.
    def getSolutionExtensions(self):
        '''
        Get the Visual Studio solution valid extensions.
        '''
        return self._solutionExtensions

    ##
    # @param self The Config instance.
    # @param value The Visual Studio solution valid extensions.
    def setSolutionExtensions(self, value):
        '''
        Set the Visual Studio solution valid extensions.
        '''
        self._solutionExtensions = value

    ##
    # @param self The Config instance.
    # @return The Visual Studio project valid extensions.
    def getProjectExtensions(self):
        '''
        Get the Visual Studio project valid extensions.
        '''
        return self._projectExtensions

    ##
    # @param self The Config instance.
    # @param value The Visual Studio project valid extensions.
    def setProjectExtensions(self, value):
        '''
        Set the Visual Studio project valid extensions.
        '''
        self._projectExtensions = value
    
    ##
    # Properties: use these properties to get/set the configuration parameters.
    defaultLanguage = property(getDefaultLanguage, setDefaultLanguage)
    cpp_defaultRootFolder = property(getCppDefaultRootFolder, setCppDefaultRootFolder)
    python_defaultRootFolder = property(getPythonDefaultRootFolder, setPythonDefaultRootFolder)
    defaultCompilingCommand = property(getDefaultCompilingCommand, setDefaultCompilingCommand)
    cpp_defaultExeCommand = property(getCppDefaultExeCommand, setCppDefaultExeCommand)
    python_defaultExeCommand = property(getPythonDefaultExeCommand, setPythonDefaultExeCommand)
    boostIncludeFolder = property(getBoostIncludeFolder, setBoostIncludeFolder)
    boostLibraryFolder = property(getBoostLibraryFolder, setBoostLibraryFolder)
    visualStudioExe = property(getVisualStudioExe, setVisualStudioExe)
    solutionExtensions = property(getSolutionExtensions, setSolutionExtensions)
    projectExtensions = property(getProjectExtensions, setProjectExtensions) 

installationConfigInstance = InstallationConfig()
configInstance = Config()

##
# @return: The ONLY InstallationConfig instance.
def installationConfig():
    '''
    Return the ONLY InstallationConfig instance (Singleton Pattern). 
    '''
    return installationConfigInstance

##
# @return: The ONLY InstallationConfig instance.
def instance():
    '''
    Return the ONLY Config instance (Singleton Pattern).
    '''
    return configInstance

class ConfigSerializer:
    '''
    Configuration serializer.
    It loads/stores the configuration in disk and the registry.
    '''
    PROJECTS_FOLDER = 'projectsFolder'
    DEFAULT_LANGUAGE = 'defaultLanguage'
    CPP_DEFAULT_ROOT_FOLDER = 'cpp_defaultRootFolder'
    PYTHON_DEFAULT_ROOT_FOLDER = 'python_defaultRootFolder'
    DEFAULT_COMPILING_COMMAND = 'defaultCompilingCommand'
    CPP_DEFAULT_EXE_COMMAND = 'cpp_defaultExeCommand'
    PYTHON_DEFAULT_EXE_COMMAND = 'python_defaultExeCommand'
    BOOST_INCLUDE_FOLDER = 'boostIncludeFolder'
    BOOST_LIBRARY_FOLDER = 'boostLibraryFolder'
    VISUAL_STUDIO_EXE = 'visualStudioExe'
    SOLUTION_EXTENSIONS = 'solutionExtensions'
    PROJECT_EXTENSIONS = 'projectExtensions'
   
    CONFIG_FILE_NAME = 'userSettings.json'
    CONFIG_FILE_PATH = None
    INDENT = 4

    @staticmethod
    ##
    def loadConfig():
        '''
        Load configuration.
        '''
        dataFolder = installationConfig().getDataFolder()
        file_utils.createFolderIfNotExists(dataFolder)
        projectsFolder = _getProjectsFolder()
        file_utils.createFolderIfNotExists(projectsFolder)
           
        settingsFolder = os.path.join(dataFolder, Config.SETTINGS_FOLDER_NAME)
        file_utils.createFolderIfNotExists(settingsFolder)
        
        ConfigSerializer.CONFIG_FILE_PATH = os.path.join(settingsFolder, ConfigSerializer.CONFIG_FILE_NAME)

        #Check existence of configuration file, and load it. Use default values otherwise
        if os.path.exists(ConfigSerializer.CONFIG_FILE_PATH):
            with open(ConfigSerializer.CONFIG_FILE_PATH, 'r') as fp:
                configMap = json.load(fp)
                defaultLanguage = configMap[ConfigSerializer.DEFAULT_LANGUAGE]
                cpp_defaultRootFolder = configMap[ConfigSerializer.CPP_DEFAULT_ROOT_FOLDER]
                python_defaultRootFolder = configMap[ConfigSerializer.PYTHON_DEFAULT_ROOT_FOLDER]
                defaultCompilingCommand = configMap[ConfigSerializer.DEFAULT_COMPILING_COMMAND]
                cpp_defaultExeCommand = configMap[ConfigSerializer.CPP_DEFAULT_EXE_COMMAND]
                python_defaultExeCommand = configMap[ConfigSerializer.PYTHON_DEFAULT_EXE_COMMAND]
                boostIncludeFolder = configMap[ConfigSerializer.BOOST_INCLUDE_FOLDER]
                boostLibraryFolder = configMap[ConfigSerializer.BOOST_LIBRARY_FOLDER]                
                visualStudioExe = configMap[ConfigSerializer.VISUAL_STUDIO_EXE] 
                solutionExtensions = configMap[ConfigSerializer.SOLUTION_EXTENSIONS]
                projectExtensions = configMap[ConfigSerializer.PROJECT_EXTENSIONS]
        else:
            #TODO GERVA: Move this code to installer
            defaultLanguage, cpp_defaultRootFolder, python_defaultRootFolder, defaultCompilingCommand, cpp_defaultExeCommand, python_defaultExeCommand, boostIncludeFolder, boostLibraryFolder, visualStudioExe, solutionExtensions, projectExtensions = getDefaultValues()
        
        myConfig = instance()
        myConfig.defaultLanguage = defaultLanguage
        myConfig.cpp_defaultRootFolder = cpp_defaultRootFolder
        myConfig.python_defaultRootFolder = python_defaultRootFolder
        myConfig.defaultCompilingCommand = defaultCompilingCommand
        myConfig.cpp_defaultExeCommand = cpp_defaultExeCommand
        myConfig.python_defaultExeCommand = python_defaultExeCommand
        myConfig.boostIncludeFolder = boostIncludeFolder
        myConfig.boostLibraryFolder = boostLibraryFolder        
        myConfig.visualStudioExe = visualStudioExe
        myConfig.solutionExtensions = solutionExtensions
        myConfig.projectExtensions = projectExtensions
    
    @staticmethod
    def saveConfig():
        '''
        Save configuration.
        '''
        assert ConfigSerializer.CONFIG_FILE_PATH
        myConfig = instance()
        configMap = {}
        configMap[ConfigSerializer.DEFAULT_LANGUAGE] = myConfig.defaultLanguage
        configMap[ConfigSerializer.CPP_DEFAULT_ROOT_FOLDER] = myConfig.cpp_defaultRootFolder
        configMap[ConfigSerializer.PYTHON_DEFAULT_ROOT_FOLDER] = myConfig.python_defaultRootFolder
        configMap[ConfigSerializer.DEFAULT_COMPILING_COMMAND] = myConfig.defaultCompilingCommand
        configMap[ConfigSerializer.CPP_DEFAULT_EXE_COMMAND] = myConfig.cpp_defaultExeCommand
        configMap[ConfigSerializer.PYTHON_DEFAULT_EXE_COMMAND] = myConfig.python_defaultExeCommand
        configMap[ConfigSerializer.BOOST_INCLUDE_FOLDER] = myConfig.boostIncludeFolder
        configMap[ConfigSerializer.BOOST_LIBRARY_FOLDER] = myConfig.boostLibraryFolder               
        configMap[ConfigSerializer.VISUAL_STUDIO_EXE] = myConfig.visualStudioExe
        configMap[ConfigSerializer.SOLUTION_EXTENSIONS] = myConfig.solutionExtensions
        configMap[ConfigSerializer.PROJECT_EXTENSIONS] = myConfig.projectExtensions
       
        with open(ConfigSerializer.CONFIG_FILE_PATH, 'w') as fp:
            json.dump(configMap, fp, sort_keys=True, indent = ConfigSerializer.INDENT )