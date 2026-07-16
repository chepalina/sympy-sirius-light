# Баг 05. `PythonCodePrinter` не поддерживает индексированные объекты

## ID

`sympy__sympy-16766`

## Исходный текст из dataset

````text
PythonCodePrinter doesn't support Indexed
I use `lambdify()` to generate some functions and save the code for further use. But the generated code for `Indexed` operation has some warnings which can be confirmed by following code;

```
from sympy import *
p = IndexedBase("p")

pycode(p[0])
```
the output is

```
  # Not supported in Python:
  # Indexed
p[0]
```

We should add following method to `PythonCodePrinter`:

```
def _print_Indexed(self, expr):
    base, *index = expr.args
    return "{}[{}]".format(str(base), ", ".join([self._print(ind) for ind in index]))
```
````

## Описание бага

- Используется генератор Python-кода `PythonCodePrinter` для объекта `Indexed`.
- Пользователь преобразует индексированный элемент, например `p[0, 1]`, в исполняемое Python-выражение.
- Принтер считает стандартную индексную запись неподдерживаемой и в строгом режиме выбрасывает исключение вместо строки с кодом.

## Ожидаемое поведение

Индексированный объект с двумя индексами должен печататься как обычное обращение к элементу Python:

```text
p[0, 1]
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy.printing.pycode import PythonCodePrinter
from sympy.tensor import IndexedBase

indexed = IndexedBase("p")
assert PythonCodePrinter().doprint(indexed[0, 1]) == "p[0, 1]"
PY
```

В `sirius-og-buggy` принтер выбрасывает `PrintMethodNotImplementedError` для `Indexed`, поэтому строка `p[0, 1]` не создаётся.

## Автоматический тест

Точный селектор теста:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_16766_test_PythonCodePrinter
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/printing/pycode.py
```
