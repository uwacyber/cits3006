#include <stdio.h>
#include <string.h>

int validate_password(char * pass) {

  /* check the password */
  if (pass[0] == 'h') {
    if (pass[1] == 'e') {
      if (pass[2] == 'l') {
        if (pass[3] == 'l') {
          if (pass[4] == 'o') {
            return 0;
          }
        }
      }
    }
  }
  return -1;
}


int main(int argc, char * argv[]) {
  char pass[5];

  printf("Enter password: ");
  scanf("%s", pass);

  if ((strlen(pass) == 5) &&
    (validate_password(pass) == 0)) {
    printf("Success!\n");
  } else {
    printf("Failure!\n");
  }
  return 0;
}
