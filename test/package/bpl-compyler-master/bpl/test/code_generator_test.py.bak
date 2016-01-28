from bpl.code_generator.code_generator import *
from bpl.scanner.scanner import ScannerException
from bpl.parser.parser import ParserException, Parser
from bpl.type_checker.type_checker import TypeCheckerException, type_check
import sys, os

if __name__ == "__main__":
    file_name = "bpl/test/test3.bpl"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    if not file_name.endswith('.bpl'):
        print "Error: File is not a .bpl file!"
        sys.exit()
    try:
        input_file = open(file_name)
    except IOError:
        print "Error: File not found!"
        sys.exit()
    try: 
        parser = Parser(input_file)
        parse_tree = parser.parse()
    except (ScannerException, ParserException) as e:
        print e.message
        sys.exit()
    try:
        type_check(parse_tree)
    except TypeCheckerException as t:
        print t.message
        sys.exit()
    output_file_name = os.path.basename(file_name).rstrip('.bpl') + '.s'
    output_file = open(os.path.join(os.path.dirname(file_name), output_file_name), 'w')
    generate_code(parse_tree, output_file)
    input_file.close()
    output_file.close()
