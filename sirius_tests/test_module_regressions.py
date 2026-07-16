import subprocess
import sys
from pathlib import Path

import pytest


MODULE_REGRESSION_TEST_FILES = [
    "sympy/matrices/expressions/tests/test_blockmatrix.py",
    "sympy/printing/tests/test_mathematica.py",
    "sympy/core/tests/test_kind.py",
    "sympy/geometry/tests/test_point.py",
    "sympy/functions/elementary/tests/test_complexes.py",
    "sympy/solvers/tests/test_polysys.py",
    "sympy/combinatorics/tests/test_permutations.py",
    "sympy/core/tests/test_power.py",
]


@pytest.mark.parametrize("test_file", MODULE_REGRESSION_TEST_FILES)
def test_module_regressions_for_light_bugs(test_file):
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", test_file],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=180,
    )

    assert result.returncode == 0, result.stdout
