# Баг 07. Permutation не принимает пересекающиеся циклы

## ID

`sympy__sympy-12481`

## Исходный текст из dataset

````text
`Permutation` constructor fails with non-disjoint cycles Calling `Permutation([[0,1],[0,1]])` raises a `ValueError` instead of constructing the identity permutation. If the cycles passed in are non-disjoint, they should be applied in left-to-right order and the resulting permutation should be returned. This should be easy to compute. I don't see a reason why non-disjoint cycles should be forbidden.
````

## Описание бага

`Permutation` строит перестановку по циклам. Циклы могут пересекаться, если их последовательно применить слева направо.

Баг проявляется на списке циклов `[[0, 1], [0, 2]]`: bug-ветка считает повторяющийся элемент ошибкой и не строит перестановку.

## Ожидаемое поведение

Пересекающиеся циклы должны применяться последовательно и давать итоговую перестановку.

```text
(0 1 2)
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-light-buggy`.

```bash
git switch sirius-light-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy.combinatorics import Permutation

print(Permutation([[0, 1], [0, 2]]))
PY
```

В `sirius-light-buggy` команда падает с ошибкой:

```text
ValueError: there were repeated elements; to resolve cycles use Cycle(0, 1)(0, 2).
```

## Сравнение с golden-веткой

Golden-ветка нужна только для ознакомления с исправленным поведением.

```bash
git switch sirius-light-golden
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy.combinatorics import Permutation

print(Permutation([[0, 1], [0, 2]]))
PY
```

В `sirius-light-golden` команда выводит:

```text
(0 1 2)
```

## Автоматический тест

Команда для запуска теста, который фиксирует этот баг:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_light_bugs.py::test_args
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/combinatorics/permutations.py
sympy/combinatorics/tests/test_permutations.py
sirius_tests/test_light_bugs.py
```
