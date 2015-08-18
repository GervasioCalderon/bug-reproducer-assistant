#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
#include <bug_reproducer_assistant/bug_reproducer_assistant.h>
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
//STL
#include <string>
#include <vector>
#include <map>
#include <iostream>

//Boost
#include <boost/lexical_cast.hpp>

using namespace std;

//Empty print for not disturbing the unit tests output
void myPrint(const string& str)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("myPrint", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h");
	bug_reproducer_assistant::Annotator::instance().addArgument("<string>", "const string&", str);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	cout << str << endl;
}

int add(int i,  int j)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("add", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h");
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", i);
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", j);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	return i + j;
}
	
int subtract(int i, int j)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("subtract", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h");
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", i);
	bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", j);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	return i - j;
}

void innerFunction()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("innerFunction", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h");
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
}

void outerFunction()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("outerFunction", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h");
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	innerFunction();
}

void noParamsFunction()
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("noParamsFunction", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h");
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
}
	
std::string mySubstring(const string& str, size_t length)
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("mySubstring", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h");
	bug_reproducer_assistant::Annotator::instance().addArgument("<string>", "const string&", str);
	bug_reproducer_assistant::Annotator::instance().addArgument("myFunctions.h", "size_t", length);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	return str.substr(0, length);
}

void processVector( const vector< int >& aList )
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("processVector", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h");
	bug_reproducer_assistant::Annotator::instance().addArgument("<vector>", "const vector<int>&", aList);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	myPrint("Entered processVector");
	for ( vector< int >::const_iterator it = aList.begin(); it != aList.end(); ++it )
		myPrint ("elem: " + boost::lexical_cast< string >(*it) + "\n");
}

void processIntMap( const map<int,int>& aMap )
{
#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
	bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
	bug_reproducer_assistant::Annotator::instance().addFunctionInfo("processIntMap", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h");
	bug_reproducer_assistant::Annotator::instance().addArgument("<map>", "const map<int,int>&", aMap);
	bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
	myPrint("Entered processIntMap");
	for ( map< int, int >::const_iterator it = aMap.begin(); it != aMap.end(); ++it )
	{
		myPrint ("key: " + boost::lexical_cast< string >(it->first) + "\n");
		myPrint ("value: " + boost::lexical_cast< string >(it->second) + "\n");
	}
}

struct MyClass
{
	void f1()
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f1", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h", "MyClass", this);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		myPrint( "No params" );
	}

	void f2(int i)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f2", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h", "MyClass", this);
		bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", i);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		myPrint( "i:" + boost::lexical_cast< string > (i) );
	}

	void f3(const std::vector< int > aVector)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f3", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h", "MyClass", this);
		bug_reproducer_assistant::Annotator::instance().addArgument("<vector>", "const std::vector<int>", aVector);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		int x = aVector[0];
		myPrint( "x:" + boost::lexical_cast< string >(x) );
	}
	void f4(std::map< std::string, int > aMap, MyClass * anObj)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("f4", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h", "MyClass", this);
		bug_reproducer_assistant::Annotator::instance().addArgument("<map>", "std::map<std::string,int>", aMap);
		bug_reproducer_assistant::Annotator::instance().addArgument("myFunctions.h", "MyClass*", anObj);
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

class ClassWithConstructor
{
public:
	ClassWithConstructor(int x, int y):
		x_(x),
		y_(y)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("ClassWithConstructor", bug_reproducer_assistant::FunctionCall::MethodType::CONSTRUCTOR, "myFunctions.h", "ClassWithConstructor", this);
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
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("getX", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h", "ClassWithConstructor", this);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		return x_;
	}

	void setX(int x)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("setX", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h", "ClassWithConstructor", this);
		bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", x);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		x_ = x;
	}

	int getY()
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("getY", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h", "ClassWithConstructor", this);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		return y_;
	}

	void setY(int y)
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("setY", bug_reproducer_assistant::FunctionCall::MethodType::METHOD, "myFunctions.h", "ClassWithConstructor", this);
		bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", y);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		y_ = y;
	}
private:
	int x_;
	int y_;
};

		
struct ClassWithStaticMethods
{
	static void static0()
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("static0", bug_reproducer_assistant::FunctionCall::MethodType::STATIC_METHOD, "myFunctions.h", "ClassWithStaticMethods");
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		myPrint("static0");
	}

	static void static1( int x )
	{
	#ifdef BUG_REPRODUCER_ASSISTANT_ENABLED
		bug_reproducer_assistant::Annotation bugReproducerAssistantAnnotation;
		bug_reproducer_assistant::Annotator::instance().addFunctionInfo("static1", bug_reproducer_assistant::FunctionCall::MethodType::STATIC_METHOD, "myFunctions.h", "ClassWithStaticMethods");
		bug_reproducer_assistant::Annotator::instance().addArgument(bug_reproducer_assistant::CPlusPlusConstants::BUILTINS_MODULE_NAME, "int", x);
		bug_reproducer_assistant::Annotator::instance().endFunctionCallAnnotation();
	#endif //BUG_REPRODUCER_ASSISTANT_ENABLED
		myPrint( "x:" + boost::lexical_cast< string >(x) );
	}
};