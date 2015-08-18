#include <tchar.h>
#include <string>
#include <vector>
#include <map>
#include "MyFunctions.h"

int _tmain(int argc, _TCHAR* argv[])
{
	MyClass foo;
	foo.f1();
	foo.f2(5);

	std::vector<int> myVector;
	myVector.push_back(5);

	std::map< std::string, int > myMap;
	myMap["x"] = 1;
	myMap["y"] = 2;
	foo.f3(myVector);
	foo.f4(myMap, NULL);
}