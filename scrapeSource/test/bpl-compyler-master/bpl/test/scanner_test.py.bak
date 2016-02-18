from bpl.scanner.scanner import Scanner
from bpl.scanner.token import TokenType
import sys

if __name__ == "__main__":
    file_name = "bpl/test/test.bpl"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    try:
        input_file = open(file_name)
    except IOError:
        print("Error: File not found!")
        sys.exit()
    scanner = Scanner(input_file)
    try:
        scanner.get_next_token()
        while(scanner.next_token.kind != TokenType.T_EOF):
            print scanner.next_token
            scanner.get_next_token()
    except ScannerException as e:
        print e.message
        sys.exit()
    input_file.close()
