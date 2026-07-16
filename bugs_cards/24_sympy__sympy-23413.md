# Баг 24. Нормальная форма Эрмита теряет нулевые строки

## ID

`sympy__sympy-23413`

## Исходный текст из dataset

````text
bug with HNF removing rows
I expect
`np.flip (hermite_normal_form (Matrix (np.flip (np.array ([[5, 8, 12], [0, 0, 1]]))).T).T))`
to give
`[[5,  8, 0], [0,  0, 1]]`
but instead I get
`[[5,  8, 0]]`
It seems to be falsely identifying my matrix as rank-deficient and removing the row when I try to achieve a row-style HNF using flips and transposes.

````

## Описание бага

- Используется вычисление нормальной формы Эрмита для обычных и доменных матриц.
- Пользователь преобразует высокую матрицу, содержащую нулевые строки.
- Результат ошибочно теряет строки и получает неверную форму.

## Ожидаемое поведение

Обе реализации нормальной формы Эрмита должны сохранить три строки исходной
матрицы и вернуть один столбец со значениями `1, 0, 0`.

```text
Matrix([[1], [0], [0]])
DM([[1], [0], [0]], ZZ)
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form
from sympy.polys.domains import ZZ
from sympy.polys.matrices import DM
from sympy.polys.matrices.normalforms import hermite_normal_form as dm_hermite_normal_form

matrix = Matrix([[2, 7], [0, 0], [0, 0]])
assert hermite_normal_form(matrix) == Matrix([[1], [0], [0]])

domain_matrix = DM([[2, 7], [0, 0], [0, 0]], ZZ)
assert dm_hermite_normal_form(domain_matrix) == DM([[1], [0], [0]], ZZ)
PY
```

В `sirius-og-buggy` одна из реализаций возвращает результат с потерянными
строками, поэтому соответствующее утверждение завершается ошибкой.

## Автоматический тест

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_23413_test_hermite_normal
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага
он должен проходить.

## Где смотреть код

```text
sympy/polys/matrices/normalforms.py
```
