# Баг 52. `nthroot_mod` пропускает нулевой корень

## ID

`sympy__sympy-18199`

## Исходный текст из dataset

````text
nthroot_mod function misses one root of x = 0 mod p.
When in the equation x**n = a mod p , when a % p == 0. Then x = 0 mod p is also a root of this equation. But right now `nthroot_mod` does not check for this condition. `nthroot_mod(17*17, 5 , 17)` has a root `0 mod 17`. But it does not return it.
````

## Описание бага

- Решается сравнение `x**n = a mod p`.
- Число `a` делится на модуль `p` без остатка.
- Функция не возвращает очевидный корень `x = 0`.

## Ожидаемое поведение

Вызов `nthroot_mod(17*17, 5, 17)` должен вернуть корень `0`.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy.ntheory.residue_ntheory import nthroot_mod

assert nthroot_mod(17*17, 5, 17) == 0
PY
```

В `sirius-og-buggy` нулевой корень не возвращается.

## Автоматический тест

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_18199_test_solve_modular
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага
он должен проходить.

## Где смотреть код

Связанные тесты из dataset:

```text
sympy/ntheory/tests/test_residue.py
sympy/solvers/tests/test_solveset.py
```
