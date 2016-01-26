from bpl.code_generator.code_generator import generate_code
from bpl.scanner.scanner import ScannerException
from bpl.parser.parser import ParserException, Parser
from bpl.type_checker.type_checker import TypeCheckerException, type_check

def compile(input_file, assembly_file): 
    parser = Parser(input_file)
    parse_tree = parser.parse()
    type_check(parse_tree)
    generate_code(parse_tree, assembly_file)
