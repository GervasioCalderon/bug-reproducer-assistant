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

#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
#include <bug_reproducer_assistant/bug_reproducer_assistant.h>
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
//Boost
#include <boost/lexical_cast.hpp>
//annotator_test
#include "MyFunctions_annotated.h"

using namespace std;

//Empty print for not disturbing the unit tests output
void myPrint(const string& str)
{}

namespace MyFunctions
{

int add(int i,  int j)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("add", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h");
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", i);
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", j);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	return i + j;
}
	
int subtract(int i, int j)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("subtract", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h");
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", i);
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", j);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	return i - j;
}

std::string mySubstring(const string& str, size_t length)
{
	return str.substr(0, length);
}

void processVector( const vector< int >& aList )
{
	myPrint("Entered processVector");
	for ( vector< int >::const_iterator it = aList.begin(); it != aList.end(); ++it )
		myPrint ("elem: " + boost::lexical_cast< string >(*it) + "\n");
}

void processIntMap( const map<int,int>& aMap )
{
	myPrint("Entered processIntMap");
	for ( map< int, int >::const_iterator it = aMap.begin(); it != aMap.end(); ++it )
	{
		myPrint ("key: " + boost::lexical_cast< string >(it->first) + "\n");
		myPrint ("value: " + boost::lexical_cast< string >(it->second) + "\n");
	}
}

void innerFunction()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("innerFunction", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h");
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
}

void outerFunction()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("outerFunction", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h");
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	innerFunction();
}

void noParamsFunction()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("noParamsFunction", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h");
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
}

//MyClass
void MyClass::f1()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f1", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h", "MyClass", this);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	myPrint( "No params" );
}

void MyClass::f2(int i)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f2", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h", "MyClass", this);
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", i);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	myPrint( "i:" + boost::lexical_cast< string > (i) );
}

void MyClass::f3(const std::vector< int >& aVector)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f3", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h", "MyClass", this);
	bug_reproducer_assistant::Annotator::instance().addArgument("vector", "const std::vector<int>&", aVector);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	int x = aVector[0];
	myPrint( "x:" + boost::lexical_cast< string >(x) );
}
void MyClass::f4(std::map< std::string, int > aMap, MyClass * anObj)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f4", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h", "MyClass", this);
	bug_reproducer_assistant::Annotator::instance().addArgument("map", "std::map<std::string,int>", aMap);
	bug_reproducer_assistant::Annotator::instance().addArgument("MyFunctions.h", "MyClass*", anObj);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	int x = aMap["x"];
	int y = aMap["y"];
	myPrint("x: " + boost::lexical_cast< string >(x)+ ", y:" + boost::lexical_cast< string >(y) );
	if ( anObj == NULL )
		myPrint("anObj is NULL");
	else
		myPrint("anObj is not NULL");
}

//ClassWithConstructor
ClassWithConstructor::ClassWithConstructor(int x, int y):
	x_(x),
	y_(y)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("ClassWithConstructor", bug_reproducer_assistant::FunctionCall::MethodType::CONSTRUCTOR, "MyFunctions.h", "ClassWithConstructor", this);
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", x);
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", y);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	myPrint("No params");
}

int ClassWithConstructor::getX()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("getX", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h", "ClassWithConstructor", this);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	return x_;
}
void ClassWithConstructor::setX(int x)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("setX", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h", "ClassWithConstructor", this);
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", x);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	x_ = x;
}

int ClassWithConstructor::getY()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("getY", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h", "ClassWithConstructor", this);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	return y_;
}

void ClassWithConstructor::setY(int y)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("setY", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "MyFunctions.h", "ClassWithConstructor", this);
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", y);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	y_ = y;
}

// ClassWithStaticMethods
void ClassWithStaticMethods::static0()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("static0", bug_reproducer_assistant::FunctionCall::MethodType::STATIC_METHOD, "MyFunctions.h", "ClassWithStaticMethods");
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	myPrint("static0");
}

void ClassWithStaticMethods::static1( int x )
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("static1", bug_reproducer_assistant::FunctionCall::MethodType::STATIC_METHOD, "MyFunctions.h", "ClassWithStaticMethods");
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", x);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	myPrint( "x:" + boost::lexical_cast< string >(x) );
}

} // namespace MyFunctions