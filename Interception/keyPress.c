#include<stdio.h>
#include<stdlib.h>
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
    raise_process_priority();

    context = interception_create_context();

    interception_set_filter(context, interception_is_keyboard, INTERCEPTION_FILTER_KEY_DOWN | INTERCEPTION_FILTER_KEY_UP);
  
    InterceptionKeyStroke check_code;
    
    int received = interception_receive(context, device = interception_wait(context), (InterceptionStroke*)&stroke, 1);
    printf("console application!\n");
    fflush(stdout);
    while(received > 0)
    {
        int len;
        scanf("%d", &len);
        int array[len], inter_time[len], outer_time[len];
        int input;

        for(int i=0;i<len;i++)
            scanf("%d", &array[i]);
        for(int i=0;i<len;i++)
            scanf("%d", &inter_time[i]);
        for(int i=0;i<len;i++)
            scanf("%d", &outer_time[i]);

        for(int i=0;i<len;i++){
            Sleep(outer_time[i]);

            stroke.code = number2key[array[i]];
            stroke.state = INTERCEPTION_KEY_DOWN;
            interception_send(context, device, (InterceptionStroke*)&stroke, 1);

            Sleep(inter_time[i]);

            stroke.state = INTERCEPTION_KEY_UP;
            interception_send(context, device, (InterceptionStroke*)&stroke, 1);

        }

        printf("done\n");
        fflush(stdout);

        ///////////////////////////////////
        /*
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
        */
    }
}