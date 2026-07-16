# Баг 17. `diophantine` зависит от порядка символов

## ID

`sympy__sympy-18189`

## Исходный текст из dataset

````text
diophantine: incomplete results depending on syms order with permute=True
```
In [10]: diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(m,n), permute=True)
Out[10]: {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}

In [11]: diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(n,m), permute=True)
Out[11]: {(3, 2)}
```

diophantine: incomplete results depending on syms order with permute=True
```
In [10]: diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(m,n), permute=True)
Out[10]: {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}

In [11]: diophantine(n**4 + m**4 - 2**4 - 3**4, syms=(n,m), permute=True)
Out[11]: {(3, 2)}
```

````

## Описание бага

- Используется решатель диофантовых уравнений с явным порядком символов и `permute=True`.
- Пользователь ищет все целочисленные решения симметричного уравнения четвёртой степени.
- Перестановка символов в параметре `syms` резко сокращает результат, хотя должна лишь изменить порядок координат в тех же решениях.

## Ожидаемое поведение

Для обоих порядков `(x, y)` и `(y, x)` решатель должен вернуть полный набор из восьми комбинаций знаков и перестановок чисел 2 и 3.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy` и проверяет оба порядка символов.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import symbols
from sympy.solvers.diophantine.diophantine import diophantine

x, y = symbols("x y", integer=True)
expected = {
    (-3, -2), (-3, 2), (-2, -3), (-2, 3),
    (2, -3), (2, 3), (3, -2), (3, 2),
}
equation = y**4 + x**4 - 2**4 - 3**4
assert diophantine(equation, syms=(x, y), permute=True) == expected
assert diophantine(equation, syms=(y, x), permute=True) == expected
PY
```

В неисправном состоянии один порядок `syms` возвращает полный набор, а другой — только часть решений, например `{(3, 2)}`, поэтому одна из двух проверок падает.

## Автоматический тест

Точный селектор теста:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_18189_test_diophantine
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/solvers/diophantine.py
```
