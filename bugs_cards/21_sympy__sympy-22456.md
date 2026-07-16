# Баг 21. Объект String нельзя восстановить из его аргументов

## ID

`sympy__sympy-22456`

## Исходный текст из dataset

````text
Argument invariance of codegen.ast String
Currently, the `codegen.ast` `String` class does not support argument invariance like:
`expr.func(*expr.args) == expr`, but instead uses the invariance `expr.func(**expr.kwargs()) == expr`.
The former should hold for any `Basic` subclass, which `String` is.

````

## Описание бага

- Используется узел `String` из абстрактного синтаксического дерева генератора кода.
- Пользователь применяет общий для объектов `Basic` способ восстановления `expr.func(*expr.args)`.
- Восстановленный объект не равен исходному, поэтому нарушается ожидаемый контракт выражений SymPy.

## Ожидаемое поведение

Объект `String("foobar")` должен без потери значения восстанавливаться своей
функцией из `args`.

```text
value.func(*value.args) == value
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy.codegen.ast import String

value = String("foobar")
assert value.func(*value.args) == value
PY
```

В `sirius-og-buggy` проверка равенства завершается ошибкой: создание `String`
из его позиционных аргументов не воспроизводит исходный объект.

## Автоматический тест

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_22456_test_String
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага
он должен проходить.

## Где смотреть код

```text
sympy/codegen/ast.py
```
