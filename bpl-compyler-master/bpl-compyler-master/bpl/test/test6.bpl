void printArray(int x[]) {
    int i;
    i = 0;
    while(i < 10) {
        write(x[i]);
        writeln();
        i = i + 1;
    }
}

void main(void) {
    int a[10];
    int i;
    i= 0;
    while(i < 10) {
        a[i] = i;
        i = i + 1;
    }
    printArray(a);
}
