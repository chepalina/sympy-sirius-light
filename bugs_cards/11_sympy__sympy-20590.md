# Баг 11. Базовые символьные объекты получили `__dict__`

## ID

`sympy__sympy-20590`

## Исходный текст из dataset

````text
Symbol instances have __dict__ since 1.7?
In version 1.6.2 Symbol instances had no `__dict__` attribute
```python
>>> sympy.Symbol('s').__dict__
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-3-e2060d5eec73> in <module>
----> 1 sympy.Symbol('s').__dict__

AttributeError: 'Symbol' object has no attribute '__dict__'
>>> sympy.Symbol('s').__slots__
('name',)
```

This changes in 1.7 where `sympy.Symbol('s').__dict__` now exists (and returns an empty dict)
I may misinterpret this, but given the purpose of `__slots__`, I assume this is a bug, introduced because some parent class accidentally stopped defining `__slots__`.
````

## Описание бага

- Используются базовые неизменяемые объекты ядра SymPy, от которых наследуется `Symbol`.
- Пользователь рассчитывает на ограничение атрибутов через `__slots__`, важное для неизменяемости и расхода памяти большого числа выражений.
- У экземпляров появляется `__dict__`, и им можно назначать произвольные атрибуты, хотя базовые символьные объекты должны оставаться неизменяемыми.

## Ожидаемое поведение

У экземпляра `Basic` не должно быть `__dict__`. Попытка присвоить произвольный атрибут `value.x` должна выбрасывать `AttributeError`.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Basic
from sympy.testing.pytest import raises

value = Basic()
assert not hasattr(value, "__dict__")
with raises(AttributeError):
    value.x = 1
PY
```

В `sirius-og-buggy` у `Basic()` обнаруживается `__dict__`, поэтому первая проверка падает; наличие словаря также допускает нежелательные произвольные атрибуты.

## Автоматический тест

Точный селектор теста:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_20590_test_immutable
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/core/_print_helpers.py
```
