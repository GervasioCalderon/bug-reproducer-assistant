#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
#include <bug_reproducer_assistant/bug_reproducer_assistant.h>
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
//ClassWithConstructor

class ClassWithConstructor
{
public:
	ClassWithConstructor(int x, int y)
		x_(x),
		y_(y)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("ClassWithConstructor", bug_reproducer_assistant::FunctionCall::MethodType::CONSTRUCTOR, "testClassWithConstructor.h", "ClassWithConstructor", this);
		bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", x);
		bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", y);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		myPrint("No params");
	}
	int getX()
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("getX", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "testClassWithConstructor.h", "ClassWithConstructor", this);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		return x_;
	}
	void setX(int x)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("setX", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "testClassWithConstructor.h", "ClassWithConstructor", this);
		bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", x);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		x_ = x;
	}
	int getY()
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("getY", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "testClassWithConstructor.h", "ClassWithConstructor", this);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		return y_;
	}
	void setY(int y)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("setY", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "testClassWithConstructor.h", "ClassWithConstructor", this);
		bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", y);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		y_ = y;
	}
private:
	int x_;
	int y_;
};