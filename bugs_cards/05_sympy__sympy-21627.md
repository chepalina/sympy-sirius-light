# Баг 05. Abs вызывает RecursionError на сложном выражении

## ID

`sympy__sympy-21627`

## Исходный текст из dataset

````text
Bug: maximum recusion depth error when checking is_zero of cosh expression The following code causes a `RecursionError: maximum recursion depth exceeded while calling a Python object` error when checked if it is zero: ``` expr =sympify("cosh(acos(-i + acosh(-g + i)))") expr.is_zero ```
````

## Описание бага

SymPy умеет проверять свойства выражений, например равно ли выражение нулю. Такие проверки используются внутри многих функций.

Баг проявляется на сложном комплексном выражении: при попытке построить `Abs` для выражения из `im(acos(...))` bug-ветка уходит в бесконечную рекурсию и падает с `RecursionError`.

## Ожидаемое поведение

Построение `Abs` не должно приводить к переполнению стека. В тесте проверяется, что выражение остаётся неизменённым после попытки построить `Abs`.

```text
True
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-light-buggy`.

```bash
git switch sirius-light-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Abs, S
from sympy.core.expr import unchanged

expr = S("im(acos(-i + acosh(-g + i)))")
print(unchanged(Abs, expr))
PY
```

В `sirius-light-buggy` команда падает с ошибкой:

```text
RecursionError: maximum recursion depth exceeded
```

## Сравнение с golden-веткой

Golden-ветка нужна только для ознакомления с исправленным поведением.

```bash
git switch sirius-light-golden
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Abs, S
from sympy.core.expr import unchanged

expr = S("im(acos(-i + acosh(-g + i)))")
print(unchanged(Abs, expr))
PY
```

В `sirius-light-golden` команда выводит:

```text
True
```

## Автоматический тест

Команда для запуска теста, который фиксирует этот баг:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_light_bugs.py::test_Abs
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/functions/elementary/complexes.py
sympy/functions/elementary/tests/test_complexes.py
sirius_tests/test_light_bugs.py
```
