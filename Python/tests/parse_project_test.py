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

from __future__ import with_statement
from cStringIO import StringIO
import unittest

import os
import sys
import shutil
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import gui.parse_project


TEST_FILES_FOLDER = os.path.join(os.path.dirname(__file__), "parse_project_test_files")

class AnnotatorTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testAddCustomBraInfoToProject(self):
        projectFileName = os.path.join(TEST_FILES_FOLDER, 'testAddCustomBraInfoToProject.vcxproj')
        expectedFileName = os.path.join(TEST_FILES_FOLDER, 'testAddCustomBraInfoToProject_expected.vcxproj')

        projectFileBackup = projectFileName + ".mybkp"

        try:
            shutil.copy(projectFileName, projectFileBackup)
            
            additionalDependencies = ['bug_reproducer_assistant.lib', 'jsoncpp.lib']
            preprocessorDefinitions = ['BUG_REPRODUCER_ASSISTANT_ENABLED']
            
            BOOST_LIB = r'Z:\Libraries\boost_1_45_0\stage\lib'
            LIBRARIES_LIB_PREFIX = 'C:\\Program Files\\Bug-reproducer Assistant\\C++\\libs\\'
            additionalLibraryDirectoriesDebug = [BOOST_LIB, LIBRARIES_LIB_PREFIX + 'Debug']
            additionalLibraryDirectoriesRelease = [BOOST_LIB, LIBRARIES_LIB_PREFIX + 'Release']
            additionalIncludeDirectories = [r'Z:\Libraries\boost_1_45_0', r'C:\Program Files\Bug-reproducer Assistant\C++\include']
            
            myBraCustomProjectInfo = gui.parse_project.BraCustomProjectInfo(additionalDependencies, preprocessorDefinitions, additionalLibraryDirectoriesDebug, additionalLibraryDirectoriesRelease, additionalIncludeDirectories)

            myProjectParser = gui.parse_project.ProjectParser(projectFileBackup, projectFileName, 'vcxproj', myBraCustomProjectInfo)
            myProjectParser.parseProject()
            
            self.compareFileContents_(projectFileName, expectedFileName)
        finally:
            if os.path.exists(projectFileBackup):
                shutil.copy(projectFileBackup, projectFileName)
                os.remove(projectFileBackup)
    
    def compareFileContents_(self, fileName1, fileName2):
        with open(fileName1, "r") as f1:
            with open(fileName2, "r") as f2:
                str1 = f1.readlines()
                str2 = f2.readlines()
                self.assertEqual(str1, str2)

if __name__ == '__main__':
    unittest.main()
