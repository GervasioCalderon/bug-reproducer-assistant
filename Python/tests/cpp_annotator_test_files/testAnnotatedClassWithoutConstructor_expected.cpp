#include <tchar.h>
#include "MyFunctions.h"
#include <vector>
#include <map>

int _tmain(int argc, _TCHAR* argv[])
{
	MyClass * var0 = new MyClass;
	var0->f1();
	var0->f2(5);
	std::vector<int> var2;
	var2.push_back(5);
	var0->f3(var2);
	std::map<std::string,int> var3;
	var3[u"y"] = 2;
	var3[u"x"] = 1;
	var0->f4(var3, NULL);
}