# toy_vm
Toy Stack-based VM with some threading experiments.

Python interpreter
python toyvm/main.py scripts/sample.asm

Machine code translation (No threading/stack jumping support)
python toyvm/main.py -c out.exe scripts/sum10000.asm
./out.exe
