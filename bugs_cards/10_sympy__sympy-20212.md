# Баг 10. 0**-oo возвращает 0 вместо zoo

## ID

`sympy__sympy-20212`

## Исходный текст из dataset

````text
0**-oo produces 0, the documentation says it should produce zoo Using SymPy 1.5.1, evaluate `0**-oo` produces `0`. The documentation for the Pow class states that it should return `ComplexInfinity`, aka `zoo` | expr | value | reason | | :-- | :-- | :--| | `0**-oo` | `zoo` | This is not strictly true, as 0**oo may be oscillating between positive and negative values or rotating in the complex plane. It is convenient, however, when the base is positive.|
````

## Описание бага

В SymPy `oo` обозначает бесконечность, а `zoo` обозначает комплексную бесконечность.

Баг проявляется при вычислении `0 ** -oo`: bug-ветка возвращает `0`, хотя по ожидаемому поведению результатом должна быть комплексная бесконечность `zoo`.

## Ожидаемое поведение

И оператор `**`, и функция `power` должны возвращать `zoo`.

```text
zoo
zoo
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-light-buggy`.

```bash
git switch sirius-light-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import oo
from sympy.core.power import power

print(0 ** -oo)
print(power(0, -oo))
PY
```

В `sirius-light-buggy` команда выводит:

```text
0
0
```

## Сравнение с golden-веткой

Golden-ветка нужна только для ознакомления с исправленным поведением.

```bash
git switch sirius-light-golden
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import oo
from sympy.core.power import power

print(0 ** -oo)
print(power(0, -oo))
PY
```

В `sirius-light-golden` команда выводит:

```text
zoo
zoo
```

## Автоматический тест

Команда для запуска теста, который фиксирует этот баг:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_light_bugs.py::test_zero
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/core/power.py
sympy/core/tests/test_power.py
sirius_tests/test_light_bugs.py
```
