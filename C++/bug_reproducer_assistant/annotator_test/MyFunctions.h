#pragma once

//STL
#include <string>
#include <vector>
#include <map>

//Empty print for not disturbing the unit tests output
void myPrint(const std::string& str);

int add(int i,  int j);
int subtract(int i, int j);
	
std::string mySubstring(const std::string& str, size_t length);

void processVector( const std::vector< int >& aList );
void processIntMap( const std::map<int,int>& aMap );

void innerFunction();
void outerFunction();
void noParamsFunction();

struct MyClass
{
	void f1();
	void f2(int i);
	void f3(const std::vector< int > aVector);
	void f4(std::map< int, int > aMap, MyClass * anObj);
};	

class ClassWithConstructor
{
public:
	ClassWithConstructor(int x, int y);
	int getX();
	void setX(int x);
	int getY();
	void setY(int y);
private:
	int x_;
	int y_;
};

		
class ClassWithStaticMethods
{
	static void static0();
	static void static1( int x );
};