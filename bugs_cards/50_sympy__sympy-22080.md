# Баг 50. `lambdify` меняет смысл отрицательного `Mod`

## ID

`sympy__sympy-22080`

## Исходный текст из dataset

````text
Mod function lambdify bug
Description:
When lambdifying any function of structure like `expr * Mod(a, b)` sympy moves the multiplier into the first argument of Mod, like `Mod(expr * a, b)`, WHEN we specify `modules=[]`

This is an example from Sympy online shell
```
>>> from sympy import Mod, lambdify, symbols
>>> x, y = symbols('x y')
>>> expr = -Mod(x, y)
>>> f = lambdify([x, y], expr)
>>> f(3, 7)
-3
>>> inspect.getsource(f)
def _lambdifygenerated(x, y):
    return (-mod(x, y))


>>> g = lambdify([x, y], expr, modules=[])
>>> g(3, 7)
4
>>> inspect.getsource(g)
def _lambdifygenerated(x, y):
    return (-x % y)
```
````

## Описание бага

- Через `lambdify` создаётся функция для выражения `-Mod(x, y)`.
- При пустом списке модулей используется встроенный оператор `%`.
- Минус переносится внутрь остатка, поэтому численный результат меняется.

## Ожидаемое поведение

Скобки должны сохранять структуру `-(x % y)`. Для аргументов `3` и `7` функция должна возвращать `-3` независимо от списка модулей.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Mod, lambdify, symbols

x, y = symbols("x y")
expression = -Mod(x, y)
default = lambdify([x, y], expression)
empty = lambdify([x, y], expression, modules=[])
assert default(3, 7) == empty(3, 7) == -3
PY
```

В `sirius-og-buggy` функция с `modules=[]` возвращает `4` вместо `-3`.

## Автоматический тест

Точные селекторы всех тестов этого бага:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_22080_test_create_expand_pow_optimization
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_22080_test_PythonCodePrinter
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_22080_test_empty_modules
```

В начале работы над bug-веткой эти тесты должны падать. После исправления бага они должны проходить.

## Где смотреть код

Связанные тесты из dataset:

```text
sympy/codegen/tests/test_rewriting.py
sympy/printing/tests/test_pycode.py
sympy/utilities/tests/test_lambdify.py
```
