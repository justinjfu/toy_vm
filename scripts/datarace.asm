spawn_thread .spawn1 0
spawn_thread .spawn1 0

.spawn1
spawn_thread .spawn2 0
spawn_thread .spawn2 0

.spawn2
push_i 5
push_i 0
memstore_i

exit