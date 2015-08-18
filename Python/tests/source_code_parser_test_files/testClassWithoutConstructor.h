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

	void f3(const std::vector< int >& aVector)
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