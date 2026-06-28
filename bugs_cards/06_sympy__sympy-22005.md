# Баг 06. solve_poly_system не распознаёт бесконечное число решений

## ID

`sympy__sympy-22005`

## Исходный текст из dataset

````text
detection of infinite solution request ```python >>> solve_poly_system((x - 1,), x, y) Traceback (most recent call last): ... NotImplementedError: only zero-dimensional systems supported (finite number of solutions) >>> solve_poly_system((y - 1,), x, y) <--- this is not handled correctly [(1,)] ``` ```diff diff --git a/sympy/solvers/polysys.py b/sympy/solvers/polysys.py index b9809fd4e9..674322d4eb 100644 --- a/sympy/solvers/polysys.py +++ b/sympy/solvers/polysys.py @@ -240,7 +240,7 @@ def _solve_reduced_system(system, gens, entry=False): univariate = list(filter(_is_univariate, basis)) - if len(univariate) == 1: + if len(univariate) == 1 and len(gens) == 1: f = univariate.pop() else: raise NotImplementedError(filldedent(''' diff --git a/sympy/solvers/tests/test_polysys.py b/sympy/solvers/tests/test_polysys.py index 58419f8762..9e674a6fe6 100644 ---...
````

## Описание бага

`solve_poly_system` решает системы полиномиальных уравнений. Если система имеет бесконечно много решений, функция должна явно сообщать, что такой случай не поддержан.

Баг проявляется на системе `y - 1` с переменными `(x, y)`: переменная `x` остаётся свободной, значит решений бесконечно много. Bug-ветка вместо ошибки возвращает неполный результат.

## Ожидаемое поведение

Для системы с бесконечным числом решений должен быть `NotImplementedError`.

```text
NotImplementedError: only zero-dimensional systems supported (finite number of solutions)
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-light-buggy`.

```bash
git switch sirius-light-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import solve_poly_system, symbols

x, y = symbols("x y")
print(solve_poly_system([y - 1], (x, y)))
PY
```

В `sirius-light-buggy` команда выводит неполный результат:

```text
[(1,)]
```

## Сравнение с golden-веткой

Golden-ветка нужна только для ознакомления с исправленным поведением.

```bash
git switch sirius-light-golden
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import solve_poly_system, symbols

x, y = symbols("x y")

try:
    solve_poly_system([y - 1], (x, y))
except Exception as e:
    print(type(e).__name__)
    print(str(e))
PY
```

В `sirius-light-golden` команда выводит:

```text
NotImplementedError

only zero-dimensional systems supported (finite number of solutions)
```

## Автоматический тест

Команда для запуска теста, который фиксирует этот баг:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_light_bugs.py::test_solve_poly_system
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/solvers/polysys.py
sympy/solvers/tests/test_polysys.py
sirius_tests/test_light_bugs.py
```
