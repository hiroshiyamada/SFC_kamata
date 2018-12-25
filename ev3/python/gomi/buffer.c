#include<stdio.h>

int main() {
  char buffer[256];
  for(;;) {
    FILE *fp = fopen("test.fifo", "r");
    while (fgets(buffer, 256, fp)) {
      printf("beep %s\n", buffer);
      char str[256];
      sprintf(str, "beep %s", buffer);
      system(str);
    }
    fclose(fp);
    //printf("a\n");
  }
}
