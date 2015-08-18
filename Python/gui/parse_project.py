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
Helpers to parse a C++ project (add custom "Bug-reproducer Assistant" configuration).
'''
from __future__ import with_statement
import shutil
import os
import re

LINE_INITIAL_SPACES_REGEX = re.compile( r"(?P<initSpaces>\s*)[^\s]+.*" )

##
# @param line A project line.
# @return The initial spaces from this line.
def getInitialSpacesFromLine(line):
    '''
    Return the initial spaces from this line.
    '''
    if line:
        match = LINE_INITIAL_SPACES_REGEX.match( line )
        if match:
            return match.group( 'initSpaces' )
        else:
            return None
    else:
        return None

class BraCustomProjectInfo:
    '''
    A simple struct to hold Bug-reproducer Assistant project information.
    '''
    ##
    # @param self The BraCustomProjectInfo instance to construct.
    # @param additionalDependencies Additional dependencies to add.
    # @param preprocessorDefinitions Preprocessor definitions (like macros).
    # @param additionalLibraryDirectoriesDebug Additional libraries (boost, BRA libraries, etc.) for Debug configuration.
    # @param additionalLibraryDirectoriesRelease Additional libraries (boost, BRA libraries, etc.) for Release configuration.
    # @param additionalIncludeDirectories Additional include directories (boost, BRA includes, etc.).
    def __init__(self, additionalDependencies, preprocessorDefinitions, additionalLibraryDirectoriesDebug, additionalLibraryDirectoriesRelease, additionalIncludeDirectories):
        '''
        Constructor.
        '''
        self.additionalDependencies = additionalDependencies
        self.preprocessorDefinitions = preprocessorDefinitions
        self.additionalLibraryDirectoriesDebug = additionalLibraryDirectoriesDebug
        self.additionalLibraryDirectoriesRelease = additionalLibraryDirectoriesRelease
        self.additionalIncludeDirectories = additionalIncludeDirectories
        
class ProjectTokenizer:
    '''
    Parser for Visual Studio projects. It discovers project regions to be process later by ProjectParser.
    Base class of this hierarchy. Actual implementations depending on the project format are implemented
    in the derivatives (depending on the Visual Studio project file version).
    '''
    class Configurations:
        '''
        Project configurations constants.
        '''
        NONE, DEBUG, RELEASE = range(3)

    ##
    # @param self The ProjectTokenizer to construct.
    def __init__(self):
        '''
        Constructor.
        '''
        #LINE events
        self.currentConfiguration_ = ProjectTokenizer.Configurations.NONE
        #Additional dependencies
        self.isAdditionalDependencies_ = False
        self.exitAdditionalDependenciesParent_ = False
        #Preprocessor definitions
        self.isPreprocessorDefinitions_ = False
        self.exitPreprocessorDefinitionsParent_ = False
        #Additional library directories
        self.isAdditionalLibraryDirectories_ = False
        self.exitAdditionalLibraryDirectoriesParent_ = False
        #Additional include directories
        self.isAdditionalIncludeDirectories_ = False
        self.exitAdditionalIncludeDirectoriesParent_ = False
        #Previous line spaces, necessary for default insertions
        self.previousLineSpaces_ = ''
        self.previousLine_ = ''

    ##
    # @param self The ProjectTokenizer instance.
    # @param line A C++ project line.
    def parseLine(self, line):
        '''
        Parse the line, discovering the flags for regions.
        '''
        self.previousLineSpaces_ = getInitialSpacesFromLine(self.previousLine_)
        self.cleanFlags()
        #Template method
        self.parseLine_(line)
        self.previousLine_ = line
                

    #Template methods: Leave this work to derivatives

    ##
    # @param self The ProjectTokenizer instance.
    # @param line A C++ project line.
    def parseLine_(self, line):
        '''
        Parse the line, discovering the flags for regions.
        Abstract method: derivatives must implement it, because it depends on the
        Visual Studio project version.
        '''
        raise NotImplementedError( "Should have implemented this" )

    ##
    # @param self The ProjectTokenizer instance.
    def getDefaultAdditionalDependencies(self):    
        '''
        Get default additional dependencies.
        Abstract method: derivatives must implement it, because it depends on the
        Visual Studio project version.
        '''
        raise NotImplementedError( "Should have implemented this" )

    ##
    # @param self The ProjectTokenizer instance.
    def getAdditionalDependenciesTag(self):
        '''
        Get Additional Dependencies tag.
        Abstract method: derivatives must implement it, because it depends on the
        Visual Studio project version.
        '''
        raise NotImplementedError( "Should have implemented this" )

    ##
    # @param self The ProjectTokenizer instance.
    def getPreprocessorDefinitionsTag(self):
        '''
        Get preprocessor definitions tag.
        Abstract method: derivatives must implement it, because it depends on the
        Visual Studio project version. 
        '''
        raise NotImplementedError( "Should have implemented this" )

    ##
    # @param self The ProjectTokenizer instance.
    def getAdditionalLibraryDirectoriesTag(self):
        '''
        Get additional library directories tag.
        Abstract method: derivatives must implement it, because it depends on the
        Visual Studio project version. 
        '''
        raise NotImplementedError( "Should have implemented this" )

    ##
    # @param self The ProjectTokenizer instance.
    def getAdditionalIncludeDirectoriesTag(self):
        '''
        Get additional include directories tag.
        Abstract method: derivatives must implement it, because it depends on the
        Visual Studio project version. 
        '''
        raise NotImplementedError( "Should have implemented this" )

    ##
    ##
    # @param self The ProjectTokenizer instance.
    # @param line A project line.
    # @param nextLine The following line.
    # @param featureTag Feature name in the project file (for example: "PreprocessorDefinitions").
    # @param features The new features list to add.
    # @return The feature line to insert in the project file.
    def addFeaturesToLine(self, line, nextLine, featureTag, features):
        '''
        Action method to add features to a line.
        Abstract method: derivatives must implement it, because it depends on the
        Visual Studio project version.
        '''
        raise NotImplementedError( "Should have implemented this" )

    ##
    # @param self The ProjectTokenizer instance.
    # @param features The features list to insert.
    # @param featureTag Feature name in the project file (for example: "PreprocessorDefinitions").
    # @param defaultFeaturesStr Default features to insert.
    # @return The feature line to insert in the project file.
    def getFeatureLine(self, features, featureTag, defaultFeaturesStr = ''):
        '''
        It returns the line with the tags and the feature information.
        Abstract method: derivatives must implement it, because it depends on the
        Visual Studio project version. 
        '''
        raise NotImplementedError( "Should have implemented this" )
    
    #Getter functions
    
    ##
    # @param self The ProjectTokenizer instance.
    # @return current project configuration.
    def getCurrentConfiguration(self):
        '''
        Get current project configuration (see Configurations).
        '''
        return self.currentConfiguration_

    ##
    # @param self The ProjectTokenizer instance.
    # @return Whether or not the current line is "Additional Dependencies".
    def isAdditionalDependencies(self):
        '''
        Tell if the current line is "Additional Dependencies".
        '''
        return self.isAdditionalDependencies_

    ##
    # @param self The ProjectTokenizer instance.
    # @return Whether or not the current line exits "Additional Dependencies" parent.
    def exitAdditionalDependenciesParent(self):
        '''
        Tell whether or not the current line exits "Additional Dependencies" parent.
        If True, "Additional Dependencies" has not been found, and it must be inserted.
        '''
        return self.exitAdditionalDependenciesParent_

    ##
    # @param self The ProjectTokenizer instance.
    # @return Whether or not the current line is "Preprocessor definitions".
    def isPreprocessorDefinitions(self):
        '''
        Tell if the current line is "Preprocessor definitions".
        '''        
        return self.isPreprocessorDefinitions_

    ##
    # @param self The ProjectTokenizer instance.
    # @return Whether or not the current line exits "Preprocessor Definitions" parent.
    def exitPreprocessorDefinitionsParent(self):
        '''
        Tell whether or not the current line exits "Preprocessor Definitions" parent.
        If True, "Additional Dependencies" has not been found, and it must be inserted.
        '''
        return self.exitPreprocessorDefinitionsParent_

    ##
    # @param self The ProjectTokenizer instance.
    # @return Whether or not the current line is "Additional library directories".
    def isAdditionalLibraryDirectories(self):
        '''
        Tell if the current line is "Additional library directories".
        '''
        return self.isAdditionalLibraryDirectories_

    ##
    # @param self The ProjectTokenizer instance.
    # @return Whether or not the current line exits "Additional Library Directories" parent.
    def exitAdditionalLibraryDirectoriesParent(self):
        '''
        Tell whether or not the current line exits "Additional Library Directories" parent.
        If True, "Additional Library Directories" has not been found, and it must be inserted.
        '''
        return self.exitAdditionalLibraryDirectoriesParent_

    ##
    # @param self The ProjectTokenizer instance.
    # @return Whether or not the current line is "Additional include directories".
    def isAdditionalIncludeDirectories(self):
        '''
        Tell if the current line is "Additional include directories".
        '''
        return self.isAdditionalIncludeDirectories_

    ##
    # @param self The ProjectTokenizer instance.
    # @return Whether or not the current line exits "Additional Include Directories" parent.    
    def exitAdditionalIncludeDirectoriesParent(self):
        '''
        Tell whether or not the current line exits "Additional Include Directories" parent.
        If True, "Additional Include Directories" has not been found, and it must be inserted.
        '''
        return self.exitAdditionalIncludeDirectoriesParent_

    #Previous line spaces
    ##
    # @param self The ProjectTokenizer instance.
    # @return The initial spaces from the previous line.    
    def getPreviousLineSpaces(self):
        '''
        Get the initial spaces from the previous line.
        '''
        return self.previousLineSpaces_

    ##
    # @param self The ProjectTokenizer instance.
    def cleanFlags(self):
        '''
        Clear the flags. Call this method before processing the current line,
        to start in a clean environment. 
        '''
        #Additional dependencies
        self.isAdditionalDependencies_ = False
        self.exitAdditionalDependenciesParent_ = False
        #Preprocessor definitions
        self.isPreprocessorDefinitions_ = False
        self.exitPreprocessorDefinitionsParent_ = False
        #Additional library directories
        self.isAdditionalLibraryDirectories_ = False
        self.exitAdditionalLibraryDirectoriesParent_ = False
        #Additional include directories
        self.isAdditionalIncludeDirectories_ = False
        self.exitAdditionalIncludeDirectoriesParent_ = False

class VcxprojTokenizer(ProjectTokenizer):
    '''
    ProjectTokenizer implementation for Visual Studio 10 project files
    (.vcxproj extension).
    '''
    ADDITIONAL_DEPENDENCIES_TAG    = 'AdditionalDependencies'
    ADDITIONAL_DEPENDENCIES_SEARCH = '<' + ADDITIONAL_DEPENDENCIES_TAG + '>'

    PREPOCESSOR_DEFINITIONS_TAG    = 'PreprocessorDefinitions'
    PREPOCESSOR_DEFINITIONS_SEARCH = '<' + PREPOCESSOR_DEFINITIONS_TAG + '>'

    ADDITIONAL_LIBRARY_DIRECTORIES_TAG    = 'AdditionalLibraryDirectories'
    ADDITIONAL_LIBRARY_DIRECTORIES_SEARCH = '<' + ADDITIONAL_LIBRARY_DIRECTORIES_TAG + '>'

    ADDITIONAL_INCLUDE_DIRECTORIES_TAG = 'AdditionalIncludeDirectories'
    ADDITIONAL_INCLUDE_DIRECTORIES_SEARCH = '<' + ADDITIONAL_INCLUDE_DIRECTORIES_TAG + '>'

    DEFAULT_ADDITIONAL_DEPENDENCIES = 'kernel32.lib;user32.lib;gdi32.lib;winspool.lib;comdlg32.lib;advapi32.lib;shell32.lib;ole32.lib;oleaut32.lib;uuid.lib;odbc32.lib;odbccp32.lib;%(AdditionalDependencies)'

    ##
    # @param self The VcxprojTokenizer instance.
    def __init__(self):
        '''
        Constructor.
        '''
        ProjectTokenizer.__init__(self)

    ##
    # @param self The VcxprojTokenizer instance.
    # @param line A C++ project line.
    def parseLine_(self, line):
        '''
        Parse the line, discovering the flags for regions.
        '''
        if line.find("Release|Win") >= 0:
            self.currentConfiguration_ = ProjectTokenizer.Configurations.RELEASE
        elif line.find("Debug|Win") >= 0:
            self.currentConfiguration_ = ProjectTokenizer.Configurations.DEBUG
        #Additional dependencies
        elif line.find(VcxprojTokenizer.ADDITIONAL_DEPENDENCIES_SEARCH) >= 0:
            self.isAdditionalDependencies_ = True
        elif line.find('</Link>') >= 0:
            self.exitAdditionalDependenciesParent_ = True
            #Also exit Additional library directories
            self.exitAdditionalLibraryDirectoriesParent_ = True
        #Preprocessor definitions
        elif line.find(VcxprojTokenizer.PREPOCESSOR_DEFINITIONS_SEARCH) >= 0:
            self.isPreprocessorDefinitions_ = True
        elif line.find('</ClCompile>') >= 0:
            self.exitPreprocessorDefinitionsParent_ = True
            #Also exit Additional include directories
            self.exitAdditionalIncludeDirectoriesParent_ = True
        #Additional library directories
        elif line.find(VcxprojTokenizer.ADDITIONAL_LIBRARY_DIRECTORIES_SEARCH) >= 0:
            self.isAdditionalLibraryDirectories_ = True
        #Additional include directories
        elif line.find(VcxprojTokenizer.ADDITIONAL_INCLUDE_DIRECTORIES_SEARCH) >= 0:
            self.isAdditionalIncludeDirectories_ = True

    ##
    # @param self The VcxprojTokenizer instance.
    def getDefaultAdditionalDependencies(self):    
        '''
        Get default additional dependencies.
        '''
        return VcxprojTokenizer.DEFAULT_ADDITIONAL_DEPENDENCIES

    ##
    # @param self The VcxprojTokenizer instance.
    def getAdditionalDependenciesTag(self):
        '''
        Get Additional Dependencies tag.
        '''
        return VcxprojTokenizer.ADDITIONAL_DEPENDENCIES_TAG

    ##
    # @param self The VcxprojTokenizer instance.
    def getPreprocessorDefinitionsTag(self):
        '''
        Get preprocessor definitions tag.
        '''
        return VcxprojTokenizer.PREPOCESSOR_DEFINITIONS_TAG

    ##
    # @param self The VcxprojTokenizer instance.
    def getAdditionalLibraryDirectoriesTag(self):
        '''
        Get additional library directories tag.
        '''
        return VcxprojTokenizer.ADDITIONAL_LIBRARY_DIRECTORIES_TAG

    ##
    # @param self The VcxprojTokenizer instance.
    def getAdditionalIncludeDirectoriesTag(self):
        '''
        Get additional include directories tag.
        '''
        return VcxprojTokenizer.ADDITIONAL_INCLUDE_DIRECTORIES_TAG

    ##
    # @param self The VcxprojTokenizer instance.
    # @param line A project line.
    # @param nextLine The following line.
    # @param featureTag Feature name in the project file (for example: "PreprocessorDefinitions").
    # @param features The new features list to add.
    # @return The feature line to insert in the project file.
    def addFeaturesToLine(self, line, nextLine, featureTag, features):
        '''
        Add features to a line. See getFeatureLine() for more details.
        '''
        skipNextLine = False
        FEATURES_LIST = 'featuresList'
        INIT_SPACES = 'initSpaces'
        FEATURE_REGEX_FORMAT_HEAD = "(?P<" + INIT_SPACES + ">\s*)<%s>(?P<" + FEATURES_LIST + ">.*)"
        FEATURE_REGEX_FORMAT_COMPLETE = FEATURE_REGEX_FORMAT_HEAD + "</%s>"
        FEATURE_REGEX_FORMAT_INCOMPLETE = FEATURE_REGEX_FORMAT_HEAD

        aux = FEATURE_REGEX_FORMAT_COMPLETE % (featureTag, featureTag)
        featureRegex = re.compile(aux)
        featureMatch = featureRegex.match(line)
        if featureMatch:
            initSpaces = featureMatch.group(INIT_SPACES)
            featuresList = featureMatch.group(FEATURES_LIST)
        else:
            skipNextLine = True
            aux = FEATURE_REGEX_FORMAT_INCOMPLETE % featureTag
            featureRegex = re.compile(aux)
            featureMatch = featureRegex.match(line)
            assert featureMatch
            initSpaces = featureMatch.group(INIT_SPACES)
            featuresList = featureMatch.group(FEATURES_LIST)
            #Verify that an incomplete line is only for empty features
            assert featuresList == ''
            assert nextLine
            assert nextLine.strip() == '</' + featureTag + '>'
            
        for feature in features:
            if featuresList.find(feature) == -1:
                featuresList += (";" + feature)
        
        if featuresList.startswith(';'):
            featuresList = featuresList[1:] 
                
        return (initSpaces + self.__getFeatureLineImpl(featuresList, featureTag), skipNextLine)

    ##
    # @param self The VcxprojTokenizer instance.
    # @param features The features list to insert.
    # @param featureTag Feature name in the project file (for example: "PreprocessorDefinitions").
    # @param defaultFeaturesStr Default features to insert.
    # @return The feature line to insert in the project file.
    def getFeatureLine(self, features, featureTag, defaultFeaturesStr = ''):
        '''
        Implementation for "Get feature line".
        It returns the line with the tags and the feature information.
        For instance, for the feature "Preprocessor definitions in "Debug" configuration, it returns:
        "<PreprocessorDefinitions>WIN32;_DEBUG;_CONSOLE;%(PreprocessorDefinitions);BUG_REPRODUCER_ASSISTANT_ENABLED</PreprocessorDefinitions>".
        
        NOTE: The default features

        Take "Additional Dependencies" as an example. When Visual Studio creates a project, it does not store in the
        vcxproj file a line with the additional dependencies. However, if you use the IDE to add a new dependency (like bug_reproducer_assistant.lib),
        you will see a default list: "kernel32.lib;user32.lib...". That list is not stored until you add a new dependency at the end of it. Then ALL
        the list is stored. To mimic the Visual Studio IDE behavior, this method stores the default features (they are hardcoded) the first time.
        '''
        featuresStr = ';'.join(features)
        return self.__getFeatureLineImpl(featuresStr, featureTag, defaultFeaturesStr)

    ##
    # @param self The VcxprojTokenizer instance.
    # @param featuresStr The features list to insert, as a string.
    # @param featureTag Feature name in the project file (for example: "PreprocessorDefinitions").
    # @param defaultFeaturesStr Default features to insert.
    # @return The feature line to insert in the project file.
    def __getFeatureLineImpl(self, featuresStr, featureTag, defaultFeaturesStr = ''):
        '''
        Implementation for "Get feature line" (it receives the final features string).
        It returns the line with the tags and the feature information.
        '''
        defaultFeaturesHead = defaultFeaturesStr + ';' if defaultFeaturesStr else ''
        return "<" + featureTag + ">" + defaultFeaturesHead + featuresStr + "</" + featureTag + ">\n"


class LineProcessor:
    '''
    It process a C++ project file lines 
    in processLine() function, to add Bug-reproducer Assistant custom info.
    '''
    ##
    # @param self The LineProcessor instance to construct.
    # @param myBraCustomProjectInfo Custom info to add to the project. See BraCustomProjectInfo.
    # @param aProjectTokenizer The concrete ProjectTokenizer instance to discover the features project regions.
    # @param resultFile: New project file with the custom BRA information.
    def __init__(self, myBraCustomProjectInfo, aProjectTokenizer, resultFile):
        '''
        Constructor.
        '''
        self.braCustomProjectInfo_ = myBraCustomProjectInfo
        self.projectTokenizer_ = aProjectTokenizer
        self.resultFile_ = resultFile
        self.skipNextLine_ = False
        self.alreadyProcessedAdditionalDependencies_ = False
        self.alreadyProcessedPreprocessorDefinitions_ = False
        self.alreadyProcessedAdditionalLibraryDirectories_ = False
        self.alreadyProcessedAdditionalIncludeDirectories_ = False

    ##
    # @param self The LineProcessor instance.
    # @param line The current projectline being processed.
    # @param nextLine The next project line.
    def processLine(self, line, nextLine):
        '''
        Process the current project line, adding custom information if necessary.
        '''
        ##
        # @param line Line to write in the result file.
        def writeNewFeatureLine(line):
            '''
            Write a new feature line in the result file (adding initial spaces as well).
            '''
            self.resultFile_.write(self.projectTokenizer_.getPreviousLineSpaces() + line)

        def getAdditionalLibraryDirectoriesFeatures():
            '''
            Get "Additional Library Directories" features.
            They have a special function to do this, because they depend on the
            configuration.
            '''
            currentConfiguration = self.projectTokenizer_.getCurrentConfiguration()
            if currentConfiguration == ProjectTokenizer.Configurations.DEBUG:
                return self.braCustomProjectInfo_.additionalLibraryDirectoriesDebug
            else:
                assert currentConfiguration == ProjectTokenizer.Configurations.RELEASE
                return self.braCustomProjectInfo_.additionalLibraryDirectoriesRelease


        if self.skipNextLine_:
            self.skipNextLine_ = False
            return
        
        self.projectTokenizer_.parseLine(line)
        #Additional dependencies
        if self.projectTokenizer_.isAdditionalDependencies():
            myTag = self.projectTokenizer_.getAdditionalDependenciesTag()
            features = self.braCustomProjectInfo_.additionalDependencies
            line, self.skipNextLine_ = self.projectTokenizer_.addFeaturesToLine(line, nextLine, myTag, features)
            self.alreadyProcessedAdditionalDependencies_ = True
        elif self.projectTokenizer_.isPreprocessorDefinitions():
            myTag = self.projectTokenizer_.getPreprocessorDefinitionsTag()
            features = self.braCustomProjectInfo_.preprocessorDefinitions
            line, self.skipNextLine_ = self.projectTokenizer_.addFeaturesToLine(line, nextLine, myTag, features)
            self.alreadyProcessedPreprocessorDefinitions_ = True
        elif self.projectTokenizer_.isAdditionalLibraryDirectories():
            myTag = self.projectTokenizer_.getAdditionalLibraryDirectoriesTag()
            features = getAdditionalLibraryDirectoriesFeatures()
            line, self.skipNextLine_ = self.projectTokenizer_.addFeaturesToLine(line, nextLine, myTag, features)
            self.alreadyProcessedAdditionalLibraryDirectories_ = True
        if self.projectTokenizer_.isAdditionalIncludeDirectories():
            myTag = self.projectTokenizer_.getAdditionalIncludeDirectoriesTag()
            features = self.braCustomProjectInfo_.additionalIncludeDirectories
            line, self.skipNextLine_ = self.projectTokenizer_.addFeaturesToLine(line, nextLine, myTag, features)
            self.alreadyProcessedAdditionalIncludeDirectories_ = True
        else:
        #DO NOT USE ELIF here, because the same line may  lead to exit
        #more than one feature
        #IMPORTANT: respect this order
            if self.projectTokenizer_.exitPreprocessorDefinitionsParent() and not self.alreadyProcessedPreprocessorDefinitions_:
                myTag = self.projectTokenizer_.getPreprocessorDefinitionsTag()
                features = self.braCustomProjectInfo_.preprocessorDefinitions
                aLine = self.projectTokenizer_.getFeatureLine(features, myTag)
                writeNewFeatureLine(aLine)
            if self.projectTokenizer_.exitAdditionalIncludeDirectoriesParent() and not self.alreadyProcessedAdditionalIncludeDirectories_:
                myTag = self.projectTokenizer_.getAdditionalIncludeDirectoriesTag()
                features = self.braCustomProjectInfo_.additionalIncludeDirectories
                aLine = self.projectTokenizer_.getFeatureLine(features, myTag)
                writeNewFeatureLine(aLine)
            if self.projectTokenizer_.exitAdditionalLibraryDirectoriesParent() and not self.alreadyProcessedAdditionalLibraryDirectories_:
                myTag = self.projectTokenizer_.getAdditionalLibraryDirectoriesTag()
                features = getAdditionalLibraryDirectoriesFeatures()
                aLine = self.projectTokenizer_.getFeatureLine(features, myTag)
                writeNewFeatureLine(aLine)
            if self.projectTokenizer_.exitAdditionalDependenciesParent() and not self.alreadyProcessedAdditionalDependencies_:
                myTag = self.projectTokenizer_.getAdditionalDependenciesTag()
                features = self.braCustomProjectInfo_.additionalDependencies
                defaultDeps = self.projectTokenizer_.getDefaultAdditionalDependencies()
                aLine = self.projectTokenizer_.getFeatureLine(features, myTag, defaultDeps)
                writeNewFeatureLine(aLine)
        self.resultFile_.write(line)

class ProjTokenizerFactory:
    '''
    Factory to create ProjectTokenizer instances depending on the
    project extension (currently, only 'vcxproj' is supported).
    '''
    @staticmethod
    ##
    # @param projectExtension Project extension (it affects the type of tokenizer to create).
    def createProjectsTokenizer(projectExtension):
        '''
        Create the ProjectTokenizer instance according to the project extension.
        '''
        #TODO GERVA: Add vcproj extension
        assert projectExtension == 'vcxproj'
        return VcxprojTokenizer()

class ProjectParser:
    '''
    Project parser to add BRA custom information.
    This is the class to be called from client code.
    '''
    ##
    # @param self The ProjectParser instance to construct.
    # @param projectFileName: Path from the project file to parse.
    # @param resultProjectFileName: Path for the new project file with the custom BRA information.
    # @param projectExtension Valid extension for the project file.
    # @param myBraCustomProjectInfo Custom info to add to the project. See BraCustomProjectInfo.
    def __init__(self, projectFileName, resultProjectFileName, projectExtension, myBraCustomProjectInfo):
        '''
        Constructor.
        '''
        self.projectFileName_ = projectFileName
        self.resultProjectFileName_ = resultProjectFileName
        self.projectExtension_ = projectExtension
        self.braCustomProjectInfo_ = myBraCustomProjectInfo

    ##
    # @param self The ProjectParser instance.
    def parseProject(self):
        '''
        Parse the project indicated in the constructor, adding BRA custom info in the result file.
        '''
        projTokenizer = ProjTokenizerFactory.createProjectsTokenizer(self.projectExtension_)
        with open(self.resultProjectFileName_, 'w') as newProjectFile:
            myLineProcessor = LineProcessor(self.braCustomProjectInfo_, projTokenizer, newProjectFile)
            with open( self.projectFileName_, 'r' ) as oldProjectFile:
                fileLines = oldProjectFile.readlines()
            currentLine = 0
            lastLine = len(fileLines) - 1
            
            for line in fileLines:
                if currentLine == lastLine:
                    nextLine = None
                else:
                    nextLine = fileLines[currentLine + 1]
                    currentLine += 1
                myLineProcessor.processLine(line, nextLine)