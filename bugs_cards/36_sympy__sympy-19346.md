# Баг 36. srepr не раскрывает элементы словаря

## ID

`sympy__sympy-19346`

## Исходный текст из dataset

````text
srepr not printing dict and set properly
`srepr` prints the element in `list` and `tuple` correctly.
```python
>>> from sympy import srepr
>>> from sympy.abc import x,y
>>> srepr([x,y])
[Symbol('x'), Symbol('y')]
>>> srepr((x,y))
(Symbol('x'), Symbol('y'))
```

However, `srepr` prints the elements in `dict` and `set` wrong.
```python
>>> srepr({x, y})
{x, y}
>>> srepr({x: y})
{x: y}
```

Is this behavior intended? If it isn't, fixing it will be an easy job.

````

## Описание бага

- Используется структурное строковое представление `srepr` для словарей с объектами SymPy.
- Пользователь хочет получить явное представление типов ключей и значений, как для списков и кортежей.
- Внутренние символьные объекты печатаются обычными именами, поэтому результат нельзя использовать как полноценное структурное представление.

## Ожидаемое поведение

Пустой словарь должен печататься как `{}`. Каждый ключ и значение, включая
вложенный словарь, должен быть рекурсивно представлен через `Symbol(...)`;
для словаря из двух пар допустим любой порядок элементов.

```text
{}
{Symbol('x'): Symbol('y')}
{Symbol('x'): {Symbol('y'): Symbol('z')}}
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import srepr
from sympy.abc import x, y, z

assert srepr({}) == "{}"
assert srepr({x: y}) == "{Symbol('x'): Symbol('y')}"
assert srepr({x: y, y: z}) in (
    "{Symbol('x'): Symbol('y'), Symbol('y'): Symbol('z')}",
    "{Symbol('y'): Symbol('z'), Symbol('x'): Symbol('y')}",
)
assert srepr({x: {y: z}}) == "{Symbol('x'): {Symbol('y'): Symbol('z')}}"
PY
```

В `sirius-og-buggy` проверки словарей падают: `srepr` оставляет имена
символов в сокращённом виде вместо структурного `Symbol(...)`.

## Автоматический тест

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_19346_test_dict
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага
он должен проходить.

## Где смотреть код

```text
sympy/printing/repr.py
```
