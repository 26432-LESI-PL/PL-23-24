def check_alphabet(afd: dict, word: str) -> bool:
    alphabet = afd["V"]
    for char in word:
        if char not in alphabet:
            return False
    return True