def combinations_with_replacement(alphabet, repeat):
    return {''.join(sorted(a + b)) for a in alphabet for b in (combinations_with_replacement(alphabet, repeat-1) if repeat >= 2 else [''])}
