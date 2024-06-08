import cparser
import argparse

# Parse the command line arguments
parser = argparse.ArgumentParser(description='Compile a simple language to C')
parser.add_argument('--input', type=argparse.FileType('r', encoding="utf8"), help='Input file', required=False)
parser.add_argument('--output', type=argparse.FileType('w', encoding="utf8"), help='Output file', required=False)
args = parser.parse_args()

# If theres no input file, read from stdin
if args.input:
    data = args.input.read()
else:
    data = ''
    print("Insira a liguagem a FCA para ser convertida em C.")
    print("Digite 'exit' para sair.")
    while True:
        try:
            line = input()
            if line == 'exit':
                break
        except EOFError:
            break
        data += line + '\n'
        if not line:
            break

c_code = cparser.parse(data)
# Print the generated C code
print("Código C gerado:")
print("\n".join(c_code))
if args.output:
    args.output.write("#include <stdio.h>\n#include <string.h>\n")
    args.output.write("void main() {\n")
    args.output.write("\n".join(c_code))
    args.output.write("\n}")