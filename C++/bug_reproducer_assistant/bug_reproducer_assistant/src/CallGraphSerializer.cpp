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
#include <algorithm>
//Boost
#include <boost/lexical_cast.hpp>
#include <boost/make_shared.hpp>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/LanguageObject.h>
#include <bug_reproducer_assistant/FunctionCall.h>
#include <bug_reproducer_assistant/Json_specific.h>
#include <bug_reproducer_assistant/CallGraphSerializer.h>

namespace bug_reproducer_assistant
{

namespace
{
	id_t getOptionalObjectId_(boost::shared_ptr<LanguageObject> obj)
	{
		return obj ? obj->getId() : 0L;
	}
	
	boost::shared_ptr< LanguageObject > getLanguageObjectFromId_(const ProgramExecution& aProgramExecution, id_t id)
	{
		return id ? aProgramExecution.getLanguageObjects()[id] : boost::shared_ptr< LanguageObject >();
	}
            

	void CHECK_JSON_VALUE_INTEGER(const Json::Value& aValue, const std::string& elementName)
	{
		if (!aValue.isInt())
			throw  CallGraphSerializer::CallGraphLoadException(elementName + " should be integer.");
	}
	void CHECK_JSON_VALUE_BOOL(const Json::Value& aValue, const std::string& elementName)
	{
		if (!aValue.isBool())
			throw  CallGraphSerializer::CallGraphLoadException(elementName + " should be bool.");
	}
	void CHECK_JSON_VALUE_STRING(const Json::Value& aValue, const std::string& elementName)
	{
		if (!aValue.isString())
			throw  CallGraphSerializer::CallGraphLoadException(elementName + " should be string.");
	}
	void CHECK_JSON_VALUE_ARRAY(const Json::Value& aValue, const std::string& elementName)
	{
		if (!aValue.isArray())
			throw  CallGraphSerializer::CallGraphLoadException(elementName + " should be array.");
	}
	void CHECK_JSON_VALUE_OBJECT(const Json::Value& aValue, const std::string& elementName)
	{
		if (!aValue.isObject())
			throw  CallGraphSerializer::CallGraphLoadException(elementName + " should be object.");
	}
}

void CallGraphSerializer::dump(const ProgramExecution& aProgramExecution, std::ostream& os)
{
	std::auto_ptr< Json::Value > progExecMap = this->dumpProgramExecutionAsJsonMap_(aProgramExecution);

	std::string indentation;
	for (unsigned int i = 0; i < JSON::INDENT; ++i)
	{
		indentation += " ";
	}

	Json::StyledStreamWriter jsonWriter(indentation);
	jsonWriter.write(os, *progExecMap);
}

std::auto_ptr< ProgramExecution > CallGraphSerializer::load (std::istream& is)
{
	Json::Value progExecMap;
	Json::Reader reader;

	// Move stream contents to a string
	std::string str((std::istreambuf_iterator<char>(is)), std::istreambuf_iterator<char>());


	bool parsingSuccessful = reader.parse(str, progExecMap);
	if ( !parsingSuccessful )
		// report to the user the failure and their locations in the document.
		throw CallGraphLoadException(std::string("Failed to parse Json file\n") + reader.getFormatedErrorMessages() );

	return this->loadProgramExecutionFromJsonMap_(progExecMap);
}

std::auto_ptr< Json::Value > CallGraphSerializer::dumpProgramExecutionAsJsonMap_(const ProgramExecution& aProgramExecution)
{
	//TODO GERVA
	std::auto_ptr< Json::Value > progExecMapPtr(new Json::Value);
	Json::Value& progExecMap = *progExecMapPtr;
	
	//Language
	progExecMap[JSON::LANGUAGE] = aProgramExecution.getLanguage();
	
	//Language Types
	Json::Value languageTypesVector(Json::arrayValue);
	LanguageTypesVector myLanguageTypes = aProgramExecution.getLanguageTypes();
	for( LanguageTypesVector::iterator lt = myLanguageTypes.begin(); lt != myLanguageTypes.end(); ++lt )
	{
		Json::Value ltValue(Json::objectValue);
		ltValue[JSON::ID] = *lt;
		ltValue[JSON::NAME] = LanguageType::asString(*lt);
		languageTypesVector.append(ltValue);
	}
	progExecMap[JSON::LANGUAGE_TYPES] = languageTypesVector;

	//Language Objects
	Json::Value languageObjectVector(Json::arrayValue);
	IdToLanguageObjectMap langObjects = aProgramExecution.getLanguageObjects();
	for( IdToLanguageObjectMap::iterator idLo = langObjects.begin(); idLo != langObjects.end(); ++idLo )
	{
		id_t oId = idLo->first;
		boost::shared_ptr< LanguageObject > lo = idLo->second;
		assert(lo);

		Json::Value loValue(Json::objectValue);
		loValue[JSON::ID] = oId;
		loValue[JSON::LANGUAGE_TYPE_ID] = lo->getLanguageType();
		loValue[JSON::DECLARATION_TYPE] = lo->getDeclarationType();

		// Persist declarationCode as a Json Value, not as a string
		Json::Value declarationCodeValue;
		Json::Reader reader;
		bool parsingSuccessful = reader.parse(lo->getDeclarationCode(), declarationCodeValue);
		if ( !parsingSuccessful )
		// report to the user the failure and their locations in the document.
			throw CallGraphDumpException(std::string("Failed to dump to Json this string: '") + lo->getDeclarationCode() + "'\n" + reader.getFormatedErrorMessages() );
		loValue[JSON::DECLARATION_CODE] = declarationCodeValue;

		boost::shared_ptr< LanguageObject > parentLo = lo->getParent();
		loValue[JSON::PARENT_ID] = getOptionalObjectId_(parentLo);
		languageObjectVector.append(loValue);
	}
	progExecMap[JSON::LANGUAGE_OBJECTS] = languageObjectVector;

	//Call Graph
	Json::Value callGraphVector(Json::arrayValue);
	FunctionCallsVector theCalls = aProgramExecution.getFunctionCalls();

	for( FunctionCallsVector::iterator fcIt = theCalls.begin(); fcIt != theCalls.end(); ++fcIt )
	{
		boost::shared_ptr<FunctionCall> fc = *fcIt;
		
		Json::Value fcValue(Json::objectValue);
		fcValue[JSON::ID] = fc->getId();
		fcValue[JSON::CALLEE_ID] = fc->getCallee()->getId();
		fcValue[JSON::FUNC_NAME] = fc->getFunctionName();
		fcValue[JSON::METHOD_TYPE] = fc->getMethodType();
		fcValue[JSON::LEVEL] = fc->getLevel();

		boost::optional< boost::posix_time::time_duration > totalTime = fc->getTotalTime();
		if ( totalTime )
		{
			double timeInSeconds = totalTime->total_microseconds() / 10E6;
			fcValue[JSON::TOTAL_TIME] = timeInSeconds;
		}

		//Arguments
		Json::Value argumentsValue(Json::objectValue);
		Json::Value argsListValue(Json::arrayValue);
		
		ArgumentsVector argsVector = fc->getArgsVector();

		for( ArgumentsVector::iterator argIt = argsVector.begin(); argIt != argsVector.end(); ++argIt )
		{
			Json::Value argValue(Json::objectValue);

			Json::Value argIdValue = argIt->getLanguageObject()->getId();
			Json::Value argIdArgType = argIt->getArgumentType();
			Json::Value argIsConstValue = argIt->isConst();

			argValue[JSON::ID] = argIdValue;
			argValue[JSON::ARG_TYPE] = argIdArgType;
			argValue[JSON::IS_CONST] = argIsConstValue;

			argsListValue.append(argValue);
		}
		argumentsValue[JSON::ARGS] = argsListValue;
		fcValue[JSON::ARGUMENTS] = argumentsValue;
		callGraphVector.append(fcValue);
	}
	progExecMap[JSON::CALL_GRAPH] = callGraphVector;

	return progExecMapPtr;
}

std::auto_ptr< ProgramExecution > CallGraphSerializer::loadProgramExecutionFromJsonMap_(const Json::Value& progExecMap)
{
	CHECK_JSON_VALUE_OBJECT(progExecMap, "Program execution");

	//Language
	Json::Value languageValue = progExecMap[JSON::LANGUAGE];
	CHECK_JSON_VALUE_STRING(languageValue, "Language");
	std::string language = languageValue.asString();
	std::auto_ptr< ProgramExecution > aProgramExecutionPtr( new ProgramExecution(language) );
	ProgramExecution& aProgramExecution = *aProgramExecutionPtr;

	//Language Types
	Json::Value languageTypesArray = progExecMap[JSON::LANGUAGE_TYPES];
	CHECK_JSON_VALUE_ARRAY(languageTypesArray, "Language Types");

    LanguageTypesVector langTypes;
	for ( unsigned int i = 0; i < languageTypesArray.size(); ++i )
	{
		Json::Value ltValue = languageTypesArray[i];
		CHECK_JSON_VALUE_OBJECT(ltValue, "Language type (id, name)");

		Json::Value ltIdValue = ltValue[JSON::ID];
		CHECK_JSON_VALUE_INTEGER(ltIdValue, "Language type id");
		LanguageType::Type ltId = static_cast<LanguageType::Type>(ltIdValue.asInt());

		Json::Value ltNameValue = ltValue[JSON::NAME];
		CHECK_JSON_VALUE_STRING(ltNameValue, "Language type name");
		std::string ltName = ltNameValue.asString();
		if (LanguageType::asString(ltId) != ltName)
			throw CallGraphLoadException(std::string("Invalid LanguageType pair. Id: ") + boost::lexical_cast< std::string >(ltId) + ", name:'" + ltName + "'");
		langTypes.push_back(ltId);
	}
	
	LanguageTypesVector progExecLangTypes = aProgramExecution.getLanguageTypes();

	sort(langTypes.begin(), langTypes.end());
	sort(progExecLangTypes.begin(), progExecLangTypes.end());
	if (langTypes != progExecLangTypes)
		throw CallGraphLoadException("Invalid LanguageType's.");

	//Language Objects
	Json::Value languageObjectVector = progExecMap[JSON::LANGUAGE_OBJECTS];
	CHECK_JSON_VALUE_ARRAY(languageObjectVector, "Language Objects");

	for ( unsigned int i = 0; i < languageObjectVector.size(); ++i )
	{
		Json::Value loValue = languageObjectVector[i];
		CHECK_JSON_VALUE_OBJECT(loValue, "Language object");

		Json::Value loIdValue = loValue[JSON::ID];
		CHECK_JSON_VALUE_INTEGER(loIdValue, "Language object id");
		id_t oId = loIdValue.asInt();

		Json::Value loLanguageTypeIdValue = loValue[JSON::LANGUAGE_TYPE_ID];
		CHECK_JSON_VALUE_INTEGER(loLanguageTypeIdValue, "Language object, language type id");
		LanguageType::Type ltId = static_cast<LanguageType::Type>(loLanguageTypeIdValue.asInt());

		Json::Value loDeclTypeValue = loValue[JSON::DECLARATION_TYPE];
		CHECK_JSON_VALUE_STRING(loDeclTypeValue, "Decl object, Declaration type");
		std::string declType = loDeclTypeValue.asString();

		Json::Value loDeclCodeValue = loValue[JSON::DECLARATION_CODE];
		//No checking, type may be integer, string, etc.
		std::string declCode = getStringFromJson(loDeclCodeValue);

		Json::Value loParentIdValue = loValue[JSON::PARENT_ID];
		CHECK_JSON_VALUE_INTEGER(loParentIdValue, "Language object parent id");
		id_t parentId = loParentIdValue.asInt();

		boost::shared_ptr< LanguageObject > parentLo = getLanguageObjectFromId_(aProgramExecution, parentId);

		boost::shared_ptr< LanguageObject > lo = boost::make_shared< LanguageObject >(oId, ltId, parentLo, declType, declCode);
		aProgramExecution.addLanguageObject(lo);
	}

	//Call Graph
	Json::Value callGraphVector = progExecMap[JSON::CALL_GRAPH];
	CHECK_JSON_VALUE_ARRAY(callGraphVector, "Call Graph");
	for ( unsigned int j = 0; j < callGraphVector.size(); ++j )
	{
		Json::Value fcValue = callGraphVector[j];
		CHECK_JSON_VALUE_OBJECT(fcValue, "Function call");

		Json::Value callIdValue = fcValue[JSON::ID];
		CHECK_JSON_VALUE_INTEGER(callIdValue, "Function call id");
		id_t callId = callIdValue.asInt();

		Json::Value calleeIdValue = fcValue[JSON::CALLEE_ID];
		CHECK_JSON_VALUE_INTEGER(callIdValue, "Function callee id");
		id_t calleeId = calleeIdValue.asInt();
		boost::shared_ptr< LanguageObject > callee = getLanguageObjectFromId_(aProgramExecution, calleeId);

		Json::Value funcNameValue = fcValue[JSON::FUNC_NAME];
		CHECK_JSON_VALUE_STRING(funcNameValue, "Func name");
		std::string funcName = funcNameValue.asString();

		Json::Value methodTypeValue = fcValue[JSON::METHOD_TYPE];
		CHECK_JSON_VALUE_STRING(methodTypeValue, "Method type");
		std::string methodType = methodTypeValue.asString();

		Json::Value levelValue = fcValue[JSON::LEVEL];
		CHECK_JSON_VALUE_INTEGER(levelValue, "Level");
		function_level_t level = levelValue.asInt();

		boost::optional< boost::posix_time::time_duration > totalTimeDuration;
		if ( fcValue.isMember(JSON::TOTAL_TIME) )
		{
			Json::Value totalTimeValue = fcValue[JSON::TOTAL_TIME];
			CHECK_JSON_VALUE_STRING(totalTimeValue, "Total time");
			double totalTimeInSecs = totalTimeValue.asDouble();
			totalTimeDuration.reset(boost::posix_time::time_duration(0, 0, static_cast<boost::posix_time::time_duration::sec_type>(totalTimeInSecs)));
		}
		
		ArgumentsVector argsVector;

		Json::Value argumentsValue = fcValue[JSON::ARGUMENTS];
		CHECK_JSON_VALUE_OBJECT(argumentsValue, "Arguments");

		Json::Value argsListVector = argumentsValue[JSON::ARGS];
		CHECK_JSON_VALUE_ARRAY(argsListVector, "Args");
		for ( unsigned int k = 0; k < argsListVector.size(); ++k )
		{
			Json::Value argValue = argsListVector[k];
			CHECK_JSON_VALUE_OBJECT(argValue, "Argument");

			Json::Value argIdValue = argValue[JSON::ID];
			CHECK_JSON_VALUE_INTEGER(argIdValue, "Argument id");
			id_t argId = argIdValue.asInt();

			Json::Value argIdArgType= argValue[JSON::ARG_TYPE];
			CHECK_JSON_VALUE_INTEGER(argIdArgType, "Argument type");
			Argument::ArgumentType argType = static_cast< Argument::ArgumentType >(argIdArgType.asInt());


			Json::Value argIsConstValue = argValue[JSON::IS_CONST];
			CHECK_JSON_VALUE_BOOL(argIsConstValue, "Argument is const");
			bool isConst = argIsConstValue.asBool();

			argsVector.push_back(Argument(getLanguageObjectFromId_(aProgramExecution, argId), argType, isConst));
		}

		boost::shared_ptr< FunctionCall > func = boost::make_shared< FunctionCall >(callId, callee, funcName, methodType, argsVector, level, totalTimeDuration);
		aProgramExecution.addFunctionCall(func);
	}
	return aProgramExecutionPtr;
}

} // namespace bug_reproducer_assistant