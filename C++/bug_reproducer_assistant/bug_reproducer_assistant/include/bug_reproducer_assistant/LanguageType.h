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
/*! \file LanguageType.h
    \brief Introduces LanguageType, to classify LanguageObject instances.
*/
#pragma once

//STD
#include <string>
//Boost
#include <boost/shared_ptr.hpp>

namespace bug_reproducer_assistant
{

//! Classification for LanguageObject instances.
/*!
    It represents which language element an object belongs to.
    C++ objects (as well as Python ones) do have a hierarchical structure:
        Module (the include)
          |
        Class
          |
        Instance

    LanguageType indicates where the object is located in the hierarchy,
    or a special "None" value (for a "module parent").
*/
//
struct LanguageType
{
	//! The concrete type's enumerate.
	enum Type
	{
		NONE = 0,
		MODULE = 1,
		CLASS = 2,
		INSTANCE = 3
	};
	//! Get string representation for a LanguageType.
	/*!
	 /param lt Language Type to query.
	 /return String representation for a LanguageType.
	*/
	//
	static std::string asString( Type lt )
	{
		switch( lt )
		{
		case NONE:
			return "None";
		case MODULE:
			return "Module";
		case CLASS:
			return "Class";
		case INSTANCE:
			return "Instance";
		}
		assert(!"Invalid LanguageType!");
		return ""; //Just to get rid of the warning
	}
	//! Is it a valid parent-child relation?
	/*!
      Return whether or not this is a valid parent-child relation.
      For instance, an instance parent and a child module is not valid.
      See the graphic representation for objects hierarchy in this class documentation (LanguageType).
	 /param parentLanguageType Language Type for the parent object.
	 /param childLanguageType Language Type for the child object.
	 /return Whether or not this is a valid parent-child relation.
	*/
	//
	static bool isValidParent(Type parentLanguageType, Type childLanguageType)
	{
        return parentLanguageType == childLanguageType - 1;
	}
};

} // namespace bug_reproducer_assistant