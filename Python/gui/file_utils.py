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
Utilities for File System.
'''
import ctypes
import shutil
import os
import config

BEGIN_MARK = "["
END_MARK = "]"
SOLUTION_FOLDER_MARK = BEGIN_MARK + "SOLUTION_FOLDER" + END_MARK
SOLUTION_NAME_MARK = BEGIN_MARK + "SOLUTION_NAME" + END_MARK
SOLUTION_PATH_MARK = BEGIN_MARK + "SOLUTION_PATH" + END_MARK
PROJECT_NAME_MARK = BEGIN_MARK + "PROJECT_NAME" + END_MARK
CPP_PROJECT_NAME_MARK = BEGIN_MARK + "CPP_PROJECT_NAME" + END_MARK
MAIN_FILE_MARK = BEGIN_MARK + "MAIN_FILE" + END_MARK
VISUAL_STUDIO_EXE_MARK = BEGIN_MARK + "VISUAL_STUDIO_EXE" + END_MARK

##
def getMyDocumentsFolder():
    '''
    Get "My Documents" folder, according to the OS.
    '''
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(300)
    dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)
    return buf.value

##
# @param folderPath The folder to create.
def createFolderIfNotExists(folderPath):
    '''
    Create a folder, if it doesn't exist.
    '''
    if not os.path.exists(folderPath):
        os.mkdir(folderPath)

##
# @param folderPath The folder to remove.
def removeFolder(folderPath):
    '''
    Remove a folder tree.
    '''
    shutil.rmtree(folderPath)

##
# @param aPath A path to be normalized. 
def normalizePathSeparators(aPath):
    '''
    Normalize a path, using "/" as folders separator.
    '''
    return aPath.replace('\\', '/')

##
# @param strWithTags A command string with tags to replace.
# @param mainFile The program's main file.
# @param projectName Bug-reproducer Assistant project name.
# @param solutionPath Visual Studio solution path.
# @param cppProjectFile Visual Studio project path.
# @return The command string with all the tags replaced.
def replaceTags(strWithTags, mainFile, projectName, solutionPath, cppProjectFile):
    '''
    In a command string, replace special tags with the actual values.
    For instance: "[MAIN_FILE]" should be replaced by mainFile parameter.
    '''
    def getNameFromPath(aPath):
        theName = os.path.basename(aPath)
        #Skip extension
        theName = theName[ : theName.find('.') ]
        return theName

    if strWithTags.find(MAIN_FILE_MARK) >= 0:
        strWithTags = strWithTags.replace(MAIN_FILE_MARK, mainFile)
    if strWithTags.find(PROJECT_NAME_MARK) >= 0:
        strWithTags = strWithTags.replace(PROJECT_NAME_MARK, projectName)
    if strWithTags.find(SOLUTION_PATH_MARK) >= 0:
        strWithTags = strWithTags.replace(SOLUTION_PATH_MARK, solutionPath)
    if strWithTags.find(SOLUTION_FOLDER_MARK) >= 0:
        solutionFolder = os.path.dirname(solutionPath)
        strWithTags = strWithTags.replace(SOLUTION_FOLDER_MARK, solutionFolder)
    if strWithTags.find(SOLUTION_NAME_MARK) >= 0:
        solutionName = getNameFromPath(solutionPath)
        strWithTags = strWithTags.replace(SOLUTION_NAME_MARK, solutionName)
    if strWithTags.find(CPP_PROJECT_NAME_MARK) >= 0:
        cppProjectName = getNameFromPath(cppProjectFile)
        strWithTags = strWithTags.replace(CPP_PROJECT_NAME_MARK, cppProjectName)
    if strWithTags.find(VISUAL_STUDIO_EXE_MARK) >= 0:
        strWithTags = strWithTags.replace(VISUAL_STUDIO_EXE_MARK, config.instance().visualStudioExe)

    #Just in case there's a double \\ (for instance: concatenating solution folder with Debug subdirectory
    #for exe command
    strWithTags = strWithTags.replace("\\\\", "\\")
    strWithTags = strWithTags.replace("\\/", "\\")
    strWithTags = strWithTags.replace("/\\", "\\")
    
    return strWithTags