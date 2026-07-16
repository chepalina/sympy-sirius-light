# Баг 12. `itermonomials` пропускает смешанные мономы

## ID

`sympy__sympy-21847`

## Исходный текст из dataset

````text
itermonomials returns incorrect monomials when using min_degrees argument
`itermonomials` returns incorrect monomials when using optional `min_degrees` argument

For example, the following code introduces three symbolic variables and generates monomials with max and min degree of 3:


```
import sympy as sp
from sympy.polys.orderings import monomial_key

x1, x2, x3 = sp.symbols('x1, x2, x3')
states = [x1, x2, x3]
max_degrees = 3
min_degrees = 3
monomials = sorted(sp.itermonomials(states, max_degrees, min_degrees=min_degrees),
                   key=monomial_key('grlex', states))
print(monomials)
```
The code returns `[x3**3, x2**3, x1**3]`, when it _should_ also return monomials such as `x1*x2**2, x2*x3**2, etc...` that also have total degree of 3. This behaviour is inconsistent with the documentation that states that

> A generator of all monomials `monom` is returned, such that either `min_degree <= total_degree(monom) <= max_degree`...

The monomials are also missing when `max_degrees` is increased above `min_degrees`.
````

## Описание бага

- Используется генератор `itermonomials` для перечисления мономов в заданном диапазоне степеней.
- Пользователь задаёт ненулевую минимальную степень и ожидает все коммутативные либо некоммутативные комбинации допустимой полной степени.
- Генератор возвращает лишь часть вариантов и пропускает смешанные произведения переменных, хотя их полная степень входит в заданный диапазон.

## Ожидаемое поведение

Для коммутативных `x, y` должны возвращаться все мономы полной степени 3 при диапазоне `3..3` и все мономы степеней 2 и 3 при диапазоне `2..3`. Для некоммутативных `i, j, k` должны присутствовать все различные слова соответствующих длин, включая разные порядки множителей.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy` и включает все сценарии теста.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import symbols
from sympy.polys.monomials import itermonomials

x, y = symbols("x y")
assert set(itermonomials([x, y], 3, 3)) == {
    x**3, x**2*y, x*y**2, y**3,
}
assert set(itermonomials([x, y], 3, 2)) == {
    x**2, x*y, y**2, x**3, x**2*y, x*y**2, y**3,
}

i, j, k = symbols("i j k", commutative=False)
assert set(itermonomials([i, j, k], 2, 2)) == {
    k*i, i**2, i*j, j*k, j*i, k**2, j**2, k*j, i*k,
}
assert set(itermonomials([i, j, k], 3, 2)) == {
    j*k**2, i*k**2, k*i*j, k*i**2, k**2, j*k*j, k*j**2,
    i*k*i, i*j, j**2*k, i**2*j, j*i*k, j**3, i**3, k*j*i,
    j*k*i, j*i, k**2*j, j*i**2, k*j, k*j*k, i*j*i, j*i*j,
    i*j**2, j**2, k*i*k, i**2, j*k, i*k, i*k*j, k**3,
    i**2*k, j**2*i, k**2*i, i*j*k, k*i,
}
PY
```

В неисправном состоянии генератор пропускает смешанные мономы допустимой полной степени; например, для диапазона `3..3` результат не совпадает с множеством `{x**3, x**2*y, x*y**2, y**3}`. Аналогично неполны сценарии диапазона `2..3` и некоммутативных переменных.

## Автоматический тест

Точный селектор теста:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_21847_test_monomials
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/polys/monomials.py
```
