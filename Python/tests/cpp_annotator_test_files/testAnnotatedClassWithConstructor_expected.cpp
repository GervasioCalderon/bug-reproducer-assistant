#include <tchar.h>
#include "MyFunctions.h"

int _tmain(int argc, _TCHAR* argv[])
{
	ClassWithConstructor * var0 = new ClassWithConstructor(1, 2);
	var0->getX();
	var0->setX(5);
	var0->getY();
	var0->setY(10);
	delete var0;
}