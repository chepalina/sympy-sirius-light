# Sirius OG Buggy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `sirius-og-buggy` with all 54 SWE-bench OG regressions reproducible by 65 targeted pytest checks.

**Architecture:** Keep the complete SymPy checkout at `sympy-sirius-light/og-buggy` and the student dataset inside its `bugs_cards/` directory. Derive checks from the official `test_patch`/`FAIL_TO_PASS` records, prove all 65 checks pass on the unmodified base, then reverse or semantically adapt the 54 production patches so every targeted check fails for the intended reason. Fifteen reverse patches apply directly; thirty-nine require adaptation to SymPy 1.15.0.dev.

**Tech Stack:** Python 3.11+, SymPy 1.15.0.dev, pytest, hypothesis, Bash, Git worktrees, official SWE-bench JSONL.

---

## File map

- Create `bugs_cards/sympy_og_tickets.csv`: unchanged 54-row dataset copied from the benchmark repository.
- Create `bugs_cards/sympy_og_tickets_input.csv`: five-column student/agent input.
- Create `bugs_cards/template.md`: same concise card template used by `sirius-light-buggy`.
- Create `sirius_tests/test_sympy_og_bugs.py`: 65 targeted regression checks covering all 54 `instance_id` values.
- Create `scripts/setup_sirius.sh`: local virtual-environment setup.
- Create `scripts/run_sirius_tests.sh`: targeted buggy-suite runner.
- Modify the 54 production paths named by `patch_files`; no two tasks share the same production path.
- Do not copy `sympy_og_tickets_full.jsonl` into this branch because it contains answer patches.

The immutable sources are:

- `/Users/family/Documents/Сириус/sirius-swebench-light/sirius_benchmark/tickets/sympy_og_tickets.csv`
- `/Users/family/Documents/Сириус/sirius-swebench-light/sirius_benchmark/tickets/sympy_og_tickets_full.jsonl`

### Task 1: Protect existing worktrees and create student data files

**Files:**
- Create: `bugs_cards/sympy_og_tickets.csv`
- Create: `bugs_cards/sympy_og_tickets_input.csv`
- Create: `bugs_cards/template.md`

- [ ] **Step 1: Record the protected state**

Run these commands from `/Users/family/Documents/Сириус/sympy-sirius-light/og-buggy`:

```bash
git -C ../.repo status --short --branch
git -C ../buggy status --short --branch
git -C ../golden status --short --branch
git status --short --branch
shasum -a 256 /Users/family/Documents/Сириус/sirius-swebench-light/sirius_benchmark/tickets/sympy_og_tickets.csv
```

Expected protected state: master has only `M README.md`; `sirius-light-buggy` has only the pre-existing untracked `bugs_cards/sympy_og_tickets.csv`; `sirius-light-golden` is clean; `sirius-og-buggy` is clean. Expected source hash: `68722a795bf86a81d313073c239aecbc29c6baeda4949eec2eaaea3fe41ffe63`.

- [ ] **Step 2: Copy the source CSV and template mechanically**

```bash
mkdir -p bugs_cards
cp /Users/family/Documents/Сириус/sirius-swebench-light/sirius_benchmark/tickets/sympy_og_tickets.csv bugs_cards/sympy_og_tickets.csv
cp ../buggy/bugs_cards/template.md bugs_cards/template.md
```

- [ ] **Step 3: Generate the reduced five-column CSV**

Run:

```bash
python3 -c 'import csv,pathlib
source=pathlib.Path("bugs_cards/sympy_og_tickets.csv")
target=pathlib.Path("bugs_cards/sympy_og_tickets_input.csv")
fields=["instance_id","title","ticket_description","expected_fail_to_pass_tests","test_files"]
with source.open(encoding="utf-8",newline="") as f:
    rows=list(csv.DictReader(f))
with target.open("w",encoding="utf-8",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=fields)
    writer.writeheader()
    writer.writerows({field: row[field] for field in fields} for row in rows)'
```

- [ ] **Step 4: Validate both CSV contracts**

Run:

```bash
python3 -c 'import csv,pathlib
root=pathlib.Path("bugs_cards")
full=list(csv.DictReader((root/"sympy_og_tickets.csv").open(encoding="utf-8",newline="")))
agent=list(csv.DictReader((root/"sympy_og_tickets_input.csv").open(encoding="utf-8",newline="")))
fields=["instance_id","title","ticket_description","expected_fail_to_pass_tests","test_files"]
assert len(full)==len(agent)==54
assert len({row["instance_id"] for row in full})==54
assert list(agent[0])==fields
assert [row["instance_id"] for row in full]==[row["instance_id"] for row in agent]
print("54 dataset rows; 54 agent rows; five-column contract valid")'
cmp /Users/family/Documents/Сириус/sirius-swebench-light/sirius_benchmark/tickets/sympy_og_tickets.csv bugs_cards/sympy_og_tickets.csv
```

Expected: validation message and `cmp` exit 0.

- [ ] **Step 5: Commit the data files**

```bash
git add bugs_cards/sympy_og_tickets.csv bugs_cards/sympy_og_tickets_input.csv bugs_cards/template.md
git commit -m "Add SymPy OG ticket inputs"
```

### Task 2: Add targeted setup and run scripts

**Files:**
- Create: `scripts/setup_sirius.sh`
- Create: `scripts/run_sirius_tests.sh`

- [ ] **Step 1: Create `scripts/setup_sirius.sh` with this exact content**

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$(cd "$REPO_ROOT/.." && pwd)/.venv"

python3 -m venv "$VENV_DIR"
. "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -e "$REPO_ROOT" pytest hypothesis
```

- [ ] **Step 2: Create `scripts/run_sirius_tests.sh` with this exact content**

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$(cd "$REPO_ROOT/.." && pwd)/.venv"

if [ -d "$VENV_DIR" ]; then
  . "$VENV_DIR/bin/activate"
fi

cd "$REPO_ROOT"
python -m pytest -q sirius_tests/test_sympy_og_bugs.py
```

- [ ] **Step 3: Make scripts executable and validate Bash syntax**

```bash
chmod +x scripts/setup_sirius.sh scripts/run_sirius_tests.sh
bash -n scripts/setup_sirius.sh
bash -n scripts/run_sirius_tests.sh
```

Expected: both commands exit 0 without output.

- [ ] **Step 4: Create or refresh the shared environment**

```bash
./scripts/setup_sirius.sh
```

Expected: editable SymPy install plus pytest and hypothesis complete successfully.

- [ ] **Step 5: Commit the scripts**

```bash
git add scripts/setup_sirius.sh scripts/run_sirius_tests.sh
git commit -m "Add SymPy OG test scripts"
```

### Task 3: Build the 65-check golden baseline

**Files:**
- Create: `sirius_tests/test_sympy_og_bugs.py`
- Source: `/Users/family/Documents/Сириус/sirius-swebench-light/sirius_benchmark/tickets/sympy_og_tickets_full.jsonl`

- [ ] **Step 1: Print the exact official test material for each task**

Use this command with each of the 54 exact IDs from `bugs_cards/sympy_og_tickets.csv`:

```bash
python3 -c 'import json,pathlib,sys
iid=sys.argv[1]
rows=map(json.loads,pathlib.Path("/Users/family/Documents/Сириус/sirius-swebench-light/sirius_benchmark/tickets/sympy_og_tickets_full.jsonl").open(encoding="utf-8"))
row=next(row for row in rows if row["instance_id"]==iid)
print(row["FAIL_TO_PASS"])
print(row["test_patch"])' sympy__sympy-14711
```

For every `FAIL_TO_PASS` entry, move the minimal assertions, imports, fixtures, and setup from `test_patch` into one uniquely named pytest function in `sirius_tests/test_sympy_og_bugs.py`. Prefix the function with the issue number, for example:

```python
from sympy.physics.vector import ReferenceFrame


def test_og_14711_test_Vector():
    frame = ReferenceFrame("A")
    assert frame.x + 0 == frame.x
```

For tasks with multiple official checks, keep separate functions. For example, `sympy__sympy-15809` contributes both:

```python
from sympy import Max, Min, S


def test_og_15809_test_Min():
    assert Min() == S.Infinity


def test_og_15809_test_Max():
    assert Max() == S.NegativeInfinity
```

- [ ] **Step 2: Preserve the complete official check mapping**

The final file must contain one pytest item for each of these 65 mappings:

```text
14711: test_Vector
23534: test_symbols
23824: test_kahane_simplify1
23950: test_as_set
16766: test_PythonCodePrinter
15017: test_ndim_array_initiation
15809: test_Min, test_Max
13551: test_issue_13546
13480: test_coth
16886: test_encode_morse
20590: test_immutable
21847: test_monomials
19637: test_kernS
15349: test_quaternion_conversions
16450: test_posify
13372: test_evalf_bugs
18189: test_diophantine
20916: test_super_sub
13031: test_sparse_matrix
24213: test_issue_24211
22456: test_String
12419: test_Identity
23262: test_issue_14941
23413: test_hermite_normal
17318: test_issue_12420
13647: test_col_insert
15875: test_Add_is_zero
18211: test_issue_18188
19954: test_sylow_subgroup
21612: test_Mul
24539: test_PolyElement_as_expr
17139: test__TR56, test_issue_17137
19495: test_subs_CondSet
13615: test_Complement
20801: test_zero_not_false
19346: test_dict
24661: test_issue_24288
19783: test_dagger_mul, test_identity
16792: test_ccode_unused_array_arg
19040: test_issue_5786
21379: test_Mod
21930: test_create, test_commutation, test_create_f, test_NO, test_Tensors, test_issue_19661
13852: test_polylog_values
20154: test_partitions, test_uniq
20428: test_issue_20427
13757: test_issue_13079
13974: test_tensor_product_simp
24443: test_homomorphism
21596: test_imageset_intersect_real
22080: test_create_expand_pow_optimization, test_PythonCodePrinter, test_empty_modules
13877: test_determinant
18199: test_solve_modular
15976: test_presentation_symbol
13878: test_arcsin
```

- [ ] **Step 3: Verify count and coverage structurally**

Run:

```bash
python3 -c 'import ast,csv,pathlib,re
path=pathlib.Path("sirius_tests/test_sympy_og_bugs.py")
tree=ast.parse(path.read_text(encoding="utf-8"))
tests=[node.name for node in tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.name.startswith("test_og_")]
ids={re.match(r"test_og_(\d+)_",name).group(1) for name in tests}
with pathlib.Path("bugs_cards/sympy_og_tickets.csv").open(encoding="utf-8",newline="") as f:
    expected={row["instance_id"].rsplit("-",1)[1] for row in csv.DictReader(f)}
assert len(tests)==65, len(tests)
assert ids==expected, (expected-ids,ids-expected)
print("65 checks cover all 54 instance IDs")'
```

- [ ] **Step 4: Prove the unmodified base is green**

```bash
python -m pytest -q sirius_tests/test_sympy_og_bugs.py
```

Expected: `65 passed`; collection errors, skips, xfails, and warnings that hide a target assertion are not accepted.

- [ ] **Step 5: Commit the green regression suite**

```bash
git add sirius_tests/test_sympy_og_bugs.py
git commit -m "Add SymPy OG regression checks"
```

### Task 4: Reintroduce the 15 directly reversible regressions

**Files:**
- Modify: `sympy/physics/vector/vector.py`
- Modify: `sympy/core/symbol.py`
- Modify: `sympy/crypto/crypto.py`
- Modify: `sympy/core/_print_helpers.py`
- Modify: `sympy/core/sympify.py`
- Modify: `sympy/simplify/simplify.py`
- Modify: `sympy/physics/units/unitsystem.py`
- Modify: `sympy/combinatorics/perm_groups.py`
- Modify: `sympy/printing/str.py`
- Modify: `sympy/simplify/fu.py`
- Modify: `sympy/printing/repr.py`
- Modify: `sympy/utilities/codegen.py`
- Modify: `sympy/utilities/iterables.py`
- Modify: `sympy/polys/domains/expressiondomain.py`
- Modify: `sympy/printing/mathml.py`

- [ ] **Step 1: Reconfirm these 17 checks are green**

```bash
python -m pytest -q sirius_tests/test_sympy_og_bugs.py -k 'og_14711 or og_23534 or og_16886 or og_20590 or og_19637 or og_16450 or og_24213 or og_19954 or og_21612 or og_17139 or og_19346 or og_16792 or og_20154 or og_20428 or og_15976'
```

Expected: `17 passed, 48 deselected`.

- [ ] **Step 2: Apply the exact reverse patches**

Save and run this script as `/private/tmp/apply_clean_og.py`:

```python
import json
import pathlib
import subprocess

source = pathlib.Path("/Users/family/Documents/Сириус/sirius-swebench-light/sirius_benchmark/tickets/sympy_og_tickets_full.jsonl")
ids = {
    "sympy__sympy-14711", "sympy__sympy-23534", "sympy__sympy-16886",
    "sympy__sympy-20590", "sympy__sympy-19637", "sympy__sympy-16450",
    "sympy__sympy-24213", "sympy__sympy-19954", "sympy__sympy-21612",
    "sympy__sympy-17139", "sympy__sympy-19346", "sympy__sympy-16792",
    "sympy__sympy-20154", "sympy__sympy-20428", "sympy__sympy-15976",
}
for row in map(json.loads, source.open(encoding="utf-8")):
    if row["instance_id"] not in ids:
        continue
    patch = pathlib.Path("/private/tmp") / f"{row['instance_id']}.patch"
    patch.write_text(row["patch"], encoding="utf-8")
    subprocess.run(["git", "apply", "-R", str(patch)], check=True)
```

Run:

```bash
python3 /private/tmp/apply_clean_og.py
```

Expected: exit 0 and modifications limited to the 15 listed production paths.

- [ ] **Step 3: Prove all 17 checks now fail for assertions or expected exceptions**

```bash
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k 'og_14711 or og_23534 or og_16886 or og_20590 or og_19637 or og_16450 or og_24213 or og_19954 or og_21612 or og_17139 or og_19346 or og_16792 or og_20154 or og_20428 or og_15976'
```

Expected: `17 failed, 48 deselected`, with no collection or import errors.

- [ ] **Step 4: Commit the directly reversible regressions**

```bash
git add sympy
git commit -m "Reintroduce directly reversible SymPy OG bugs"
```

### Task 5: Adapt manual regressions 23824 through 13372

**Files and checks:**

```text
23824 sympy/physics/hep/gamma_matrices.py test_kahane_simplify1
23950 sympy/sets/contains.py test_as_set
16766 sympy/printing/pycode.py test_PythonCodePrinter
15017 sympy/tensor/array/dense_ndim_array.py test_ndim_array_initiation
15809 sympy/functions/elementary/miscellaneous.py test_Min, test_Max
13551 sympy/concrete/products.py test_issue_13546
13480 sympy/functions/elementary/hyperbolic.py test_coth
21847 sympy/polys/monomials.py test_monomials
15349 sympy/algebras/quaternion.py test_quaternion_conversions
13372 sympy/core/evalf.py test_evalf_bugs
```

- [ ] **Step 1: Prove the 11 group checks are green before mutation**

```bash
python -m pytest -q sirius_tests/test_sympy_og_bugs.py -k 'og_23824 or og_23950 or og_16766 or og_15017 or og_15809 or og_13551 or og_13480 or og_21847 or og_15349 or og_13372'
```

Expected: `11 passed, 54 deselected`.

- [ ] **Step 2: Extract every manual inverse patch**

Run this once to create the thirty-nine exact patch files used by Tasks 5–8:

```bash
python3 -c 'import json,pathlib
source=pathlib.Path("/Users/family/Documents/Сириус/sirius-swebench-light/sirius_benchmark/tickets/sympy_og_tickets_full.jsonl")
ids={"23824","23950","16766","15017","15809","13551","13480","21847","15349","13372","18189","20916","13031","22456","12419","23262","23413","17318","13647","15875","18211","24539","19495","13615","20801","24661","19783","19040","21379","21930","13852","13757","13974","24443","21596","22080","13877","18199","13878"}
for row in map(json.loads,source.open(encoding="utf-8")):
    issue=row["instance_id"].rsplit("-",1)[1]
    if issue in ids:
        pathlib.Path(f"/private/tmp/{row['instance_id']}.patch").write_text(row["patch"],encoding="utf-8")
print("39 manual patches extracted")'
```

Then run `git apply -R --reject --whitespace=nowarn` one ID at a time. Use each generated `.rej` as the exact inverse specification and transpose only that rejected hunk into the current implementation with `apply_patch`. Remove the `.rej` after the hunk is represented in the production file.

```bash
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-23824.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-23950.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-16766.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-15017.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-15809.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-13551.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-13480.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-21847.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-15349.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-13372.patch
```

- [ ] **Step 3: Verify each mutation immediately**

After each file edit, run the matching command below. Every selected check must fail by assertion or the historical exception; import, syntax, fixture, timeout, and collection errors are rejected.

```bash
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_23824
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_23950
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_16766
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_15017
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_15809
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_13551
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_13480
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_21847
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_15349
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_13372
```

- [ ] **Step 4: Verify the complete group**

```bash
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k 'og_23824 or og_23950 or og_16766 or og_15017 or og_15809 or og_13551 or og_13480 or og_21847 or og_15349 or og_13372'
```

Expected: `11 failed, 54 deselected`.

- [ ] **Step 5: Commit the group**

```bash
git add sympy
git commit -m "Reintroduce SymPy OG bugs batch one"
```

### Task 6: Adapt manual regressions 18189 through 15875

**Files and checks:**

```text
18189 sympy/solvers/diophantine.py test_diophantine
20916 sympy/printing/conventions.py test_super_sub
13031 sympy/matrices/sparse.py test_sparse_matrix
22456 sympy/codegen/ast.py test_String
12419 sympy/matrices/expressions/matexpr.py test_Identity
23262 sympy/utilities/lambdify.py test_issue_14941
23413 sympy/polys/matrices/normalforms.py test_hermite_normal
17318 sympy/simplify/radsimp.py and sympy/simplify/sqrtdenest.py test_issue_12420
13647 sympy/matrices/common.py test_col_insert
15875 sympy/core/add.py test_Add_is_zero
```

- [ ] **Step 1: Run the 10 checks before mutation**

```bash
python -m pytest -q sirius_tests/test_sympy_og_bugs.py -k 'og_18189 or og_20916 or og_13031 or og_22456 or og_12419 or og_23262 or og_23413 or og_17318 or og_13647 or og_15875'
```

Expected: `10 passed, 55 deselected`.

- [ ] **Step 2: Apply or transpose the ten inverse patches individually**

Run the exact commands below, transpose rejected inverse hunks with `apply_patch`, and remove `.rej` files. For `18189`, locate the current implementation after the historical `sympy/solvers/diophantine.py` package move and place the inverse behavior in the current module that exports `diophantine`.

```bash
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-18189.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-20916.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-13031.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-22456.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-12419.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-23262.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-23413.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-17318.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-13647.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-15875.patch
```

- [ ] **Step 3: Verify each issue selector after its production edit**

Run the matching command immediately after each production edit. Expected: every selected check fails for the historic behavior only.

```bash
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_18189
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_20916
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_13031
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_22456
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_12419
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_23262
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_23413
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_17318
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_13647
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_15875
```

- [ ] **Step 4: Verify and commit the full group**

```bash
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k 'og_18189 or og_20916 or og_13031 or og_22456 or og_12419 or og_23262 or og_23413 or og_17318 or og_13647 or og_15875'
git add sympy
git commit -m "Reintroduce SymPy OG bugs batch two"
```

Expected pytest result: `10 failed, 55 deselected`.

### Task 7: Adapt manual regressions 18211 through 21379

**Files and checks:**

```text
18211 sympy/core/relational.py test_issue_18188
24539 sympy/polys/rings.py test_PolyElement_as_expr
19495 sympy/sets/conditionset.py test_subs_CondSet
13615 sympy/sets/sets.py test_Complement
20801 sympy/core/numbers.py test_zero_not_false
24661 sympy/parsing/sympy_parser.py test_issue_24288
19783 sympy/physics/quantum/dagger.py and sympy/physics/quantum/operator.py test_dagger_mul, test_identity
19040 sympy/polys/factortools.py test_issue_5786
21379 sympy/core/mod.py test_Mod
```

- [ ] **Step 1: Run the 10 checks before mutation**

```bash
python -m pytest -q sirius_tests/test_sympy_og_bugs.py -k 'og_18211 or og_24539 or og_19495 or og_13615 or og_20801 or og_24661 or og_19783 or og_19040 or og_21379'
```

Expected: `10 passed, 55 deselected`.

- [ ] **Step 2: Apply or transpose inverse patches one production path at a time**

Run these commands separately, use rejected hunks as the exact old-behavior specification, and edit only the paths listed above. Keep the two `19783` checks separate and verify both after changing the two quantum modules.

```bash
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-18211.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-24539.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-19495.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-13615.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-20801.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-24661.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-19783.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-19040.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-21379.patch
```

- [ ] **Step 3: Verify individual historic failures**

Run the matching selector after each edit. Expected: assertion failure or historic exception for every selected item, with successful collection.

```bash
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_18211
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_24539
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_19495
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_13615
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_20801
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_24661
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_19783
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_19040
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_21379
```

- [ ] **Step 4: Verify and commit the group**

```bash
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k 'og_18211 or og_24539 or og_19495 or og_13615 or og_20801 or og_24661 or og_19783 or og_19040 or og_21379'
git add sympy
git commit -m "Reintroduce SymPy OG bugs batch three"
```

Expected pytest result: `10 failed, 55 deselected`.

### Task 8: Adapt manual regressions 21930 through 13878

**Files and checks:**

```text
21930 sympy/physics/secondquant.py test_create, test_commutation, test_create_f, test_NO, test_Tensors, test_issue_19661
13852 sympy/functions/special/zeta_functions.py test_polylog_values
13757 sympy/polys/polytools.py test_issue_13079
13974 sympy/physics/quantum/tensorproduct.py test_tensor_product_simp
24443 sympy/combinatorics/homomorphisms.py test_homomorphism
21596 sympy/sets/handlers/intersection.py test_imageset_intersect_real
22080 sympy/printing/codeprinter.py and sympy/printing/precedence.py test_create_expand_pow_optimization, test_PythonCodePrinter, test_empty_modules
13877 sympy/matrices/matrices.py and sympy/utilities/randtest.py test_determinant
18199 sympy/ntheory/residue_ntheory.py test_solve_modular
13878 sympy/stats/crv_types.py test_arcsin
```

- [ ] **Step 1: Run the 17 checks before mutation**

```bash
python -m pytest -q sirius_tests/test_sympy_og_bugs.py -k 'og_21930 or og_13852 or og_13757 or og_13974 or og_24443 or og_21596 or og_22080 or og_13877 or og_18199 or og_13878'
```

Expected: `17 passed, 48 deselected`.

- [ ] **Step 2: Apply or transpose the final ten inverse patches**

Run these commands separately and transpose rejected inverse hunks only into the listed paths. Preserve six independent checks for `21930` and three independent checks for `22080`.

```bash
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-21930.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-13852.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-13757.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-13974.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-24443.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-21596.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-22080.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-13877.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-18199.patch
git apply -R --reject --whitespace=nowarn /private/tmp/sympy__sympy-13878.patch
```

- [ ] **Step 3: Verify each issue selector after mutation**

Run the matching command after each mutation. Expected: every selected item fails for the target regression, while import and collection remain successful.

```bash
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_21930
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_13852
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_13757
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_13974
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_24443
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_21596
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_22080
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_13877
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_18199
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k og_13878
```

- [ ] **Step 4: Verify and commit the group**

```bash
python -m pytest -q --tb=short sirius_tests/test_sympy_og_bugs.py -k 'og_21930 or og_13852 or og_13757 or og_13974 or og_24443 or og_21596 or og_22080 or og_13877 or og_18199 or og_13878'
git add sympy
git commit -m "Reintroduce SymPy OG bugs batch four"
```

Expected pytest result: `17 failed, 48 deselected`.

### Task 9: Verify all 54 bugs and preserve protected branches

**Files:**
- Verify: `sirius_tests/test_sympy_og_bugs.py`
- Verify: `bugs_cards/sympy_og_tickets.csv`
- Verify: `bugs_cards/sympy_og_tickets_input.csv`
- Verify: all production paths changed in Tasks 4–8

- [ ] **Step 1: Verify collection count and task coverage**

Run the structural checker from Task 3 again.

Expected: `65 checks cover all 54 instance IDs`.

- [ ] **Step 2: Run only the targeted buggy suite**

```bash
./scripts/run_sirius_tests.sh
```

Expected: pytest collects 65 items and reports `65 failed`; no errors, skips, xfails, hangs, or unrelated tests. A nonzero exit code is expected because this is the buggy branch.

- [ ] **Step 3: Confirm the test file is green against the unmodified base**

Create a detached temporary worktree at base commit `bd33731801cefa2b3d2df9c515956530dceb1077`, copy only `sirius_tests/test_sympy_og_bugs.py` into it, and run the same test file there with the existing Python environment. Remove the temporary worktree after recording the output.

```bash
git worktree add --detach /private/tmp/sirius-og-baseline bd33731801cefa2b3d2df9c515956530dceb1077
mkdir -p /private/tmp/sirius-og-baseline/sirius_tests
cp sirius_tests/test_sympy_og_bugs.py /private/tmp/sirius-og-baseline/sirius_tests/test_sympy_og_bugs.py
cd /private/tmp/sirius-og-baseline
python -m pytest -q sirius_tests/test_sympy_og_bugs.py
cd /Users/family/Documents/Сириус/sympy-sirius-light/og-buggy
git worktree remove /private/tmp/sirius-og-baseline
```

Expected baseline result: `65 passed`.

- [ ] **Step 4: Recheck protected statuses and source integrity**

```bash
git -C ../.repo status --short --branch
git -C ../buggy status --short --branch
git -C ../golden status --short --branch
shasum -a 256 /Users/family/Documents/Сириус/sirius-swebench-light/sirius_benchmark/tickets/sympy_og_tickets.csv
git status --short --branch
git diff --check master...HEAD
```

Expected: protected statuses match Task 1; source hash remains `68722a795bf86a81d313073c239aecbc29c6baeda4949eec2eaaea3fe41ffe63`; new worktree is clean; diff check exits 0.

- [ ] **Step 5: Produce the final evidence table**

For all 54 rows, report `instance_id`, every test function whose numeric segment matches that instance, changed production paths, and the observed failure reason. Use fresh pytest output and `git diff --name-only master...HEAD` as evidence.
