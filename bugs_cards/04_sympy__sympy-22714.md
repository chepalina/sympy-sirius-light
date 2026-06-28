# Баг 04. Point падает внутри evaluate(False)

## ID

`sympy__sympy-22714`

## Исходный текст из dataset

````text
simpify gives `Imaginary coordinates are not permitted.` with evaluate(False) ## Issue `with evaluate(False)` crashes unexpectedly with `Point2D` ## Code ```python import sympy as sp with sp.evaluate(False): sp.S('Point2D(Integer(1),Integer(2))') ``` ## Error ``` Traceback (most recent call last): File "<stdin>", line 1, in <module> File "/home/avinash/.local/lib/python3.8/site-packages/sympy/core/sympify.py", line 472, in sympify expr = parse_expr(a, local_dict=locals, transformations=transformations, evaluate=evaluate) File "/home/avinash/.local/lib/python3.8/site-packages/sympy/parsing/sympy_parser.py", line 1026, in parse_expr raise e from ValueError(f"Error from parse_expr with transformed code: {code!r}") File "/home/avinash/.local/lib/python3.8/site-packages/sympy/parsing/sympy_parser.py", line 1017, in parse_expr rv = eval_expr(code, local_dict, global_dict) File...
````

## Описание бага

SymPy позволяет временно отключать автоматическое вычисление выражений через `evaluate(False)`.

Баг проявляется при создании точки `Point` внутри такого контекста. Координаты обычные и вещественные, но bug-ветка ошибочно считает их недопустимыми мнимыми координатами.

## Ожидаемое поведение

Создание `Point(1, 2)` внутри `evaluate(False)` не должно падать.

```text
Point2D(1, 2)
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-light-buggy`.

```bash
git switch sirius-light-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Point
from sympy.core.parameters import evaluate

with evaluate(False):
    p = Point(1, 2)

print(p)
PY
```

В `sirius-light-buggy` команда падает с ошибкой:

```text
ValueError: Imaginary coordinates are not permitted.
```

## Сравнение с golden-веткой

Golden-ветка нужна только для ознакомления с исправленным поведением.

```bash
git switch sirius-light-golden
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Point
from sympy.core.parameters import evaluate

with evaluate(False):
    p = Point(1, 2)

print(p)
PY
```

В `sirius-light-golden` команда выводит:

```text
Point2D(1, 2)
```

## Автоматический тест

Команда для запуска теста, который фиксирует этот баг:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_light_bugs.py::test_issue_22684
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/geometry/point.py
sympy/geometry/tests/test_point.py
sirius_tests/test_light_bugs.py
```
