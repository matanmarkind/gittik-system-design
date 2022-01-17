def permutations(alphabet, repeat):
    return {a + b for a in alphabet for b in (permutations(alphabet, repeat-1) if repeat >= 2 else ['']) if a not in b}
