//Boost
#include <boost/lexical_cast.hpp>
//annotator_test
#include "MyFunctions.h"

using namespace std;

//Empty print for not disturbing the unit tests output
void myPrint(const string& str)
{}

int add(int i,  int j)
{
	return i + j;
}
	
int subtract(int i, int j)
{
	return i - j;
}
	
std::string mySubstring(const string& str, size_t length)
{
	return str.substr(0, length);
}

void processVector( const vector< int >& aList )
{
	myPrint("Entered processVector");
	for ( vector< int >::const_iterator it = aList.begin(); it != aList.end(); ++it )
		myPrint ("elem: " + boost::lexical_cast< string >(*it) + "\n");
}

void processIntMap( const map<int,int>& aMap )
{
	myPrint("Entered processIntMap");
	for ( map< int, int >::const_iterator it = aMap.begin(); it != aMap.end(); ++it )
	{
		myPrint ("key: " + boost::lexical_cast< string >(it->first) + "\n");
		myPrint ("value: " + boost::lexical_cast< string >(it->second) + "\n");
	}
}

void innerFunction()
{
}

void outerFunction()
{
	innerFunction();
}

void noParamsFunction()
{
}

//MyClass
void MyClass::f1()
{
	myPrint( "No params" );
}

void MyClass::f2(int i)
{
	myPrint( "i:" + boost::lexical_cast< string > (i) );
}

void MyClass::f3(const std::vector< int > aVector)
{
	int x = aVector[0];
	myPrint( "x:" + boost::lexical_cast< string >(x) );
}
void MyClass::f4(std::map< int, int > aMap, MyClass * anObj)
{
	int x = aMap[1];
	int y = aMap[2];
	myPrint("x: " + boost::lexical_cast< string >(x)+ ", y:" + boost::lexical_cast< string >(y) );
	if ( anObj == NULL )
		myPrint("anObj is NULL");
	else
		myPrint("anObj is not NULL");
}

//ClassWithConstructor
ClassWithConstructor::ClassWithConstructor(int x, int y):
	x_(x),
	y_(y)
{
	myPrint("No params");
}

int ClassWithConstructor::getX()
{
	return x_;
}
void ClassWithConstructor::setX(int x)
{
	x_ = x;
}

int ClassWithConstructor::getY()
{
	return y_;
}

void ClassWithConstructor::setY(int y)
{
	y_ = y;
}

// ClassWithStaticMethods
void ClassWithStaticMethods::static0()
{
	myPrint("static0");
}

void ClassWithStaticMethods::static1( int x )
{
	myPrint( "x:" + boost::lexical_cast< string >(x) );
}