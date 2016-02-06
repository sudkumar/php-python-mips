# Arithmetic operations

- Most of the instructions uses 3 operands
- All operands are _registers_; no _address_
- Operands size is word (4 bytes)
- In multiplication, _mflo_, _mfhi_ can be used to access the lower 32 and higher 32 bits respectively
- In division, _mflo_, _mfhi_ can be used to get quotient and reminder respectively

## Examples
        HR                  IR                  LR

        a = b + c           +, a, b, c          add $a, $b, $c

        a = b - c           -, a, b, c          sub $a, $b, $c

        a = b + 1           +, a, b, 1          addi $a, $b, 1

        a = b * c           *, a, b, c          mul $a, $b, $c // a = least 32-bit

        a = b / c           /, a, b, c          div $a, $b, $c // a = quotient
