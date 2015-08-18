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

//STD
#include <sstream>
#include <string>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/Json_specific.h>

namespace bug_reproducer_assistant
{

//String constants
//Global
const std::string JSON::ID = "id";
const std::string JSON::NAME = "name";
    
//LanguageObject
const std::string JSON::LANGUAGE_TYPE_ID = "languageTypeId";
const std::string JSON::DECLARATION_TYPE = "declarationType";
const std::string JSON::DECLARATION_CODE =  "declarationCode";
const std::string JSON::PARENT_ID = "parentId";

//Argument
const std::string JSON::ARGS = "args";
const std::string JSON::IS_CONST = "isConst";
const std::string JSON::ARG_TYPE = "argType";
    
//FunctionCall
const std::string JSON::CALLEE_ID = "calleeId";
const std::string JSON::FUNC_NAME = "funcName";
const std::string JSON::METHOD_TYPE = "methodType";
const std::string JSON::TOTAL_TIME = "totalTime";
const std::string JSON::ARGUMENTS = "arguments";

//ProgramExecution
const std::string JSON::FUNCTION_CALL = "functionCall";
const std::string JSON::LEVEL = "level";
const std::string JSON::CALLS = "calls";

//ProgramExecution
const std::string JSON::LANGUAGE = "language";
const std::string JSON::LANGUAGE_TYPES = "languageTypes";
const std::string JSON::LANGUAGE_OBJECTS = "languageObjects";
const std::string JSON::CALL_GRAPH = "callGraph";


std::string getIndentationString()
{
	std::string indentation;
	for (unsigned int i = 0; i < JSON::INDENT; ++i)
	{
		indentation += " ";
	}
	return indentation;
}

std::string getStringFromJson(const Json::Value& val)
{
	std::ostringstream oss;
	Json::StyledStreamWriter jsonWriter(getIndentationString());

	jsonWriter.write(oss, val);

	std::string ret = oss.str();
	if (ret[ret.size() - 1 ] == '\n')
		ret = ret.substr(0, ret.size() - 1);
	return ret;
}

} // namespace bug_reproducer_assistant