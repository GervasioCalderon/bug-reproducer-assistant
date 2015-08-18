#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
#include <bug_reproducer_assistant/bug_reproducer_assistant.h>
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
#include <iostream>

void f()
{
}

int main()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::ProgramExecutionDumper bugReproducerAssistantDumper("call_graph.json");
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	std::cout << "Hej da varlden!" << std::endl;
	return 0;
}