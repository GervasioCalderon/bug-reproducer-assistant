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
	cout << str << endl;
}

int add(int i,  int j)
{
	return i + j;
}
	
int subtract(int i, int j)
{
	return i - j;
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

struct MyClass
{
	void f1()
	{
		myPrint( "No params" );
	}

	void f2(int i)
	{
		myPrint( "i:" + boost::lexical_cast< string > (i) );
	}

	void f3(const std::vector< int > aVector)
	{
		int x = aVector[0];
		myPrint( "x:" + boost::lexical_cast< string >(x) );
	}
	void f4(std::map< std::string, int > aMap, MyClass * anObj)
	{
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
		myPrint("No params");
	}

	int getX()
	{
		return x_;
	}

	void setX(int x)
	{
		x_ = x;
	}

	int getY()
	{
		return y_;
	}

	void setY(int y)
	{
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
		myPrint("static0");
	}

	static void static1( int x )
	{
		myPrint( "x:" + boost::lexical_cast< string >(x) );
	}
};