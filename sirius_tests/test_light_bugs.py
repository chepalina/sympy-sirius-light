from sympy import (
    Abs,
    BlockDiagMatrix,
    Derivative,
    Matrix,
    MatrixSymbol,
    Max,
    Min,
    Point,
    Point3D,
    S,
    mathematica_code as mcode,
    oo,
    sin,
    solve_poly_system,
    symbols,
    zoo,
)
from sympy.combinatorics import Permutation
from sympy.core.expr import unchanged
from sympy.core.kind import NumberKind
from sympy.core.parameters import evaluate
from sympy.core.power import power
from sympy.matrices import MatrixKind
from sympy.testing.pytest import raises


x, y, z = symbols("x y z")


def test_issue_18618():
    A = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert A == Matrix(BlockDiagMatrix(A))


def test_Function():
    assert mcode(Max(x, y, z) * Min(y, z)) == "Max[x, y, z]*Min[y, z]"


def test_Derivative_kind():
    A = MatrixSymbol("A", 2, 2)
    assert Derivative(x, x).kind is NumberKind
    assert Derivative(A, x).kind is MatrixKind(NumberKind)


def test_issue_22684():
    with evaluate(False):
        Point(1, 2)


def test_Abs():
    assert unchanged(Abs, S("im(acos(-i + acosh(-g + i)))"))


def test_solve_poly_system():
    raises(NotImplementedError, lambda: solve_poly_system([x - 1], (x, y)))
    raises(NotImplementedError, lambda: solve_poly_system([y - 1], (x, y)))


def test_args():
    assert Permutation([[0, 1], [0, 2]]) == Permutation(0, 1, 2)


def test_Derivative():
    assert mcode(Derivative(sin(x), x)) == "Hold[D[Sin[x], x]]"
    assert mcode(Derivative(x, x)) == "Hold[D[x, x]]"
    assert mcode(Derivative(sin(x) * y**4, x, 2)) == "Hold[D[y^4*Sin[x], {x, 2}]]"
    assert mcode(Derivative(sin(x) * y**4, x, y, x)) == "Hold[D[y^4*Sin[x], x, y, x]]"
    assert mcode(Derivative(sin(x) * y**4, x, y, 3, x)) == "Hold[D[y^4*Sin[x], x, {y, 3}, x]]"


def test_point():
    p4 = Point(1, 1)
    assert p4 * 5 == Point(5, 5)
    assert p4 / 5 == Point(0.2, 0.2)
    assert 5 * p4 == Point(5, 5)


def test_point3D():
    p4 = Point3D(1, 1, 1)
    assert p4 * 5 == Point3D(5, 5, 5)
    assert p4 / 5 == Point3D(0.2, 0.2, 0.2)
    assert 5 * p4 == Point3D(5, 5, 5)


def test_zero():
    assert 0 ** -oo is zoo
    assert power(0, -oo) is zoo
