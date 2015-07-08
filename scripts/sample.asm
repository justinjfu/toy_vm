push_i 45
push_i 20
add_i
print_i
push_i 15
push_i 10
sub_i
mul_i
print_i
pop_i

push_d 15.001
push_d 15.002
mul_d
print_d
pop_d

spawn_thread 0 3
spawn_thread 0 2
exit

spawn_thread 0 3
spawn_thread 0 2
exit

push_i 123
print_i
pop_i
push_i 124
print_i
pop_i
exit
