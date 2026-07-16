# Баг 02. `symbols` игнорирует `cls=Function` во вложенной группе

## ID

`sympy__sympy-23534`

## Исходный текст из dataset

````text
Using symbols to create functions doesn't work if there is an extra layer of parentheses
Sympy version == 1.10.1

Using `symbols` to create symbol-like objects like instances of `Function` as shown in the [documentation](https://docs.sympy.org/latest/modules/core.html?highlight=symbols#symbols) creates objects of class `Symbol` instead of `Function` if there is an extra layer of parentheses.

The extra layer of parentheses are necessary to deconstruct the output as separate tuples.

Running the code:
```
q, u = smp.symbols(('q:2', 'u:2'), cls=smp.Function)
print(type(q[0]))
```
#### Expected result:
<class 'sympy.core.function.UndefinedFunction'>

#### Actual result:
<class 'sympy.core.symbol.Symbol'>
````

## Описание бага

- Используется фабрика `symbols` из ядра SymPy с параметром `cls=Function`.
- Пользователь передаёт сгруппированные диапазоны имён, чтобы получить отдельные кортежи неопределённых функций.
- При дополнительном уровне группировки параметр класса теряется, и вместо функций создаются обычные объекты `Symbol`.

## Ожидаемое поведение

Все элементы результата, включая элементы вложенных групп, должны иметь запрошенный класс. В частности, первый элемент первой группы должен быть `UndefinedFunction`.

```text
type(functions[0][0]) is UndefinedFunction
```

## Ручное воспроизведение в bug-ветке

Команда работает в ветке `sirius-og-buggy`.

```bash
git switch sirius-og-buggy
./scripts/setup_sirius.sh

../.venv/bin/python - <<'PY'
from sympy import Function, symbols
from sympy.core.function import UndefinedFunction

functions = symbols(("q:2", "u:2"), cls=Function)
assert type(functions[0][0]) is UndefinedFunction
PY
```

В `sirius-og-buggy` `functions[0][0]` имеет тип `Symbol`, поэтому проверка ожидаемого класса завершается `AssertionError`.

## Автоматический тест

Точный селектор теста:

```bash
../.venv/bin/python -m pytest -q sirius_tests/test_sympy_og_bugs.py::test_og_23534_test_symbols
```

В начале работы над bug-веткой этот тест должен падать. После исправления бага он должен проходить.

## Где смотреть код

```text
sympy/core/symbol.py
```
