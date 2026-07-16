# Баг 46. Умножение выражения на `Poly` зависит от порядка операндов

## ID

`sympy__sympy-13757`

## Исходный текст из dataset

````text
Multiplying an expression by a Poly does not evaluate when the expression is on the left side of the multiplication
Tested in Python 3.4 64-bit and 3.6 64-bit
Version: 1.1.2.dev0
```
>>> Poly(x)*x
Poly(x**2, x, domain='ZZ')

>>> x*Poly(x)
x*Poly(x, x, domain='ZZ')

>>> -2*Poly(x)
Poly(-2*x, x, domain='ZZ')

>>> S(-2)*Poly(x)
-2*Poly(x, x, domain='ZZ')

>>> Poly(x)*S(-2)
Poly(-2*x, x, domain='ZZ')
```
````

## Описание бага

- Перемножаются обычное выражение SymPy и объект `Poly`.
- При расположении `Poly` слева результат вычисляется корректно.
- При расположении того же `Poly` справа произведение остаётся невычисленным.

## Ожидаемое поведение

`Poly(x)*x` и `x*Poly(x)` должны оба давать `Poly(x**2, x, domain='ZZ')`; аналогично должно работать умножение на целый коэффициент.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Poly, symbols

x = symbols("x")
expected = Poly(x**2, x, domain="ZZ")
assert Poly(x)*x == expected
assert x*Poly(x) == expected
PY
```

В `sirius-og-buggy` `x*Poly(x)` остаётся обычным произведением вместо объекта `Poly`.

## Автоматический тест

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_13757_test_issue_13079
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага
он должен проходить.

## Где смотреть код

Связанные тесты из dataset:

```text
sympy/core/tests/test_match.py
sympy/polys/tests/test_polytools.py
```
