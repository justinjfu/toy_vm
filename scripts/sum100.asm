# Sums numbers from 1 to 100

push_i 0

.loop
    # i += 1
    push_i 1
    add_i

    # mem[0] += i
    clone_i
    push_i 0
    memread_i
    add_i
    push_i 0
    memstore_i

    # Check if i == 100
    clone_i
    push_i 100
    neq_i
    b .loop
j .print_sum

.print_sum
push_i 0
memread_i
print_i
j .exit

# Add some junk here
push_i 12345
print_i

.exit
exit
