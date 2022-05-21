def convert_keys_of_hom_to_binary_strings(hom):
    newhom = {}
    n = 0
    while 2**n < len(hom):
        n += 1
    if 2**n != len(hom):
        raise ValueError("Length of hom is not a power of 2.")
    for i in hom:
            newhom[bin(i)[2:].zfill(n)] = hom[i]
    return newhom


def compress_homomorphism(hom):
    n = 0
    while 2**n < len(hom):
        n += 1
    if 2**n != len(hom):
        raise ValueError("Length of hom is not a power of 2.")
    c = n-1
    while c > 0:
        for i in range(2**c):
            b = bin(i)[2:].zfill(c)
            if b+"0" in hom and b+"1" in hom and hom[b+"0"] == hom[b+"1"]:
                hom[b] = hom[b + "0"]
                del hom[b + "0"]
                del hom[b + "1"]
        c = c-1
    filled_with_stars = {}
    for i in hom:
        filled_with_stars[i.ljust(n, '*')] = hom[i]
    return filled_with_stars
