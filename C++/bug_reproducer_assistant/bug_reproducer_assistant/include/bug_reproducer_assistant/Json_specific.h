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
/*! \file Json_specific.h
    \brief Bridge between this library and jsoncpp.
*/
#pragma once

//STD
#include <string>
//jsoncpp
#include <json/json.h>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/TypesSerializer.h>

namespace bug_reproducer_assistant
{
//! JSON-related constants. 
struct JSON
{
	//! Indentation for json pretty-printing.
	static const unsigned int INDENT = 4;

	//String constants
	//Global
	//! Id (same constant name for different containers).
	static const std::string ID;
	//! Name.
	static const std::string NAME;
    
	//LanguageObject
	//! Id for LanguageType.
	static const std::string LANGUAGE_TYPE_ID;
	//! DeclarationTypes value.
	static const std::string DECLARATION_TYPE;
	//! Declaration code.
	static const std::string DECLARATION_CODE;
	//! Parent LanguageObject id.
	static const std::string PARENT_ID;

	//Argument
	//! Concrete list of function arguments.
	static const std::string ARGS;
	//! Is argument const?
	static const std::string IS_CONST;
	//! Argument::ArgumentType
    static const std::string ARG_TYPE;

	//FunctionCall
	//! Id for callee object (the one receiving a message).
	static const std::string CALLEE_ID;
	//! Function name.
	static const std::string FUNC_NAME;
	//!FunctionCall::MethodType
	static const std::string METHOD_TYPE;
	//! Total time taken by the function.
	static const std::string TOTAL_TIME;
	//! Function arguments.
	static const std::string ARGUMENTS;

	//ProgramExecution
	//! Fuction call (see FunctionCall).
	static const std::string FUNCTION_CALL;
	//! Function nesting level.
	static const std::string LEVEL;
	//! Function calls list.
	static const std::string CALLS;

	//ProgramExecution
	//! The program's language.
	static const std::string LANGUAGE;
	//! LanguageType.
	static const std::string LANGUAGE_TYPES;
	//! List of LanguageObject.
	static const std::string LANGUAGE_OBJECTS;
	//! The program's call graph.
	static const std::string CALL_GRAPH;
};

//! Get indentation string to make the Json file look prettier.
/*!
 /return The indentation string for a Json file.
*/
//
std::string getIndentationString();

template < typename PointerType >
//! Helper class to get a Json string.
/*!
  It's a template, with specializations for custom types.
*/
struct JsonValueGetter
{
	//! Get a Json value string from an object.
	/*!
	  /param obj An object.
	  /return The Json string representation for the object (an emtpy string as default).
	*/
	//
	static std::string getValue(PointerType obj)
	{
		return "";
	}
};


template <>
//! JsonValueGetter specialization for integers.
struct JsonValueGetter< const int* >
{
	//! Get a Json value string from an integer.
	/*!
	  /param i An integer.
	  /return The Json string representation for this integer.
	*/
	//
	static std::string getValue(const int* i)
	{
		return TypesSerializer::getJsonIntValue(i);
	}
};

template <>
//! JsonValueGetter specialization for longs.
struct JsonValueGetter< const long* >
{
	//! Get a Json value string from a long.
	/*!
	  /param l A long.
	  /return The Json string representation for this long.
	*/
	//
	static std::string getValue(const long* l)
	{
		//TODO GERVA: I'm losing precision
		int i = static_cast< int >(*l);
		return TypesSerializer::getJsonIntValue(&i);
	}
};

template <>
//! JsonValueGetter specialization for unsigned integers.
struct JsonValueGetter< const unsigned int* >
{
	//! Get a Json value string from an unsigned integer.
	/*!
		/param u An unsigned integer.
		/return The Json string representation for this unsigned integer.
	*/
	//
	static std::string getValue(const unsigned int* u)
	{
		return TypesSerializer::getJsonUIntValue(u);
	}
};

template <>
//! JsonValueGetter specialization for unsigned longs.
struct JsonValueGetter< const unsigned long* >
{
	//! Get a Json value string from an unsigned long.
	/*!
		/param u An unsigned long.
		/return The Json string representation for this unsigned long.
	*/
	//
	static std::string getValue(const unsigned long* u)
	{
		//TODO GERVA: I'm losing precision
		unsigned int uu = static_cast< unsigned int >(*u);
		return TypesSerializer::getJsonUIntValue(&uu);
	}
};
		
template <>
//! JsonValueGetter specialization for strings.
struct JsonValueGetter< const std::string* >
{
	//! Get a Json value string from a string.
	/*!
		/param str A string.
		/return The Json string representation for this string.
	*/
	//
	static std::string getValue(const std::string* str)
	{
		return TypesSerializer::getJsonStringValue(str);
	}
};

template <typename T>
//! JsonValueGetter specialization for vectors.
struct JsonValueGetter< const std::vector< T >* >
{
	//! Get a Json value string from a string.
	/*!
		/param v A vector.
		/return The Json string for this vector.
	*/
	//
	static std::string getValue(const std::vector< T >* v)
	{
		return TypesSerializer::getJsonArrayValue(v);
	}
};

template <typename Key, typename Value>
//! JsonValueGetter specialization for maps.
struct JsonValueGetter< const std::map< Key, Value >* >
{
	//! Get a Json value string from a map.
	/*!
		/param m A map.
		/return The Json string for this map.
	*/
	//
	static std::string getValue(const std::map< Key, Value >* m)
	{
		return TypesSerializer::getJsonObjectValue(m);
	}
};

} // namespace bug_reproducer_assistant