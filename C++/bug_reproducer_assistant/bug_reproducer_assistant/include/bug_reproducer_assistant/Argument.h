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
/*! \file Argument.h
    \brief Module with Argument class, to represent function arguments.
    
	Arguments are related to FunctionCall in a one-to-many relationship
	(one function call has a -possibly empty- list of arguments).
	Differently from Python, there are no named arguments.
*/
#pragma once

//STD
#include <string>
//Boost
#include <boost/shared_ptr.hpp>

namespace bug_reproducer_assistant
{

class LanguageObject;

//! It represents a function argument. 
/*!
  The argument has a type (see ArgumentType) and may nor not be const.
*/
//
class Argument
{
public:
	//! Type of argument.
	enum ArgumentType
	{
		VALUE = 0,
		POINTER = 1,
		REFERENCE = 2
	};

	/**
	* Constructor.
	*/
	/*!
		\param aLanguageObject Language Object representing the argument.
		\param argumentType Argument type (see ArgumentType for the values).
		\param isConst It's a const argument (for C++ only).
	*/
	Argument(boost::shared_ptr<LanguageObject> aLanguageObject, ArgumentType argumentType = VALUE, bool isConst = false):
		languageObject_(aLanguageObject),
		argumentType_(argumentType),
		isConst_(isConst)
	{}

	/**
    * Tell whether or not it's a const argument.
    */
	/*!
	 \return Whether or not it's a const argument.
	*/
	bool isConst() const
	{
		return this->isConst_;
	}

	/**
    * Get the argument type (see ArgumentType for values).
    */
	/*!
	 \return The argument type.
	*/
	ArgumentType getArgumentType() const
	{
		return this->argumentType_;
	}

	/**
    * Get the Language Object representing the argument.
    */
	/*!
	 \return The Language Object representing the argument.
	*/
	boost::shared_ptr< LanguageObject > getLanguageObject() const
	{
        return this->languageObject_;
	}
	/**
    * Equality operator.
    */
	/*!
	 \param other Other Argument to compare.
	 \return Whether or not "this" argument is equal to "other".
	*/
	bool operator ==(const Argument& other) const
	{
		return this->argumentType_ == other.argumentType_ && this->isConst_ == other.isConst_ && this->languageObject_ == other.languageObject_;
	}
private:
	boost::shared_ptr< LanguageObject > languageObject_;
	ArgumentType argumentType_;
	bool isConst_;
};
/**
* Insertion operator.
*/
/*!
 \param os An ostream.
 \param arg An Argument to insert in the ostream.
 \return The parameter os.
*/
inline std::ostream& operator<< (std::ostream& os, const Argument& arg)
{
	os << arg.getArgumentType() << "," << arg.isConst() << "," << arg.getLanguageObject();
    return os;
}

} // namespace bug_reproducer_assistant