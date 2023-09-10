# Converts number to base 36
def indexToUUID(number : int, alphabet='0123456789abcdefghijklmnopqrstuvwxyz') -> str:
    result = ''
    sign = ''
 
    if number < 0:
        sign = '-'
        number = -number
 
    if 0 <= number < len(alphabet):
        return sign + alphabet[number]
 
    while number != 0:
        number, i = divmod(number, len(alphabet))
        result = alphabet[i] + result
 
    return sign + result
 
def base36decode(number):
    return int(number, 36)
 
print(base5encode(1412823931503067241))
print(base36decode('AQF8AA0006EH'))