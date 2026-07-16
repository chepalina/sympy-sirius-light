# Баг 35. Ноль с плавающей точкой равен логическому false

## ID

`sympy__sympy-20801`

## Исходный текст из dataset

````text
S(0.0) == S.false returns True
This issue is related to those listed in #20033.

As shown by @sayandip18, comparing `S.false` to `S(0.0)` returns 2 different results depending on the order in which they are compared:

```pycon
>>> from sympy import *
>>> S(0.0) == S.false
True
>>> S.false == S(0.0)
False
```
Based on the results of comparison to `S(0)`:

```pycon
>>> S(0) == S.false
False
>>> S.false == S(0)
False
```
I assume we would want `S(0.0) == S.false` to return True as well?

````

## Описание бага

- Используется сравнение числовых нулей SymPy с логическим объектом `S.false`.
- Пользователь сравнивает объекты в обоих порядках и для целого и вещественного нуля.
- Равенство зависит от порядка аргументов, а вещественный ноль ошибочно считается логическим значением.

## Ожидаемое поведение

Числовые объекты `S(0.0)` и `S(0)` не должны быть равны `S.false` ни при одном
порядке сравнения. Все четыре выражения должны возвращать обычное `False`.

```text
False
False
False
False
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import S

assert (S(0.0) == S.false) is False
assert (S.false == S(0.0)) is False
assert (S(0) == S.false) is False
assert (S.false == S(0)) is False
PY
```

В `sirius-og-buggy` первая проверка падает: `S(0.0) == S.false` возвращает
`True`, тогда как сравнение в обратном порядке возвращает `False`.

## Автоматический тест

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_20801_test_zero_not_false
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага
он должен проходить.

## Где смотреть код

```text
sympy/core/numbers.py
```
