#!/bin/bash
echo 'Testing python interpreter'
time python ../toyvm/main.py sum10000.asm

echo 'Testing machine code translator'
time /bin/bash -c 'python ../toyvm/main.py -c sumtest sum10000.asm; ./sumtest'
rm sumtest
