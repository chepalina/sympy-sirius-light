# Баг 03. У Derivative неверный kind для чисел и матриц

## ID

`sympy__sympy-21614`

## Исходный текст из dataset

````text
Wrong Derivative kind attribute I'm playing around with the `kind` attribute. The following is correct: ``` from sympy import Integral, Derivative from sympy import MatrixSymbol from sympy.abc import x A = MatrixSymbol('A', 2, 2) i = Integral(A, x) i.kind # MatrixKind(NumberKind) ``` This one is wrong: ``` d = Derivative(A, x) d.kind # UndefinedKind ```
````

## Описание бага

В SymPy у выражений есть атрибут `kind`, который описывает тип математического объекта: число, матрица и так далее.

Баг проявляется у `Derivative`: производная от числового выражения и производная от матричного выражения получают `UndefinedKind`, хотя SymPy должен сохранять информацию о типе результата.

## Ожидаемое поведение

Производная от обычного символа должна иметь `NumberKind`, а производная от `MatrixSymbol` должна иметь `MatrixKind(NumberKind)`.

```text
NumberKind
MatrixKind(NumberKind)
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-light-buggy`.

```bash
git switch sirius-light-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Derivative, MatrixSymbol, symbols

x = symbols("x")
A = MatrixSymbol("A", 2, 2)

print(Derivative(x, x).kind)
print(Derivative(A, x).kind)
PY
```

В `sirius-light-buggy` команда выводит:

```text
UndefinedKind
UndefinedKind
```

## Сравнение с golden-веткой

Golden-ветка нужна только для ознакомления с исправленным поведением.

```bash
git switch sirius-light-golden
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Derivative, MatrixSymbol, symbols

x = symbols("x")
A = MatrixSymbol("A", 2, 2)

print(Derivative(x, x).kind)
print(Derivative(A, x).kind)
PY
```

В `sirius-light-golden` команда выводит:

```text
NumberKind
MatrixKind(NumberKind)
```

## Автоматический тест

Команда для запуска теста, который фиксирует этот баг:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_light_bugs.py::test_Derivative_kind
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/core/function.py
sympy/core/tests/test_kind.py
sirius_tests/test_light_bugs.py
```
