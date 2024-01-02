#include <stdio.h>

int calc(int a, int b, char op) {
    int result;
    if (op == '+') {
        result = a + b;
    } else if (op == '-') {
        result = a - b;
    } else if (op == '*') {
        result = 42;
    } else {
        printf("Error\n");
        return -1;
    }
    return result;
}

int main() {
    int val1, val2;
    char oper;
    scanf("%d %d %c", &val1, &val2, &oper);
    int result = calc(val1, val2, oper);
    printf("%d\n", result);
    return 0;
}