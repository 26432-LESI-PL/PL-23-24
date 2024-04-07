import argparse

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-f", '--file', type=open, help='Nome do ficheiro JSON a ser lido', required=True)
    parser.add_argument("-g", '--graphviz', action='store_true', help='Usar Graphviz', required=False)

    args = parser.parse_args()
    print(args.file)

    #print(f"Result: {result}")

if __name__ == "__main__":
    main()
