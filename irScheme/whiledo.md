# While & Do-While Loop

> While & Do-while loop will get translated into if-else statements

        HR                  MR                          LR

        while(a<b){         L1: ifgoto, bge, a, b, L2   L1: bge, a, b, L2
            actions1        actions1                      actions1
        }                   goto L1                       g L2
                            L2:                         L2:

        do{                 L1: actions1                L1:
            actions1        ifgoto, blt, a, b, L1         actions1
        }while(a<b);                                      blt a, b, L1