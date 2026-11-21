class EmptyQueueError(Exception):
    """Операция над пустой очередью"""

class NotIntError(TypeError):
    """Введено не целое число"""

class IncorrectExpError(ValueError):
    """Некорректное значение степени"""

class CliError(Exception):
    """Ошибка пользовательского ввода"""