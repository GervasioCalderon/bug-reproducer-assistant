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
#include <memory>
#include <cstdlib>
//Boost
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/make_shared.hpp>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/LanguageType.h>
#include <bug_reproducer_assistant/LanguageObject.h>
#include <bug_reproducer_assistant/Argument.h>
#include <bug_reproducer_assistant/FunctionCall.h>
#include <bug_reproducer_assistant/CallGraphSerializer.h>
#include <bug_reproducer_assistant/ProgramExecution.h>
//test_utils
#include <test_utils/test_utils.h>
//serialization_test
#include "serialization_test_suite.h"

CPPUNIT_TEST_SUITE_REGISTRATION(SerializationTest);

using namespace bug_reproducer_assistant;

namespace
{
	std::auto_ptr< ProgramExecution > createSampleProgramExecution_()
	{
		boost::shared_ptr< LanguageObject > nullParent;
		boost::optional< boost::posix_time::time_duration > nullTotalTime = boost::optional< boost::posix_time::time_duration >();

		std::auto_ptr< ProgramExecution > myProgramExecution(new ProgramExecution("C++"));

		boost::shared_ptr< LanguageObject > mod = boost::make_shared< LanguageObject >(1l, LanguageType::MODULE, nullParent, LanguageObject::DeclarationTypes::FIXED_VALUE, "\"dir//dir2//header1.h\"");
		myProgramExecution->addLanguageObject(mod);
		boost::shared_ptr< LanguageObject > cls = boost::make_shared< LanguageObject >(2L, LanguageType::CLASS, mod, LanguageObject::DeclarationTypes::CONSTRUCTOR, "\"Class1\"");
		myProgramExecution->addLanguageObject(cls);
		boost::shared_ptr< LanguageObject > obj = boost::make_shared< LanguageObject >(3L, LanguageType::INSTANCE, cls, LanguageObject::DeclarationTypes::FIXED_VALUE, "5");
		myProgramExecution->addLanguageObject(obj);
		boost::shared_ptr< LanguageObject > obj2 = boost::make_shared< LanguageObject >(4L, LanguageType::INSTANCE, cls, LanguageObject::DeclarationTypes::FIXED_VALUE, "25");
		myProgramExecution->addLanguageObject(obj2);
		boost::shared_ptr< LanguageObject > obj3 = boost::make_shared< LanguageObject >(5L, LanguageType::INSTANCE, cls, LanguageObject::DeclarationTypes::CONSTRUCTOR, "\"Gerva\"");
		myProgramExecution->addLanguageObject(obj3);

		ArgumentsVector argsVector;
		argsVector.push_back(Argument(obj));
		argsVector.push_back(Argument(obj2, Argument::POINTER));
		argsVector.push_back(Argument(obj3, Argument::REFERENCE, true));

		boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(1L, mod, "fun", FunctionCall::MethodType::METHOD, argsVector, 0, nullTotalTime);
		boost::shared_ptr< FunctionCall > aCall2 = boost::make_shared< FunctionCall >(2L, cls, "static_fun", FunctionCall::MethodType::STATIC_METHOD, argsVector, 1, nullTotalTime);
		boost::shared_ptr< FunctionCall > aCall3 = boost::make_shared< FunctionCall >(3L, obj3, "Class1", FunctionCall::MethodType::CONSTRUCTOR, argsVector, 0, nullTotalTime);
		boost::shared_ptr< FunctionCall > aCall4 = boost::make_shared< FunctionCall >(4L, obj3, "obj_fun", FunctionCall::MethodType::METHOD, argsVector, 1, nullTotalTime);

		myProgramExecution->addFunctionCall(aCall);
		myProgramExecution->addFunctionCall(aCall2);
		myProgramExecution->addFunctionCall(aCall3);
		myProgramExecution->addFunctionCall(aCall4);
		return myProgramExecution;
	}
}

void SerializationTest::testSerialization()
{
	std::auto_ptr< ProgramExecution > myProgramExecution = createSampleProgramExecution_();
	CallGraphSerializer aSerializer;

	std::string tempDir = std::getenv("TEMP");
	//TODO GERVA: use boost file system
	std::string fileName = tempDir + "\\call_graph.json";

	std::ofstream jsonFileOut(fileName.c_str());
	CPPUNIT_ASSERT(jsonFileOut.is_open());

	aSerializer.dump(*myProgramExecution, jsonFileOut);
	jsonFileOut.close();

	std::ifstream jsonFileIn(fileName.c_str());
	CPPUNIT_ASSERT(jsonFileIn.is_open());

	std::auto_ptr< ProgramExecution > loadedProgramExecution = aSerializer.load(jsonFileIn);
	jsonFileIn.close();
	
	test_utils::compareProgramExecutions(*myProgramExecution, *loadedProgramExecution);
}