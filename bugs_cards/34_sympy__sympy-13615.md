# Баг 34. Complement преждевременно упрощает смесь чисел и символов

## ID

`sympy__sympy-13615`

## Исходный текст из dataset

````text
Complement doesn't work when input is a mixture of Symbols and numbers
```
>>> a=FiniteSet(x,y,2)
>>> b=Interval(-10,10)
>>> Complement(a,b)
{x, y}
```
`{x, y} \ [-10,10]` is expected as output.

````

## Описание бага

- Используется разность множеств `Complement` между конечным набором и числовым интервалом.
- Пользователь передаёт в конечное множество как известное число, так и символы с неизвестными значениями.
- SymPy удаляет число из интервала, но одновременно теряет неразрешённое условие для символов.

## Ожидаемое поведение

Число `2`, безусловно входящее в интервал, должно исчезнуть. Для символов `x`
и `y` принадлежность интервалу неизвестна, поэтому разность должна остаться
символическим объектом `Complement`.

```text
Complement(FiniteSet(x, y), Interval(-10, 10))
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Complement, FiniteSet, Interval, symbols

x, y = symbols("x y")
assert Complement(FiniteSet(x, y, 2), Interval(-10, 10)) == Complement(
    FiniteSet(x, y), Interval(-10, 10)
)
PY
```

В `sirius-og-buggy` левая часть упрощается до обычного конечного множества,
хотя принадлежность символов интервалу неизвестна, и проверка падает.

## Автоматический тест

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_13615_test_Complement
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага
он должен проходить.

## Где смотреть код

```text
sympy/sets/sets.py
```
