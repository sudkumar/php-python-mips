#!/usr/bin/python


from parser import runParser
import sys
 
if __name__ == '__main__':
    result = runParser()
    print result["ir"].printTac()
