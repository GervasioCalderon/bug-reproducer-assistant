#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
#include <bug_reproducer_assistant/bug_reproducer_assistant.h>
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
void noParamsFunction()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("noParamsFunction", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "testFunctionWithoutParams.h");
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
}
