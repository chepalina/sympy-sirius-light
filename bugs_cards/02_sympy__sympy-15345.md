# Баг 02. mathematica_code неправильно печатает Max и Min

## ID

`sympy__sympy-15345`

## Исходный текст из dataset

````text
mathematica_code gives wrong output with Max If I run the code ``` x = symbols('x') mathematica_code(Max(x,2)) ``` then I would expect the output `'Max[x,2]'` which is valid Mathematica code but instead I get `'Max(2, x)'` which is not valid Mathematica code.
````

## Описание бага

SymPy умеет печатать выражения в синтаксисе Wolfram Mathematica через `mathematica_code`.

Баг проявляется на функциях `Max` и `Min`: printer не умеет корректно превращать их в Mathematica-формат. В bug-ветке выражение с `Max` и `Min` не печатается как валидный Mathematica-код.

## Ожидаемое поведение

`Max` и `Min` должны печататься в квадратных скобках, как это принято в Mathematica.

```text
Max[x, y, z]*Min[y, z]
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-light-buggy`.

```bash
git switch sirius-light-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Max, Min, mathematica_code as mcode, symbols

x, y, z = symbols("x y z")
print(mcode(Max(x, y, z) * Min(y, z)))
PY
```

В `sirius-light-buggy` команда падает с ошибкой:

```text
PrintMethodNotImplementedError: Unsupported by <class 'sympy.printing.mathematica.MCodePrinter'>: Max
```

## Сравнение с golden-веткой

Golden-ветка нужна только для ознакомления с исправленным поведением.

```bash
git switch sirius-light-golden
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Max, Min, mathematica_code as mcode, symbols

x, y, z = symbols("x y z")
print(mcode(Max(x, y, z) * Min(y, z)))
PY
```

В `sirius-light-golden` команда выводит:

```text
Max[x, y, z]*Min[y, z]
```

## Автоматический тест

Команда для запуска теста, который фиксирует этот баг:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_light_bugs.py::test_Function
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/printing/mathematica.py
sympy/printing/tests/test_mathematica.py
sirius_tests/test_light_bugs.py
```
