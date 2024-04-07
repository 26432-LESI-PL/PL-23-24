import argparse

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-f", '--file', type=open, help='Nome do ficheiro JSON a ser lido', required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", '--det', action='store_true', help='Usar autómato finito determinístico')
    group.add_argument("-er", '--er', action='store_true', help='Usar expressão regular')
    group.add_argument("-nd", '--ndet', action='store_true', help='Usar autómato finito não determinístico')
    parser.add_argument("-g", '--graphviz', action='store_true', help='Usar Graphviz', required=False)
    parser.add_argument("-r", '--reconhecedor', type=str, help='Verificar se uma palavra é reconhecida', required=False)

    args = parser.parse_args()
    print(args.file)

    #print(f"Result: {result}")

if __name__ == "__main__":
    main()
