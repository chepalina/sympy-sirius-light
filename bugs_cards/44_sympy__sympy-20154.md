# Баг 44. `partitions()` повторно использует один словарь

## ID

`sympy__sympy-20154`

## Исходный текст из dataset

````text
partitions() reusing the output dictionaries
The partitions() iterator in sympy.utilities.iterables reuses the output dictionaries. There is a caveat about it in the docstring.

I'm wondering if it's really that important for it to do this. It shouldn't be that much of a performance loss to copy the dictionary before yielding it. This behavior is very confusing. It means that something as simple as list(partitions()) will give an apparently wrong result. And it can lead to much more subtle bugs if the partitions are used in a nontrivial way.
````

## Описание бага

- Итератор `partitions()` выдаёт разбиения числа в виде словарей.
- Пользователь сохраняет результаты через `list(partitions(...))`.
- Итератор повторно использует один объект словаря, поэтому уже сохранённые элементы неожиданно меняются.

## Ожидаемое поведение

Каждое разбиение должно быть отдельным словарём. Например, `list(partitions(6, k=2))` должно содержать четыре разные записи от `{2: 3}` до `{1: 6}`.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy.utilities.iterables import partitions

assert list(partitions(6, k=2)) == [
    {2: 3},
    {1: 2, 2: 2},
    {1: 4, 2: 1},
    {1: 6},
]
PY
```

В `sirius-og-buggy` элементы списка оказываются повторно использованными словарями с неверным содержимым.

## Автоматический тест

Точные селекторы всех тестов этого бага:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_20154_test_partitions
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_20154_test_uniq
```

В начале работы над bug-веткой эти тесты должны падать. После исправления бага они должны проходить.

## Где смотреть код

Связанный тест из dataset:

```text
sympy/utilities/tests/test_iterables.py
```
