def check_alphabet(afd: dict, word: str) -> bool:
    alphabet = afd["V"]
    for char in word:
        if char not in alphabet:
            return False
    return True

def reconhecedor(afd: dict, word: str) -> bool:
    word = word.replace("ε", "")
    estado_atual = afd["q0"]
    for char in word:
        if char in afd["delta"][estado_atual]:
            estado_atual = afd["delta"][estado_atual][char]
        elif "ε" in afd["delta"][estado_atual]:
            estado_atual_aux = afd["delta"][estado_atual]["ε"]
            if char in afd["delta"][estado_atual_aux]:
                estado_atual = afd["delta"][estado_atual_aux][char]
        else:
            return False
    return estado_atual in afd["F"]