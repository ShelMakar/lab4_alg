import random

from .errors import NotIntError


def _check_n(n: int) -> None:
    if type(n) != int:
        raise NotIntError("n должен быть числом ")
    if n < 0:
        raise ValueError("n должен быть >= 0")


def random_list(n: int, seed: int | None = None) -> list[int]:
    """Случайный набор. Значения в [-n, n]. Один seed -> один результат."""
    _check_n(n)
    rng = random.Random(seed)
    return [rng.randint(-n, n) for _ in range(n)]


def sorted_list(n: int, seed: int | None = None) -> list[int]:
    """Случайные значения, отсортированные по возрастанию."""
    return sorted(random_list(n, seed))


def reversed_list(n: int, seed: int | None = None) -> list[int]:
    """Случайные значения, отсортированные по убыванию."""
    return sorted(random_list(n, seed), reverse=True)


def nearly_sorted(n: int, seed: int | None = None,
                  swap_fraction: float = 0.05) -> list[int]:
    """Отсортированный список, в котором переставлено ~swap_fraction*n пар."""
    _check_n(n)
    if not 0 <= swap_fraction <= 1:
        raise ValueError("swap_fraction должен быть равен [0, 1]")
    rng = random.Random(seed)
    data = sorted(rng.randint(-n, n) for _ in range(n))
    if n >= 2:
        for _ in range(max(1, int(n * swap_fraction))):
            i, j = rng.randrange(n), rng.randrange(n)
            data[i], data[j] = data[j], data[i]
    return data


def many_duplicates(n: int, seed: int | None = None,
                    distinct: int = 10) -> list[int]:
    """Набор, где всего `distinct` различных значений (много повторов)."""
    _check_n(n)
    if distinct < 1:
        raise ValueError("distinct должен быть >= 1")
    rng = random.Random(seed)
    pool = [rng.randint(-n, n) for _ in range(distinct)]
    return rng.choices(pool, k=n)


GENERATORS = {
    "random": random_list,
    "sorted": sorted_list,
    "reversed": reversed_list,
    "nearly_sorted": nearly_sorted,
    "many_duplicates": many_duplicates,
}