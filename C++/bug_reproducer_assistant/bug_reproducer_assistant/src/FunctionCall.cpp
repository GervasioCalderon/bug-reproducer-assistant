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

//bug_reproducer_assistant
#include <bug_reproducer_assistant/FunctionCall.h>

namespace bug_reproducer_assistant
{
const std::string FunctionCall::MethodType::STATIC_METHOD = "static method";
const std::string FunctionCall::MethodType::CONSTRUCTOR = "constructor";
const std::string FunctionCall::MethodType::DESTRUCTOR = "destructor";
const std::string FunctionCall::MethodType::METHOD = "method";
const std::string FunctionCall::MethodType::CLASS_METHOD = "class method";
const std::string FunctionCall::MethodType::PROPERTY = "property";

FunctionCall::FunctionCall(id_t id, const boost::shared_ptr< LanguageObject > callee, const std::string& functionName, const std::string& myMethodType,
	ArgumentsVector argsVector, function_level_t level, boost::optional< boost::posix_time::time_duration> totalTime):
	id_ (id),
	callee_ (callee),
	functionName_ (functionName),
	methodType_ (myMethodType),
	argsVector_ (argsVector),
	level_ (level),
	totalTime_ (totalTime)
{
}

} // namespace bug_reproducer_assistant