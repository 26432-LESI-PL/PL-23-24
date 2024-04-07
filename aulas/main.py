"""
	Processamento de Linguagens (ESI) 
	Trabalho Prático 1
	Exemplo de Apoio: er_main.py
	
	invocar como: python er_main.py exemplo01.er.json
"""

from er_to_text import evaluate
import sys
import json

if len(sys.argv) == 2:
	with open(sys.argv[1], "r") as f:
		try:
			arvore = json.load(f)
			res, _ = evaluate(arvore)
			print(res)
		except Exception as e:
			print(e, file=sys.stderr)
else:
	print("falta indicar o ficheiro de entrada:", file=sys.stderr)


# Exemplos de utilização
# exemplo01.er.json
# 
# python er_main.py exemplo01.er.json
# a|ab*
# python er_main.py exemplo02.er.json
# a(ε|b+)
# python er_main.py exemplo03.er.json
# a|(ab)*