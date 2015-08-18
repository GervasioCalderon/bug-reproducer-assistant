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
/*! \file Annotator.h
    \brief Module that annotates functions.
    
	KEY MODULE. It's the interface between the code and the classes that store the graph call.
	It allows to "annotate" a function, i.e.: replace it with another one that has the same behavior,
	but it also stores its data and parameters in a memory representation of the call graph,
	to persist it later in a Database.
*/

#pragma once

//STD
#include <utility> //pair
#include <map>
//Boost
#include <boost/type_traits.hpp>
#include <boost/algorithm/string/predicate.hpp>
//bug_reproducer_assistant
#include <bug_reproducer_assistant/Base.h>
#include <bug_reproducer_assistant/Argument.h>
#include <bug_reproducer_assistant/TypesSerializer.h>

namespace bug_reproducer_assistant
{

class ProgramExecution;

namespace
{
	//For pointers
	template<typename T>
	//! MPL utility to add constness to a class.
	/*!
		Call ConstPointerType<AType>::type to get AType's const type.
		If already const, it returns the very type AType. Otherwise, returns const AType.
	*/
	//
	struct ConstPointerType
	{
		typedef typename boost::add_pointer< typename boost::add_const< T >::type >::type type;
	};

	template<typename T>
	//! Template specialization for ConstPointerType to be used for pointers.
	//
	struct ConstPointerType< T* >
	{
		typedef T * type;
	};


	template< typename T >
	/**
    * Get address for an argument.
    */
	/*!
	 This is the default: specialization for pointers.
	 \param argument Argument whose address we want to get.
	 \param isPointer It's a pointer (not a reference): fixed Boost "True" type (MPL pattern "Select").
	 \return The argument's address.
	*/
	typename const T getArgumentPointer(const T argument, const boost::true_type& isPointer)
	{
		return const_cast< const T > (argument);
	}

	//For references
	template< typename T >
	/**
    * Get address for an argument.
    */
	/*!
	 Specialization for references.
	 \param argument Argument whose address we want to get.
	 \param isPointer It's a pointer (not a reference): fixed Boost "False" type (MPL pattern "Select").
	 \return The argument's address.
	*/
	typename const T* getArgumentPointer(const T& argument, const boost::false_type&)
	{
		return const_cast< const T* > (&argument);
	}

	/**
    * Get rid of qualifiers (const, pointer, reference) in a class string,
	* and calculate if it's const and the argument type (see Argument::ArgumentType).
    */
	/*!
	 \param isConst Output argument that states whether or not the class is const.
	 \param className Class name whose qualifiers are to be stripped.
	 \param argType Output argument for the deduced argument type (see Argument::ArgumentType).
	*/
	void stripQualifiersFromClassName(bool& isConst, std::string& className, Argument::ArgumentType& argType)
	{
		isConst = false;
		argType = Argument::VALUE;
		const std::string constPattern = "const ";
		if ( boost::starts_with( className, constPattern ) )
		{
			isConst = true;
			className = className.substr( constPattern.size() );
		}
	
		if ( boost::ends_with( className, "*" ) )
		{
			argType = Argument::POINTER;
			className = className.substr( 0, className.size() - 1 );
		}
		else if ( boost::ends_with( className, "&" ) )
		{
			argType = Argument::REFERENCE;
			className = className.substr( 0, className.size() - 1 );
		}
	}
}

//! It annotates the functions.
/*!
  It's a Singleton.
*/
//
class Annotator
{
public:
	/**
    * Get the ONLY Annotator instance.
    */
	static Annotator& instance();

	/**
    * Reset function to start new annotations.
    */
	static void resetAnnotations();

	/**
    * Get the program execution, i.e.: the call graph and all the objects being used in the functions.
	*/
	/*!
     \return The program execution.
	*/
	boost::shared_ptr< ProgramExecution > getProgramExecution()
	{
		return programExecution_;
	}

	/**
    * Serialize the call graph into a database (Json file indicated in "dumpFileName" parameter).
    */
	/*!
     \param dumpFileName File where the call graph database will be dumped.
	*/
	void dumpProgramExecution(const std::string& dumpFileName);

	/**
    * Start the annotations.
    */
	/*!
	 Call this function before any call to addFunctionInfo().
	*/
	void startFunctionCallAnnotation();

	/**
    * Add function information. This is the base for the annotations processing for this function.
    */
	/*!
	 Call this function before any call to addArgument().
     \param funcName File where the call graph database will be dumped.
	 \param methodType Method type (@see FunctionCall::MethodType).
	 \param header Header to include for the file where funcName is declared.
	 \param className Name for the class that funcName belongs to.
	 \param callee The callee, i.e.: the receiver of the message (the function call). If NULL, it's a global function.
	*/
	void addFunctionInfo(const std::string& funcName, const std::string& methodType, const std::string& header, const std::string& className = "", void * callee = NULL);

	template < typename T >
	/**
    * Add an argument, taken from the function arguments list (it is calculated in the code parser).
    */
	/*!
	 This function is a template, to work with any argument type. This simplifies the parser,
	 because no matter the type, this function is called like this:
		addArgument([BUILTINS], "int", i);
		addArgument([MY_MODULE], "const MyClass&", myInstance);
	 To get this flexibility in the parser, the cost is that this "generic" function
	 must work for any argument type. This function does not have template specializations, there's
	 only one version: all the "hard work" is forwarded to the MPL functions like getArgumentPointer().
     \param header Header where the argument type is declared (or the special constant CPlusPlusConstants::BUILTINS_MODULE_NAME for native types).
	 \param qualifiedClassName Class name with "raw" qualifiers (for instance: "const MyClass&").
	 \param anArgument Argument to be added.
	*/
	void addArgument(const std::string& header, const std::string& qualifiedClassName, T anArgument)
	{
		bool isConst = false;
		Argument::ArgumentType argType = Argument::VALUE;
		std::string className = qualifiedClassName;
		
		stripQualifiersFromClassName(isConst, className, argType);

		ConstPointerType<T>::type argumentPtr = getArgumentPointer(anArgument, boost::is_pointer< T >::type());

		std::string argumentFixedValue = this->getJsonFixedValue_(argumentPtr);
		this->addResolvedArgument_( header, className, argumentPtr, argumentFixedValue, isConst, argType );
	}
	/**
    * End the annotation helper functions (like addArgument()).
    */
	/*!
	 Call this function after the sequence addFunctionInfo() and the optional calls to addArgument() -one per argument-.
	 Now that there are no more "adding" functions to call, commit this function to the ProgramExecution.
	*/
	void endFunctionCallAnnotation();
	/**
    * Message to be sent at the end of the function (with the RAII idiom).
    */
	/*!
	 It decreases the function nesting level.
	*/
	void functionEnded();

private:
	// Hide construction
	Annotator();
	// The ONLY instance
	static Annotator * instance_;

    // Constants
	//! Type of container. Language Objects and Function Calls are stored separately.
	enum ContainerType
	{
		LANGUAGE_OBJECTS = 0,
		FUNCTION_CALLS = 1
	};
	
	template < class PointerType >
	/**
    * Translate an argument to a Json string.
    */
	/*!
	 It's a template: it calls the correspondent JsonValueGetter::getValue() function.
	 \param argument Argument to translate to a Json string.
	 \return The argument as a Json string.
	*/
	std::string getJsonFixedValue_(PointerType argument ) const
	{
		if ( argument == NULL )
			return TypesSerializer::getJsonNullValue();
		else
			return JsonValueGetter< PointerType >::getValue(argument);
	}

	typedef std::map< ContainerType, id_t > ContainerTypeToNextIdMap_;
	typedef std::map< const void*, id_t > AddressToLanguageObjectIdMap_;
	typedef std::map< std::string, id_t > FixedValuesToLanguageObjectIdMap_;
	typedef std::map< std::string, id_t > HeaderOrClassToLanguageObjectIdMap_;

	//! It represents a particular member of an "Objects Family"
	/*!
	  An Objects Family maps a hierarchical relation MODULE, CLASS, INSTANCE.
	  This struct does not only represent the family, but the current element.
	  WARNING: this is kinda obscure. The Object Family information is mixed
	  with the "current" member. Alas, an abstract FamilyMember base class and
	  Module, Class and Instance implementations should be much more maintainable.
	*/
	//
	struct LanguageObjectsFamily_
	{
		/**
		* Constructor.
		*/
		/*!
		 This is just a convenience constructor for this struct.
		 \param currentObjectType Type for the current family member (see LanguageType::Type).
		 \param header Header to include for the file where className is declared.
		 \param className Name for the class (instance's class, or an indepentent class if instance is NULL).
		 \param instance Optional instance (whose class is className).
		 \param instanceFixedValue Optional string to declare the instance (for instance: "5" for number 5).
		*/
		LanguageObjectsFamily_(LanguageType::Type currentObjectType, const std::string& header, const std::string& className,
			const void * instance, const std::string& instanceFixedValue = ""):
			currentObjectType(currentObjectType),
			header(header),
			className(className),
			instance(instance),
			instanceFixedValue(instanceFixedValue)
		{}
		LanguageType::Type currentObjectType;
		std::string header;
		std::string className;
		const void * instance;
		std::string instanceFixedValue; // If possible, else it is ""
	};

	/**
    * Low-level implementation for addArgument().
    */
	/*!
	 This function is called by addArgument() after:
	  - the instance address has been calculated (depending on its type).
	  - the class name has been stripped from its qualifiers.
	 \param header Header where the argument type is declared (or the special constant CPlusPlusConstants::BUILTINS_MODULE_NAME for native types).
	 \param className Class name (it doesn't have qualifiers -for instance: it's "MyClass", not "const MyClass&"-.
	 \param anArgument Argument to be added.
	 \param argumentFixedName The argument as a Json string.
	 \param isConst States whether or not the class is const.
	 \param argType Argument type (see Argument::ArgumentType).
	*/
	void addResolvedArgument_(const std::string& header, const std::string& className, const void* argumentAddress, const std::string& argumentFixedName, bool isConst, Argument::ArgumentType argType );

	typedef std::pair< std::string, std::string > DeclarationTypeAndCodePair_;
	/**
    * Tell whether or not an object is declared.
    */
	/*!
	 It checks in different containers, according to the object type.
	 \param obj An "object" (module, class or instance -> see LanguageObjectsFamily_).
	 \return True if obj has been declared.
	*/
	bool isCurrentObjectDeclared_(const LanguageObjectsFamily_& obj) const;
	/**
    * Get the LanguageObject correspondent to an object.
    */
	/*!
	 It checks in different containers, according to the object type.
	 \param obj An "object" (module, class or instance -> see LanguageObjectsFamily_).
	 \return The correspondent LanguageObject instance.
	*/
	boost::shared_ptr< LanguageObject > getCurrentLanguageObject_(const LanguageObjectsFamily_& obj) const;
	/**
    * Map the object "id" to the LanguageObject id.
    */
	/*!
	 It uses different containers, according to the object type.
	 And also the "id" is different: use addresses for instances,
	 and fixed values for the rest.
	 \param obj An "object" (module, class or instance -> see LanguageObjectsFamily_).
	 \param id The LanguageObject id.
	*/
	void addCurrentObjectIdToMap_(const LanguageObjectsFamily_& obj, id_t id);
	/**
    * Recursive function to get a LanguageObject.
    */
	/*!
      If not previously declared, "declare" a Python object (module, class or instance),
      but declaring first its parent (and here is where the recursion appears).
	 \param obj An "object" (module, class or instance -> see LanguageObjectsFamily_).
	 \param isCallee Obj is the callee, i.e.: the receiver of the message (the function call).
	 \return The newly declared LanguageObject.
	*/
	boost::shared_ptr< LanguageObject > declareObjectAndParents_(const LanguageObjectsFamily_& obj, bool isCallee);
	/**
    * Returns a pair (declarationType, declarationCode) with information to declare obj parameter.
    */
	/*!
        For declarationType values, see LanguageObject::DeclarationTypes.
        The declarationCode is a string with the object representation.
        For instance: for obj == 5 -> (FIXED_VALUE, "5")
                          obj == int class -> (FIXED_VALUE, "int")
                          obj == instance -> (CONSTRUCTOR, "NULL")
        NOTE: For constructor, declarationCode doesn't matter, because the object will be declared
        with the constructor notation: MyClass * var1 = new MyClass;
        But for the FIXED_VALUE's, this code is used to declare:
            var2 = 5; ("5" is read from declarationCode).
	 \param obj An "object" (module, class or instance -> see LanguageObjectsFamily_).
	 \param isCallee Obj is the callee, i.e.: the receiver of the message (the function call).
	 \return A pair (declarationType, declarationCode) for this object.
	*/
	DeclarationTypeAndCodePair_ _getDeclarationInfo(const LanguageObjectsFamily_& obj, bool isCallee) const;
	/**
    * Get a new id to be used for a new LanguageObject or FunctionCall,
    * according to the containerType (ContainerType::LANGUAGE_OBJECTS or ContainerType::FUNCTION_CALLS).
    */
	/*!
	 \param ct Container type (for Language objects or Function calls).
	 \return The new id for the containerType.
	*/
	id_t getNewId_(ContainerType ct);

	boost::shared_ptr< ProgramExecution > programExecution_;
	boost::shared_ptr< LanguageObject > callee_;
	std::string funcName_;
	std::string methodType_;
	ArgumentsVector argumentsVector_;

	function_level_t currentFunctionLevel_;
	ContainerTypeToNextIdMap_ nextIdsMap_;
	AddressToLanguageObjectIdMap_ addressToLanguageObjectId_;
	FixedValuesToLanguageObjectIdMap_ fixedValuesToLanguageObjectId_;
	HeaderOrClassToLanguageObjectIdMap_ headerOrClassToLanguageObjectId_;

};

//! RAII idiom to dump the execution in a database.
/*!
    In the constructor, it tells the annotator instance to enter the annotations process,
    and in the destructor, it tells it to exit, and later it dumps the results in a database.
*/
class ProgramExecutionDumper
{
public:
	/**
	* Constructor.
	*/
	/*!
	 \param dumpFileName File where the call graph database will be dumped.
	*/
	ProgramExecutionDumper(const std::string& dumpFileName):
		dumpFileName_(dumpFileName)
	{}
	/**
	* Destructor.
	*/
	/*!
	 It tells the annotator instance to exit the annotation process,
     and dumps the call graph in a database.
	*/
	~ProgramExecutionDumper()
	{
		try
		{
			Annotator::instance().dumpProgramExecution( this->dumpFileName_ );
		}
		catch(...)
		{
			//Prevent exceptions from leaving destructors
		}
	}
private:
	std::string dumpFileName_;
};

} // bug_reproducer_assistant