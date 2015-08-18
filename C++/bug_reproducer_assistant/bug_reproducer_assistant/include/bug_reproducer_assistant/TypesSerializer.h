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
/*! \file TypesSerializer.h
    \brief Helpers to serialize types into Json objects.
*/
#pragma once

//STD
#include <string>
#include <fstream>
//jsoncpp
#include <json/json.h>

namespace bug_reproducer_assistant
{
//! Class that serializes types into Json strings.
/*!
  Monostate pattern (only static methods, because this class is stateless, only "action").
*/
//
struct TypesSerializer
{
public:
	//! Exception class for an error dumping a type into a Json string.
	struct TypeDumpException: public std::runtime_error
	{
		/**
		* Constructor.
		*/
		/*!
		 \param msg Exception's error message.
		*/
		TypeDumpException(const std::string& msg):
			std::runtime_error(msg)
		{}
	};

	//! Get Json representation for NULL.
	/*!
	 /return The Json representation for NULL.
	*/
	//
	static std::string getJsonNullValue();

	//! Get Json representation for an integer.
	/*!
	 /param i An integer.
	 /return The Json representation for the integer i.
	*/
	//
	static std::string getJsonIntValue(const int* i);

	//! Get Json representation for an unsigned integer.
	/*!
	 /param u An unsigned integer.
	 /return The Json representation for the unsigned integer i.
	*/
	//
	static std::string getJsonUIntValue(const unsigned int* u);

	//! Get Json representation for a double.
	/*!
	 /param d A double.
	 /return The Json representation for the integer i.
	*/
	//
	static std::string getJsonDoubleValue(const double* d);

	//! Get Json representation for a double.
	/*!
	 /param d A double.
	 /return The Json representation for the integer i.
	*/
	//
	static std::string getJsonStringValue(const std::string* str);
	
	template < class T >
	//! Get Json representation for a vector.
	/*!
	 /param v A vector.
	 /return The Json representation for the vector v.
	*/
	//
	static std::string getJsonArrayValue(const std::vector<T>* v);

	template < class Key, class Value >
	//! Get Json representation for a map.
	/*!
	 /param m A map.
	 /return The Json representation for the map m.
	*/
	//
	static std::string getJsonObjectValue(const std::map< Key, Value >* m );
};

//! Get string representation for a Json::Value.
/*!
	/param val A Json::Value.
	/return The string representation for val.
*/
//
std::string getStringFromJson(const Json::Value& val);

} // namespace bug_reproducer_assistant

#include <bug_reproducer_assistant/TypesSerializer.inl>