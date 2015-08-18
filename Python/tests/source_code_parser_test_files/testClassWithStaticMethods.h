//ClassWithStaticMethods

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