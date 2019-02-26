#include <stdio.h>
#include <unistd.h>

extern int optind;
extern int getopt(int argc, char * const argv[], const char *optstring);

int main(int argc, char **argv) {
  int c;

  for (int i=0; i<argc; i++)
    printf("argv[%d]: `%s`\n", i, argv[i]);

  while ((c = getopt(argc, argv, "l")) != -1) {
    printf("getopt saw option -%c\n", c);
  }
  
  printf("optind=%d\n", optind);

  return 0;
}
