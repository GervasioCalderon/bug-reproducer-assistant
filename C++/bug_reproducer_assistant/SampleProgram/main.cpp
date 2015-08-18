#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
#include <bug_reproducer_assistant/bug_reproducer_assistant.h>
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
#include <tchar.h>
#include "MyFunctions.h"

int _tmain(int argc, _TCHAR* argv[])
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::ProgramExecutionDumper bugReproducerAssistantDumper("C:\\Users\\Gerva\\Documents\\Bug-reproducer Assistant\\Projects\\SampleProgram\\Executions\\SampleProgram.json");
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	add(4, 5);
	subtract(4, 5);
}