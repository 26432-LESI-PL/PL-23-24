import argparse
import json
import afd
import er

def main():
    parser = argparse.ArgumentParser(description="Programa em Pytho para Processamento de Linguagens")
    parser.add_argument("-f", "--file", type=open, help="Nome do ficheiro JSON a ser lido", required=True)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--det", action="store_true", help="Usar autómato finito determinístico")
    group.add_argument("-er", "--er", action="store_true", help="Usar expressão regular")
    group.add_argument("-nd", "--ndet", action="store_true", help="Usar autómato finito não determinístico")

    parser.add_argument("-g", "--graphviz", action="store_true", help="Usar Graphviz", required=False)
    parser.add_argument("-r", "--reconhecedor", type=str, help="Verificar se uma palavra é reconhecida", required=False)

    parser.add_argument("-o", "--output", type=str, help="Guardar ficheiro AFND em JSON", required=False)

    args = parser.parse_args()
    
    file: dict = {}
    with args.file as f:
        file = json.load(f)

    # Validar os argumentos
    if (args.reconhecedor and args.graphviz) and not args.det:
        parser.error("O argumento -r/--reconhecedor ou -g/--graphviz só pode ser usado com o argumento -d/--det")

    if args.det:
        print("Autómato finito determinístico")
        if args.reconhecedor:
            afd.reconhecedor(file, args.reconhecedor)
        if args.graphviz:
            afd.graphviz(file)
        else:
            print("Nenhuma ação especificada")

    if args.er:
        print("Expressão regular")
        if args.output:
            er.output(file, args.output)
        else:
            print("Nenhuma ação especificada")

    #print(f"Result: {result}")

if __name__ == "__main__":
    main()
