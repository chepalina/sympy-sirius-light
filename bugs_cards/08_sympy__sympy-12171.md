# Баг 08. Mathematica printer не печатает Derivative

## ID

`sympy__sympy-12171`

## Исходный текст из dataset

````text
matematica code printer does not handle floats and derivatives correctly In its current state the mathematica code printer does not handle Derivative(func(vars), deriver) e.g. Derivative(f(t), t) yields Derivative(f(t), t) instead of D[f[t],t] Also floats with exponents are not handled correctly e.g. 1.0e-4 is not converted to 1.0*^-4 This has an easy fix by adding the following lines to MCodePrinter: def _print_Derivative(self, expr): return "D[%s]" % (self.stringify(expr.args, ", ")) def _print_Float(self, expr): res =str(expr) return res.replace('e','*^')
````

## Описание бага

`mathematica_code` должен переводить SymPy-выражения в синтаксис Wolfram Mathematica.

Баг проявляется на производных: `Derivative(...)` не превращается в Mathematica-форму `D[...]`, а printer падает с ошибкой неподдержанного метода.

## Ожидаемое поведение

Производные должны печататься через `Hold[D[...]]`.

```text
Hold[D[Sin[x], x]]
Hold[D[y^4*Sin[x], {x, 2}]]
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-light-buggy`.

```bash
git switch sirius-light-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Derivative, mathematica_code as mcode, sin, symbols

x, y = symbols("x y")
print(mcode(Derivative(sin(x), x)))
print(mcode(Derivative(sin(x) * y**4, x, 2)))
PY
```

В `sirius-light-buggy` команда падает с ошибкой:

```text
PrintMethodNotImplementedError: Unsupported by <class 'sympy.printing.mathematica.MCodePrinter'>: <class 'sympy.core.function.Derivative'>
```

## Сравнение с golden-веткой

Golden-ветка нужна только для ознакомления с исправленным поведением.

```bash
git switch sirius-light-golden
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Derivative, mathematica_code as mcode, sin, symbols

x, y = symbols("x y")
print(mcode(Derivative(sin(x), x)))
print(mcode(Derivative(sin(x) * y**4, x, 2)))
PY
```

В `sirius-light-golden` команда выводит:

```text
Hold[D[Sin[x], x]]
Hold[D[y^4*Sin[x], {x, 2}]]
```

## Автоматический тест

Команда для запуска теста, который фиксирует этот баг:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_light_bugs.py::test_Derivative
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/printing/mathematica.py
sympy/printing/tests/test_mathematica.py
sirius_tests/test_light_bugs.py
```
