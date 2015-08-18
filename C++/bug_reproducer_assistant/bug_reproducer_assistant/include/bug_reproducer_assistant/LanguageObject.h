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
/*! \file LanguageObject.h
    \brief In-memory representation for a C++ object (module, class or instance).
*/
#pragma once

//STD
#include <string>
#include <stdexcept>
//Boost
#include <boost/shared_ptr.hpp>
// bug_reproducer_assistant
#include <bug_reproducer_assistant/LanguageType.h>
#include <bug_reproducer_assistant/Base.h>

namespace bug_reproducer_assistant
{
//! A class representing an C++ language element (module, class or instance).
/*
    KEY CLASS. It represents a C++ "object" (it may be a module, class, or instance) whose functions we're annotating.
    EVERY OBJECT is declared as a LanguageObject. For instance, if we find the object "number 5", these are the new LanguageObject's to declare:
    * BUILTINS module (an imaginary module to hold native classes).
    * int class.
    * 5.
*/
//
class LanguageObject
{
public:
	//! Exception class for "Invalid parent".
	/* For example, an instance's parent should be a class,
	   not a module or another instance.
	*/
	struct InvalidParentException: public std::runtime_error
	{
		//! Constructor.
		/*
		 /param parentLanguageType Language Type (see LanguageType class for constants) for the parent.
		 /param childLanguageType Language Type for the child.
		*/
		InvalidParentException(LanguageType::Type parentLanguageType, LanguageType::Type childLanguageType):
			std::runtime_error(LanguageType::asString(parentLanguageType) +  "' is not a valid parent language type for '" + LanguageType::asString(parentLanguageType) + "'")
		{}
	};

	//! Different options to declare a LanguageObject.
	struct DeclarationTypes
	{
		//! Object will be declared with a constructor syntax ( MyClass var1; ).
		static const std::string CONSTRUCTOR;
	    //! There's a fixed string representation for the object. For instance, number 5 representation is "5".
        static const std::string FIXED_VALUE;
		//! As we don't know how to create the object, use a Dummy class.
        static const std::string DUMMY;
		//! Object is NULL.
        static const std::string NULL_VALUE;
	};

	//! Constructor.
	/*
     /param id Unique id to identify this Language Object.
     /param languageType Object's LanguageType.
     /param parent Parent Language Object for the new instance.
     /param declarationType Declaration Type for this object. See DECLARATION_TYPES enum. 
     /param declarationCode It's a string with the object representation.
	*/
    LanguageObject(id_t id, LanguageType::Type languageType, const boost::shared_ptr< LanguageObject > parent, const std::string& declarationType, const std::string& declarationCode = "null" );

	//! Get the unique id to identify this Language Object.
	/*
	 /return The unique id to identify this Language Object.
	*/
	id_t getId() const
	{
        return this->id_;
	}

	//! Get the object's language type (see LanguageType::Type).
	/*
	 /return The object's language type.
	*/
    LanguageType::Type getLanguageType() const
	{
        return this->languageType_;
	}

	//! Get the object's declaration type (see DeclarationTypes).
	/*
	 /return The object's declaration type.
	*/
    std::string getDeclarationType() const
	{
        return this->declarationType_;
	}

	//! Get a string with the object representation.
	/*
	 /return A string with the object representation.
	*/
    std::string getDeclarationCode() const
	{
        return this->declarationCode_;
	}

	//! Get the parent Language Object.
	/*
	 /return The parent Language Object.
	*/
    boost::shared_ptr< LanguageObject > getParent() const
	{
        return this->parent_;
	}
private:
	id_t id_;
	LanguageType::Type languageType_;
	std::string declarationType_;
	std::string declarationCode_;
	boost::shared_ptr< LanguageObject > parent_;
};

} // namespace bug_reproducer_assistant