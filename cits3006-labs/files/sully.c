#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

int main(){
	int x = 5;

	x < 0 ? exit(1):0;

	if ((strchr(__FILE__, '_')) != NULL)
		x--;

	char *c="#include <stdio.h>%5$c#include <stdlib.h>%5$c#include <string.h>%5$c#include <fcntl.h>%5$c#include <unistd.h>%5$c%5$cint main(){%5$c%4$cint x = %3$d;%5$c%5$c%4$cx < 0 ? exit(1):0;%5$c%5$c%4$cif ((strchr(__FILE__, '_')) != NULL)%5$c%4$c%4$cx--;%5$c%5$c%4$cchar *c=%2$c%6$s%2$c;%5$c%4$cchar *sully;%5$c%4$cchar *filename;%5$c%4$cchar *compile;%5$c%4$cchar *execute;%5$c%4$cint f;%5$c%5$c%4$casprintf(&sully,%2$csully_%1$cd%2$c, x);%5$c%4$casprintf(&filename,%2$csully_%1$cd.c%2$c, x);%5$c%4$casprintf(&compile, %2$cclang sully_%1$c1$d.c -o sully_%1$c1$d; %2$c, x);%5$c%4$casprintf(&execute, %2$c./sully_%1$cd%2$c, x);%5$c%5$c%4$cf=open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);%5$c	if (f < 0)%5$c%4$c%4$cexit(1);%5$c%4$cdprintf(f,c,37,34,x,9,10,c);%5$c%4$cclose(f);%5$c%4$csystem(compile);%5$c	if (x > 0)%5$c%4$c%4$csystem(execute);%5$c%4$creturn (0);%5$c}";
	char *sully;
	char *filename;
	char *compile;
	char *execute;
	int f;

	asprintf(&sully,"sully_%d", x);
	asprintf(&filename,"sully_%d.c", x);
	asprintf(&compile, "clang sully_%1$d.c -o sully_%1$d; ", x);
	asprintf(&execute, "./sully_%d", x);

	f=open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
	if (f < 0)
		exit(1);
	dprintf(f,c,37,34,x,9,10,c);
	close(f);
	system(compile);
	if (x > 0)
		system(execute);
	return (0);
}
