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
/*! \file ProgramExecution.h
    \brief In-memory representation for a program execution's call graph.
*/
#pragma once

//STD
#include <string>
#include <stdexcept>
//Boost
#include <boost/shared_ptr.hpp>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/Base.h>

namespace bug_reproducer_assistant
{
//! It represents a program execution.
/*!
  The program execution is the call graph
  and all the objects being used in the functions.
*/
//
class ProgramExecution
{
public:
	//! "Root" indentation level, i.e.: the outsider functions seen from main().
	static const function_level_t MIN_LEVEL = 0;

	//! Exception class for "Duplicated LanguageObject id".
	/*!
	  It is raised when there's an attempt to create a LanguageObject
	  with an already-used id.
	*/
	//
	struct DuplicatedLanguageObjectIdException: public std::runtime_error
	{
		//! Constructor.
		/*!
		  /param id The duplicated id to report.
		*/
		//
		DuplicatedLanguageObjectIdException(id_t id);
	};
	//! Languages supported by "Bug-reproducer Assistant".
	struct Languages
	{
		//! Constant for Python language.
		static const std::string PYTHON;
		//! Constant for C++ language.
		static const std::string C_PLUS_PLUS;
	};

	//! Constructor.
	/*!
		/param language The program's programming language.
	*/
	//
	ProgramExecution(const std::string& language);

	//! Return the program's programming language.
	/*!
	 /return The program's programming language.
	*/
	//
	std::string getLanguage() const
	{
		return this->language_;
	}

	//! Get the list of all available LanguageType's (see LanguageType).
	/*!
	 /return A list of all available LanguageType's (see LanguageType).
	*/
	//
	LanguageTypesVector getLanguageTypes() const
	{
		return this->languageTypes_;
	}

	//! Add a LanguageObject instance to an internal container.
	/*!
	 /param aLanguageObject The LanguageObject instance to add to the container.
	*/
	//
	void addLanguageObject(const boost::shared_ptr< LanguageObject >& aLanguageObject);

	//! Get the internal LanguageObject container.
	/*!
	 /return The internal LanguageObject container.
	*/
	//
	IdToLanguageObjectMap getLanguageObjects() const
	{
		return this->languageObjects_;
	}

	//! Add a new function call to an internal container.
	/*!
	 /param aFunctionCall A FunctionCall instance.
	*/
	//
	void addFunctionCall(const boost::shared_ptr< FunctionCall >& aFunctionCall)
	{
		this->functionCalls_.push_back(aFunctionCall);
	}

	//! Get the internal FunctionCall container.
	/*!
	 /return The internal FunctionCall container.
	*/
	//
	FunctionCallsVector getFunctionCalls() const
	{
		return this->functionCalls_;
	}
	
private:
	std::string language_;
	LanguageTypesVector languageTypes_;
	IdToLanguageObjectMap languageObjects_;
	FunctionCallsVector functionCalls_;
};

} // namespace bug_reproducer_assistant