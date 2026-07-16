# Баг 19. Неверный размер при объединении пустых разреженных матриц

## ID

`sympy__sympy-13031`

## Исходный текст из dataset

````text
Behavior of Matrix hstack and vstack changed in sympy 1.1
In sympy 1.0:
```
import sympy as sy
M1 = sy.Matrix.zeros(0, 0)
M2 = sy.Matrix.zeros(0, 1)
M3 = sy.Matrix.zeros(0, 2)
M4 = sy.Matrix.zeros(0, 3)
sy.Matrix.hstack(M1, M2, M3, M4).shape
```
returns
`(0, 6)`

Now, same in sympy 1.1:
```
import sympy as sy
M1 = sy.Matrix.zeros(0, 0)
M2 = sy.Matrix.zeros(0, 1)
M3 = sy.Matrix.zeros(0, 2)
M4 = sy.Matrix.zeros(0, 3)
sy.Matrix.hstack(M1, M2, M3, M4).shape
```
returns
`(0, 3)
`
whereas:
```
import sympy as sy
M1 = sy.Matrix.zeros(1, 0)
M2 = sy.Matrix.zeros(1, 1)
M3 = sy.Matrix.zeros(1, 2)
M4 = sy.Matrix.zeros(1, 3)
sy.Matrix.hstack(M1, M2, M3, M4).shape
```
returns
`(1, 6)
`

````

## Описание бага

- Используется объединение разреженных матриц через `SparseMatrix.hstack` и `SparseMatrix.vstack`.
- Пользователь складывает размеры матриц, у которых одна из осей имеет нулевую длину.
- SymPy теряет часть нулевых строк или столбцов и возвращает матрицу неверного размера.

## Ожидаемое поведение

Горизонтальное объединение матриц размеров `0×0`, `0×1`, `0×2` и `0×3`
должно давать матрицу размера `0×6`. Вертикальное объединение матриц размеров
`0×0`, `1×0`, `2×0` и `3×0` должно давать матрицу размера `6×0`.

```text
Matrix(0, 6, [])
Matrix(6, 0, [])
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Matrix, SparseMatrix

horizontal = [SparseMatrix.zeros(0, n) for n in range(4)]
vertical = [SparseMatrix.zeros(n, 0) for n in range(4)]
assert SparseMatrix.hstack(*horizontal) == Matrix(0, 6, [])
assert SparseMatrix.vstack(*vertical) == Matrix(6, 0, [])
PY
```

В `sirius-og-buggy` одна из проверок завершается ошибкой: результат объединения
не сохраняет ожидаемую сумму размеров по ненулевой оси.

## Автоматический тест

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_13031_test_sparse_matrix
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага
он должен проходить.

## Где смотреть код

```text
sympy/matrices/sparse.py
```
