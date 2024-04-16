import argparse
import json
import afd

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-f", '--file', type=open, help='Nome do ficheiro JSON a ser lido', required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", '--det', action='store_true', help='Usar autómato finito determinístico')
    group.add_argument("-er", '--er', action='store_true', help='Usar expressão regular')
    group.add_argument("-nd", '--ndet', action='store_true', help='Usar autómato finito não determinístico')
    parser.add_argument("-g", '--graphviz', action='store_true', help='Usar Graphviz', required=False)
    parser.add_argument("-r", '--reconhecedor', type=str, help='Verificar se uma palavra é reconhecida', required=False)
    parser.add_argument("-o", '--output', type=str, help='Guardar ficheiro AFND em JSON', required=False)

    args = parser.parse_args()
    
    file: dict = {}
    with args.file as f:
        file = json.load(f)

    if args.det:
        print("Autómato finito determinístico")
        if args.reconhecedor:
            afd.reconhecedor(file, args.reconhecedor)
        elif args.graphviz:
            afd.graphviz(file)
        elif args.output:
            afd.output(file, args.output)
        else:
            print("Nenhuma ação especificada")

    #print(f"Result: {result}")

if __name__ == "__main__":
    main()
