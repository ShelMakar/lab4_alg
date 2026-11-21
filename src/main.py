import argparse
import sys

from .benchmark import benchmark, write_csv
from .errors import CliError, EmptyQueueError
from .generators import GENERATORS
from .recur import fast_pow_loop, fast_pow_rec
from .sort import quick_sort, selection_sort
from .struct import Queue

POW_METHODS = {"rec": fast_pow_rec, "loop": fast_pow_loop}

ALGORITHMS = {"selection": selection_sort, "quick": quick_sort}
MIN_REPEATS = 5


def _parse_int(text: str) -> int:
    try:
        return int(text)
    except ValueError:
        raise CliError(f"не целое число: {text!r}") from None




def cmd_pow(args) -> int:
    names = list(POW_METHODS) if args.method == "both" else [args.method]
    results = {}
    for name in names:
        try:
            results[name] = POW_METHODS[name](args.number, args.exp)
        except (TypeError, ValueError) as exc:
            raise CliError(str(exc)) from None
        except RecursionError:
            raise CliError("превышена глубина рекурсии Python") from None

    if len(set(results.values())) > 1:
        raise CliError(f"результаты методов расходятся: {results}")
    print(next(iter(results.values())))
    return 0

def cmd_sort(args) -> int:
    data = args.numbers
    print(*ALGORITHMS[args.algorithm](data))
    return 0


def cmd_generate(args) -> int:
    try:
        data = GENERATORS[args.kind](args.n, seed=args.seed)
    except (TypeError, ValueError) as exc:
        raise CliError(str(exc)) from None
    print(*data)
    return 0


def cmd_queue(args) -> int:
    q = Queue()
    ops, i = args.ops, 0
    while i < len(ops):
        op, i = ops[i], i + 1
        if op == "add":
            if i >= len(ops):
                raise CliError("после add нужно значение")
            q.add_queue(_parse_int(ops[i]))
            i += 1
        elif op == "pop":
            print(q.pop_queue())
        elif op == "next":
            print(q.next())
        elif op == "len":
            print(len(q))
        elif op == "bool":
            print(bool(q))
        else:
            raise CliError(f"неизвестная операция: {op!r} "
                           f"(доступны: add, pop, next, len, bool)")
    return 0


def _parse_limits(items: list[str] | None) -> dict[str, int]:
    limits = {}
    for item in items or []:
        name, sep, value = item.partition("=")
        if not sep or name not in ALGORITHMS:
            raise CliError(f"ожидается АЛГОРИТМ=N, например insertion=1000: {item!r}")
        limits[name] = _parse_int(value)
    return limits


def cmd_benchmark(args) -> int:
    if args.repeats < MIN_REPEATS:
        raise CliError(f"по заданию нужно не менее {MIN_REPEATS} повторов")
    algorithms = {name: ALGORITHMS[name] for name in args.algorithms}
    generators = {name: GENERATORS[name] for name in args.inputs}
    rows = benchmark(
        algorithms=algorithms, generators=generators, sizes=args.sizes, repeats=args.repeats, seed=args.seed,
        max_size=_parse_limits(args.max_size),
    )
    if not rows:
        raise CliError("нет результатов: все размеры отфильтрованы --max-size")
    write_csv(rows, args.csv)

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="algopack", description="Алгоритмический мини-пакет")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser(
        "pow", help="быстрое возведение в степень",
        description="Пример: algopack pow 2 10 --method both")
    p.add_argument("number", type=int, help="основание")
    p.add_argument("exp", type=int, help="показатель (>= 0)")
    p.add_argument("-m", "--method", choices=[*POW_METHODS, "both"], default="both")
    p.set_defaults(func=cmd_pow)

    p = sub.add_parser("sort", help="отсортировать числа")
    p.add_argument("numbers", nargs="*",
                   help="целые числа")
    p.add_argument("-a", "--algorithm", choices=ALGORITHMS, default="quick")
    p.set_defaults(func=cmd_sort)

    p = sub.add_parser("generate", help="сгенерировать тестовый набор")
    p.add_argument("kind", choices=GENERATORS)
    p.add_argument("n", type=int, help="размер набора")
    p.add_argument("--seed", type=int, default=None,
                   help="seed для воспроизводимости")
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser(
        "queue", help="цепочка операций над очередью",
        description="Операции: add X, pop, next, len, bool. "
                    "Пример: algopack queue add 1 add 2 pop next len")
    p.add_argument("ops", nargs="+")
    p.set_defaults(func=cmd_queue)

    p = sub.add_parser("benchmark", help="замеры времени, CSV и отчёт")
    p.add_argument("--sizes", type=int, nargs="+", default=[100, 1000, 10000])
    p.add_argument("--repeats", type=int, default=MIN_REPEATS)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--algorithms", nargs="+", choices=ALGORITHMS,
                   default=list(ALGORITHMS))
    p.add_argument("--inputs", nargs="+", choices=GENERATORS,
                   default=list(GENERATORS))
    p.add_argument("--max-size", action="append", metavar="АЛГОРИТМ=N",
                   help="не запускать алгоритм на n больше N "
                        "(можно указывать несколько раз)")
    p.add_argument("--csv", default="benchmark.csv")
    p.set_defaults(func=cmd_benchmark)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except CliError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1
    except EmptyQueueError as exc:
        print(f"Ошибка: очередь пуста ({exc})", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
