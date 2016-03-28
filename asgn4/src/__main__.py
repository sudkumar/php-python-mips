#!/usr/bin/python


from IR import IR
import sys

def main():
    fileName = "./../test/test1.php"
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
    ir = IR(fileName)

if __name__ == '__main__':
    main()
