# Баг 06. Длина массива ранга 0 равна нулю

## ID

`sympy__sympy-15017`

## Исходный текст из dataset

````text
`len` of rank-0 arrays returns 0
`sympy.tensor.array.NDimArray.__len__` always returns zero for rank-0 arrays (scalars). I believe the correct value should be one, which is the number of elements of the iterator and the observed behaviour in numpy.

```python
>>> import sympy
>>> a = sympy.Array(3)
>>> len(a)
0
>>> len(list(a))
1
```
In numpy we have the following:

```python
>>> import numpy
>>> numpy.asarray(1).size
1
```

This was tested in sympy 1.2-rc1 running in Python 3.6.6
`len` of rank-0 arrays returns 0
`sympy.tensor.array.NDimArray.__len__` always returns zero for rank-0 arrays (scalars). I believe the correct value should be one, which is the number of elements of the iterator and the observed behaviour in numpy.

```python
>>> import sympy
>>> a = sympy.Array(3)
>>> len(a)
0
>>> len(list(a))
1
```
In numpy we have the following:

```python
>>> import numpy
>>> numpy.asarray(1).size
1
```

This was tested in sympy 1.2-rc1 running in Python 3.6.6
````

## Описание бага

- Используется `ImmutableDenseNDimArray` для представления как обычных массивов, так и скаляров ранга 0.
- Пользователь спрашивает количество элементов скалярного массива через `len()`.
- Скаляру соответствует один элемент, но метод возвращает ноль, что противоречит итерации по массиву и его форме.

## Ожидаемое поведение

Пустой массив формы `(0,)` должен иметь длину 0 и ранг 1. Скалярный массив должен иметь длину 1, форму `()`, ранг 0 и возвращать исходный элемент по индексу `()`.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import ImmutableDenseNDimArray, Symbol

empty = ImmutableDenseNDimArray([], shape=(0,))
assert len(empty) == 0
assert empty.ndim == 1

x = Symbol("x")
scalar = ImmutableDenseNDimArray(x)
assert len(scalar) == 1
assert scalar.shape == ()
assert scalar.ndim == 0
assert scalar[()] == x
PY
```

В `sirius-og-buggy` `len(scalar)` возвращает `0`, поэтому проверка ожидаемой длины `1` падает до остальных проверок скаляра.

## Автоматический тест

Точный селектор теста:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_15017_test_ndim_array_initiation
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/tensor/array/dense_ndim_array.py
```
