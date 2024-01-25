#include<stdio.h>
#include<stdlib.h>
#include<time.h> 
#include<windows.h>
#include"interception.h"
#include"utils.h"

enum ScanCode
{
    SCANCODE_X   = 0x2D,
    SCANCODE_Y   = 0x15,
    SCANCODE_W   = 0x11,
    SCANCODE_S   = 0x1f,
    SCANCODE_A   = 0x1e,
    SCANCODE_D   = 0x20,
    SCANCODE_J   = 0x24,
    SCANCODE_K   = 0x25,
    SCANCODE_ESC = 0x01
};

int number2key[] = {0, SCANCODE_W, SCANCODE_S, SCANCODE_A, SCANCODE_D, SCANCODE_J, SCANCODE_K};

int turn = 0;
InterceptionContext context;
InterceptionDevice device;
InterceptionKeyStroke stroke;

DWORD WINAPI ThreadMethod()
{
    while (1)
    {
        if (turn)
        {
            for (int i = 0; i < 1; i++)
            {
                Sleep(1355);
                InterceptionKeyStroke stroke2;
                stroke2.code = SCANCODE_K;
                stroke2.state = INTERCEPTION_KEY_DOWN;
                interception_send(context, device, (const InterceptionStroke *)&stroke2, 1);
                Sleep(65);
                stroke2.state = INTERCEPTION_KEY_UP;
                interception_send(context, device, (const InterceptionStroke *)&stroke2, 1);

                Sleep(3135);
                stroke2.code = SCANCODE_K;
                stroke2.state = INTERCEPTION_KEY_DOWN;
                interception_send(context, device, (const InterceptionStroke *)&stroke2, 1);
                Sleep(73);
                stroke2.state = INTERCEPTION_KEY_UP;
                interception_send(context, device, (const InterceptionStroke *)&stroke2, 1);
                turn = 0;
            }
        }
        else Sleep(1);
    }
}

int main(){
    srand( time(NULL) );

    raise_process_priority();

    context = interception_create_context();

    interception_set_filter(context, interception_is_keyboard, INTERCEPTION_FILTER_KEY_DOWN | INTERCEPTION_FILTER_KEY_UP);
  
    InterceptionKeyStroke check_code;
      
    while(interception_receive(context, device = interception_wait(context), (InterceptionStroke*)&stroke, 1) > 0)
    {
        printf("console application!\n");
        fflush(stdout);

        int* array = NULL;
        int len = 0;
        int input;

        while(1){
            scanf("%d", &input);

            if (input == 0)
                break;

            len += 1;
            array = realloc(array, len * sizeof(int));

            if (array == NULL) {
                printf("Memory allocation failed.\n");
                exit(EXIT_FAILURE);
            }
        }
        //fread(array, sizeof(int), 16, stdin);

        printf("I got something\n");
        fflush(stdout);
        return 0;
        printf("get");
        for(int i=0;i<16;i++){
            if (array[i] == 0){
                len = i;
                break;
            }
            printf(" %d", array[i]);
        }
        printf("over\n");
        fflush(stdout);
        return 0;

        boolean bpflag = (array[0]>=5); //j or k
        printf("%d", bpflag); 
        int inter_key_time[len];
        int outer_key_time[len];
        inter_key_time[0] = rand()%20+10;
        outer_key_time[0] = rand()%350+930;
        for(int i=1;i<len;i++){
            inter_key_time[i] = rand()%20+10;

            if(bpflag && array[i]<5){
                outer_key_time[i] = rand()%250+660;
                bpflag = FALSE;
            }
            else
                outer_key_time[i] = rand()%250+100;
            if(array[i]>=5)
                bpflag = TRUE;
        }

        ////////////////////////////////////
        stroke.code = SCANCODE_X;
        stroke.state = INTERCEPTION_KEY_DOWN;
        interception_send(context, device, (InterceptionStroke*)&stroke, 1);
        Sleep(75);
        stroke.state = INTERCEPTION_KEY_UP;
        interception_send(context, device, (InterceptionStroke*)&stroke, 1);
        Sleep(1035);

        if (check_code.code == SCANCODE_X) turn = 1;
        else
            interception_send(context, device, (InterceptionStroke*)&stroke, 1);
                
        if (check_code.code == SCANCODE_ESC) break;
    }
}