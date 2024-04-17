import argparse
import json
import afd
import er
import afnd

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
    if args.reconhecedor and not args.det:
        parser.error("O argumento -r/--reconhecedor só pode ser usado com o argumento -d/--det")
    elif args.graphviz and not (args.det or args.ndet):
        parser.error("O argumento -g/--graphviz só pode ser usado com o argumento -d/--det ou -nd/--ndet")
    elif args.output and not (args.er or args.ndet):
        parser.error("O argumento -o/--output só pode ser usado com o argumento -er/--er ou -nd/--ndet")

    if args.det:
        print("Autómato finito determinístico")
        if args.reconhecedor:
            afd.reconhecedor(file, args.reconhecedor)
        if args.graphviz:
            afd.graphviz(file)

    if args.er:
        print("Expressão regular")
        if args.output:
            afnd_dict = er.to_afnd(file)
            with open(args.output, "w", encoding="utf8") as f:
                json.dump(afnd_dict, f, ensure_ascii=False, indent=4)
                print("Ficheiro " + args.output + " criado com sucesso")

    if args.ndet:
        print("Autómato finito não determinístico")
        if args.graphviz:
            afnd.graphviz(file)
        if args.output:
            afd_dict = afnd.to_afd(file)
            with open(args.output, "w", encoding="utf8") as f:
                json.dump(afd_dict, f, ensure_ascii=False, indent=4)
                print("Ficheiro " + args.output + " criado com sucesso")

if __name__ == "__main__":
    main()
