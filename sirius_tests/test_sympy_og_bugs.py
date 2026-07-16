"""Focused golden checks for the official SymPy OG bug tickets."""


def test_og_14711_test_Vector():
    from sympy.physics.vector import ReferenceFrame

    frame = ReferenceFrame("A")
    assert frame.x + 0 == frame.x


def test_og_23534_test_symbols():
    from sympy import Function, symbols
    from sympy.core.function import UndefinedFunction

    functions = symbols(("q:2", "u:2"), cls=Function)
    assert type(functions[0][0]) is UndefinedFunction


def test_og_23824_test_kahane_simplify1():
    from sympy.physics.hep.gamma_matrices import (
        GammaMatrix,
        LorentzIndex,
        kahane_simplify,
    )
    from sympy.tensor.tensor import tensor_indices

    mu, rho, sigma = tensor_indices("mu rho sigma", LorentzIndex)
    left_contraction = GammaMatrix(mu)*GammaMatrix(-mu)*GammaMatrix(rho)*GammaMatrix(sigma)
    right_contraction = GammaMatrix(rho)*GammaMatrix(sigma)*GammaMatrix(mu)*GammaMatrix(-mu)
    expected = 4*GammaMatrix(rho)*GammaMatrix(sigma)
    assert kahane_simplify(left_contraction).equals(expected)
    assert kahane_simplify(right_contraction).equals(expected)


def test_og_23950_test_as_set():
    from sympy import Contains, FiniteSet, S, Symbol

    x = Symbol("x")
    y = Symbol("y")
    assert Contains(x, FiniteSet(y)).as_set() == FiniteSet(y)
    assert Contains(x, S.Integers).as_set() == S.Integers
    assert Contains(x, S.Reals).as_set() == S.Reals


def test_og_16766_test_PythonCodePrinter():
    from sympy.printing.pycode import PythonCodePrinter
    from sympy.tensor import IndexedBase

    indexed = IndexedBase("p")
    assert PythonCodePrinter().doprint(indexed[0, 1]) == "p[0, 1]"


def test_og_15017_test_ndim_array_initiation():
    from sympy import ImmutableDenseNDimArray, Symbol

    empty = ImmutableDenseNDimArray([], shape=(0,))
    assert len(empty) == 0
    assert empty.ndim == 1

    x = Symbol("x")
    scalar = ImmutableDenseNDimArray(x)
    assert len(scalar) == 1
    assert scalar.shape == ()
    assert scalar.ndim == 0
    assert scalar[()] == x


def test_og_15809_test_Min():
    from sympy import Min, S, Symbol

    x = Symbol("x")
    assert Min() == S.Infinity
    assert Min(x) == x


def test_og_15809_test_Max():
    from sympy import Max, S, Symbol

    x = Symbol("x")
    assert Max() == S.NegativeInfinity
    assert Max(x) == x


def test_og_13551_test_issue_13546():
    from sympy import Product, S, Symbol

    n = Symbol("n")
    k = Symbol("k")
    product = Product(n + 1/2**k, (k, 0, n - 1)).doit()
    assert product.subs(n, 2).doit() == S(15)/2


def test_og_13480_test_coth():
    from sympy import I, coth, log, pi, tan, tanh

    assert coth(log(tan(2))) == coth(log(-tan(2)))
    assert coth(1 + I*pi/2) == tanh(1)


def test_og_16886_test_encode_morse():
    from sympy.crypto.crypto import encode_morse

    assert encode_morse("12345") == ".----|..---|...--|....-|....."
    assert encode_morse("67890") == "-....|--...|---..|----.|-----"


def test_og_20590_test_immutable():
    from sympy import Basic
    from sympy.testing.pytest import raises

    value = Basic()
    assert not hasattr(value, "__dict__")
    with raises(AttributeError):
        value.x = 1


def test_og_21847_test_monomials():
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


def test_og_19637_test_kernS():
    from sympy import Symbol
    from sympy.core.sympify import kernS

    x = Symbol("x")
    assert kernS("(2*x)/(x-1)") == 2*x/(x - 1)


def test_og_15349_test_quaternion_conversions():
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


def test_og_16450_test_posify():
    from sympy import Symbol, posify

    original = Symbol("k", finite=True)
    positive, replacements = posify(original)
    assert positive.is_positive is True
    assert positive.is_finite is True
    assert positive.subs(replacements) == original


def test_og_13372_test_evalf_bugs():
    from sympy import Max, Mul, Symbol, sympify
    from sympy.printing.str import sstr

    x = Symbol("x")
    y = Symbol("y")
    expression = Mul(Max(0, y), x, evaluate=False).evalf()
    assert sstr(sympify(expression), full_prec=True) == "x*Max(0, y)"


def test_og_18189_test_diophantine():
    from sympy import symbols
    from sympy.solvers.diophantine.diophantine import diophantine

    x, y = symbols("x y", integer=True)
    expected = {
        (-3, -2), (-3, 2), (-2, -3), (-2, 3),
        (2, -3), (2, 3), (3, -2), (3, 2),
    }
    equation = y**4 + x**4 - 2**4 - 3**4
    assert diophantine(equation, syms=(x, y), permute=True) == expected
    assert diophantine(equation, syms=(y, x), permute=True) == expected


def test_og_20916_test_super_sub():
    from sympy.printing.conventions import split_super_sub

    expected = {
        "w1": ("w", [], ["1"]),
        "w𝟙": ("w", [], ["𝟙"]),
        "w11": ("w", [], ["11"]),
        "w𝟙𝟙": ("w", [], ["𝟙𝟙"]),
        "w𝟙2𝟙": ("w", [], ["𝟙2𝟙"]),
        "w1^a": ("w", ["a"], ["1"]),
        "ω1": ("ω", [], ["1"]),
        "ω11": ("ω", [], ["11"]),
        "ω1^a": ("ω", ["a"], ["1"]),
        "ω𝟙^α": ("ω", ["α"], ["𝟙"]),
        "ω𝟙2^3α": ("ω", ["3α"], ["𝟙2"]),
    }
    for name, parts in expected.items():
        assert split_super_sub(name) == parts


def test_og_13031_test_sparse_matrix():
    from sympy import Matrix, SparseMatrix

    horizontal = [SparseMatrix.zeros(0, n) for n in range(4)]
    vertical = [SparseMatrix.zeros(n, 0) for n in range(4)]
    assert SparseMatrix.hstack(*horizontal) == Matrix(0, 6, [])
    assert SparseMatrix.vstack(*vertical) == Matrix(6, 0, [])


def test_og_24213_test_issue_24211():
    from sympy.physics.units import (
        Quantity,
        acceleration,
        meter,
        second,
        time,
        velocity,
    )
    from sympy.physics.units.systems.si import SI

    velocity_quantity = Quantity("V1")
    SI.set_quantity_dimension(velocity_quantity, velocity)
    SI.set_quantity_scale_factor(velocity_quantity, meter/second)
    acceleration_quantity = Quantity("A1")
    SI.set_quantity_dimension(acceleration_quantity, acceleration)
    SI.set_quantity_scale_factor(acceleration_quantity, meter/second**2)
    time_quantity = Quantity("T1")
    SI.set_quantity_dimension(time_quantity, time)
    SI.set_quantity_scale_factor(time_quantity, second)

    factor, dimension = SI._collect_factor_and_dimension(
        acceleration_quantity*time_quantity + velocity_quantity
    )
    assert factor == 2
    assert SI.get_dimension_system().equivalent_dims(dimension, velocity)


def test_og_22456_test_String():
    from sympy.codegen.ast import String

    value = String("foobar")
    assert value.func(*value.args) == value


def test_og_12419_test_Identity():
    from sympy import Identity, Sum, symbols

    i, j, n = symbols("i j n")
    identity = Identity(n)
    assert identity[i, j] != 0
    assert Sum(identity[i, j], (i, 0, n - 1), (j, 0, n - 1)).subs(n, 3).doit() == 3
    assert Sum(Sum(identity[i, j], (i, 0, n - 1)), (j, 0, n - 1)).subs(n, 3).doit() == 3


def test_og_23262_test_issue_14941():
    from sympy.utilities.lambdify import lambdify

    function = lambdify([], (1,))
    assert function() == (1,)


def test_og_23413_test_hermite_normal():
    from sympy import Matrix
    from sympy.matrices.normalforms import hermite_normal_form
    from sympy.polys.domains import ZZ
    from sympy.polys.matrices import DM
    from sympy.polys.matrices.normalforms import hermite_normal_form as dm_hermite_normal_form

    matrix = Matrix([[2, 7], [0, 0], [0, 0]])
    assert hermite_normal_form(matrix) == Matrix([[1], [0], [0]])

    domain_matrix = DM([[2, 7], [0, 0], [0, 0]], ZZ)
    assert dm_hermite_normal_form(domain_matrix) == DM([[1], [0], [0]], ZZ)


def test_og_17318_test_issue_12420():
    from sympy import I, sqrt, sqrtdenest

    assert sqrtdenest((3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2) == I
    expression = 3 - sqrt(2)*sqrt(4 + I) + 3*I
    assert sqrtdenest(expression) == expression


def test_og_13647_test_col_insert():
    from sympy import Matrix
    from sympy.matrices.common import _CastableMatrix, _MinimalMatrix, MatrixShaping
    from sympy.testing.pytest import warns_deprecated_sympy

    with warns_deprecated_sympy():
        class ShapingOnlyMatrix(_MinimalMatrix, _CastableMatrix, MatrixShaping):
            pass

    inserted = Matrix([[2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2]])
    identity = ShapingOnlyMatrix(6, 6, lambda i, j: int(i == j))
    assert identity.col_insert(3, inserted) == Matrix([
        [1, 0, 0, 2, 2, 0, 0, 0],
        [0, 1, 0, 2, 2, 0, 0, 0],
        [0, 0, 1, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 1, 0, 0],
        [0, 0, 0, 2, 2, 0, 1, 0],
        [0, 0, 0, 2, 2, 0, 0, 1],
    ])


def test_og_15875_test_Add_is_zero():
    from sympy import I

    expression = -2*I + (1 + I)**2
    assert expression.is_zero is None


def test_og_18211_test_issue_18188():
    from sympy import ConditionSet, Eq, S, Symbol, cos, sin, sqrt

    x = Symbol("x", real=True)
    first = Eq(x*cos(x) - 3*sin(x), 0)
    assert first.as_set() == ConditionSet(x, first, S.Reals)

    second = Eq(x**2 + sqrt(2*x) + sin(x), 0)
    expected = ConditionSet(x, Eq(sqrt(2)*sqrt(x) + x**2 + sin(x), 0), S.Reals)
    assert second.as_set() == expected


def test_og_19954_test_sylow_subgroup():
    from sympy.combinatorics.named_groups import DihedralGroup

    assert DihedralGroup(18).sylow_subgroup(p=2).order() == 4
    assert DihedralGroup(50).sylow_subgroup(p=2).order() == 4


def test_og_21612_test_Mul():
    from sympy import Mul, Pow, symbols

    x, y = symbols("x y")
    expression = Mul(x, Pow(1/y, -1, evaluate=False), evaluate=False)
    assert str(expression) == "x/(1/y)"


def test_og_24539_test_PolyElement_as_expr():
    from sympy import symbols
    from sympy.polys.domains import ZZ
    from sympy.polys.rings import ring

    _, x, y, z = ring("x,y,z", ZZ)
    polynomial = 3*x**2*y - x*y*z + 7*z**3 + 1
    u, v, w = symbols("u v w")
    expected = 3*u**2*v - u*v*w + 7*w**3 + 1
    assert polynomial.as_expr(u, v, w) == expected


def test_og_17139_test__TR56():
    from sympy import I, cos, sin, symbols
    from sympy.simplify.fu import _TR56

    x = symbols("x")
    replacement = lambda value: 1 - value
    assert _TR56(sin(x)**I, sin, cos, replacement, 4, True) == sin(x)**I
    assert _TR56(sin(x)**(2*I + 1), sin, cos, replacement, 4, True) == sin(x)**(2*I + 1)


def test_og_17139_test_issue_17137():
    from sympy import I, cos, simplify, symbols

    x = symbols("x")
    assert simplify(cos(x)**I) == cos(x)**I
    assert simplify(cos(x)**(2 + 3*I)) == cos(x)**(2 + 3*I)


def test_og_19495_test_subs_CondSet():
    from sympy import (
        ConditionSet,
        Contains,
        ImageSet,
        Interval,
        Lambda,
        S,
        Symbol,
        asin,
        oo,
        pi,
    )

    n = Symbol("n", negative=True)
    x = Symbol("x")
    y = Symbol("y")
    positive = Symbol("p", positive=True)
    assert ConditionSet(n, n < x, Interval(-oo, 0)).subs(x, positive) == Interval(-oo, 0)

    k = Symbol("k")
    symbolic_image = ImageSet(Lambda(k, 2*k*pi + asin(y)), S.Integers)
    expected_image = ImageSet(Lambda(k, 2*k*pi + asin(S.One/3)), S.Integers)
    result = ConditionSet(
        x,
        Contains(y, Interval(-1, 1)),
        symbolic_image,
    ).subs(y, S.One/3)
    assert result.dummy_eq(expected_image)


def test_og_13615_test_Complement():
    from sympy import Complement, FiniteSet, Interval, symbols

    x, y = symbols("x y")
    assert Complement(FiniteSet(x, y, 2), Interval(-10, 10)) == Complement(
        FiniteSet(x, y), Interval(-10, 10)
    )


def test_og_20801_test_zero_not_false():
    from sympy import S

    assert (S(0.0) == S.false) is False
    assert (S.false == S(0.0)) is False
    assert (S(0) == S.false) is False
    assert (S.false == S(0)) is False


def test_og_19346_test_dict():
    from sympy import srepr
    from sympy.abc import x, y, z

    assert srepr({}) == "{}"
    assert srepr({x: y}) == "{Symbol('x'): Symbol('y')}"
    assert srepr({x: y, y: z}) in (
        "{Symbol('x'): Symbol('y'), Symbol('y'): Symbol('z')}",
        "{Symbol('y'): Symbol('z'), Symbol('x'): Symbol('y')}",
    )
    assert srepr({x: {y: z}}) == "{Symbol('x'): {Symbol('y'): Symbol('z')}}"


def test_og_24661_test_issue_24288():
    from sympy import Eq, Ge, Gt, Le, Lt, Ne
    from sympy.parsing.sympy_parser import parse_expr

    expected = {
        "1 < 2": Lt(1, 2, evaluate=False),
        "1 <= 2": Le(1, 2, evaluate=False),
        "1 > 2": Gt(1, 2, evaluate=False),
        "1 >= 2": Ge(1, 2, evaluate=False),
        "1 != 2": Ne(1, 2, evaluate=False),
        "1 == 2": Eq(1, 2, evaluate=False),
    }
    for text, result in expected.items():
        assert parse_expr(text, evaluate=False) == result


def test_og_19783_test_dagger_mul():
    from sympy import Mul
    from sympy.physics.quantum.dagger import Dagger
    from sympy.physics.quantum.operator import IdentityOperator, Operator
    from sympy.testing.pytest import warns_deprecated_sympy

    operator = Operator("O")
    with warns_deprecated_sympy():
        identity = IdentityOperator()
        assert Dagger(operator)*operator*identity == Mul(Dagger(operator), operator)*identity
        assert Dagger(operator)*Dagger(identity) == Dagger(operator)
    assert Dagger(operator)*Dagger(operator) == Dagger(operator)**2


def test_og_19783_test_identity():
    from sympy.physics.quantum.dagger import Dagger
    from sympy.physics.quantum.operator import IdentityOperator, Operator
    from sympy.testing.pytest import warns_deprecated_sympy

    with warns_deprecated_sympy():
        identity = IdentityOperator()
        operator = Operator("O")
        assert identity*Dagger(operator) == Dagger(operator)
        assert Dagger(operator)*identity == Dagger(operator)


def test_og_16792_test_ccode_unused_array_arg():
    from sympy import MatrixSymbol
    from sympy.utilities.codegen import CCodeGen, codegen

    x = MatrixSymbol("x", 2, 1)
    generated = codegen(
        ("test", 1.0),
        code_gen=CCodeGen(),
        header=False,
        empty=False,
        argument_sequence=(x,),
    )
    assert generated[0][1] == (
        '#include "test.h"\n'
        '#include <math.h>\n'
        'double test(double *x) {\n'
        '   double test_result;\n'
        '   test_result = 1.0;\n'
        '   return test_result;\n'
        '}\n'
    )


def test_og_19040_test_issue_5786():
    from sympy import I, expand, factor, symbols

    t, x, y, z = symbols("t x y z")
    expression = expand(factor(expand((x - I*y)*(z - I*t)), extension=[I]))
    assert expression == -I*t*x - t*y + x*z - I*y*z


def test_og_21379_test_Mod():
    from sympy import Mod, Piecewise, exp, sinh, symbols

    x, y = symbols("x y", real=True)
    z = symbols("z")
    piecewise = Piecewise((x, y > x), (y, True))
    modulo = (piecewise/z) % 1
    assert modulo == Mod(piecewise/z, 1)
    expression = exp(sinh(piecewise/z))
    assert expression.subs({1: 1.0}) == exp(sinh(piecewise/z**1.0))
    assert sinh(piecewise*z**-1.0).is_zero is None


def test_og_21930_test_create():
    from sympy import latex, symbols
    from sympy.physics.secondquant import Bd

    i = symbols("i")
    assert latex(Bd(i)) == r"{b^\dagger_{i}}"


def test_og_21930_test_commutation():
    from sympy import latex, symbols
    from sympy.physics.secondquant import Commutator, F, Fd

    i, j = symbols("i j", below_fermi=True)
    a, b = symbols("a b", above_fermi=True)
    commutator = Commutator(Fd(a)*F(i), Fd(b)*F(j))
    assert latex(commutator) == r"\left[{a^\dagger_{a}} a_{i},{a^\dagger_{b}} a_{j}\right]"


def test_og_21930_test_create_f():
    from sympy import latex, symbols
    from sympy.physics.secondquant import Fd

    p = symbols("p")
    assert latex(Fd(p)) == r"{a^\dagger_{p}}"


def test_og_21930_test_NO():
    from sympy import latex, symbols
    from sympy.physics.secondquant import Fd, NO

    a = symbols("a", above_fermi=True)
    i = symbols("i", below_fermi=True)
    normal_order = NO(Fd(a)*Fd(i))
    assert latex(normal_order) == r"\left\{{a^\dagger_{a}} {a^\dagger_{i}}\right\}"


def test_og_21930_test_Tensors():
    from sympy import Dummy, latex, symbols
    from sympy.physics.secondquant import AntiSymmetricTensor

    i, j = symbols("i j", below_fermi=True, cls=Dummy)
    a, b = symbols("a b", above_fermi=True, cls=Dummy)
    tensor = AntiSymmetricTensor("t", (a, b), (i, j))
    assert latex(tensor) == r"{t^{ab}_{ij}}"


def test_og_21930_test_issue_19661():
    from sympy import Symbol, latex
    from sympy.physics.secondquant import B, Bd, Commutator

    zero = Symbol("0")
    assert latex(Commutator(Bd(zero)**2, B(zero))) == (
        r"- \left[b_{0},{b^\dagger_{0}}^{2}\right]"
    )


def test_og_13852_test_polylog_values():
    from sympy import Abs, I, S, log, pi, polylog, sqrt

    assert polylog(2, 2) == pi**2/4 - I*pi*log(2)
    assert polylog(2, S.Half) == pi**2/12 - log(2)**2/2
    values = [
        S.Half,
        2,
        (sqrt(5) - 1)/2,
        -(sqrt(5) - 1)/2,
        -(sqrt(5) + 1)/2,
        (3 - sqrt(5))/2,
    ]
    for value in values:
        evaluated = polylog(2, value).evalf()
        unevaluated = polylog(2, value, evaluate=False).evalf()
        assert Abs(evaluated - unevaluated) < 1e-15


def test_og_20154_test_partitions():
    from sympy.utilities.iterables import partitions

    assert list(partitions(6, k=2)) == [
        {2: 3},
        {1: 2, 2: 2},
        {1: 4, 2: 1},
        {1: 6},
    ]
    assert list(partitions(6, k=3)) == [
        {3: 2},
        {1: 1, 2: 1, 3: 1},
        {1: 3, 3: 1},
        {2: 3},
        {1: 2, 2: 2},
        {1: 4, 2: 1},
        {1: 6},
    ]


def test_og_20154_test_uniq():
    from sympy.utilities.iterables import partitions, uniq

    assert list(uniq(partition for partition in partitions(4))) == [
        {4: 1},
        {1: 1, 3: 1},
        {2: 2},
        {1: 2, 2: 1},
        {1: 4},
    ]


def test_og_20428_test_issue_20427():
    from sympy import Poly, S, sqrt, symbols

    x = symbols("x")
    polynomial = Poly(
        -117968192370600*18**(S(1)/3)/(
            217603955769048*(24201 + 253*sqrt(9165))**(S(1)/3)
            + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(S(1)/3)
        )
        - 15720318185*2**(S(2)/3)*3**(S(1)/3)*(
            24201 + 253*sqrt(9165)
        )**(S(2)/3)/(
            217603955769048*(24201 + 253*sqrt(9165))**(S(1)/3)
            + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(S(1)/3)
        )
        + 15720318185*12**(S(1)/3)*(24201 + 253*sqrt(9165))**(S(2)/3)/(
            217603955769048*(24201 + 253*sqrt(9165))**(S(1)/3)
            + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(S(1)/3)
        )
        + 117968192370600*2**(S(1)/3)*3**(S(2)/3)/(
            217603955769048*(24201 + 253*sqrt(9165))**(S(1)/3)
            + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(S(1)/3)
        ),
        x,
    )
    assert polynomial == Poly(0, x, domain="EX")


def test_og_13757_test_issue_13079():
    from sympy import Poly, S, symbols

    x = symbols("x")
    expected_square = Poly(x**2, x, domain="ZZ")
    expected_scaled = Poly(-2*x, x, domain="ZZ")
    assert Poly(x)*x == expected_square
    assert x*Poly(x) == expected_square
    assert -2*Poly(x) == expected_scaled
    assert S(-2)*Poly(x) == expected_scaled
    assert Poly(x)*S(-2) == expected_scaled


def test_og_13974_test_tensor_product_simp():
    from sympy import symbols
    from sympy.physics.quantum.operator import Operator
    from sympy.physics.quantum.tensorproduct import TensorProduct, tensor_product_simp
    from sympy.testing.pytest import warns_deprecated_sympy

    a, b, c, d = [Operator(name) for name in "ABCD"]
    x = symbols("x")
    exponent = symbols("y", integer=True, positive=True)
    with warns_deprecated_sympy():
        assert tensor_product_simp(TensorProduct(a, b)**exponent) == TensorProduct(
            a**exponent, b**exponent
        )
        assert tensor_product_simp(x*TensorProduct(a, b)**2) == x*TensorProduct(a**2, b**2)
        assert tensor_product_simp(
            x*TensorProduct(a, b)**2*TensorProduct(c, d)
        ) == x*TensorProduct(a**2*c, b**2*d)
        assert tensor_product_simp(
            TensorProduct(a, b) - TensorProduct(c, d)**exponent
        ) == TensorProduct(a, b) - TensorProduct(c**exponent, d**exponent)


def test_og_24443_test_homomorphism():
    from sympy.combinatorics.homomorphisms import homomorphism
    from sympy.combinatorics.named_groups import DihedralGroup

    group = DihedralGroup(3)
    mapping = homomorphism(group, group, group.generators, group.generators)
    assert mapping.is_isomorphism()


def test_og_21596_test_imageset_intersect_real():
    from sympy import ConditionSet, Eq, FiniteSet, I, ImageSet, Lambda, S, imageset
    from sympy.abc import n, x

    assert imageset(
        Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers
    ).intersect(S.Reals) == FiniteSet(-1, 1)

    imaginary_part = (n - 1)*(n + S.Half)
    assert imageset(
        Lambda(n, n + imaginary_part*I), S.Integers
    ).intersect(S.Reals) == FiniteSet(1)
    assert imageset(
        Lambda(n, n + imaginary_part*(n + 1)*I), S.Naturals0
    ).intersect(S.Reals) == FiniteSet(1)
    assert imageset(
        Lambda(n, n/2 + imaginary_part.expand()*I), S.Integers
    ).intersect(S.Reals) == ImageSet(
        Lambda(x, x/2),
        ConditionSet(n, Eq(n**2 - n/2 - S(1)/2, 0), S.Integers),
    )
    assert imageset(
        Lambda(n, n/(1/n - 1) + imaginary_part*(n + 1)*I), S.Integers
    ).intersect(S.Reals) == FiniteSet(S.Half)
    assert imageset(
        Lambda(n, n/(n - 6) + (n - 3)*(n + 1)*I/(2*n + 2)),
        S.Integers,
    ).intersect(S.Reals) == FiniteSet(-1)
    assert imageset(
        Lambda(n, n/(n**2 - 9) + (n - 3)*(n + 1)*I/(2*n + 2)),
        S.Integers,
    ).intersect(S.Reals) is S.EmptySet


def test_og_22080_test_create_expand_pow_optimization():
    from sympy import Symbol, ccode
    from sympy.codegen.rewriting import create_expand_pow_optimization, optimize

    x = Symbol("x")
    expand_pow = create_expand_pow_optimization(4)

    def optimized_ccode(expression):
        return ccode(optimize(expression, [expand_pow]))

    assert optimized_ccode(-x**4) == "-(x*x*x*x)"
    assert optimized_ccode(x**4 - x**2) == "-(x*x) + x*x*x*x"
    i = Symbol("i", integer=True)
    assert optimized_ccode(x**i - x**2) == "pow(x, i) - (x*x)"


def test_og_22080_test_PythonCodePrinter():
    from sympy import Mod, symbols
    from sympy.printing.pycode import PythonCodePrinter

    x, y = symbols("x y")
    printer = PythonCodePrinter()
    assert printer.doprint(-Mod(x, y)) == "-(x % y)"
    assert printer.doprint(Mod(-x, y)) == "(-x) % y"


def test_og_22080_test_empty_modules():
    from sympy import symbols
    from sympy.utilities.lambdify import lambdify

    x, y = symbols("x y")
    expression = -(x % y)
    default_modules = lambdify([x, y], expression)
    empty_modules = lambdify([x, y], expression, modules=[])
    assert default_modules(3, 7) == empty_modules(3, 7)
    assert default_modules(3, 7) == -3


def test_og_13877_test_determinant():
    from sympy import Matrix, symbols

    a = symbols("a")

    def matrix(size):
        return Matrix([[i + a*j for i in range(size)] for j in range(size)])

    assert matrix(5).det() == 0
    assert matrix(6).det() == 0
    assert matrix(7).det() == 0


def test_og_18199_test_solve_modular():
    from sympy import Dummy, ImageSet, Lambda, Mod, S, Union, symbols
    from sympy.solvers.solveset import solveset

    x = symbols("x")
    n = Dummy("n", integer=True)
    cubic = solveset(Mod(x**3, 8) - 1, x, S.Integers)
    expected_cubic = ImageSet(Lambda(n, 8*n + 1), S.Integers)
    assert cubic.dummy_eq(expected_cubic)

    quartic = solveset(Mod(x**4, 9) - 4, x, S.Integers)
    expected_quartic = Union(
        ImageSet(Lambda(n, 9*n + 4), S.Integers),
        ImageSet(Lambda(n, 9*n + 5), S.Integers),
    )
    assert quartic.dummy_eq(expected_quartic)


def test_og_15976_test_presentation_symbol():
    from sympy import Symbol
    from sympy.printing.mathml import MathMLPresentationPrinter

    printer = MathMLPresentationPrinter()
    expected = {
        "x^2": "<msup><mi>x</mi><mi>2</mi></msup>",
        "x__2": "<msup><mi>x</mi><mi>2</mi></msup>",
        "x_2": "<msub><mi>x</mi><mi>2</mi></msub>",
        "x^3_2": "<msubsup><mi>x</mi><mi>2</mi><mi>3</mi></msubsup>",
        "x__3_2": "<msubsup><mi>x</mi><mi>2</mi><mi>3</mi></msubsup>",
        "x_2_a": "<msub><mi>x</mi><mrow><mi>2</mi><mo> </mo><mi>a</mi></mrow></msub>",
        "x^2^a": "<msup><mi>x</mi><mrow><mi>2</mi><mo> </mo><mi>a</mi></mrow></msup>",
        "x__2__a": "<msup><mi>x</mi><mrow><mi>2</mi><mo> </mo><mi>a</mi></mrow></msup>",
    }
    for name, xml in expected.items():
        assert printer._print(Symbol(name)).toxml() == xml


def test_og_13878_test_arcsin():
    from sympy import Piecewise, Symbol, asin, pi, sqrt
    from sympy.stats import Arcsin, cdf

    a = Symbol("a", real=True)
    b = Symbol("b", real=True)
    x = Symbol("x")
    distribution = Arcsin("x", a, b)
    assert cdf(distribution)(x) == Piecewise(
        (0, a > x),
        (2*asin(sqrt((-a + x)/(-a + b)))/pi, b >= x),
        (1, True),
    )
