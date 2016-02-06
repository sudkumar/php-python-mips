# System calls and I/0

- Used to read or print values or string from input/output window, and indicate program end
- Use __syscall__ operating system routine call
- First supply appropriate values in registers $v0 and $a0-$a1
- result value(if any) returned in register $v0

## Syscall services available

<table>
    <thead>
        <th>Service</th>
        <th>$vo</th>
        <th>$a0-1</th>
        <th>Result</th>
    </thead>
    <tbody>
        <tr>
            <td>print int</td>
            <td>1</td>
            <td>$a0 = int to print <br>
            // read int, float, double - reads till end to line including \n</td>
            <td></td>
        </tr>
        <tr>
            <td>print float</td>
            <td>2</td>
            <td>$a0 = float to print</td>
            <td></td>
        </tr>
        <tr>
            <td>print double</td>
            <td>3</td>
            <td>$a0 = double  to print</td>
            <td></td>
        </tr>
        <tr>
            <td>print string</td>
            <td>4</td>
            <td>$a0 = address of string in memory <br>
            // String has to be null-terminated
            </td>
            <td></td>
        </tr>
        <tr>
            <td>read int</td>
            <td>5</td>
            <td></td>
            <td>int returned in $v0</td>
        </tr>
        <tr>
            <td>read float</td>
            <td>6</td>
            <td></td>
            <td>float returned in $v0</td>
        </tr>
        <tr>
            <td>read double</td>
            <td>7</td>
            <td></td>
            <td>double returned in $v0</td>
        </tr>
        <tr>
            <td>read string</td>
            <td>8</td>
            <td>
            $a0 = memory address of string input buffer <br>
            $a1 = length(n) of string buffer <br>
            //Read n-1 chars and add null at end from a single line <br>
            //If fewer then n-1 chars in single line, read upto \n and add null and terminate
            </td>
            <td></td>
        </tr>
        <tr>
            <td>sbrk</td>
            <td>9</td>
            <td>$a0 = amount <br>
            //Used in dynamic memory allocation</td>
            <td>address in $v0</td>
        </tr>
        <tr>
            <td>exit</td>
            <td>10</td>
            <td>// Stop the program</td>
            <td></td>
        </tr>
    </tbody>
</table>


## Examples

        HR                  IR                  LR

        exit                exit                li $v0, 10
                                                syscall

        print, x            print, x            lw $a0, x
                                                li $v0, 1
                                                syscall

