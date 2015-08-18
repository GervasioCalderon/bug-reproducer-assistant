#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
#include <bug_reproducer_assistant/bug_reproducer_assistant.h>
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
int add(int i,  int j)
{
	return i + j;
}

int subtract(int i, int j)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("subtract", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "testOneIntegerFunction.h");
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", i);
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", j);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	return i - j;
}