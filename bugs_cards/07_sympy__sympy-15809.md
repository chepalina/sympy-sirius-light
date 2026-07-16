# Баг 07. `Min()` и `Max()` без аргументов не определены

## ID

`sympy__sympy-15809`

## Исходный текст из dataset

````text
Zero-argument Min() and Max()
Right now `Min()` and `Max()` with no arguments raise `ValueError: The Max/Min functions must have arguments.`. It might be mathematically more convenient to have them return `oo` and `-oo`, respectively. See https://en.wikipedia.org/wiki/Empty_set#Extended_real_numbers for why these are valid answers mathematically.
````

## Описание бага

- Используются функции `Min` и `Max` из элементарных функций SymPy.
- Пользователь вычисляет минимум или максимум пустого набора аргументов, например при свёртке динамически построенной коллекции.
- Вместо математических нейтральных значений обе функции выбрасывают `ValueError`, из-за чего пустой случай приходится обрабатывать отдельно.

## Ожидаемое поведение

`Min()` должен возвращать положительную бесконечность, а `Max()` — отрицательную. Для одного аргумента поведение остаётся обычным: `Min(x) == x` и `Max(x) == x`.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy` и проверяет оба релевантных сценария.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Max, Min, S, Symbol

x = Symbol("x")
assert Min() == S.Infinity
assert Min(x) == x

assert Max() == S.NegativeInfinity
assert Max(x) == x
PY
```

В `sirius-og-buggy` уже вызов `Min()` выбрасывает `ValueError: The Max/Min functions must have arguments`; отдельный вызов `Max()` завершается той же ошибкой.

## Автоматический тест

Точные селекторы всех тестов этого бага:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_15809_test_Min
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_15809_test_Max
```

В начале работы над bug-веткой эти тесты должны падать. После исправления бага они должны проходить.

## Где смотреть код

```text
sympy/functions/elementary/miscellaneous.py
```
