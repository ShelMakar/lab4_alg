from .errors import IncorrectExpError, NotIntError


def _validate(number, exp):
    if type(number) != int or type(exp) != int:
        raise NotIntError("number и exp должны быть целыми числами")
    if exp < 0:
        raise IncorrectExpError("exp должен быть неотрицательным")


def fast_pow_rec(number: int, exp: int) -> int:
    _validate(number, exp)
    if exp == 0:
        return 1
    if exp % 2 == 1:
        return number * fast_pow_rec(number, exp - 1)
    half = fast_pow_rec(number, exp // 2)
    return half * half


def fast_pow_loop(number: int, exp: int) -> int:
    _validate(number, exp)
    result, base = 1, number
    while exp > 0:
        if exp & 1:
            result *= base
        base *= base
        exp >>= 1
    return result


print()