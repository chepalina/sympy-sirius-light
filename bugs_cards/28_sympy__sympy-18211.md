# Баг 28. as_set выбрасывает исключение вместо ConditionSet

## ID

`sympy__sympy-18211`

## Исходный текст из dataset

````text
`solveset` raises `NotImplementedError` instead of returning `ConditionSet`
The problem is
```julia
In [10]: Eq(n*cos(n) - 3*sin(n), 0).as_set()
---------------------------------------------------------------------------
NotImplementedError
```
Here `solveset` raises `NotImplementedError` but probably a `ConditionSet` should be returned by `solveset` instead. The obvious result of `as_set()` here is
```julia
In [11]: ConditionSet(n, Eq(n*cos(n) - 3*sin(n), 0), Reals)
Out[11]: {n | n ∊ ℝ ∧ n⋅cos(n) - 3⋅sin(n) = 0}
```

_Originally posted by @oscarbenjamin in https://github.com/sympy/sympy/pull/17771_

````

## Описание бага

- Используется преобразование равенства в множество решений через `Eq.as_set()`.
- Пользователь задаёт трансцендентное уравнение, для которого нет явного решения.
- Вместо символического множества условий SymPy выбрасывает `NotImplementedError`.

## Ожидаемое поведение

Оба уравнения должны преобразовываться в `ConditionSet` над вещественными
числами. Во втором случае условие должно содержать канонически представленное
выражение со `sqrt(2)*sqrt(x)`.

```text
ConditionSet(x, first, S.Reals)
ConditionSet(x, Eq(sqrt(2)*sqrt(x) + x**2 + sin(x), 0), S.Reals)
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import ConditionSet, Eq, S, Symbol, cos, sin, sqrt

x = Symbol("x", real=True)
first = Eq(x*cos(x) - 3*sin(x), 0)
assert first.as_set() == ConditionSet(x, first, S.Reals)

second = Eq(x**2 + sqrt(2*x) + sin(x), 0)
expected = ConditionSet(x, Eq(sqrt(2)*sqrt(x) + x**2 + sin(x), 0), S.Reals)
assert second.as_set() == expected
PY
```

В `sirius-og-buggy` преобразование одного из уравнений завершается
`NotImplementedError` вместо возврата `ConditionSet`.

## Автоматический тест

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_18211_test_issue_18188
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага
он должен проходить.

## Где смотреть код

```text
sympy/core/relational.py
```
