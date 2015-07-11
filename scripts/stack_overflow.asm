# Loops forever
push_i 0

.loop
    push_i 1
    add_i
    print_i
    clone_i
    j .loop
j .exit

.exit
exit
