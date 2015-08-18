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
from bug_reproducer_assistant.base import AnnotationState
from bug_reproducer_assistant.call_graph import ProgramExecution
from bug_reproducer_assistant.source_code_parser import SourceCodeParser

TEST_FILES_FOLDER = os.path.join(os.path.dirname(__file__), "source_code_parser_test_files")

class AnnotatorTestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testFunctionWithoutParams(self):
        self.processCppTestingFunction_(True, "testFunctionWithoutParams", functionNames = ["noParamsFunction"])
    
    def testOneIntegerFunction(self):
        self.processCppTestingFunction_(True, "testOneIntegerFunction", functionNames = ["add"])

    def testTwoIntegerFunctions(self):
        self.processCppTestingFunction_(True, "testTwoIntegerFunctions", functionNames = ["add", "subtract"])

    def testAllModuleFunctions(self):
        self.processCppTestingFunction_(True, "testAllModuleFunctions", functionNames = [])
        
    def testClassWithoutConstructor(self):
        self.processCppTestingFunction_(True, "testClassWithoutConstructor", classNames = ["MyClass"])

    def testClassFunctions(self):
        self.processCppTestingFunction_(True, "testClassFunctions", classNames = ["MyClass"], functionNames = ["f1", "f3"] )

    def testClassWithConstructor(self):
        self.processCppTestingFunction_(True, "testClassWithConstructor", classNames = ["ClassWithConstructor"])

    def testClassWithStaticMethods(self):
        self.processCppTestingFunction_(True, "testClassWithStaticMethods", classNames = ["ClassWithStaticMethods"])

    def testAnnotateWholeFile(self):
        self.processCppTestingFunction_(True, "myFunctions")

    def testAnnotateMainCpp(self):
        self.processAnnotateMainTestingFunction_(True, ProgramExecution.Languages.C_PLUS_PLUS, "testAnnotateMainCpp")

    def testAnnotateMainPython(self):
        self.processAnnotateMainTestingFunction_(True, ProgramExecution.Languages.PYTHON, "testAnnotateMainPython")

    def testAnnotateMainPython2(self):
        self.processAnnotateMainTestingFunction_(True, ProgramExecution.Languages.PYTHON, "testAnnotateMainPython2")

    def testAnnotatePythonObjectsWithFunctionName(self):
        self.processAnnotatePythonObject_(True, "testAnnotatePythonObjectsWithFunctionName", "MyClass", False, "h")

    def testAnnotatePythonObjectsNoFunctionName(self):
        self.processAnnotatePythonObject_(True, "testAnnotatePythonObjectsNoFunctionName", "dir1.dir2.MyClass", False)

    def testAnnotatePythonObjectsOnlyAnnotation(self):
        self.processAnnotatePythonObject_(True, "testAnnotatePythonObjectsOnlyAnnotation", "dir1.dir2.MyClass", False)

    def testAnnotatePythonObjectsModuleNoClass(self):
        self.processAnnotatePythonObject_(True, "testAnnotatePythonObjectsModuleNoClass", "dir1.dir2", True, "f")

    def testCppGetAllClassesAndFunctions(self):
        MY_HEADER = "MyFunctions.h"
        myFunctionsFileName = os.path.join(TEST_FILES_FOLDER, MY_HEADER)
        mySourceCodeParser = SourceCodeParser(ProgramExecution.Languages.C_PLUS_PLUS, myFunctionsFileName)
        classes, functions = mySourceCodeParser.getAllClassesAndFunctions(myFunctionsFileName)
        
        expectedFunctions = ['myPrint', 'add', 'subtract', 'innerFunction', 'outerFunction', 'noParamsFunction', 'mySubstring', 'processVector', 'processIntMap']
        expectedClasses = ['MyClass', 'ClassWithConstructor', 'ClassWithStaticMethods']

        self.assertEqual(expectedFunctions, functions)
        self.assertEqual(expectedClasses, classes)

    def testCppGetAllClassesAndFunctionsAnnotations(self):
        MY_HEADER = "MyFunctions.h"
        expectedFunctions = ['myPrint', 'add', 'subtract', 'innerFunction', 'outerFunction', 'noParamsFunction', 'mySubstring', 'processVector', 'processIntMap']
        expectedClasses = ['MyClass', 'ClassWithConstructor', 'ClassWithStaticMethods']
        
        def verifyStates(classes, functions, expectedAnnotClasses, expectedAnnotFunctions):
            def verifyContainer(container, expectedContainer, expectedAnnotations):
                i = 0
                for obj, annotState in container:
                    self.assertEqual(obj, expectedContainer[i])
                    status = AnnotationState.ANNOTATED if obj in expectedAnnotations else AnnotationState.NOT_ANNOTATED 
                    self.assertEqual(annotState, status)
                    i += 1
            
            verifyContainer(classes, expectedClasses, expectedAnnotClasses)
            verifyContainer(functions, expectedFunctions, expectedAnnotFunctions)

        #Check without annotations
        mainFileName = os.path.join(TEST_FILES_FOLDER, "testAnnotateMainCpp.cpp")
        myFunctionsFileName = os.path.join(TEST_FILES_FOLDER, MY_HEADER)
        
        mySourceCodeParser = SourceCodeParser(ProgramExecution.Languages.C_PLUS_PLUS, mainFileName)
        classes, functions = mySourceCodeParser.getAllClassesAndFunctionsAnnotations(myFunctionsFileName, )

        #No annotations expected, just the function and classes names
        verifyStates(classes, functions, expectedAnnotClasses = [], expectedAnnotFunctions = [])
                   
        #Now, annotate a couple of functions and classes
        myFunctionsFileBackup = myFunctionsFileName + ".mybkp"
        resultFileName = os.path.join(TEST_FILES_FOLDER, myFunctionsFileName + "_result.h")
        resultFileName2 = resultFileName + ".2"
        try:
            shutil.copy(myFunctionsFileName, myFunctionsFileBackup)

            #Annotate a couple of classes
            expectedAnnotClasses = ['MyClass', 'ClassWithConstructor']
            mySourceCodeParser.annotateCppClasses(myFunctionsFileName, resultFileName, MY_HEADER, expectedAnnotClasses)
            
            #Annotate a couple of functions
            expectedAnnotFunctions = ['subtract', 'outerFunction']
            mySourceCodeParser.annotateCppFunctions(resultFileName, resultFileName2, MY_HEADER, expectedAnnotFunctions)
            
            #Get states, and verify annotations
            classes, functions = mySourceCodeParser.getAllClassesAndFunctionsAnnotations(resultFileName2, MY_HEADER)
            verifyStates(classes, functions, expectedAnnotClasses, expectedAnnotFunctions)
        finally:
            if os.path.exists(myFunctionsFileBackup):
                shutil.copy(myFunctionsFileBackup, myFunctionsFileName)
                os.remove(myFunctionsFileBackup)
            if os.path.exists(resultFileName):
                os.remove(resultFileName)
            if os.path.exists(resultFileName2):
                os.remove(resultFileName2)
               
    def testPythonGetAllClassesAndFunctions(self):
        mainFileName = 'mainFileForTests.py'
        myFunctionsFileName = os.path.join(TEST_FILES_FOLDER, "MyFunctions.py")
        mySourceCodeParser = SourceCodeParser(ProgramExecution.Languages.PYTHON, mainFileName)
        classes, functions = mySourceCodeParser.getAllClassesAndFunctions(myFunctionsFileName, "myFunctions")

        expectedFunctions = ['myPrint', 'add', 'subtract', 'innerFunction', 'outerFunction', 'noParamsFunction', 'mySubstring', 'processList', 'processDict']
        expectedClasses = ['MyClass', 'ClassWithDummyParameters', 'NonAnnotatedClass', 'ClassWithConstructor', 'ClassWithStaticAndClassMethods']
        
        self.assertEqual(expectedFunctions, functions)
        self.assertEqual(expectedClasses, classes)

    def testPythonGetAllClassesAndFunctionsAnnotations(self):

        expectedFunctions = ['myPrint', 'add', 'subtract', 'innerFunction', 'outerFunction', 'noParamsFunction', 'mySubstring', 'processList', 'processDict']
        expectedClasses = ['MyClass', 'ClassWithDummyParameters', 'NonAnnotatedClass', 'ClassWithConstructor', 'ClassWithStaticAndClassMethods']
        
        def verifyStates(classes, functions, expectedAnnotClasses, expectedAnnotFunctions):
            def verifyContainer(container, expectedContainer, expectedAnnotations):
                i = 0
                for pythonObj, annotState in container:
                    self.assertEqual(pythonObj, expectedContainer[i])
                    status = AnnotationState.ANNOTATED if pythonObj in expectedAnnotations else AnnotationState.NOT_ANNOTATED 
                    self.assertEqual(annotState, status)
                    i += 1
            
            verifyContainer(classes, expectedClasses, expectedAnnotClasses)
            verifyContainer(functions, expectedFunctions, expectedAnnotFunctions)

        #Check without annotations
        mainFileName = 'mainFileForTests.py'
        myFunctionsFileName = os.path.join(TEST_FILES_FOLDER, "MyFunctions.py")
        
        mySourceCodeParser = SourceCodeParser(ProgramExecution.Languages.PYTHON, mainFileName)
        classes, functions = mySourceCodeParser.getAllClassesAndFunctionsAnnotations(myFunctionsFileName, "MyFunctions")

        #No annotations expected, just the function and classes names
        verifyStates(classes, functions, expectedAnnotClasses = [], expectedAnnotFunctions = [])
                   
        #Now, annotate a couple of functions and classes
        mainFileBackup = mainFileName + ".mybkp"
        try:
            shutil.copy(mainFileName, mainFileBackup)
            #Annotate main file
            mySourceCodeParser.annotateMainFile("dumpFileName.json")
            #Annotate a couple of classes
            mySourceCodeParser.annotatePythonObject("MyFunctions.MyClass", False)
            mySourceCodeParser.annotatePythonObject("MyFunctions.ClassWithConstructor", False)
            expectedAnnotClasses = ['MyClass', 'ClassWithConstructor']
            #Annotate a couple of functions
            mySourceCodeParser.annotatePythonObject("MyFunctions", True, 'subtract')
            mySourceCodeParser.annotatePythonObject("MyFunctions", True, 'outerFunction')
            expectedAnnotFunctions = ['subtract', 'outerFunction']
            
            #Get states, and verify annotations
            classes, functions = mySourceCodeParser.getAllClassesAndFunctionsAnnotations(myFunctionsFileName, "MyFunctions")
            verifyStates(classes, functions, expectedAnnotClasses, expectedAnnotFunctions)
        finally:
            if os.path.exists(mainFileBackup):
                shutil.copy(mainFileBackup, mainFileName)
                os.remove(mainFileBackup)
      
#Unannotate
    def testUnannotateFunctionWithoutParams(self):
        self.processCppTestingFunction_(False, "testFunctionWithoutParams", functionNames = ["noParamsFunction"])
    
    def testUnannotateOneIntegerFunction(self):
        self.processCppTestingFunction_(False, "testOneIntegerFunction", functionNames = ["add"])

    def testUnannotateTwoIntegerFunctions(self):
        self.processCppTestingFunction_(False, "testTwoIntegerFunctions", functionNames = ["add", "subtract"])

    def testUnannotateAllModuleFunctions(self):
        self.processCppTestingFunction_(False, "testAllModuleFunctions", functionNames = [])
        
    def testUnannotateClassWithoutConstructor(self):
        self.processCppTestingFunction_(False, "testClassWithoutConstructor", classNames = ["MyClass"])

    def testUnannotateClassFunctions(self):
        self.processCppTestingFunction_(False, "testClassFunctions", classNames = ["MyClass"], functionNames = ["f1", "f3"] )

    def testUnannotateClassWithConstructor(self):
        self.processCppTestingFunction_(False, "testClassWithConstructor", classNames = ["ClassWithConstructor"])

    def testUnannotateClassWithStaticMethods(self):
        self.processCppTestingFunction_(False, "testClassWithStaticMethods", classNames = ["ClassWithStaticMethods"])
    
    def testUnannotateMainCpp(self):
        self.processAnnotateMainTestingFunction_(False, ProgramExecution.Languages.C_PLUS_PLUS, "testAnnotateMainCpp")

    def testUnannotateMainPython(self):
        self.processAnnotateMainTestingFunction_(False, ProgramExecution.Languages.PYTHON, "testAnnotateMainPython")

    def testUnannotateMainPython2(self):
        self.processAnnotateMainTestingFunction_(False, ProgramExecution.Languages.PYTHON, "testAnnotateMainPython2")

    def testUnannotatePythonObjectsWithFunctionName(self):
        self.processAnnotatePythonObject_(False, "testAnnotatePythonObjectsWithFunctionName", "MyClass", False, "h")

    def testUnannotatePythonObjectsNoFunctionName(self):
        self.processAnnotatePythonObject_(False, "testAnnotatePythonObjectsNoFunctionName", "dir1.dir2.MyClass", False)
        
    def testUnannotatePythonObjectsOnlyAnnotation(self):
        self.processAnnotatePythonObject_(False, "testAnnotatePythonObjectsOnlyAnnotation", "dir1.dir2.MyClass", False)

    def testUnannotatePythonObjectsModuleNoClass(self):
        self.processAnnotatePythonObject_(False, "testAnnotatePythonObjectsModuleNoClass", "dir1.dir2", True, "f")

#Implementations
    def processAnnotateMainTestingFunction_(self, doAdd, language, functionName):
        dumpFileName = "call_graph.json"
        assert language in (ProgramExecution.Languages.PYTHON, ProgramExecution.Languages.C_PLUS_PLUS)
        sourceExt = ".py" if language == ProgramExecution.Languages.PYTHON else ".cpp"
        mainFileName = os.path.join(TEST_FILES_FOLDER, functionName + sourceExt)
        expectedFileName = os.path.join(TEST_FILES_FOLDER, functionName + "_expected" + sourceExt)
        
        if not doAdd:
            aux = mainFileName
            mainFileName = expectedFileName
            expectedFileName = aux

        mainFileBackup = mainFileName + ".mybkp"

        try:
            shutil.copy(mainFileName, mainFileBackup)
            #Verify second (un)annotation yields the same file
            for i in range(2):
                mySourceCodeParser = SourceCodeParser(language, mainFileName)
                if doAdd:
                    mySourceCodeParser.annotateMainFile(dumpFileName)
                else:
                    mySourceCodeParser.unAnnotateMainFile()
                self.compareFileContents_(mainFileName, expectedFileName)
        finally:
            if os.path.exists(mainFileBackup):
                shutil.copy(mainFileBackup, mainFileName)
                os.remove(mainFileBackup)
    
    def processCppTestingFunction_(self, doAdd, functionName, classNames = None, functionNames = None):
        mainFileName = os.path.join(TEST_FILES_FOLDER, "testAnnotateMainCpp.cpp")
        originalFileName = os.path.join(TEST_FILES_FOLDER, functionName + ".h")
        resultFileName = os.path.join(TEST_FILES_FOLDER, functionName + "_result.h")
        expectedFileName = os.path.join(TEST_FILES_FOLDER, functionName + "_expected.h")
        
        if not doAdd: 
            aux = originalFileName
            originalFileName = expectedFileName
            expectedFileName = aux

        mySourceCodeParser = SourceCodeParser(ProgramExecution.Languages.C_PLUS_PLUS, mainFileName)
        headerToInclude = functionName + ".h"
        
        #Verify second (un)annotation yields the same file
        try:
            originalFileBkp = originalFileName + '.bkp'
            shutil.copy(originalFileName, originalFileBkp)
            for i in range(2):
                try:
                    ok = False
                    if doAdd:
                        if classNames is None and functionNames is None:
                            mySourceCodeParser.annotateCppFile(originalFileName, resultFileName, headerToInclude)
                        else:
                            if classNames is not None:
                                if functionNames is not None:
                                    assert len(classNames) == 1
                                    mySourceCodeParser.annotateCppClassFunctions(originalFileName, resultFileName, headerToInclude, classNames[0], functionNames)
                                else:                            
                                    mySourceCodeParser.annotateCppClasses(originalFileName, resultFileName, headerToInclude, classNames)
                            if functionNames is not None and classNames is None:
                                mySourceCodeParser.annotateCppFunctions(originalFileName, resultFileName, headerToInclude, functionNames)
                    else:
                        if classNames is None and functionNames is None:
                            mySourceCodeParser.unannotateCppFile(originalFileName, resultFileName)
                        else:
                            if classNames is not None:
                                mySourceCodeParser.unannotateCppClasses(originalFileName, resultFileName, classNames)
                            if functionNames is not None and classNames is None:
                                mySourceCodeParser.unannotateCppFunctions(originalFileName, resultFileName, functionNames)
                    self.compareFileContents_(resultFileName, expectedFileName)
                    ok = True
                finally:
                    if i == 0 and ok:
                        shutil.copy(resultFileName, originalFileName) 
                    if os.path.exists(resultFileName):
                        os.remove(resultFileName)
        finally:
            if os.path.exists(originalFileBkp):
                shutil.copy(originalFileBkp, originalFileName)
                os.remove(originalFileBkp)

    def processAnnotatePythonObject_(self, doAdd, testingFunctionName, pythonObjectName, itsAModule, functionName = None ):
        mainFileName = os.path.join(TEST_FILES_FOLDER, testingFunctionName + '.py')
        expectedFileName = os.path.join(TEST_FILES_FOLDER, testingFunctionName + "_expected" + '.py')
        
        if not doAdd:
            aux = mainFileName
            mainFileName = expectedFileName
            expectedFileName = aux

        mainFileBackup = mainFileName + ".mybkp"

        try:
            shutil.copy(mainFileName, mainFileBackup)
        #Verify second (un)annotation yields the same file
            for i in range(2):
                mySourceCodeParser = SourceCodeParser(ProgramExecution.Languages.PYTHON, mainFileName)
                if doAdd:
                    mySourceCodeParser.annotatePythonObject(pythonObjectName, itsAModule, functionName)
                else:
                    mySourceCodeParser.unAnnotatePythonObject(pythonObjectName, itsAModule, functionName)
                self.compareFileContents_(mainFileName, expectedFileName)
        finally:
            if os.path.exists(mainFileBackup):
                shutil.copy(mainFileBackup, mainFileName)
                os.remove(mainFileBackup)

    def compareFileContents_(self, fileName1, fileName2):
        with open(fileName1, "r") as f1:
            with open(fileName2, "r") as f2:
                str1 = f1.readlines()
                str2 = f2.readlines()
                self.assertEqual(str1, str2)

if __name__ == '__main__':
    unittest.main()
