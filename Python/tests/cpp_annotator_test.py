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
import shutil
from bug_reproducer_assistant.code_generator import CodeGenerator

#Set Visual Studio Env vars
os.system(r'"C:\Program Files\Microsoft Visual Studio 10.0\VC\bin\vcvars32.bat"')
from bug_reproducer_assistant.cpp_annotator import CppAnnotator

TEST_FILES_FOLDER = os.path.join(os.path.dirname(__file__), "cpp_annotator_test_files")

COMPILER_EXE_CMD = r'"C:\Program Files\Microsoft Visual Studio 10.0\Common7\IDE\VCExpress"'
CONFIGURATION = 'Debug'
SOLUTION_FOLDER = 'S:\\'
SOLUTION_FILE = os.path.join(SOLUTION_FOLDER, "bug_reproducer_assistant.sln")
SAMPLE_PROGRAM_NAME = "SampleProgram"
SAMPLE_PROGRAM_FOLDER = os.path.join(SOLUTION_FOLDER, SAMPLE_PROGRAM_NAME)
SAMPLE_PROGRAM_TEMP_FOLDER = os.path.join(SOLUTION_FOLDER, SAMPLE_PROGRAM_NAME, CONFIGURATION)
SAMPLE_PROGRAM_EXE  = os.path.join(SOLUTION_FOLDER, CONFIGURATION, SAMPLE_PROGRAM_NAME + ".exe")
BUILD_SOLUTION_COMMAND = COMPILER_EXE_CMD + " " + SOLUTION_FILE + " " + "/build"
HEADER_TO_INCLUDE = "MyFunctions.h"
FILE_TO_ANNOTATE = os.path.join(SAMPLE_PROGRAM_FOLDER, HEADER_TO_INCLUDE)
MAIN_FILE_TO_ANNOTATE = os.path.join(SAMPLE_PROGRAM_FOLDER, 'main.cpp')
MAIN_FUNCTION = '_tmain'

class AnnotatorTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testFunctionWithoutParams(self):
        self.processTestingFunction_("testFunctionWithoutParams", functionNames = ["noParamsFunction"])
    
    def testOneIntegerFunction(self):
        self.processTestingFunction_("testOneIntegerFunction", functionNames = ["add"])

    def testTwoIntegerFunctions(self):
        self.processTestingFunction_("testTwoIntegerFunctions", functionNames = ["add", "subtract"])

    def testAllModuleFunctions(self):
        self.processTestingFunction_("testAllModuleFunctions", functionNames = [])
        
    def testAnnotatedClassWithoutConstructor(self):
        self.processTestingFunction_("testAnnotatedClassWithoutConstructor", classNames = ["MyClass"])

    def testAnnotatedClassWithConstructor(self):
        self.processTestingFunction_("testAnnotatedClassWithConstructor", classNames = ["ClassWithConstructor"])

    def testAnnotatedClassWithStaticMethods(self):
        self.processTestingFunction_("testAnnotatedClassWithStaticMethods", classNames = ["ClassWithStaticMethods"])
    
    def processTestingFunction_(self, functionName, classNames = None, functionNames = None):
        mainFileName = os.path.join(TEST_FILES_FOLDER, functionName + ".cpp")
        resultMainFileName = os.path.join(TEST_FILES_FOLDER, functionName + "_result.cpp")
        expectedMainFileName = os.path.join(TEST_FILES_FOLDER, functionName + "_expected.cpp")
        dumpFileName = os.path.join(TEST_FILES_FOLDER, functionName + ".json")
        
        try:
            #TODO GERVA: keepBackupFiles == True
            shutil.copy(mainFileName, MAIN_FILE_TO_ANNOTATE)
            myCppAnnotator = CppAnnotator(MAIN_FILE_TO_ANNOTATE, MAIN_FUNCTION, BUILD_SOLUTION_COMMAND, keepBackupFiles = False)
            
            myCppAnnotator.annotateMainFile(dumpFileName)
            if classNames is None and functionNames is None:
                myCppAnnotator.annotateFile(FILE_TO_ANNOTATE, HEADER_TO_INCLUDE)
            else:
                if classNames is not None:
                    myCppAnnotator.annotateClasses(FILE_TO_ANNOTATE, HEADER_TO_INCLUDE, classNames)
                if functionNames is not None:
                    myCppAnnotator.annotateFunctions(FILE_TO_ANNOTATE, HEADER_TO_INCLUDE, functionNames)
            
            with myCppAnnotator:
                #It's annotated, it should generate a result file in resultFileName
                os.system(SAMPLE_PROGRAM_EXE)
                
            with open( dumpFileName, "r") as dumpFileFp:
                with open( resultMainFileName, "w") as equivProgramFp:
                    #Get equivalent program
                    myCodeGenerator = CodeGenerator(dumpFileFp)
                    myCodeGenerator.generateEquivalentProgram(equivProgramFp)
            self.compareFileContents_(resultMainFileName, expectedMainFileName)
        finally:
            if os.path.exists(resultMainFileName):
                os.remove(resultMainFileName)
            if os.path.exists(dumpFileName):
                os.remove(dumpFileName)
        
    def compareFileContents_(self, fileName1, fileName2):
        with open(fileName1, "r") as f1:
            with open(fileName2, "r") as f2:
                str1 = f1.readlines()
                str2 = f2.readlines()
                self.assertEqual(str1, str2)

if __name__ == '__main__':
    unittest.main()
