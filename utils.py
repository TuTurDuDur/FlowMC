# Converts number to base 36
class WtfError(BaseException):
    pass

def indexToUUID(number : int, alphabet='0123456789abcdefghijklmnopqrstuvwxyz') -> str:
    result = ''
    sign = ''
 
    if number < 0:
        raise WtfError("wtf")
 
    if 0 <= number < len(alphabet):
        return sign + alphabet[number]
 
    while number != 0:
        number, i = divmod(number, len(alphabet))
        result = alphabet[i] + result
 
    return sign + result
 
def base36decode(number):
    return int(number, 36)
 


def logger(func):
    def wrapper(*args, **kwargs):
        print(f"{func.__name__} called with args {args}{(','+kwargs) if kwargs!={} else ''} => {(returns := func(*args,**kwargs))}")
        return returns
    return wrapper

def methodLogger(func):
    def wrapper(*args, **kwargs):
        print(f"{func.__name__} called with args {args[1:]}{(','+kwargs) if kwargs!={} else ''} => {(returns := func(*args,**kwargs))}")
        return returns
    return wrapper