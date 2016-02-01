# Data Declarations

- Placed in sections of program identified with assembler directive .data
- Declares variables names used in program; storage allocated in main memory(RAM)

### Format

        name:   storage_type    value(s)

- Create storage for variable of specified type with given name and specified value
- Value(s) usually gives initial value(s)
- For storage type .space, gives number of spaces to be allocated

### Examples

        var1:   .word   3
> create a single integer variable with intial value 3

        array1: .byte   'a', 'b'
> create a 2-element character array with elements intialized to a and b
> values can be seperated into more then one line

        array2: .word   3, 4, 5, 6,
                        7, 8
> create a 6-element integer array

        array3: .space  40
> allocate 40 consecutive bytes, with storage unintialized
> could be used as a 40-element character array
> or a 10-element integer array


        HR                  IR                  LR

        a = 1;              =, a, 1                 .data   # data region starts here 
        b;                  =, b                a:  .word   1
        c = [1,2,4,5]       =, c, [1,2,4,5]     b:  .word   
        d = "string"        =, d, "string"      c:  .word   1,2,4,5
        e = 'a'             =, e, 'a'           d:  .asciiz "string"
        f = int[40]         =, f, int[40]       e:  .byte   'a'
                                                f:  .space  160

