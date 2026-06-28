# Баг 09. Число слева от Point вызывает ошибку умножения

## ID

`sympy__sympy-17655`

## Исходный текст из dataset

````text
Unexpected exception when multiplying geometry.Point and number ```python from sympy import geometry as ge import sympy point1 = ge.Point(0,0) point2 = ge.Point(1,1) ``` This line works fine ```python point1 + point2 * sympy.sympify(2.0) ``` But when I write the same this way it raises an exception ```python point1 + sympy.sympify(2.0) * point2 ``` ``` --------------------------------------------------------------------------- TypeError Traceback (most recent call last) ~/.virtualenvs/test/lib/python3.6/site-packages/sympy/geometry/point.py in __add__(self, other) 219 try: --> 220 s, o = Point._normalize_dimension(self, Point(other, evaluate=False)) 221 except TypeError: ~/.virtualenvs/test/lib/python3.6/site-packages/sympy/geometry/point.py in __new__(cls, *args, **kwargs) 128 Expecting sequence of coordinates, not `{}`''' --> 129 .format(func_name(coords)))) 130 # A point where only...
````

## Описание бага

`Point` и `Point3D` поддерживают арифметику с числами: точку можно умножать и делить на число.

Баг проявляется, когда число стоит слева от точки. В bug-ветке `Point(1, 1) * 5` работает, но `5 * Point(1, 1)` падает с `TypeError`.

## Ожидаемое поведение

Умножение должно работать одинаково с обеих сторон. Деление точки на число тоже должно возвращать точку с изменёнными координатами.

```text
Point2D(5, 5)
Point2D(5, 5)
Point3D(1/5, 1/5, 1/5)
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-light-buggy`.

```bash
git switch sirius-light-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Point, Point3D

print(Point(1, 1) * 5)
print(5 * Point(1, 1))
print(Point3D(1, 1, 1) / 5)
PY
```

В `sirius-light-buggy` команда сначала печатает первый результат, затем падает:

```text
Point2D(5, 5)
TypeError: unsupported operand type(s) for *: 'int' and 'Point2D'
```

## Сравнение с golden-веткой

Golden-ветка нужна только для ознакомления с исправленным поведением.

```bash
git switch sirius-light-golden
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Point, Point3D

print(Point(1, 1) * 5)
print(5 * Point(1, 1))
print(Point3D(1, 1, 1) / 5)
PY
```

В `sirius-light-golden` команда выводит:

```text
Point2D(5, 5)
Point2D(5, 5)
Point3D(1/5, 1/5, 1/5)
```

## Автоматический тест

Команды для запуска тестов, которые фиксируют этот баг:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_light_bugs.py::test_point
../.venv/bin/python -m pytest -q sirius_tests/test_light_bugs.py::test_point3D
```

В начале работы над bug-веткой эти тесты должны падать. После исправления бага они должны проходить.

## Где смотреть код

```text
sympy/geometry/point.py
sympy/geometry/tests/test_point.py
sirius_tests/test_light_bugs.py
```
