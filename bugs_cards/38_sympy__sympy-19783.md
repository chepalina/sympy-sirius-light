# Баг 38. Сопряжённый оператор не упрощается с единичным оператором

## ID

`sympy__sympy-19783`

## Исходный текст из dataset

````text
Dagger() * IdentityOperator() is not simplified
As discussed on the mailing list the following does not work.
```
from sympy.physics.quantum.dagger import Dagger
from sympy.physics.quantum.operator import Operator
from sympy.physics.quantum import IdentityOperator
A = Operators('A')
Identity = IdentityOperator()
A * Identity #This gives A, correctly
B = Dagger(A)
B * Identity #This returns A^\dagger I
```
````

## Описание бага

- Используются `Dagger` и `IdentityOperator` из квантового модуля.
- Обычный оператор корректно упрощается при умножении на единичный.
- Для сопряжённого оператора единичный множитель остаётся в выражении.

## Ожидаемое поведение

Единичный оператор должен исчезать с обеих сторон сопряжённого оператора: `IdentityOperator()*Dagger(O) == Dagger(O)` и `Dagger(O)*IdentityOperator() == Dagger(O)`.

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy.physics.quantum.dagger import Dagger
from sympy.physics.quantum.operator import IdentityOperator, Operator
from sympy.testing.pytest import warns_deprecated_sympy

operator = Operator("O")
with warns_deprecated_sympy():
    identity = IdentityOperator()
    assert identity*Dagger(operator) == Dagger(operator)
    assert Dagger(operator)*identity == Dagger(operator)
PY
```

В `sirius-og-buggy` единичный множитель остаётся в произведении.

## Автоматический тест

Точные селекторы всех тестов этого бага:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_19783_test_dagger_mul
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_19783_test_identity
```

В начале работы над bug-веткой эти тесты должны падать. После исправления бага они должны проходить.

## Где смотреть код

Связанные тесты из dataset:

```text
sympy/physics/quantum/tests/test_dagger.py
sympy/physics/quantum/tests/test_operator.py
```
