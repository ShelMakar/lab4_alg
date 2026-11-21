from src.main import main
from src.recur import fast_pow_loop, fast_pow_rec


def test_pow_matches_builtin():
    assert fast_pow_rec(2, 10) == fast_pow_loop(2, 10) == 2 ** 10

def test_pow_negative_exp_rejected(capsys):
    assert main(["pow", "2", "-1"]) == 1
    assert "неотрицательным" in capsys.readouterr().err

def test_pow_cli_output(capsys):
    assert main(["pow", "2", "10"]) == 0
    assert capsys.readouterr().out.strip() == "1024"


def test_sort_basic(capsys):
    assert main(["sort", "5", "-1", "3", "3", "0"]) == 0
    assert capsys.readouterr().out.split() == ["-1", "0", "3", "3", "5"]


def test_sort_empty(capsys):
    assert main(["sort"]) == 0
    assert capsys.readouterr().out.strip() == ""


def test_sort_algorithms_agree(capsys):
    main(["sort", "-a", "selection", "4", "2", "9", "2", "-7"])
    a = capsys.readouterr().out
    main(["sort", "-a", "quick", "4", "2", "9", "2", "-7"])
    assert a == capsys.readouterr().out


def test_sort_rejects_non_number(capsys):
    assert main(["sort", "1", "abc"]) == 1
    assert "не целое число" in capsys.readouterr().err


def test_generate_same_seed(capsys):
    main(["generate", "random", "30", "--seed", "7"])
    first = capsys.readouterr().out
    main(["generate", "random", "30", "--seed", "7"])
    assert first == capsys.readouterr().out


def test_generate_negative_n(capsys):
    assert main(["generate", "random", "-5"]) == 1


def test_queue_fifo(capsys):
    assert main(["queue", "add", "1", "add", "2", "pop", "next", "len"]) == 0
    assert capsys.readouterr().out.split() == ["1", "2", "1"]


def test_queue_empty_error(capsys):
    assert main(["queue", "pop"]) == 1
    assert "пуста" in capsys.readouterr().err


def test_benchmark_writes_files(tmp_path):
    csv_path = tmp_path / "b.csv"
    code = main(["benchmark", "--sizes", "100", "--repeats", "5",
                 "--inputs", "random", "sorted",
                 "--csv", str(csv_path)])
    assert code == 0
    assert csv_path.exists()


def test_benchmark_rejects_few_repeats():
    assert main(["benchmark", "--repeats", "2"]) == 1