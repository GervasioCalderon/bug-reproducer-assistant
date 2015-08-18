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

// bug_reproducer_assistant
#include <bug_reproducer_assistant/LanguageType.h>
#include <bug_reproducer_assistant/LanguageObject.h>
#include <bug_reproducer_assistant/Argument.h>
#include <bug_reproducer_assistant/FunctionCall.h>
#include <bug_reproducer_assistant/CallGraphSerializer.h>
#include <bug_reproducer_assistant/ProgramExecution.h>
//cppunit
#include <cppunit/extensions/HelperMacros.h>
//test_utils
#include "test_utils/test_utils.h"

namespace test_utils
{
using namespace bug_reproducer_assistant;

void compareProgramExecutions(const ProgramExecution& programExec1, const ProgramExecution& programExec2)
{
	//Compare languages
	CPPUNIT_ASSERT_EQUAL(programExec1.getLanguage(), programExec2.getLanguage());

	//Compare LanguageObjects
	IdToLanguageObjectMap langObjects1 = programExec1.getLanguageObjects();
	IdToLanguageObjectMap langObjects2 = programExec2.getLanguageObjects();

	//Use an auxiliary set to hold languageObject2's keys
	//Inside langObjects1 cycle, all keys should be removed from the set if both dicts are equal

	IdToLanguageObjectMap langObjectKeys2 = langObjects2;

	for ( IdToLanguageObjectMap::iterator it = langObjects1.begin(); it != langObjects1.end(); ++it )
	{
		id_t id = it->first;
		boost::shared_ptr< LanguageObject > langObject = it->second;
		CPPUNIT_ASSERT(langObjectKeys2.find(id) != langObjectKeys2.end());
		boost::shared_ptr< LanguageObject > langObject2 = langObjects2[id];
		compareLanguageObjects(langObject, langObject2);
		langObjectKeys2.erase(id);
	}
	
	//Ensure both containers have the same size
	CPPUNIT_ASSERT(langObjectKeys2.empty());

	//Compare FunctionCall's
	FunctionCallsVector calls = programExec1.getFunctionCalls();
	FunctionCallsVector calls2 = programExec2.getFunctionCalls();

	//Compare calls array. Order is important, so we assume it's possible to compare element by element
	size_t length = calls.size();
	CPPUNIT_ASSERT_EQUAL(length, calls2.size());

	for ( size_t i = 0; i <length; ++i )
	{
		boost::shared_ptr< FunctionCall > call1 = calls[i];
		boost::shared_ptr< FunctionCall > call2 = calls2[i];
		//This is similar to language objects parents' comparison above:
		//Compare just the id's.
		//Objects from the container must be equal, so any difference should have been detected above
		compareLanguageObjects(call1->getCallee(), call2->getCallee());
		CPPUNIT_ASSERT_EQUAL(call1->getFunctionName(), call2->getFunctionName());
		CPPUNIT_ASSERT_EQUAL(call1->getMethodType(), call2->getMethodType());
		//Compare arguments
		ArgumentsVector argsList1 = call1->getArgsVector();
		ArgumentsVector argsList2 = call2->getArgsVector();

		//This is similar to calls array. Order does matter, so we assume it's possible to compare element by element
		size_t argsLength = argsList1.size();
		CPPUNIT_ASSERT_EQUAL(argsLength, argsList2.size());
		for ( size_t j = 0; j <argsLength; ++j )
		{
			compareLanguageObjects(argsList1[j].getLanguageObject(), argsList2[j].getLanguageObject());
			CPPUNIT_ASSERT_EQUAL(argsList1[j].getArgumentType(), argsList2[j].getArgumentType());
			CPPUNIT_ASSERT_EQUAL(argsList1[j].isConst(), argsList2[j].isConst());
		}
		CPPUNIT_ASSERT_EQUAL(call1->getLevel(), call2->getLevel());
		CPPUNIT_ASSERT_EQUAL(call1->getTotalTime(), call2->getTotalTime());
	}
}

void compareLanguageObjects(const boost::shared_ptr< LanguageObject >& langObject1, const boost::shared_ptr< LanguageObject >& langObject2)
{
	bool bothNone = !langObject1 && !langObject2;
	if (!bothNone)
	{
		//Both none => OK
		CPPUNIT_ASSERT_EQUAL(langObject1->getId(), langObject2->getId());
		CPPUNIT_ASSERT_EQUAL(langObject1->getLanguageType(), langObject2->getLanguageType());
		CPPUNIT_ASSERT_EQUAL(langObject1->getDeclarationType(), langObject2->getDeclarationType());
		CPPUNIT_ASSERT_EQUAL(langObject1->getDeclarationCode(), langObject2->getDeclarationCode());
		//To compare parents:
		//Compare Id's
		//Parents must be in the container, so they're compared another time in this very cycle
		boost::shared_ptr< LanguageObject > parent1 = langObject1->getParent();
		boost::shared_ptr< LanguageObject > parent2 = langObject2->getParent();
        bothNone = !parent1 && !parent2;
		CPPUNIT_ASSERT(bothNone || parent1->getId() == parent2->getId());
	}
}

} // test_utils
