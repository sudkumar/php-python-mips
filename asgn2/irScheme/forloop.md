# For & Foreach loop

> For & Foreach loop will get translated to if-else statements

        HR                          IR                  LR

        for(acts1;conds1;acts2){    acts1                 acts1
            acts3                   L1: !conds1, L2     L1: !conds1, L2
        }                           acts3                 acts3
                                    acts2                 acts2
                                    L2:                 L2: