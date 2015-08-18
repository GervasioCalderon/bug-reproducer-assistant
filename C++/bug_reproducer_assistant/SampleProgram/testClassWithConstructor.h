#ifndef __MICLASE_H__
#define __MICLASE_H__

#include <stdio.h>

class	MiClase
{
private:
	int	i;

public:
	MiClase(int I=10) 
	{
		i=I;
		printf("Constructor con i=%d\r\n",i);
	}

	void Ejecutar()
	{
		for (int j=0;j<i;j++)
			printf("Ejecuto %d\r\n",j);
	}

	~MiClase()
	{
		printf("Destructor con i=%d\r\n",i);
	}



};

#endif