# Баг 27. is_zero даёт неверный ответ для комплексного выражения

## ID

`sympy__sympy-15875`

## Исходный текст из dataset

````text
is_zero is incorrect on complex integer
`is_zero` should return `None` if it cannot decide, but should never give the wrong answer. However:

```
>>> e = -2*I + (1 + I)**2
>>> e.is_zero
False
>>> simplify(e).is_zero
True
```

This is causing errors in determining the rank of a matrix. See issue #15872
Fixing is_zero for complex numbers while Add
References to other Issues or PRs
#15873

Other comments:

<!-- BEGIN RELEASE NOTES -->

- core
  - Fix `is_zero` becoming `False` on some expressions with `Add`.

<!-- END RELEASE NOTES -->


````

## Описание бага

- Используется предположение `is_zero` для суммы с комплексными числами.
- Пользователь проверяет выражение до полного упрощения, например при определении ранга матрицы.
- SymPy уверенно возвращает `False`, хотя выражение равно нулю; неопределённый случай нельзя объявлять ненулевым.

## Ожидаемое поведение

Для неупрощённого выражения `-2*I + (1 + I)**2` свойство `is_zero` должно
вернуть `None`, то есть не делать неверного окончательного вывода.

```text
None
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import I

expression = -2*I + (1 + I)**2
assert expression.is_zero is None
PY
```

В `sirius-og-buggy` проверка падает, потому что `expression.is_zero` имеет
значение `False` вместо `None`.

## Автоматический тест

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_15875_test_Add_is_zero
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага
он должен проходить.

## Где смотреть код

```text
sympy/core/add.py
```
