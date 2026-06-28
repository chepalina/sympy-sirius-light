# Баг 01. BlockDiagMatrix с одним элементом не конвертируется в Matrix

## ID

`sympy__sympy-18621`

## Исходный текст из dataset

````text
BlockDiagMatrix with one element cannot be converted to regular Matrix Creating a BlockDiagMatrix with one Matrix element will raise if trying to convert it back to a regular Matrix: ```python M = sympy.Matrix([[1, 2], [3, 4]]) D = sympy.BlockDiagMatrix(M) B = sympy.Matrix(D) ``` ``` Traceback (most recent call last): File "<ipython-input-37-5b65c1f8f23e>", line 3, in <module> B = sympy.Matrix(D) File "/home/rikard/.local/lib/python3.7/site-packages/sympy/matrices/dense.py", line 430, in __new__ return cls._new(*args, **kwargs) File "/home/rikard/.local/lib/python3.7/site-packages/sympy/matrices/dense.py", line 442, in _new rows, cols, flat_list = cls._handle_creation_inputs(*args, **kwargs) File "/home/rikard/.local/lib/python3.7/site-packages/sympy/matrices/matrices.py", line 2528, in _handle_creation_inputs return args[0].rows, args[0].cols, args[0].as_explicit()._mat File...
````

## Описание бага

В SymPy есть объект `BlockDiagMatrix`: он собирает блочную диагональную матрицу из одной или нескольких матриц.

Баг проявляется, когда `BlockDiagMatrix` содержит ровно один блок. Пользователь ожидает, что такую конструкцию можно превратить обратно в обычную `Matrix`, но в bug-ветке это приводит к ошибке.

## Ожидаемое поведение

Если `BlockDiagMatrix` создан из одной матрицы, преобразование в обычную `Matrix` должно вернуть исходную матрицу.

```text
Matrix([[1, 2], [3, 4]])
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-light-buggy`.

```bash
git switch sirius-light-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Matrix, BlockDiagMatrix

M = Matrix([[1, 2], [3, 4]])
D = BlockDiagMatrix(M)

print(Matrix(D))
PY
```

В `sirius-light-buggy` команда падает с ошибкой:

```text
TypeError: 'One' object is not subscriptable
```

## Сравнение с golden-веткой

Golden-ветка нужна только для ознакомления с исправленным поведением.

```bash
git switch sirius-light-golden
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Matrix, BlockDiagMatrix

M = Matrix([[1, 2], [3, 4]])
D = BlockDiagMatrix(M)

print(Matrix(D))
PY
```

В `sirius-light-golden` команда выводит:

```text
Matrix([[1, 2], [3, 4]])
```

## Автоматический тест

Команда для запуска теста, который фиксирует этот баг:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_light_bugs.py::test_issue_18618
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/matrices/expressions/blockmatrix.py
sympy/matrices/expressions/tests/test_blockmatrix.py
sirius_tests/test_light_bugs.py
```
