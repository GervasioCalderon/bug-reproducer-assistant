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
/*! \file FunctionCall.h
    \brief It has the FunctionCall class, to represent a function call in the program.
*/
#pragma once

//STD
#include <string>
//Boost
#include <boost/optional.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/shared_ptr.hpp>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/LanguageObject.h>
#include <bug_reproducer_assistant/Base.h>

namespace bug_reproducer_assistant
{

//! Class that represents a Function Call in the original program.
class FunctionCall
{
public:
	//! 'bug_reproducer_assistant' method type for a function.
	/*!
		Some of these constants come from Python's "inspect" module.
	*/
	//
	struct MethodType
	{
		// They're used in C++
		//! Static method.
		static const std::string STATIC_METHOD;
		//! Constructor.
		static const std::string CONSTRUCTOR;
		//! Destructor.
		static const std::string DESTRUCTOR;
		//! Regular method.
		static const std::string METHOD;

		// Just for compatibility with Python. No use in C++
		//! Class method.
		static const std::string CLASS_METHOD;
		//! Property.
		static const std::string PROPERTY;
	};

	//! Constructor.
	/*!
	 /param id Unique id to identify this FunctionCall instance.
	 /param callee The callee, i.e.: the receiver of the message (the function call).
	 /param functionName Function name.
	 /param methodType This function's method type (see MethodType for the values).
	 /param argsList List of argument objects (see Argument class).
	 /param level The function nesting level (it starts with 0, and increases going deep).
	 /param totalTime Time taken by the function (this may be used for profiling).
	*/
	//
	FunctionCall(id_t id, const boost::shared_ptr< LanguageObject > callee, const std::string& functionName, const std::string& myMethodType,
		ArgumentsVector argsVector, function_level_t level, boost::optional< boost::posix_time::time_duration > totalTime);

	//! Get the unique id to identify this FunctionCall instance.
	/*!
	 /return The unique id to identify this FunctionCall instance.
	*/
	//
	id_t getId() const
	{
		return this->id_;
	}

	//! Get the receiver of the message (the function call).
	/*!
	 /return The callee, i.e.: the receiver of the message (the function call).
	*/
	//
	boost::shared_ptr< LanguageObject > getCallee() const
	{
		return this->callee_;
	}

	//! Get the function name.
	/*!
	 /return The function name.
	*/
	//
	std::string getFunctionName() const
	{
		return this->functionName_;
	}

	//! Get this function's method type (see MethodType for the values).
	/*!
	 /return This function's method type (see MethodType for the values).
	*/
	//
	std::string getMethodType()
	{
		return this->methodType_;
	}

	//! Get the list of argument objects (see Argument class) for this function.
	/*!
	  /return The list of argument objects (see Argument class) for this function.
	*/
	//
	ArgumentsVector getArgsVector() const
	{
		return this->argsVector_;
	}

	//! Get the function nesting level (it starts with 0, and increases going deep).
	/*!
	  /return The function nesting level (it starts with 0, and increases going deep).
	*/
	//
	function_level_t getLevel() const
	{
		return this->level_;
	}

	//! Get the time taken by the function (this may be used for profiling).
	/*!
	  /return The time taken by the function (this may be used for profiling).
	*/
	//
	boost::optional< boost::posix_time::time_duration > getTotalTime() const
	{
		return this->totalTime_;
	}

private:
	id_t id_;
	boost::shared_ptr< LanguageObject > callee_;
	std::string functionName_;
	std::string methodType_;
	ArgumentsVector argsVector_;
	function_level_t level_;
	boost::optional< boost::posix_time::time_duration >  totalTime_;
};

} // namespace bug_reproducer_assistant