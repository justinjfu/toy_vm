# Sums numbers from 1 to N

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

    # Check if i == N
    clone_i
    push_i 10000
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
