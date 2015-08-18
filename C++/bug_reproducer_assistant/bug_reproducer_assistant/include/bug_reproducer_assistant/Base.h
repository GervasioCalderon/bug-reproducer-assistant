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
/*! \file Base.h
    \brief Basic includes for this module.
    
	It has common includes and forward declarations.
*/
#pragma once

//STL
#include <map>
#include <vector>
//Bost
#include <boost/shared_ptr.hpp>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/cplusplus_language.h>
#include <bug_reproducer_assistant/Argument.h>
#include <bug_reproducer_assistant/LanguageType.h>

//!namespace for Bug-reproducer Assistant classes and functions.
namespace bug_reproducer_assistant
{
class LanguageObject;
class FunctionCall;
class Argument;

//! Generic type for id's (LanguageObject, FunctionCall, etc.).
typedef long id_t;
//! Function's nesting level type.
typedef unsigned int function_level_t;
//! LanguageType vector.
typedef std::vector< LanguageType::Type > LanguageTypesVector;
//! A container used to store language objects mapping by their id.
typedef std::map< id_t, boost::shared_ptr< LanguageObject > > IdToLanguageObjectMap;
//! List of function arguments.
typedef std::vector< Argument > ArgumentsVector;
//! List of function calls.
typedef std::vector< boost::shared_ptr<FunctionCall> > FunctionCallsVector;
} // namespace bug_reproducer_assistant