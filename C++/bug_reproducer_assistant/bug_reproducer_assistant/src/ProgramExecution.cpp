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
// STL
#include <boost/lexical_cast.hpp>
// bug_reproducer_assistant
#include <bug_reproducer_assistant/LanguageObject.h>
#include <bug_reproducer_assistant/ProgramExecution.h>

namespace bug_reproducer_assistant
{

const std::string ProgramExecution::Languages::PYTHON = "Python";
const std::string ProgramExecution::Languages::C_PLUS_PLUS = "C++";


ProgramExecution::DuplicatedLanguageObjectIdException::DuplicatedLanguageObjectIdException(id_t id):
	std::runtime_error(std::string("Duplicated LanguageObject id: ") + boost::lexical_cast< std::string >(id))
{}

ProgramExecution::ProgramExecution(const std::string& language):
	language_ (language)
{
	assert(language == Languages::PYTHON || language == Languages::C_PLUS_PLUS);
	this->languageTypes_.push_back(LanguageType::NONE);
	this->languageTypes_.push_back(LanguageType::MODULE);
	this->languageTypes_.push_back(LanguageType::CLASS);
	this->languageTypes_.push_back(LanguageType::INSTANCE);
}

void ProgramExecution::addLanguageObject(const boost::shared_ptr< LanguageObject >& aLanguageObject)
{
	assert( aLanguageObject );
	id_t id = aLanguageObject->getId();
	if ( this->languageObjects_.find(id) != this->languageObjects_.end() )
		throw DuplicatedLanguageObjectIdException(id);
	boost::shared_ptr< LanguageObject > parent = aLanguageObject->getParent();
	assert(!parent || (this->languageObjects_.find(parent->getId()) != this->languageObjects_.end()));
	this->languageObjects_[id] = aLanguageObject;
}

} // namespace bug_reproducer_assistant