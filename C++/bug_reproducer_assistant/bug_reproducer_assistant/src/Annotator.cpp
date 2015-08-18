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

//Boost
#include <boost/make_shared.hpp>
#include <boost/filesystem.hpp>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/LanguageType.h>
#include <bug_reproducer_assistant/FunctionCall.h>
#include <bug_reproducer_assistant/ProgramExecution.h>
#include <bug_reproducer_assistant/Json_specific.h>
#include <bug_reproducer_assistant/Annotator.h>
#include <bug_reproducer_assistant/CallGraphSerializer.h>

namespace bug_reproducer_assistant
{

namespace
{
	bool currentObjectHasParent_(LanguageType::Type lt)
	{
		return lt != LanguageType::MODULE;
	}
	LanguageType::Type getParentLanguageType_(LanguageType::Type lt)
	{
		assert( currentObjectHasParent_(lt) );
		return static_cast<LanguageType::Type> (lt - 1);
	}

	//If isCallee, instance may not be NULL, assume function belongs to class
	LanguageType::Type calculateInitialLanguageType_(const std::string& header, const std::string& className, const void* instance, bool isCallee)
	{
		if (instance != NULL)
			return LanguageType::INSTANCE;
		if ( !isCallee )
			return LanguageType::INSTANCE; //NULL instance
		if (!className.empty())
			return LanguageType::CLASS;
		assert( !header.empty() );
		return LanguageType::MODULE;
	}

	std::string getUniqueDumpFileName(const std::string& dumpFileName)
	{
		std::string uniqueDumpFileName = dumpFileName;
		std::string extension = boost::filesystem::extension(dumpFileName);
		bool exists;
		do
		{
			exists = boost::filesystem::exists(uniqueDumpFileName);
			std::string basename = boost::filesystem::basename(uniqueDumpFileName);
			size_t folderEnd = uniqueDumpFileName.rfind(basename);
			if (exists)
			{
				bool addSeparators = false;
				size_t leftSep = basename.rfind("(");
				size_t rightSep = basename.rfind(")");
				if ( leftSep == std::string::npos || rightSep < leftSep )
					addSeparators = true;
				else
				{
					std::string currentIndexStr = basename.substr(leftSep + 1, (rightSep - leftSep) - 1 );
					try
					{
						int currentIndex = boost::lexical_cast< int >(currentIndexStr);
						++currentIndex;
						basename = basename.substr(0, leftSep + 1) + boost::lexical_cast< std::string >(currentIndex) + basename.substr(rightSep);
					}
					catch( boost::bad_lexical_cast )
					{
						addSeparators = true;
					}
				}
				if (addSeparators)
					basename += "(1)";
				uniqueDumpFileName = uniqueDumpFileName.substr(0, folderEnd) + basename + extension;
			}
		}
		while (exists);
		return uniqueDumpFileName;
	}
}
Annotator * Annotator::instance_ = NULL;

//TODO GERVA: thread-safety
Annotator& Annotator::instance()
{
	if ( instance_ == NULL )
		instance_ = new Annotator;
	return *instance_;
}

Annotator::Annotator():
	programExecution_( boost::make_shared< ProgramExecution > (ProgramExecution::Languages::C_PLUS_PLUS) )
{
	this->currentFunctionLevel_ = ProgramExecution::MIN_LEVEL - 1;
	this->nextIdsMap_[LANGUAGE_OBJECTS] = 1;
	this->nextIdsMap_[FUNCTION_CALLS] = 1;
}

void Annotator::dumpProgramExecution(const std::string& dumpFileName)
{
	CallGraphSerializer aSerializer;

	//Get a valid file path, to avoid overwriting:
	//This allows having a number of different executions for a given set of annotations
	std::string uniqueDumpFileName = getUniqueDumpFileName(dumpFileName);

	std::ofstream jsonFileOut(uniqueDumpFileName.c_str());
	if (!jsonFileOut.is_open())
		throw std::runtime_error("Could not open dumpFileName");

	aSerializer.dump(*this->programExecution_, jsonFileOut);
	jsonFileOut.close();
}

void Annotator::resetAnnotations()
{
	delete instance_;
	instance_ = NULL;
}

bool Annotator::isCurrentObjectDeclared_(const LanguageObjectsFamily_& obj) const
{
	assert( obj.currentObjectType != LanguageType::NONE );
	switch( obj.currentObjectType )
	{
		case LanguageType::MODULE:
			return this->headerOrClassToLanguageObjectId_.find( obj.header ) != headerOrClassToLanguageObjectId_.end();
			break;
		case LanguageType::CLASS:
			return this->headerOrClassToLanguageObjectId_.find( obj.className ) != headerOrClassToLanguageObjectId_.end();
			break;
		case LanguageType::INSTANCE:
			if ( !obj.instanceFixedValue.empty() )
			{
				return this->fixedValuesToLanguageObjectId_.find( obj.instanceFixedValue ) != fixedValuesToLanguageObjectId_.end();
			}
			else
				return this->addressToLanguageObjectId_.find( obj.instance ) != addressToLanguageObjectId_.end();
	}
	return false; // Just for the warning
}

boost::shared_ptr< LanguageObject > Annotator::getCurrentLanguageObject_(const LanguageObjectsFamily_& obj) const
{
	assert( obj.currentObjectType != LanguageType::NONE );
	id_t loId;
	switch( obj.currentObjectType )
	{
		case LanguageType::MODULE:
			loId = this->headerOrClassToLanguageObjectId_.find(obj.header)->second;
			break;
		case LanguageType::CLASS:
			loId = this->headerOrClassToLanguageObjectId_.find(obj.className)->second;
			break;
		case LanguageType::INSTANCE:
			if ( !obj.instanceFixedValue.empty() )
			{
				loId = this->fixedValuesToLanguageObjectId_.find( obj.instanceFixedValue )->second;
			}
			else
				loId = this->addressToLanguageObjectId_.find(obj.instance)->second;
	}
	return this->programExecution_->getLanguageObjects()[loId];
}

void Annotator::addCurrentObjectIdToMap_(const LanguageObjectsFamily_& obj, id_t id)
{
	assert( obj.currentObjectType != LanguageType::NONE );
	switch( obj.currentObjectType )
	{
		case LanguageType::MODULE:
			this->headerOrClassToLanguageObjectId_[obj.header] = id;
			break;
		case LanguageType::CLASS:
			this->headerOrClassToLanguageObjectId_[obj.className] = id;
			break;
		case LanguageType::INSTANCE:
			if ( !obj.instanceFixedValue.empty() )
			{
				this->fixedValuesToLanguageObjectId_[obj.instanceFixedValue] = id;
			}
			else
				this->addressToLanguageObjectId_[obj.instance] = id;
	}
}

id_t Annotator::getNewId_(ContainerType ct)
{
	return this->nextIdsMap_[ct]++;
}

Annotator::DeclarationTypeAndCodePair_ Annotator::_getDeclarationInfo(const LanguageObjectsFamily_& obj, bool isCallee) const
{
	//It has not been declared before
	assert(!this->isCurrentObjectDeclared_(obj));
	assert( obj.currentObjectType != LanguageType::NONE );

	std::string declarationType = LanguageObject::DeclarationTypes::FIXED_VALUE;
	std::string declarationCode = "null";

	switch( obj.currentObjectType )
	{
		case LanguageType::MODULE:
			declarationCode = obj.header;
			break;
		case LanguageType::CLASS:
			declarationCode = obj.className;
			break;
		case LanguageType::INSTANCE:
			if ( isCallee )
				//We always annotate constructors
				declarationType = LanguageObject::DeclarationTypes::CONSTRUCTOR;
			else
			{
				//Object rules configurables
				// Argument. We have two options
				// If it's an object to annotate, it should have been annotated before
				// Otherwise, try (in this precedence order):
				//
				// calleeFixedValue is not empty -> FIXED_VALUE
				// * Dummy object -> DUMMY
				if ( !obj.instanceFixedValue.empty() )
				{
					declarationType = LanguageObject::DeclarationTypes::FIXED_VALUE;
					declarationCode = obj.instanceFixedValue;
				}
				else
					declarationType = LanguageObject::DeclarationTypes::DUMMY;
			}
	}
	return DeclarationTypeAndCodePair_( declarationType, declarationCode );
}

boost::shared_ptr< LanguageObject > Annotator::declareObjectAndParents_(const LanguageObjectsFamily_& obj, bool isCallee)
{
	//Declare current obj, if not declared before
	if ( this->isCurrentObjectDeclared_(obj) )
		return this->getCurrentLanguageObject_(obj);
	
	DeclarationTypeAndCodePair_ declTypeAndCode = this->_getDeclarationInfo(obj, isCallee);
	boost::shared_ptr< LanguageObject > parentLo;
    
	if ( currentObjectHasParent_(obj.currentObjectType) )
	{
		LanguageObjectsFamily_ parentFamily = obj;
		parentFamily.currentObjectType = getParentLanguageType_(obj.currentObjectType);
		//Recursive call
		parentLo = this->declareObjectAndParents_(parentFamily, false);
	}

	id_t newId = this->getNewId_(LANGUAGE_OBJECTS);
	boost::shared_ptr< LanguageObject > lo = boost::make_shared< LanguageObject> (newId, obj.currentObjectType, parentLo, declTypeAndCode.first, declTypeAndCode.second);
	this->programExecution_->addLanguageObject(lo);
	this->addCurrentObjectIdToMap_(obj, newId);
	return lo;
}

void Annotator::startFunctionCallAnnotation()
{
	++this->currentFunctionLevel_;
	this->argumentsVector_.clear();
}

void Annotator::addFunctionInfo(const std::string& funcName, const std::string& methodType, const std::string& header, const std::string& className, void * callee)
{
	LanguageType::Type currentObjectType = calculateInitialLanguageType_(header, className, callee, true);
	std::string jsonHeader = this->getJsonFixedValue_(&header); 
	std::string jsonClass = this->getJsonFixedValue_(&className);
	LanguageObjectsFamily_ obj(currentObjectType, jsonHeader, jsonClass, callee );

	//isCallee is true, because we're annotating the function call, not the arguments
	this->callee_ = this->declareObjectAndParents_(obj, true);
	this->funcName_ = funcName;
	this->methodType_ = methodType;
}

void Annotator::addResolvedArgument_(const std::string& header, const std::string& className, const void* argumentAddress, const std::string& argumentFixedName, bool isConst, Argument::ArgumentType argType)
{
	LanguageType::Type currentObjectType = calculateInitialLanguageType_(header, className, argumentAddress, false);
	std::string jsonHeader = this->getJsonFixedValue_(&header); 
	std::string jsonClass = this->getJsonFixedValue_(&className);
	LanguageObjectsFamily_ obj(currentObjectType, jsonHeader, jsonClass, argumentAddress, argumentFixedName );

	boost::shared_ptr< LanguageObject > argLanguageObject = this->declareObjectAndParents_(obj, false);
	this->argumentsVector_.push_back(Argument(argLanguageObject, argType, isConst));
}


void Annotator::endFunctionCallAnnotation()
{
	id_t newFunctionCallId = this->getNewId_(FUNCTION_CALLS);
	boost::shared_ptr< FunctionCall > aCall = boost::make_shared< FunctionCall >(newFunctionCallId, this->callee_, this->funcName_, this->methodType_, this->argumentsVector_, this->currentFunctionLevel_, boost::optional< boost::posix_time::time_duration >());

	this->programExecution_->addFunctionCall(aCall);
}

void Annotator::functionEnded()
{
	--this->currentFunctionLevel_;
}

} // bug_reproducer_assistant