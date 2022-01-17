def is_prime(p):
    return p > 1 and not any([p % i == 0 for i in range(2, p)])
