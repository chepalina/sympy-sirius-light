# Баг 37. `parse_expr` игнорирует `evaluate=False` для сравнений

## ID

`sympy__sympy-24661`

## Исходный текст из dataset

````text
The evaluate=False parameter to `parse_expr` is ignored for relationals
See also #22305 and #22098

This inequality evaluates even though `evaluate=False` is given:
```python
In [14]: parse_expr('1 < 2', evaluate=False)
Out[14]: True
```
The result that should be returned is:
```python
In [15]: Lt(1, 2, evaluate=False)
Out[15]: 1 < 2
```
````

## Описание бага

- Используется `parse_expr` для разбора строкового сравнения.
- Пользователь отключает вычисление через `evaluate=False`.
- Несмотря на этот параметр, сравнение сразу превращается в `True` или `False`.

## Ожидаемое поведение

Все операторы сравнения должны оставаться невычисленными объектами SymPy. Например, строка `1 < 2` должна давать `Lt(1, 2, evaluate=False)`.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Lt
from sympy.parsing.sympy_parser import parse_expr

assert parse_expr("1 < 2", evaluate=False) == Lt(1, 2, evaluate=False)
PY
```

В `sirius-og-buggy` разбор возвращает булево значение `True`.

## Автоматический тест

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_24661_test_issue_24288
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага
он должен проходить.

## Где смотреть код

Связанный тест из dataset:

```text
sympy/parsing/tests/test_sympy_parser.py
```
