#include<stdio.h>

int main(){
    int array[5];
    printf("Hello World\n");
    
    fread(array, sizeof(int), 5, stdin);
    printf("get");
    for(int i=0;i<5;i++)
        printf(" %d", array[i]);
    printf("\n");
    return 0;
}