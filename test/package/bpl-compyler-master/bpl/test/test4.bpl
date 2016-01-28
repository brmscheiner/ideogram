int f(int x) { 
    return 2*x; 
} 

void main( void ) { 
    int i; 
    i = 0; 
    while (i < 10 ) { 
        write( i ); 
        write( f(i) ); 
        writeln( ); 
        i = i + 1; 
    } 
}
