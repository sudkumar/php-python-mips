# IF else statements

        HR                  IR                      LR

        if(a<b){            ifgoto, bge, a, b, L1     bge $a, $b, L1
            actions1        actions1                  actions1
        }else{              goto L2                   b L2  
            actions2        L1: actions2            L1:
        }                   L2:                       actions2
                                                    L2:

        if(a<b || c<d){     ifgoto, blt, a, b, L1     blt, $a, $b, L1       
            actions1        ifgoto, bge, c, b, L2     bge, $c, $b, L2
        }else{              L1: actions1            L1:
            actions2        goto L3                   actions1
        }                   L2: actions2              b L3
                            L3:                     L2:
                                                      actions2
                                                    L3: