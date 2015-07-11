#include <stdio.h>
#include <stdint.h>

#define push(TYPE, val) btz_push_ ## TYPE(stack, &stack_ptr, val)
#define peek(TYPE) btz_peek_ ## TYPE(stack, &stack_ptr)
#define pop(TYPE) btz_pop_ ## TYPE(stack, &stack_ptr)
#define popab(TYPE) a ## TYPE = pop(TYPE); b ## TYPE = pop(TYPE);
#define memstore(TYPE) popab(TYPE); btz_memstore_ ## TYPE(mem, a##TYPE, b##TYPE);
#define memread(TYPE) a##TYPE = pop(TYPE); b##TYPE = btz_memread_##TYPE(mem, a##TYPE); push(TYPE, b##TYPE);

#define clone(TYPE) a##TYPE = peek(TYPE); push(TYPE, a##TYPE);
#define print(TYPE) a##TYPE = peek(TYPE); printf("%d\n", a##TYPE);

#define add(TYPE) popab(TYPE); push(TYPE, a##TYPE+b##TYPE);
#define sub(TYPE) popab(TYPE); push(TYPE, a##TYPE-b##TYPE);
#define mul(TYPE) popab(TYPE); push(TYPE, a##TYPE*b##TYPE);
#define div(TYPE) popab(TYPE); push(TYPE, a##TYPE/b##TYPE);
#define eq(TYPE) popab(TYPE); push(i, a##TYPE==b##TYPE);
#define ne(TYPE) popab(TYPE); push(i, a##TYPE!=b##TYPE);

#define b(lbl) ai = pop(i); if(ai){goto lbl;}
#define j(lbl) goto lbl;

typedef float  float32_t;
typedef double float64_t;

void btz_push_i(int32_t* stack, uint32_t *stack_ptr, int32_t val){
    stack[*stack_ptr] = val;
    *stack_ptr += 1;
}

int32_t btz_pop_i(int32_t* stack, uint32_t *stack_ptr){
    *stack_ptr -= 1;
    return stack[*stack_ptr];
}

int32_t btz_peek_i(int32_t* stack, uint32_t *stack_ptr){
    return stack[(*stack_ptr)-1];
}

void btz_memstore_i(int32_t* mem, int32_t idx, int32_t val){
    mem[idx] = val;
}

int32_t btz_memread_i(int32_t* mem, int32_t idx){
    return mem[idx];
}


int main(){
int32_t ai=0, bi=0;
int64_t al=0, bl=0;
float32_t af=0, bf=0;
float64_t ad=0, bd=0;
int32_t mem[100];
int32_t stack[1024];
uint32_t stack_ptr = 0;

// BEGIN GENERATED CODE
