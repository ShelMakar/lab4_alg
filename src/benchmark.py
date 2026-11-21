import csv
import statistics
import time


def time_value(func, par, repeats=5) -> list[time]:
    time_values = []
    for i in range(repeats):
        values = list(par)
        t = time.perf_counter()
        func(values)
        time_values.append(time.perf_counter() - t)
    return time_values


def benchmark(algorithms: dict, generators, sizes: list, repeats=5, seed=42, max_size=None):
    max_size = max_size or {}
    rows = []
    for gen_name, gen in generators.items():
        for n in sizes:
            base = gen(n, seed=seed)                  # генерация вне замера
            for algo_name, func in algorithms.items():
                if n > max_size.get(algo_name, float("inf")):
                    continue                          # слишком долго, пропускаем
                times = time_value(func, base, repeats)
                rows.append({
                    "algorithm": algo_name,
                    "input": gen_name,
                    "n": n,
                    "repeats": repeats,
                    "min_s": min(times),
                    "max_s": max(times),
                    "median_s": statistics.median(times),
                    "mean_s": statistics.fmean(times),
                })
    return rows

def write_csv(rows: list, path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)