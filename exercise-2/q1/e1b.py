

def sieve_of_eratosthenes(n):
    return {i for i in range(2, n) if not any([i % j == 0 for j in range(2, i)])}
