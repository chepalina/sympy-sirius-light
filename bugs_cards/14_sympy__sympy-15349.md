# Баг 14. Кватернион даёт неверную матрицу поворота

## ID

`sympy__sympy-15349`

## Исходный текст из dataset

````text
Incorrect result with Quaterniont.to_rotation_matrix()
https://github.com/sympy/sympy/blob/ab14b02dba5a7e3e4fb1e807fc8a954f1047a1a1/sympy/algebras/quaternion.py#L489

There appears to be an error in the `Quaternion.to_rotation_matrix()` output.  The simplest example I created to illustrate the problem is as follows:

```
>>import sympy
>>print('Sympy version: ', sympy.__version__)
Sympy version: 1.2

>> from sympy import *
>> x = symbols('x')
>> q = Quaternion(cos(x/2), sin(x/2), 0, 0)
>> trigsimp(q.to_rotation_matrix())
Matrix([
[1,      0,      0],
[0, cos(x), sin(x)],
[0, sin(x), cos(x)]])
```
One of the `sin(x)` functions should be negative.  What was the reference of the original equations?
````

## Описание бага

- Используется `Quaternion.to_rotation_matrix()` из алгебраического модуля SymPy.
- Пользователь преобразует кватернион в матрицу поворота, при необходимости относительно заданной точки.
- Полученные коэффициенты матрицы имеют неверные знаки или позиции, поэтому матрица не описывает тот же поворот, что исходный кватернион.

## Ожидаемое поведение

Для `Quaternion(1, 2, 3, 4)` должна получаться точная матрица поворота из теста. При передаче точки `(1, 1, 1)` должна возвращаться соответствующая однородная матрица `4x4` с корректным столбцом переноса.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy` и проверяет оба сценария преобразования.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Matrix, Quaternion, Rational, S

quaternion = Quaternion(1, 2, 3, 4)
assert quaternion.to_rotation_matrix() == Matrix([
    [Rational(-2, 3), Rational(2, 15), Rational(11, 15)],
    [Rational(2, 3), Rational(-1, 3), Rational(2, 3)],
    [Rational(1, 3), Rational(14, 15), Rational(2, 15)],
])
assert quaternion.to_rotation_matrix((1, 1, 1)) == Matrix([
    [Rational(-2, 3), Rational(2, 15), Rational(11, 15), Rational(4, 5)],
    [Rational(2, 3), Rational(-1, 3), Rational(2, 3), S.Zero],
    [Rational(1, 3), Rational(14, 15), Rational(2, 15), Rational(-2, 5)],
    [S.Zero, S.Zero, S.Zero, S.One],
])
PY
```

В неисправном состоянии хотя бы одна из матриц отличается от ожидаемой: знаки или расположение коэффициентов поворота неверны, а для варианта с точкой также нарушается однородное преобразование.

## Автоматический тест

Точный селектор теста:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_15349_test_quaternion_conversions
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/algebras/quaternion.py
```
