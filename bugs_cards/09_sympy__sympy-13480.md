# Баг 09. Подстановка в `coth(log(tan(x)))` вызывает `NameError`

## ID

`sympy__sympy-13480`

## Исходный текст из dataset

````text
.subs on coth(log(tan(x))) errors for certain integral values
    >>> from sympy import *
    >>> x = Symbol('x')
    >>> e = coth(log(tan(x)))
    >>> print(e.subs(x, 2))
    ...
    File "C:\Users\E\Desktop\sympy-master\sympy\functions\elementary\hyperbolic.py", line 590, in eval
        if cotm is S.ComplexInfinity:
    NameError: name 'cotm' is not defined

Fails for 2, 3, 5, 6, 8, 9, 11, 12, 13, 15, 18, ... etc.
````

## Описание бага

- Используются гиперболическая функция `coth` и преобразования выражений с `log`, `tan` и мнимым периодом.
- Пользователь подставляет целое значение в `coth(log(tan(x)))` или вычисляет эквивалентное периодическое выражение.
- Внутренняя обработка суммы обращается к несуществующей локальной переменной, поэтому корректное символьное выражение завершается `NameError`.

## Ожидаемое поведение

Эквивалентные формы с `tan(2)` и `-tan(2)` должны давать одинаковый `coth`. Кроме того, периодическое тождество должно выполняться:

```text
coth(1 + I*pi/2) == tanh(1)
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy` и включает оба сценария теста.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import I, coth, log, pi, tan, tanh

assert coth(log(tan(2))) == coth(log(-tan(2)))
assert coth(1 + I*pi/2) == tanh(1)
PY
```

В `sirius-og-buggy` первый сценарий выбрасывает `NameError: name 'cotm' is not defined`, поэтому ни равенство, ни последующая проверка не завершаются штатно.

## Автоматический тест

Точный селектор теста:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_13480_test_coth
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/functions/elementary/hyperbolic.py
```
