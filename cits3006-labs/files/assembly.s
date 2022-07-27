    .file    "factorial.c"
    .text
.globl factorial
    .type    factorial, @function
factorial:
    testl    %eax, %eax
    jne    .L2
    movl    $1, %edx
    jmp    .L4
.L2:
    movl    $1, %edx
.L5:
    imull    %eax, %edx
    decl    %eax
    jne    .L5
.L4:
    movl    %edx, %eax
    ret
    .size    factorial, .-factorial
    .ident    "GCC: (GNU) 4.1.2 20060715 (prerelease) (Debian 4.1.1-9)"
    .section    .note.GNU-stack,"",@progbits
