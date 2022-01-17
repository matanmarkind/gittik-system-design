def product(alphabet, repeat):
    return {a + b for a in alphabet for b in (product(alphabet, repeat-1) if repeat >= 2 else [''])}
