#include <tchar.h>
#include "MyFunctions.h"

int _tmain(int argc, _TCHAR* argv[])
{
	ClassWithConstructor * foo = new ClassWithConstructor(1,2);
	int x = foo->getX();
	foo->setX(5);
	int y = foo->getY();
	foo->setY(10);
	myPrint( "Get rid of the warnings ;) " + boost::lexical_cast< std::string >(x + y) );
	delete foo;
}