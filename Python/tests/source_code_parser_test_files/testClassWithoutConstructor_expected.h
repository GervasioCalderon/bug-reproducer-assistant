#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
#include <bug_reproducer_assistant/bug_reproducer_assistant.h>
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
struct MyClass
{
	void f1()
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f1", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "testClassWithoutConstructor.h", "MyClass", this);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		myPrint( "No params" );
	}

	void f2(int i)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f2", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "testClassWithoutConstructor.h", "MyClass", this);
		bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", i);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		myPrint( "i:" + boost::lexical_cast< string > (i) );
	}

	void f3(const std::vector< int >& aVector)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f3", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "testClassWithoutConstructor.h", "MyClass", this);
		bug_reproducer_assistant::Annotator::instance().addArgument("<vector>", "const std::vector<int>&", aVector);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		int x = aVector[0];
		myPrint( "x:" + boost::lexical_cast< string >(x) );
	}
	void f4(std::map< std::string, int > aMap, MyClass * anObj)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f4", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "testClassWithoutConstructor.h", "MyClass", this);
		bug_reproducer_assistant::Annotator::instance().addArgument("<map>", "std::map<std::string,int>", aMap);
		bug_reproducer_assistant::Annotator::instance().addArgument("testClassWithoutConstructor.h", "MyClass*", anObj);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		int x = aMap["x"];
		int y = aMap["y"];
		myPrint("x: " + boost::lexical_cast< string >(x)+ ", y:" + boost::lexical_cast< string >(y) );
		if ( anObj == NULL )
			myPrint("anObj is NULL");
		else
			myPrint("anObj is not NULL");
	}
};