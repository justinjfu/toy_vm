# Prints out from 1 to 100
push_i 0

.loop
    push_i 1
    add_i
    print_i
    clone_i
    push_i 100
    neq_i
    b .loop
j .exit

push_i 123456
print_i
print_i

.exit
exit
