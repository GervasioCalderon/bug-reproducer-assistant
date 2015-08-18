/*
This file is part of Bug-reproducer Assistant
 The tool has been designed and developed by Gervasio Andres Calderon Fernandez, of Core Security Technologies
 
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
 */

#pragma warning(disable:4996)

//STL
//Boost
#include <boost/optional.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/make_shared.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/FunctionCall.h>
#include <bug_reproducer_assistant/ProgramExecution.h>
#include <bug_reproducer_assistant/Annotation.h>
#include <bug_reproducer_assistant/Annotator.h>
//test_utils
#include <test_utils/test_utils.h>
//annotator_test
#include "MyFunctions_annotated.h"
#include "annotator_test_suite.h"

CPPUNIT_TEST_SUITE_REGISTRATION(AnnotatorTest);

using namespace bug_reproducer_assistant;

namespace
{
	static const boost::shared_ptr< LanguageObject > NULL_PARENT;
	static const boost::optional< boost::posix_time::time_duration > NULL_TOTAL_TIME;

	std::string jsonString(const std::string& str)
	{
		return std::string("\"") + str + "\"";
	}
	void createBasicTestData( boost::shared_ptr< LanguageObject >& myFunctionsModule, boost::shared_ptr< ProgramExecution >& progExec )
	{
		progExec = boost::make_shared< ProgramExecution >("C++");
		myFunctionsModule = boost::make_shared< LanguageObject >(1l, LanguageType::MODULE, NULL_PARENT, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("MyFunctions.h"));
		progExec->addLanguageObject(myFunctionsModule);
	}
}

void AnnotatorTest::testFunctionWithoutParams()
{
	Annotator::resetAnnotations();
	//ANNOTATED CODE TO RUN
	MyFunctions::noParamsFunction();
	////////////////////////

	boost::shared_ptr< ProgramExecution > receivedProgramExec = Annotator::instance().getProgramExecution();
	
	//Create expected program execution
	//1st object: My Functions Module
	boost::shared_ptr< LanguageObject > myFunctionsModule;
	boost::shared_ptr< ProgramExecution > expectedProgramExec;

	createBasicTestData(myFunctionsModule, expectedProgramExec);

	ArgumentsVector argsVector;
	boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(1L, myFunctionsModule, "noParamsFunction", FunctionCall::MethodType::METHOD, argsVector, 0, NULL_TOTAL_TIME);

	expectedProgramExec->addFunctionCall(aCall);
	
	test_utils::compareProgramExecutions(*expectedProgramExec, *receivedProgramExec);
}

void AnnotatorTest::testOneIntegerFunction()
{
	Annotator::resetAnnotations();
	//ANNOTATED CODE TO RUN
	MyFunctions::add(4, 5);
	////////////////////////

	boost::shared_ptr< ProgramExecution > receivedProgramExec = Annotator::instance().getProgramExecution();
	
	//Create expected program execution
	//1st object: My Functions Module
	boost::shared_ptr< LanguageObject > myFunctionsModule;
	boost::shared_ptr< ProgramExecution > expectedProgramExec;

	createBasicTestData(myFunctionsModule, expectedProgramExec);

	ArgumentsVector argsVector;

	//2nd object: Built ins module
	boost::shared_ptr< LanguageObject > builtIns = boost::make_shared< LanguageObject >(2L, LanguageType::MODULE, NULL_PARENT, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString(CPlusPlusConstants::BUILTINS_MODULE_NAME));
	expectedProgramExec->addLanguageObject(builtIns);
	//3rd object: int type
	boost::shared_ptr< LanguageObject > intType = boost::make_shared< LanguageObject >(3L, LanguageType::CLASS, builtIns, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("int"));
	expectedProgramExec->addLanguageObject(intType);
	//Parameters: 4 and 5 (instances of "int" type)
	boost::shared_ptr< LanguageObject > arg1 = boost::make_shared< LanguageObject >(4L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "4");
	boost::shared_ptr< LanguageObject > arg2 = boost::make_shared< LanguageObject >(5L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "5");
	expectedProgramExec->addLanguageObject(arg1); //Default values: VALUE and not isConst
	expectedProgramExec->addLanguageObject(arg2); //Default values: VALUE and not isConst

	argsVector.push_back(Argument(arg1));
	argsVector.push_back(Argument(arg2));

	boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(1L, myFunctionsModule, "add", FunctionCall::MethodType::METHOD, argsVector, 0, NULL_TOTAL_TIME);

	expectedProgramExec->addFunctionCall(aCall);
	
	test_utils::compareProgramExecutions(*expectedProgramExec, *receivedProgramExec);
}

void AnnotatorTest::testTwoIntegerFunctions()
{
	Annotator::resetAnnotations();
	//ANNOTATED CODE TO RUN
	MyFunctions::add(4, 5);
	MyFunctions::subtract(4, 5);
	////////////////////////

	boost::shared_ptr< ProgramExecution > receivedProgramExec = Annotator::instance().getProgramExecution();
	
	//Create expected program execution
	//1st object: My Functions Module
	boost::shared_ptr< LanguageObject > myFunctionsModule;
	boost::shared_ptr< ProgramExecution > expectedProgramExec;

	createBasicTestData(myFunctionsModule, expectedProgramExec);

	ArgumentsVector argsVector;

	//2nd object: Built ins module
	boost::shared_ptr< LanguageObject > builtIns = boost::make_shared< LanguageObject >(2L, LanguageType::MODULE, NULL_PARENT, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString(CPlusPlusConstants::BUILTINS_MODULE_NAME));
	expectedProgramExec->addLanguageObject(builtIns);
	//3rd object: int type
	boost::shared_ptr< LanguageObject > intType = boost::make_shared< LanguageObject >(3L, LanguageType::CLASS, builtIns, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("int"));
	expectedProgramExec->addLanguageObject(intType);
	//Parameters: 4 and 5 (instances of "int" type)
	boost::shared_ptr< LanguageObject > arg1 = boost::make_shared< LanguageObject >(4L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "4");
	boost::shared_ptr< LanguageObject > arg2 = boost::make_shared< LanguageObject >(5L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "5");
	expectedProgramExec->addLanguageObject(arg1); //Default values: VALUE and not isConst
	expectedProgramExec->addLanguageObject(arg2); //Default values: VALUE and not isConst

	argsVector.push_back(Argument(arg1));
	argsVector.push_back(Argument(arg2));

	boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(1L, myFunctionsModule, "add", FunctionCall::MethodType::METHOD, argsVector, 0, NULL_TOTAL_TIME);
	boost::shared_ptr< FunctionCall > aCall2 = boost::make_shared< FunctionCall >(2L, myFunctionsModule, "subtract", FunctionCall::MethodType::METHOD, argsVector, 0, NULL_TOTAL_TIME);

	expectedProgramExec->addFunctionCall(aCall);
	expectedProgramExec->addFunctionCall(aCall2);
	
	test_utils::compareProgramExecutions(*expectedProgramExec, *receivedProgramExec);
}

void AnnotatorTest::testAllModuleFunctions()
{
	Annotator::resetAnnotations();
	//ANNOTATED CODE TO RUN
	MyFunctions::noParamsFunction();
	int z = MyFunctions::add(1, 2);
	////////////////////////
	
	boost::shared_ptr< ProgramExecution > receivedProgramExec = Annotator::instance().getProgramExecution();
	
	//Create expected program execution
	//1st object: My Functions Module
	boost::shared_ptr< LanguageObject > myFunctionsModule;
	boost::shared_ptr< ProgramExecution > expectedProgramExec;

	createBasicTestData(myFunctionsModule, expectedProgramExec);

	ArgumentsVector argsVector;

	//2nd object: Built ins module
	boost::shared_ptr< LanguageObject > builtIns = boost::make_shared< LanguageObject >(2L, LanguageType::MODULE, NULL_PARENT, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString(CPlusPlusConstants::BUILTINS_MODULE_NAME));
	expectedProgramExec->addLanguageObject(builtIns);
	//3rd object: int type
	boost::shared_ptr< LanguageObject > intType = boost::make_shared< LanguageObject >(3L, LanguageType::CLASS, builtIns, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("int"));
	expectedProgramExec->addLanguageObject(intType);
	//Parameters: 4 and 5 (instances of "int" type)
	boost::shared_ptr< LanguageObject > arg1 = boost::make_shared< LanguageObject >(4L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "1");
	boost::shared_ptr< LanguageObject > arg2 = boost::make_shared< LanguageObject >(5L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "2");
	expectedProgramExec->addLanguageObject(arg1); //Default values: VALUE and not isConst
	expectedProgramExec->addLanguageObject(arg2); //Default values: VALUE and not isConst

	boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(1L, myFunctionsModule, "noParamsFunction", FunctionCall::MethodType::METHOD, argsVector, 0, NULL_TOTAL_TIME);

	argsVector.push_back(Argument(arg1));
	argsVector.push_back(Argument(arg2));

	boost::shared_ptr< FunctionCall > aCall2 = boost::make_shared< FunctionCall >(2L, myFunctionsModule, "add", FunctionCall::MethodType::METHOD, argsVector, 0, NULL_TOTAL_TIME);

	expectedProgramExec->addFunctionCall(aCall);
	expectedProgramExec->addFunctionCall(aCall2);
	
	test_utils::compareProgramExecutions(*expectedProgramExec, *receivedProgramExec);
}

void AnnotatorTest::testNonAnnotatedCodeIsSkipped()
{
	Annotator::resetAnnotations();
	//ANNOTATED CODE TO RUN
	myPrint( "Hello world!" );
	MyFunctions::add(4, 5);
	int i = 2;
	myPrint( boost::lexical_cast< std::string > (i) );
	MyFunctions::subtract(4,5);
	myPrint( "On the Internet nobody knows you're a dog." );
	////////////////////////

	boost::shared_ptr< ProgramExecution > receivedProgramExec = Annotator::instance().getProgramExecution();
	
	//Create expected program execution
	//1st object: My Functions Module
	boost::shared_ptr< LanguageObject > myFunctionsModule;
	boost::shared_ptr< ProgramExecution > expectedProgramExec;

	createBasicTestData(myFunctionsModule, expectedProgramExec);

	ArgumentsVector argsVector;

	//2nd object: Built ins module
	boost::shared_ptr< LanguageObject > builtIns = boost::make_shared< LanguageObject >(2L, LanguageType::MODULE, NULL_PARENT, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString(CPlusPlusConstants::BUILTINS_MODULE_NAME));
	expectedProgramExec->addLanguageObject(builtIns);
	//3rd object: int type
	boost::shared_ptr< LanguageObject > intType = boost::make_shared< LanguageObject >(3L, LanguageType::CLASS, builtIns, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("int"));
	expectedProgramExec->addLanguageObject(intType);
	//Parameters: 4 and 5 (instances of "int" type)
	boost::shared_ptr< LanguageObject > arg1 = boost::make_shared< LanguageObject >(4L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "4");
	boost::shared_ptr< LanguageObject > arg2 = boost::make_shared< LanguageObject >(5L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "5");
	expectedProgramExec->addLanguageObject(arg1); //Default values: VALUE and not isConst
	expectedProgramExec->addLanguageObject(arg2); //Default values: VALUE and not isConst

	argsVector.push_back(Argument(arg1));
	argsVector.push_back(Argument(arg2));

	boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(1L, myFunctionsModule, "add", FunctionCall::MethodType::METHOD, argsVector, 0, NULL_TOTAL_TIME);
	boost::shared_ptr< FunctionCall > aCall2 = boost::make_shared< FunctionCall >(2L, myFunctionsModule, "subtract", FunctionCall::MethodType::METHOD, argsVector, 0, NULL_TOTAL_TIME);

	expectedProgramExec->addFunctionCall(aCall);
	expectedProgramExec->addFunctionCall(aCall2);
	
	test_utils::compareProgramExecutions(*expectedProgramExec, *receivedProgramExec);
}

void AnnotatorTest::testInnerFunctionLevel()
{
	Annotator::resetAnnotations();
	//ANNOTATED CODE TO RUN
	MyFunctions::outerFunction();
	////////////////////////

	boost::shared_ptr< ProgramExecution > receivedProgramExec = Annotator::instance().getProgramExecution();
	
	//Create expected program execution
	boost::shared_ptr< LanguageObject > myFunctionsModule;
	boost::shared_ptr< ProgramExecution > expectedProgramExec;

	createBasicTestData(myFunctionsModule, expectedProgramExec);

	ArgumentsVector argsVector;

	//Inner function is returned, but with a different function level
	boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(1L, myFunctionsModule, "outerFunction", FunctionCall::MethodType::METHOD, argsVector, 0, NULL_TOTAL_TIME);
	boost::shared_ptr< FunctionCall > aCall2 = boost::make_shared< FunctionCall >(2L, myFunctionsModule, "innerFunction", FunctionCall::MethodType::METHOD, argsVector, 1, NULL_TOTAL_TIME);

	expectedProgramExec->addFunctionCall(aCall);
	expectedProgramExec->addFunctionCall(aCall2);

	test_utils::compareProgramExecutions(*expectedProgramExec, *receivedProgramExec);
}

void AnnotatorTest::testAnnotatedClassWithoutConstructor()
{
	Annotator::resetAnnotations();
	//ANNOTATED CODE TO RUN
	MyFunctions::MyClass foo;
	foo.f1();
	foo.f2(5);

	std::vector<int> myVector;
	myVector.push_back(5);

	std::map< std::string, int > myMap;
	myMap["x"] = 1;
	myMap["y"] = 2;
	foo.f3(myVector);
	foo.f4(myMap, NULL);
	////////////////////////

	boost::shared_ptr< ProgramExecution > receivedProgramExec = Annotator::instance().getProgramExecution();
	
	//Create expected program execution
	boost::shared_ptr< LanguageObject > myFunctionsModule;
	boost::shared_ptr< ProgramExecution > expectedProgramExec;

	createBasicTestData(myFunctionsModule, expectedProgramExec);

	ArgumentsVector argsVector;

	///////////////////////   f1  //////////////////////////////
	//2nd object: MyClass
	boost::shared_ptr< LanguageObject > myClassLo = boost::make_shared< LanguageObject >(2L, LanguageType::CLASS, myFunctionsModule, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("MyClass"));
	expectedProgramExec->addLanguageObject(myClassLo);

	//3rd object: MyClass instance
	boost::shared_ptr< LanguageObject > myInstanceLo = boost::make_shared< LanguageObject >(3L, LanguageType::INSTANCE, myClassLo, LanguageObject::DeclarationTypes::CONSTRUCTOR);
	expectedProgramExec->addLanguageObject(myInstanceLo);

	//Call f1
	boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(1L, myInstanceLo, "f1", FunctionCall::MethodType::METHOD, argsVector, 0, NULL_TOTAL_TIME);
	expectedProgramExec->addFunctionCall(aCall);
	///////////////////////////////////////////////////////////

	///////////////////////   f2  //////////////////////////////
	//4th object: built ins module
	boost::shared_ptr< LanguageObject > builtIns = boost::make_shared< LanguageObject >(4L, LanguageType::MODULE, NULL_PARENT, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString(CPlusPlusConstants::BUILTINS_MODULE_NAME));
	expectedProgramExec->addLanguageObject(builtIns);

	//5th object: int type
	boost::shared_ptr< LanguageObject > intType = boost::make_shared< LanguageObject >(5L, LanguageType::CLASS, builtIns, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("int"));
	expectedProgramExec->addLanguageObject(intType);

	//6th object: Parameter 5 (instance of "int" type)
	boost::shared_ptr< LanguageObject > arg1 = boost::make_shared< LanguageObject >(6L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "5");
	expectedProgramExec->addLanguageObject(arg1); //Default values: VALUE and not isConst
	argsVector.push_back(Argument(arg1));
	//Call f2
	boost::shared_ptr< FunctionCall > aCall2 = boost::make_shared< FunctionCall >(2L, myInstanceLo, "f2", FunctionCall::MethodType::METHOD, argsVector, 0, NULL_TOTAL_TIME);
	expectedProgramExec->addFunctionCall(aCall2);
	////////////////////////////////////////////////////////////

	///////////////////////   f3  //////////////////////////////
	//7th object: vector module
	ArgumentsVector argsVector3;
	boost::shared_ptr< LanguageObject > vectorMod = boost::make_shared< LanguageObject >(7L, LanguageType::MODULE, NULL_PARENT, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("vector"));
	expectedProgramExec->addLanguageObject(vectorMod);

	//8th object:
	boost::shared_ptr< LanguageObject > vectorClassLo = boost::make_shared< LanguageObject >(8L, LanguageType::CLASS, vectorMod, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("std::vector<int>"));
	expectedProgramExec->addLanguageObject(vectorClassLo);

	//9th object: Parameter: [5] (instance of "vector" type)
	boost::shared_ptr< LanguageObject > arg2 = boost::make_shared< LanguageObject >(9L, LanguageType::INSTANCE, vectorClassLo, LanguageObject::DeclarationTypes::FIXED_VALUE, "[ 5 ]");
	expectedProgramExec->addLanguageObject(arg2); //Default values: VALUE and not isConst
	argsVector3.push_back(Argument(arg2, Argument::REFERENCE, true));
	//Call f3
	boost::shared_ptr< FunctionCall > aCall3 = boost::make_shared< FunctionCall >(3L, myInstanceLo, "f3", FunctionCall::MethodType::METHOD, argsVector3, 0, NULL_TOTAL_TIME);
	expectedProgramExec->addFunctionCall(aCall3);
	////////////////////////////////////////////////////////////

	///////////////////////   f4  //////////////////////////////
	//10th object: map module
	ArgumentsVector argsMap4;
	boost::shared_ptr< LanguageObject > mapMod = boost::make_shared< LanguageObject >(10L, LanguageType::MODULE, NULL_PARENT, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("map"));
	expectedProgramExec->addLanguageObject(mapMod);

	//8th object:
	boost::shared_ptr< LanguageObject > mapClassLo = boost::make_shared< LanguageObject >(11L, LanguageType::CLASS, mapMod, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("std::map<std::string,int>"));
	expectedProgramExec->addLanguageObject(mapClassLo);

	//9th object: Parameter: { "y" : 2 , "x" : 1 } (instance of "map" type)
	boost::shared_ptr< LanguageObject > arg3 = boost::make_shared< LanguageObject >(12L, LanguageType::INSTANCE, mapClassLo, LanguageObject::DeclarationTypes::FIXED_VALUE, "\n{\n    \"x\" : 1,\n    \"y\" : 2\n}");
	expectedProgramExec->addLanguageObject(arg3); //Default values: VALUE and not isConst
	boost::shared_ptr< LanguageObject > arg4 = boost::make_shared< LanguageObject >(13L, LanguageType::INSTANCE, myClassLo, LanguageObject::DeclarationTypes::FIXED_VALUE, "null");
	expectedProgramExec->addLanguageObject(arg4); //Default values: VALUE and not isConst
	argsMap4.push_back(Argument(arg3));
	argsMap4.push_back(Argument(arg4, Argument::POINTER));
	//Call f3
	boost::shared_ptr< FunctionCall > aCall4 = boost::make_shared< FunctionCall >(4L, myInstanceLo, "f4", FunctionCall::MethodType::METHOD, argsMap4, 0, NULL_TOTAL_TIME);
	expectedProgramExec->addFunctionCall(aCall4);
	////////////////////////////////////////////////////////////

	test_utils::compareProgramExecutions(*expectedProgramExec, *receivedProgramExec);
}

void AnnotatorTest::testAnnotatedClassWithConstructor()
{
	Annotator::resetAnnotations();
	//ANNOTATED CODE TO RUN

	MyFunctions::ClassWithConstructor foo(1,2);
	int x = foo.getX();
	foo.setX(5);
	int y = foo.getY();
	foo.setY(10);
	myPrint( "Get rid of the warnings ;) " + boost::lexical_cast< std::string >(x + y) );
	////////////////////////

	boost::shared_ptr< ProgramExecution > receivedProgramExec = Annotator::instance().getProgramExecution();
	
	//Create expected program execution
	boost::shared_ptr< LanguageObject > myFunctionsModule;
	boost::shared_ptr< ProgramExecution > expectedProgramExec;

	createBasicTestData(myFunctionsModule, expectedProgramExec);

	ArgumentsVector argsVector;

	///////////////////////   Constructor  //////////////////////////////
	//2nd object: MyClass
	boost::shared_ptr< LanguageObject > myClassLo = boost::make_shared< LanguageObject >(2L, LanguageType::CLASS, myFunctionsModule, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("ClassWithConstructor"));
	expectedProgramExec->addLanguageObject(myClassLo);

	//3rd object: MyClass instance
	boost::shared_ptr< LanguageObject > myInstanceLo = boost::make_shared< LanguageObject >(3L, LanguageType::INSTANCE, myClassLo, LanguageObject::DeclarationTypes::CONSTRUCTOR);
	expectedProgramExec->addLanguageObject(myInstanceLo);

	//4th object: built ins module
	boost::shared_ptr< LanguageObject > builtIns = boost::make_shared< LanguageObject >(4L, LanguageType::MODULE, NULL_PARENT, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString(CPlusPlusConstants::BUILTINS_MODULE_NAME));
	expectedProgramExec->addLanguageObject(builtIns);

	//5th object: int type
	boost::shared_ptr< LanguageObject > intType = boost::make_shared< LanguageObject >(5L, LanguageType::CLASS, builtIns, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("int"));
	expectedProgramExec->addLanguageObject(intType);

	//6th object: Parameter 1 (instance of "int" type)
	boost::shared_ptr< LanguageObject > arg1 = boost::make_shared< LanguageObject >(6L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "1");
	expectedProgramExec->addLanguageObject(arg1); //Default values: VALUE and not isConst
	argsVector.push_back(Argument(arg1));

	//7th object: Parameter 2 (instance of "int" type)
	boost::shared_ptr< LanguageObject > arg2 = boost::make_shared< LanguageObject >(7L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "2");
	expectedProgramExec->addLanguageObject(arg2); //Default values: VALUE and not isConst
	argsVector.push_back(Argument(arg2));

	//Call constructor
	boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(1L, myInstanceLo, "ClassWithConstructor", FunctionCall::MethodType::CONSTRUCTOR, argsVector, 0, NULL_TOTAL_TIME);
	expectedProgramExec->addFunctionCall(aCall);
	///////////////////////////////////////////////////////////

	///////////////////////   getX  //////////////////////////////
	//Call getX
	ArgumentsVector argsVectorGetX;
	boost::shared_ptr< FunctionCall > aCall2 = boost::make_shared< FunctionCall >(2L, myInstanceLo, "getX", FunctionCall::MethodType::METHOD, argsVectorGetX, 0, NULL_TOTAL_TIME);
	expectedProgramExec->addFunctionCall(aCall2);
	////////////////////////////////////////////////////////////

	///////////////////////   setX  //////////////////////////////
	ArgumentsVector argsVectorSetX;

	//6th object: Parameter 5 (instance of "int" type)
	boost::shared_ptr< LanguageObject > arg5 = boost::make_shared< LanguageObject >(8L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "5");
	expectedProgramExec->addLanguageObject(arg5); //Default values: VALUE and not isConst
	argsVectorSetX.push_back(Argument(arg5));
	//Call setX
	boost::shared_ptr< FunctionCall > aCall3 = boost::make_shared< FunctionCall >(3L, myInstanceLo, "setX", FunctionCall::MethodType::METHOD, argsVectorSetX, 0, NULL_TOTAL_TIME);
	expectedProgramExec->addFunctionCall(aCall3);
	////////////////////////////////////////////////////////////

	///////////////////////   getY  //////////////////////////////
	//Call getX
	ArgumentsVector argsVectorGetY;
	boost::shared_ptr< FunctionCall > aCall4 = boost::make_shared< FunctionCall >(4L, myInstanceLo, "getY", FunctionCall::MethodType::METHOD, argsVectorGetY, 0, NULL_TOTAL_TIME);
	expectedProgramExec->addFunctionCall(aCall4);
	////////////////////////////////////////////////////////////

	///////////////////////   setY  //////////////////////////////
	ArgumentsVector argsVectorSetY;

	//6th object: Parameter 10 (instance of "int" type)
	boost::shared_ptr< LanguageObject > arg10 = boost::make_shared< LanguageObject >(9L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "10");
	expectedProgramExec->addLanguageObject(arg10); //Default values: VALUE and not isConst
	argsVectorSetY.push_back(Argument(arg10));
	//Call setY
	boost::shared_ptr< FunctionCall > aCall5 = boost::make_shared< FunctionCall >(5L, myInstanceLo, "setY", FunctionCall::MethodType::METHOD, argsVectorSetY, 0, NULL_TOTAL_TIME);
	expectedProgramExec->addFunctionCall(aCall5);
	////////////////////////////////////////////////////////////

	test_utils::compareProgramExecutions(*expectedProgramExec, *receivedProgramExec);
}

void AnnotatorTest::testAnnotatedClassWithStaticMethods()
{
	Annotator::resetAnnotations();
	//ANNOTATED CODE TO RUN
	MyFunctions::ClassWithStaticMethods::static0();
	MyFunctions::ClassWithStaticMethods::static1(5);
	////////////////////////

	boost::shared_ptr< ProgramExecution > receivedProgramExec = Annotator::instance().getProgramExecution();
	
	//Create expected program execution
	boost::shared_ptr< LanguageObject > myFunctionsModule;
	boost::shared_ptr< ProgramExecution > expectedProgramExec;

	createBasicTestData(myFunctionsModule, expectedProgramExec);

	ArgumentsVector argsVector;

	///////////////////////   static0  //////////////////////////////
	//2nd object: MyClass
	boost::shared_ptr< LanguageObject > myClassLo = boost::make_shared< LanguageObject >(2L, LanguageType::CLASS, myFunctionsModule, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("ClassWithStaticMethods"));
	expectedProgramExec->addLanguageObject(myClassLo);

	//Call static0
	boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(1L, myClassLo, "static0", FunctionCall::MethodType::STATIC_METHOD, argsVector, 0, NULL_TOTAL_TIME);
	expectedProgramExec->addFunctionCall(aCall);

	///////////////////////   static1  //////////////////////////////
	//built ins module
	boost::shared_ptr< LanguageObject > builtIns = boost::make_shared< LanguageObject >(3L, LanguageType::MODULE, NULL_PARENT, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString(CPlusPlusConstants::BUILTINS_MODULE_NAME));
	expectedProgramExec->addLanguageObject(builtIns);

	//int type
	boost::shared_ptr< LanguageObject > intType = boost::make_shared< LanguageObject >(4L, LanguageType::CLASS, builtIns, LanguageObject::DeclarationTypes::FIXED_VALUE, jsonString("int"));
	expectedProgramExec->addLanguageObject(intType);

	//6th object: Parameter 1 (instance of "int" type)
	boost::shared_ptr< LanguageObject > arg1 = boost::make_shared< LanguageObject >(5L, LanguageType::INSTANCE, intType, LanguageObject::DeclarationTypes::FIXED_VALUE, "5");
	expectedProgramExec->addLanguageObject(arg1); //Default values: VALUE and not isConst
	argsVector.push_back(Argument(arg1));

	//Call static0
	boost::shared_ptr< FunctionCall > aCall2 = boost::make_shared< FunctionCall >(2L, myClassLo, "static1", FunctionCall::MethodType::STATIC_METHOD, argsVector, 0, NULL_TOTAL_TIME);
	expectedProgramExec->addFunctionCall(aCall2);
	///////////////////////////////////////////////////////////

	test_utils::compareProgramExecutions(*expectedProgramExec, *receivedProgramExec);
}