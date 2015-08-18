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
Business logic for annotations tree.

These are the possible items to be stored in the tree:

FOLDER, FILE, CLASS, FUNCTION

FOLDER => folder path (not implemented yet).
FILE => file path
CLASS => parent file + class name
FUNCTION => parent file or class + function name

'''
from PyQt4.QtGui import *
import os
import shutil
import sys
import traceback

from bug_reproducer_assistant.call_graph import ProgramExecution
from bug_reproducer_assistant.source_code_parser import SourceCodeParser
import project

##
# @return Current project from the manager.
def getCurrentProject():
    '''
    Get current project from the manager.
    '''
    theProjectsManager = project.projectsManagerInstance()
    currentProjectName = theProjectsManager.getCurrentProjectName()
    assert currentProjectName 
    return theProjectsManager.getProject(currentProjectName)

class TreeItemType:
    '''
    Tree item type: different options to store in the annotations tree.
    '''
    FOLDER, FILE, CLASS, FUNCTION = range(4)
    
    @staticmethod
    ##
    # @param t A tree item type.
    # @return Its string representation.
    def typeAsString( t ):
        '''
        Return string representation for a tree item type.
        '''
        return { TreeItemType.FOLDER: "Folder", TreeItemType.FILE: "File", TreeItemType.CLASS: "Class", TreeItemType.FUNCTION: "Function" } [t]

class TreeItemComposite:
    '''
    Model implementation for a graphical tree item.
    It communicates with "bug_reproducer_assistant" parser.
    It implements the composite pattern, and this is the class for the hierarchy.
    '''
    ##
    # @param self The TreeItemComposite instance to construct.
    # @param myTreeItemType The TreeItemType for this instance.
    # @param fileToAnnotate The source code file associated with this item.
    # @param headerToInclude Header (or import) to include in the annotations.
    def __init__(self, myTreeItemType, fileToAnnotate, headerToInclude):
        '''
        Constructor.
        '''
        self.treeItemType_ = myTreeItemType
        self.fileToAnnotate_ = fileToAnnotate
        self.headerToInclude_ = headerToInclude
        self.children_ = []

    ##
    # @param self The TreeItemComposite instance.
    # @return The TreeItemType.
    def getTreeItemType(self):
        '''
        Get the TreeItemType.
        '''
        return self.treeItemType_

    ##
    # @param self The TreeItemComposite instance.
    # @return The header (or import) to include in the annotations.
    def getHeaderToInclude(self):
        '''
        Get the header (or import) to include in the annotations.
        '''
        return self.headerToInclude_
 
    ##
    # @param self The TreeItemComposite instance.
    # @return The source code file associated with this item.
    def getFileToAnnotate(self):
        '''
        Get the source code file associated with this item.
        '''
        return self.fileToAnnotate_

    ##
    # @param self The TreeItemComposite instance.
    # @param child Child TreeItemComposite to add (composite pattern).
    def addChild(self, child):
        '''
        Add a child TreeItemComposite.
        '''
        assert TreeItemComposite.isValidChild(self, child)
        self.children_.append(child)

    @staticmethod
    ##
    # @param parent Parent TreeItemComposite to accept the child.
    # @param child Child TreeItemComposite to add (composite pattern).
    # @return Whether or not it's a valid child for a parent.
    def isValidChild(parent, child):
        '''
        It's a valid child for a parent (it checks the TreeItemType for this instance and the child).
        '''
        parentType = parent.getTreeItemType()
        childType = child.getTreeItemType()
        return parentType == childType - 1 or (parentType == TreeItemType.FILE and childType == TreeItemType.FUNCTION) 

    # @param self The TreeItemComposite instance.
    # @return child entities (composite pattern).
    def getChildren(self):
        '''
        Get child entities (composite pattern).
        '''
        return self.children_

    # @param self The TreeItemComposite instance.
    # @param doAnnotate If True, add annotations. Else, remove them.
    def changeAnnotationState(self, doAnnotate):
        '''
        Change annotation state.
        '''
        self.changeAnnotationState_(doAnnotate)
        for child in self.children_:
            child.changeAnnotationState(doAnnotate)

    # @param self The TreeItemComposite instance.
    # @param doAnnotate If True, add annotations. Else, remove them.
    def changeAnnotationState_(self, doAnnotate):
        '''
        Template method for the derivatives to actually change annotation state.
        '''
        raise NotImplementedError( "Should have implemented this" )

class FunctionTreeItem(TreeItemComposite):
    '''
    Tree item for a function.
    '''
    ##
    # @param self The FunctionTreeItem instance to construct.
    # @param fileToAnnotate The source code file where the class is.
    # @param headerToInclude Header (or import) to include in the annotations.
    # @param functionName The function name.
    # @param className Optional parent class.
    def __init__(self, fileToAnnotate, headerToInclude, functionName, className = "" ):
        '''
        Constructor.
        '''
        TreeItemComposite.__init__(self, TreeItemType.FUNCTION, fileToAnnotate, headerToInclude)
        self.functionName_ = functionName
        self.className_ = className

    ##
    # @param self The FunctionTreeItem instance.
    # @param doAnnotate If True, add annotations. Else, remove them.
    def changeAnnotationState_(self, doAnnotate):
        '''
        Change the function annotation state.
        '''
        LANG = ProgramExecution.Languages
        currentProject = getCurrentProject()
        mySourceCodeParser = SourceCodeParser(currentProject.getLanguage(), currentProject.getMainFile(), currentProject.getMainFunction())
        auxFileName = self.fileToAnnotate_ + ".aux"
        shutil.copy(self.fileToAnnotate_, auxFileName)
        try:
            if currentProject.getLanguage() == LANG.C_PLUS_PLUS:
                if doAnnotate:
                    mySourceCodeParser.annotateCppFunctions(auxFileName, self.fileToAnnotate_, self.headerToInclude_, [self.functionName_])
                else:
                    mySourceCodeParser.unannotateCppFunctions(auxFileName, self.fileToAnnotate_, [self.functionName_])
            else:
                assert currentProject.getLanguage() == LANG.PYTHON
                if doAnnotate:
                    mySourceCodeParser.annotatePythonObject(self.headerToInclude_, True, self.functionName_)
                else:
                    mySourceCodeParser.unAnnotatePythonObject(self.headerToInclude_, True, self.functionName_)
        except Exception:
            QMessageBox.about(None, 'ERROR','Error al (des)anotar la funcion. Traceback: \n\n"' + traceback.print_exc())
            shutil.copy(auxFileName, self.fileToAnnotate_)
            os.remove(auxFileName)

class ClassTreeItem(TreeItemComposite):
    '''
    Tree item for a class.
    '''
    ##
    # @param self The ClassTreeItem instance to construct.
    # @param fileToAnnotate The source code file where the class is.
    # @param headerToInclude Header (or import) to include in the annotations.
    # @param className The class name.
    def __init__(self, fileToAnnotate, headerToInclude, className):
        '''
        Constructor.
        '''
        TreeItemComposite.__init__(self, TreeItemType.CLASS, fileToAnnotate, headerToInclude)
        self.fileToAnnotate_ = fileToAnnotate
        self.headerToInclude_ = headerToInclude
        self.className_ = className

    ##
    # @param self The ClassTreeItem instance.
    # @param doAnnotate If True, add annotations. Else, remove them.
    def changeAnnotationState_(self, doAnnotate):
        '''
        Change the class annotation state.
        '''
        LANG = ProgramExecution.Languages
        currentProject = getCurrentProject()
        mySourceCodeParser = SourceCodeParser(currentProject.getLanguage(), currentProject.getMainFile(), currentProject.getMainFunction())
        auxFileName = self.fileToAnnotate_ + ".aux"
        shutil.copy(self.fileToAnnotate_, auxFileName)
        try:
            if currentProject.getLanguage() == LANG.C_PLUS_PLUS:
                if doAnnotate:
                    mySourceCodeParser.annotateCppClasses(auxFileName, self.fileToAnnotate_, self.headerToInclude_, [self.className_])
                else:
                    mySourceCodeParser.unannotateCppClasses(auxFileName, self.fileToAnnotate_, [self.className_])
            else:
                assert currentProject.getLanguage() == LANG.PYTHON
                classNameStr = self.headerToInclude_ + '.' + self.className_
                if doAnnotate:
                    mySourceCodeParser.annotatePythonObject(classNameStr, False)
                else:
                    mySourceCodeParser.unAnnotatePythonObject(classNameStr, False)

        except Exception:
            QMessageBox.about(None, 'ERROR','Error al (des)anotar la clase. Traceback:\n\n' + traceback.format_exc())
            shutil.copy(auxFileName, self.fileToAnnotate_)
            os.remove(auxFileName)

class FileTreeItem(TreeItemComposite):
    '''
    Tree item for a file.
    '''
    ##
    # @param self The FileTreeItem instance to construct.
    # @param fileToAnnotate The source code file being wrapped.
    # @param headerToInclude Header (or import) to include in the annotations.
    def __init__(self, fileToAnnotate, headerToInclude):
        '''
        Constructor.
        '''
        TreeItemComposite.__init__(self, TreeItemType.FILE, fileToAnnotate, headerToInclude)
        self.fileToAnnotate_ = fileToAnnotate
        self.headerToInclude_ = headerToInclude
        currentProject = getCurrentProject()
        self.parser_ = SourceCodeParser(currentProject.getLanguage(), currentProject.getMainFile(), currentProject.getMainFunction())

    ##
    # @param self The FileTreeItem instance.
    # @param doAnnotate If True, add annotations. Else, remove them.
    def changeAnnotationState_(self, doAnnotate):
        '''
        Change annotation state for all its children (composite pattern).
        
        NOT IMPLEMENTED YET.  
        '''
        pass

    ##
    # @param self The FileTreeItem instance.
    # @return The internal source code parser.
    def getParser(self):
        return self.parser_
