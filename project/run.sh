#!/bin/bash

make
spim <<ASM
load "out.s"
run
ASM