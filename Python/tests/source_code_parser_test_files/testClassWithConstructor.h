//ClassWithConstructor

class ClassWithConstructor
{
public:
	ClassWithConstructor(int x, int y)
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