# Баг 13. `kernS` обращается к неинициализированной переменной

## ID

`sympy__sympy-19637`

## Исходный текст из dataset

````text
kernS: 'kern' referenced before assignment
from sympy.core.sympify import kernS

text = "(2*x)/(x-1)"
expr = kernS(text)
//  hit = kern in s
// UnboundLocalError: local variable 'kern' referenced before assignment
````

## Описание бага

- Используется функция `kernS` из механизма преобразования строк в выражения SymPy.
- Пользователь разбирает строку с дробью и скобками, для которой защитная подстановка внутреннего маркера не требуется.
- Функция всё равно обращается к переменной маркера до её создания и выбрасывает `UnboundLocalError` вместо выражения.

## Ожидаемое поведение

Строка `(2*x)/(x-1)` должна без ошибки преобразовываться в выражение, равное `2*x/(x - 1)`.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Symbol
from sympy.core.sympify import kernS

x = Symbol("x")
assert kernS("(2*x)/(x-1)") == 2*x/(x - 1)
PY
```

В `sirius-og-buggy` вызов `kernS` завершается `UnboundLocalError`, потому что локальная переменная `kern` не была создана.

## Автоматический тест

Точный селектор теста:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_19637_test_kernS
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/core/sympify.py
```
