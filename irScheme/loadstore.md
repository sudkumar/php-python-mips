# Load-Store & Addressing Modes

## Load

        lw dst, src

> loads the _value_(word 4 bytes) in _src location_(RAM source) into _dst register_

        lb dst, src

> loads the _value_(byte) in _src location_(RAM source) into _dst register_(low-order byte)

        li dst, const

> loads the _value const_ into _dst register_


## Store

        sw src, dst

> stores the _value_(word 4 bytes) in _src register_ into _dst location_(RAM destination) 

        sb src, dst

> stores the _value_(byte low-order) in _src register_ into _dst location_(RAM destination) 


## Absolute(Direct) Addressing

        la dest, var1

> copy address of var1(a label) into _dest register_

        lw dest, labl

> copy the value, stored at address labl, into dest

## Indirect addressing

        lw dest, (src)

> load word at address, contained in src, into _dest register_

        sw src, (dest)

> store word in _src register_ into address contained in _dest_

## Based or indexed addressing

> Based adderessing is especially used in arrays and stacks (stack pointer and frame pointer)

        lw dest, 8(src)

> load word at address ( src + 4 ) into _dest register_
> "8" gives offset from address in _src register_

        sw src, -4(dest)

> store word in _src register_ into address (dest - 4)
  


##### Examples of IR
        HR                  IR                  LR

        a = b[4]            =, a, b[4]          lw $a, 4($b)

        a[4] = b            =, a[4], b          sw $b, 4($a)

        a = 3               =, a, 3             li $a, 3

        a = &lbl            =, a, &lbl          la $a, lbl

        a = *addr            =, a, lbl            lw, $a, lbl



