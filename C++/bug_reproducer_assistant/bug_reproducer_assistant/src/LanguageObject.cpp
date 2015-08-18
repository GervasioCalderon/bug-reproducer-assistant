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

//ANSI
#include <assert.h>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/LanguageObject.h>

namespace bug_reproducer_assistant
{
const std::string LanguageObject::DeclarationTypes::CONSTRUCTOR = "CONSTRUCTOR";
const std::string LanguageObject::DeclarationTypes::FIXED_VALUE = "FIXED_VALUE";
const std::string LanguageObject::DeclarationTypes::DUMMY = "DUMMY";
const std::string LanguageObject::DeclarationTypes::NULL_VALUE = "NULL";

LanguageObject::LanguageObject(id_t id, LanguageType::Type languageType, const boost::shared_ptr< LanguageObject > parent, const std::string& declarationType, const std::string& declarationCode):
	id_ (id),
	languageType_ (languageType),
	declarationType_ (declarationType),
	declarationCode_ (declarationCode),
	parent_ (parent)
{
	assert(id > 0);
	LanguageType::Type parentLanguageType = parent ? parent->languageType_ : LanguageType::NONE;
	if ( !LanguageType::isValidParent(parentLanguageType, languageType) )
		throw InvalidParentException(parentLanguageType, languageType);
}

} // bug_reproducer_assistant