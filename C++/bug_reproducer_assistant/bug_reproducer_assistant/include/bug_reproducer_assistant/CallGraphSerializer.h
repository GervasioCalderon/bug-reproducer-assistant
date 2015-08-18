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
/*! \file CallGraphSerializer.h
    \brief It serializes/deserializes a Call Graph into a Json database.
	It uses jsoncpp auxiliary project.
*/
#pragma once

//STD
#include <memory>
#include <fstream>
//jsoncpp
#include <json/json.h>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/ProgramExecution.h>

namespace bug_reproducer_assistant
{
//! Serializes a Call Graph in a Json database.
/*!
  It uses the jsoncpp module.
*/
//
class CallGraphSerializer
{
public:
	//! Exception class for an error loading a Call Graph in memory.
	struct CallGraphLoadException: public std::runtime_error
	{
		/**
		* Constructor.
		*/
		/*!
		 \param msg Exception's error message.
		*/
		CallGraphLoadException(const std::string& msg):
			std::runtime_error(msg)
		{}
	};
	//! Exception class for an error dumping a Call Graph in a Json database.
	struct CallGraphDumpException: public std::runtime_error
	{
		/**
		* Constructor.
		*/
		/*!
		 \param msg Exception's error message.
		*/
		CallGraphDumpException(const std::string& msg):
			std::runtime_error(msg)
		{}
	};
	/**
	* Dump a ProgramExecution in a Json database file.
	*/
	/*!
	 \param aProgramExecution A program Call Graph to dump.
	 \param os Output stream object where the Json database will be dumped.
	*/
	void dump(const ProgramExecution& aProgramExecution, std::ostream& os);
	/**
	* Load a ProgramExecution from a Json database file, and return it.
	*/
	/*!
	 \param is Input stream object where the Json database is stored.
	 \return A ProgramExecution (call graph) that represents the database previously stored in a Json database.
	*/
	std::auto_ptr< ProgramExecution > load (std::istream& is);
private:
	/**
	* Translate a ProgramExecution class to a "Json-compliant" format, i.e.:
    * a jsoncpp's Json::Value (jsoncpp forces the object to dump to be translated to a Json::Value)
    * with the same information.
	*/
	/*!
	 \param aProgramExecution A program Call Graph to dump.
	 \return A Json::Value with the ProgramExecution data. Storing it in a Json file is straight-forward.
	*/
	std::auto_ptr< Json::Value > dumpProgramExecutionAsJsonMap_(const ProgramExecution& aProgramExecution);
	/**
	* Load a new ProgramExecution class from a Json::Value.
	*/
	/*!
	 \param progExecMap A Json::Value with a call graph previously loaded from a Json database.
	 \return A newly-created ProgramExecution instance that represents the call graph stored in progExecMap.
	*/
	std::auto_ptr< ProgramExecution > loadProgramExecutionFromJsonMap_(const Json::Value& progExecMap);
};

} // namespace bug_reproducer_assistant