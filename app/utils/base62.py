alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode(num):

    base = len(alphabet)
    arr = []

    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])

    arr.reverse()

    return ''.join(arr)