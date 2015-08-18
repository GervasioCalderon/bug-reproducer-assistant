#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
from __future__ import with_statement
import bug_reproducer_assistant
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
class MyClass:
    def f():
        pass
    def g():
        pass
    def h():
        pass

def main():
    #ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
    BRA_annotator = bug_reproducer_assistant.annotator.annotatorInstance()
    BRA_annotator.resetForNewAnnotations()
    #ifdef BRA_ANNOTATIONS
    BRA_annotator.annotate(MyClass, 'f')
    BRA_annotator.annotate(MyClass, 'g')
    #endif //BRA_ANNOTATIONS
    with bug_reproducer_assistant.ProgramExecutionDumper("call_graph.json") as bugReproducerAssistantDumper:
    #endif //BUG_REPRODUCER_ASSISTANT_ENABLED
        print "Hej da varlden!"
        return 0

if __name__ == "__main__"
    main()