def combinations(alphabet, repeat):
    return {''.join(sorted(a + b)) for a in alphabet for b in (combinations(alphabet, repeat-1) if repeat >= 2 else ['']) if a not in b}
