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

//Boost
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/make_shared.hpp>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/LanguageType.h>
#include <bug_reproducer_assistant/LanguageObject.h>
#include <bug_reproducer_assistant/Argument.h>
#include <bug_reproducer_assistant/FunctionCall.h>
#include <bug_reproducer_assistant/ProgramExecution.h>
//call_graph_test
#include "call_graph_test_suite.h"

CPPUNIT_TEST_SUITE_REGISTRATION(CallGraphTest);

using namespace bug_reproducer_assistant;

namespace
{
	void moduleWithParentModule(id_t id, boost::shared_ptr< LanguageObject > mod)
	{
		LanguageObject mod2(id, LanguageType::MODULE, mod, LanguageObject::DeclarationTypes::FIXED_VALUE, "header2.h");
	}

	void parentlessClass(id_t id)
	{
		LanguageObject aClass(id, LanguageType::CLASS, boost::shared_ptr< LanguageObject >(), LanguageObject::DeclarationTypes::FIXED_VALUE, "AClass");
	}

	void instanceWithModuleParent(id_t id, boost::shared_ptr< LanguageObject > mod)
	{
		LanguageObject anInstance(id, LanguageType::INSTANCE, mod, LanguageObject::DeclarationTypes::FIXED_VALUE, "\"Gerva\"");
	}
	
	void languageObjectWithDuplicatedId(ProgramExecution& aProgramExecution, id_t id, const boost::shared_ptr< LanguageObject > cls)
	{
		boost::shared_ptr< LanguageObject > obj = boost::make_shared< LanguageObject >(id, LanguageType::INSTANCE, cls, LanguageObject::DeclarationTypes::FIXED_VALUE, "5");
		aProgramExecution.addLanguageObject(obj);
	}

	template < class ElemType >
	void compareVectors(const std::vector< ElemType > lhs, const std::vector< ElemType > rhs)
	{
		size_t lsize = lhs.size();
		CPPUNIT_ASSERT_EQUAL(lsize, rhs.size());
		for( size_t i = 0; i < lsize; ++i )
		{
			CPPUNIT_ASSERT_EQUAL(lhs[i], rhs[i]);
		}
	}
}

void CallGraphTest::testLanguageType()
{
		CPPUNIT_ASSERT_EQUAL(LanguageType::asString(LanguageType::MODULE), std::string("Module"));
		CPPUNIT_ASSERT_EQUAL(LanguageType::asString(LanguageType::MODULE), std::string("Module"));
		CPPUNIT_ASSERT_EQUAL(LanguageType::asString(LanguageType::CLASS), std::string("Class"));
		CPPUNIT_ASSERT_EQUAL(LanguageType::asString(LanguageType::INSTANCE), std::string("Instance"));
		CPPUNIT_ASSERT(LanguageType::isValidParent(LanguageType::NONE, LanguageType::MODULE));
		CPPUNIT_ASSERT(LanguageType::isValidParent(LanguageType::MODULE, LanguageType::CLASS));
		CPPUNIT_ASSERT(LanguageType::isValidParent(LanguageType::CLASS, LanguageType::INSTANCE));

		CPPUNIT_ASSERT(!LanguageType::isValidParent(LanguageType::INSTANCE, LanguageType::MODULE));
		CPPUNIT_ASSERT(!LanguageType::isValidParent(LanguageType::INSTANCE, LanguageType::MODULE));
		CPPUNIT_ASSERT(!LanguageType::isValidParent(LanguageType::INSTANCE, LanguageType::CLASS));
		CPPUNIT_ASSERT(!LanguageType::isValidParent(LanguageType::INSTANCE, LanguageType::INSTANCE));
		CPPUNIT_ASSERT(!LanguageType::isValidParent(LanguageType::MODULE, LanguageType::MODULE));
		CPPUNIT_ASSERT(!LanguageType::isValidParent(LanguageType::MODULE, LanguageType::INSTANCE));
		CPPUNIT_ASSERT(!LanguageType::isValidParent(LanguageType::CLASS, LanguageType::MODULE));
		CPPUNIT_ASSERT(!LanguageType::isValidParent(LanguageType::CLASS, LanguageType::CLASS));
}

void CallGraphTest::testLanguageObject()
{
	boost::shared_ptr< LanguageObject > nullParent;
	boost::shared_ptr< LanguageObject > mod = boost::make_shared< LanguageObject >(1l, LanguageType::MODULE, nullParent, LanguageObject::DeclarationTypes::FIXED_VALUE, "\"dir//header1.h\"");
	
	CPPUNIT_ASSERT_EQUAL(mod->getId(), 1L);
	CPPUNIT_ASSERT_EQUAL(mod->getLanguageType(), LanguageType::MODULE);
	CPPUNIT_ASSERT_EQUAL(mod->getDeclarationType(), LanguageObject::DeclarationTypes::FIXED_VALUE);
	CPPUNIT_ASSERT_EQUAL(mod->getDeclarationCode(), std::string("\"dir//header1.h\""));
	CPPUNIT_ASSERT(!mod->getParent());
        
        
	CPPUNIT_ASSERT_THROW(moduleWithParentModule(2L, mod), LanguageObject::InvalidParentException);
	CPPUNIT_ASSERT_THROW(parentlessClass(3L), LanguageObject::InvalidParentException);

	//Parent should be ok, no InvalidParentException thrown
	boost::shared_ptr< LanguageObject > aClass = boost::make_shared< LanguageObject >(2L, LanguageType::CLASS, mod, LanguageObject::DeclarationTypes::FIXED_VALUE, "AClass");
	
	CPPUNIT_ASSERT_EQUAL(aClass->getId(), 2L);
	CPPUNIT_ASSERT_EQUAL(aClass->getLanguageType(), LanguageType::CLASS);
	CPPUNIT_ASSERT_EQUAL(aClass->getDeclarationType(), LanguageObject::DeclarationTypes::FIXED_VALUE);
	CPPUNIT_ASSERT_EQUAL(aClass->getDeclarationCode(), std::string("AClass"));
	CPPUNIT_ASSERT_EQUAL(aClass->getParent(), mod);

	CPPUNIT_ASSERT_THROW(instanceWithModuleParent(3L, mod), LanguageObject::InvalidParentException);
	
	//Class parent is ok for an instance
    boost::shared_ptr< LanguageObject > anInstance = boost::make_shared< LanguageObject >(3L, LanguageType::INSTANCE, aClass, LanguageObject::DeclarationTypes::FIXED_VALUE, "\"Gerva\"");
	
	CPPUNIT_ASSERT_EQUAL(anInstance->getId(), 3L);
	CPPUNIT_ASSERT_EQUAL(anInstance->getLanguageType(), LanguageType::INSTANCE);
	CPPUNIT_ASSERT_EQUAL(anInstance->getDeclarationCode(), std::string("\"Gerva\""));
	CPPUNIT_ASSERT_EQUAL(anInstance->getParent(), aClass);
}

void CallGraphTest::testArgument()
{
	boost::shared_ptr< LanguageObject > nullParent;
	boost::shared_ptr< LanguageObject > mod = boost::make_shared< LanguageObject >(1l, LanguageType::MODULE, nullParent, LanguageObject::DeclarationTypes::FIXED_VALUE, "\"dir//header1.h\"");
	
	Argument arg(mod);
	CPPUNIT_ASSERT_EQUAL(arg.getLanguageObject(), mod);
	CPPUNIT_ASSERT_EQUAL(arg.getArgumentType(), Argument::VALUE);
	CPPUNIT_ASSERT_EQUAL(arg.isConst(), false);

	Argument arg2(mod, Argument::POINTER);
	CPPUNIT_ASSERT_EQUAL(arg2.getLanguageObject(), mod);
	CPPUNIT_ASSERT_EQUAL(arg2.getArgumentType(), Argument::POINTER);
	CPPUNIT_ASSERT_EQUAL(arg2.isConst(), false);

	Argument arg3(mod, Argument::REFERENCE, true);
	CPPUNIT_ASSERT_EQUAL(arg3.getLanguageObject(), mod);
	CPPUNIT_ASSERT_EQUAL(arg3.getArgumentType(), Argument::REFERENCE);
	CPPUNIT_ASSERT_EQUAL(arg3.isConst(), true);


}

void CallGraphTest::testFunctionCall()
{
	using namespace boost::posix_time;
	ptime start = second_clock::universal_time();

	boost::shared_ptr< LanguageObject > nullParent;
	boost::shared_ptr< LanguageObject > mod = boost::make_shared< LanguageObject >(1l, LanguageType::MODULE, nullParent, LanguageObject::DeclarationTypes::FIXED_VALUE, "\"dir//header1.h\"");
	boost::shared_ptr< LanguageObject > cls = boost::make_shared< LanguageObject >(2L, LanguageType::CLASS, mod, LanguageObject::DeclarationTypes::FIXED_VALUE, "AClass");
	boost::shared_ptr< LanguageObject > obj = boost::make_shared< LanguageObject >(3L, LanguageType::INSTANCE, cls, LanguageObject::DeclarationTypes::FIXED_VALUE, "5");
	boost::shared_ptr< LanguageObject > obj2 = boost::make_shared< LanguageObject >(4L, LanguageType::INSTANCE, cls, LanguageObject::DeclarationTypes::FIXED_VALUE, "\"Gerva\"");

	ArgumentsVector argsVector;
	argsVector.push_back(Argument(obj));
	argsVector.push_back(Argument(obj2, Argument::POINTER, true));
	argsVector.push_back(Argument(obj2, Argument::REFERENCE));

	FunctionCall aCall(1L, mod, "fun", FunctionCall::MethodType::METHOD, argsVector, 1, boost::optional< time_duration >());
	FunctionCall aCall2(2L, mod, "fun2", FunctionCall::MethodType::METHOD, argsVector, 2, boost::optional< time_duration >());

	CPPUNIT_ASSERT_EQUAL(aCall.getId(), 1L);
	CPPUNIT_ASSERT_EQUAL(aCall.getCallee(), mod);
	CPPUNIT_ASSERT_EQUAL(aCall.getFunctionName(), std::string("fun"));

	compareVectors(aCall.getArgsVector(), argsVector);
	CPPUNIT_ASSERT(!aCall.getTotalTime());
	CPPUNIT_ASSERT_EQUAL(aCall2.getId(), 2L);
        
	ptime finish = second_clock::universal_time();
	time_duration totalTime = finish - start;
	
	FunctionCall aCall3(2L, mod, "fun3", FunctionCall::MethodType::METHOD, argsVector, 1, totalTime);
	CPPUNIT_ASSERT_EQUAL(*aCall3.getTotalTime(), totalTime);
}

void CallGraphTest::testProgramExecution()
{
	boost::shared_ptr< LanguageObject > nullParent;
	boost::optional< boost::posix_time::time_duration > nullTotalTime = boost::optional< boost::posix_time::time_duration >();

	ProgramExecution myProgramExecution("C++");
                
	LanguageTypesVector	theLanguageTypes = myProgramExecution.getLanguageTypes();

	CPPUNIT_ASSERT_EQUAL(LanguageType::NONE, theLanguageTypes[LanguageType::NONE]);
	CPPUNIT_ASSERT_EQUAL(LanguageType::MODULE, theLanguageTypes[LanguageType::MODULE]);
	CPPUNIT_ASSERT_EQUAL(LanguageType::CLASS, theLanguageTypes[LanguageType::CLASS]);
	CPPUNIT_ASSERT_EQUAL(LanguageType::INSTANCE, theLanguageTypes[LanguageType::INSTANCE]);


	boost::shared_ptr< LanguageObject > mod = boost::make_shared< LanguageObject >(1l, LanguageType::MODULE, nullParent, LanguageObject::DeclarationTypes::FIXED_VALUE, "\"dir//dir2//header1.h\"");
	myProgramExecution.addLanguageObject(mod);

	boost::shared_ptr< LanguageObject > cls = boost::make_shared< LanguageObject >(2L, LanguageType::CLASS, mod, LanguageObject::DeclarationTypes::FIXED_VALUE, "Class1");
	myProgramExecution.addLanguageObject(cls);
        
	//test duplicated id
	CPPUNIT_ASSERT_THROW(languageObjectWithDuplicatedId(myProgramExecution, 2L, cls), ProgramExecution::DuplicatedLanguageObjectIdException);

	boost::shared_ptr< LanguageObject > obj = boost::make_shared< LanguageObject >(3L, LanguageType::INSTANCE, cls, LanguageObject::DeclarationTypes::FIXED_VALUE, "5");
	myProgramExecution.addLanguageObject(obj);
	boost::shared_ptr< LanguageObject > obj2 = boost::make_shared< LanguageObject >(4L, LanguageType::INSTANCE, cls, LanguageObject::DeclarationTypes::FIXED_VALUE, "25");
	myProgramExecution.addLanguageObject(obj2);
	boost::shared_ptr< LanguageObject > obj3 = boost::make_shared< LanguageObject >(5L, LanguageType::INSTANCE, cls, LanguageObject::DeclarationTypes::CONSTRUCTOR, "");
	myProgramExecution.addLanguageObject(obj3);

	ArgumentsVector argsVector;
	argsVector.push_back(Argument(obj));
	argsVector.push_back(Argument(obj2, Argument::REFERENCE, true));

	boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(1L, mod, "fun", FunctionCall::MethodType::METHOD, argsVector, 0, nullTotalTime);
	boost::shared_ptr< FunctionCall > aCall2 = boost::make_shared< FunctionCall >(2L, cls, "static_fun", FunctionCall::MethodType::STATIC_METHOD, argsVector, 1, nullTotalTime);
	boost::shared_ptr< FunctionCall > aCall3 = boost::make_shared< FunctionCall >(3L, obj3, "Class1", FunctionCall::MethodType::CONSTRUCTOR, argsVector, 0, nullTotalTime);
	boost::shared_ptr< FunctionCall > aCall4 = boost::make_shared< FunctionCall >(4L, obj3, "obj_fun", FunctionCall::MethodType::METHOD, argsVector, 0, nullTotalTime);

	myProgramExecution.addFunctionCall(aCall);
	myProgramExecution.addFunctionCall(aCall2);
	myProgramExecution.addFunctionCall(aCall3);

	CPPUNIT_ASSERT_EQUAL(myProgramExecution.getLanguage(), std::string("C++"));

	IdToLanguageObjectMap theLanguageObejcts = myProgramExecution.getLanguageObjects();

	CPPUNIT_ASSERT_EQUAL( theLanguageObejcts[1], mod);
	CPPUNIT_ASSERT_EQUAL( theLanguageObejcts[2], cls);
	CPPUNIT_ASSERT_EQUAL( theLanguageObejcts[3], obj);
	CPPUNIT_ASSERT_EQUAL( theLanguageObejcts[4], obj2);
	CPPUNIT_ASSERT_EQUAL( theLanguageObejcts[5], obj3);

	FunctionCallsVector theCalls = myProgramExecution.getFunctionCalls();
	CPPUNIT_ASSERT_EQUAL(theCalls[0], aCall);
	CPPUNIT_ASSERT_EQUAL(theCalls[1], aCall2);
	CPPUNIT_ASSERT_EQUAL(theCalls[2], aCall3);
}