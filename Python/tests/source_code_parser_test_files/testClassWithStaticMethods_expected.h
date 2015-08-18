#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
#include <bug_reproducer_assistant/bug_reproducer_assistant.h>
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
//ClassWithStaticMethods

struct ClassWithStaticMethods
{
	static void static0()
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("static0", bug_reproducer_assistant::FunctionCall::MethodType::STATIC_METHOD, "testClassWithStaticMethods.h", "ClassWithStaticMethods");
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		myPrint("static0");	
	}
	static void static1( int x )
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("static1", bug_reproducer_assistant::FunctionCall::MethodType::STATIC_METHOD, "testClassWithStaticMethods.h", "ClassWithStaticMethods");
		bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", x);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		myPrint( "x:" + boost::lexical_cast< string >(x) );
	}
};