# Sirius OG Bug Cards Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create 54 complete Markdown bug cards from the Sirius OG CSV and existing regression checks.

**Architecture:** Treat the CSV as the ordered metadata source and `sirius_tests/test_sympy_og_bugs.py` as the source for executable reproductions and exact pytest selectors. Generate one independent card per `instance_id`, then validate the complete set against both sources before committing.

**Tech Stack:** Markdown, Python 3 standard library (`csv`, `ast`, `pathlib`), Git.

---

### Task 1: Build the source mapping

**Files:**
- Read: `bugs_cards/sympy_og_tickets.csv`
- Read: `bugs_cards/template.md`
- Read: `sirius_tests/test_sympy_og_bugs.py`

- [ ] **Step 1: Verify source counts**

Run:

```bash
python3 -c 'import ast,csv; rows=list(csv.DictReader(open("bugs_cards/sympy_og_tickets.csv",newline="",encoding="utf-8"))); tree=ast.parse(open("sirius_tests/test_sympy_og_bugs.py",encoding="utf-8").read()); tests=[n.name for n in tree.body if isinstance(n,ast.FunctionDef) and n.name.startswith("test_og_")]; print(len(rows),len({r["instance_id"] for r in rows}),len(tests))'
```

Expected output: `54 54 65`.

- [ ] **Step 2: Map tests to instance IDs**

For each `sympy__sympy-NNNNN`, select every function whose name begins with
`test_og_NNNNN_`. Preserve all matching functions when one ticket has multiple
regression checks.

- [ ] **Step 3: Confirm every ticket has a test**

Run:

```bash
python3 - <<'PY'
import ast
import csv

with open("bugs_cards/sympy_og_tickets.csv", newline="", encoding="utf-8") as source:
    rows = list(csv.DictReader(source))
tree = ast.parse(open("sirius_tests/test_sympy_og_bugs.py", encoding="utf-8").read())
tests = [
    node.name
    for node in tree.body
    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_og_")
]
for row in rows:
    number = row["instance_id"].rsplit("-", 1)[1]
    matches = [name for name in tests if name.startswith(f"test_og_{number}_")]
    if not matches:
        raise SystemExit(f"No regression check for {row['instance_id']}")
print(f"{len(rows)} tickets mapped")
PY
```

Expected output: `54 tickets mapped`.

### Task 2: Create cards 01 through 18

**Files:**
- Create: `bugs_cards/01_sympy__sympy-14711.md`
- Create: `bugs_cards/02_sympy__sympy-23534.md`
- Create: `bugs_cards/03_sympy__sympy-23824.md`
- Create: `bugs_cards/04_sympy__sympy-23950.md`
- Create: `bugs_cards/05_sympy__sympy-16766.md`
- Create: `bugs_cards/06_sympy__sympy-15017.md`
- Create: `bugs_cards/07_sympy__sympy-15809.md`
- Create: `bugs_cards/08_sympy__sympy-13551.md`
- Create: `bugs_cards/09_sympy__sympy-13480.md`
- Create: `bugs_cards/10_sympy__sympy-16886.md`
- Create: `bugs_cards/11_sympy__sympy-20590.md`
- Create: `bugs_cards/12_sympy__sympy-21847.md`
- Create: `bugs_cards/13_sympy__sympy-19637.md`
- Create: `bugs_cards/14_sympy__sympy-15349.md`
- Create: `bugs_cards/15_sympy__sympy-16450.md`
- Create: `bugs_cards/16_sympy__sympy-13372.md`
- Create: `bugs_cards/17_sympy__sympy-18189.md`
- Create: `bugs_cards/18_sympy__sympy-20916.md`

- [ ] **Step 1: Populate each template section**

Copy `ticket_description` byte-for-byte into a quadruple-fenced source-text
block so embedded triple backticks remain valid Markdown. Add a
Russian title and explanation, state the corrected behavior represented by the
assertions, embed the matching test body as the reproduction, list every exact
pytest selector, and copy `patch_files` as code paths.

- [ ] **Step 2: Check the batch**

Run `rg -n 'sympy__sympy-XXXXX|Баг NN|Вставить|Описать|test_NAME|path/to' bugs_cards/{01..18}_*.md`.
Expected: no matches.

### Task 3: Create cards 19 through 36

**Files:**
- Create: `bugs_cards/19_sympy__sympy-13031.md`
- Create: `bugs_cards/20_sympy__sympy-24213.md`
- Create: `bugs_cards/21_sympy__sympy-22456.md`
- Create: `bugs_cards/22_sympy__sympy-12419.md`
- Create: `bugs_cards/23_sympy__sympy-23262.md`
- Create: `bugs_cards/24_sympy__sympy-23413.md`
- Create: `bugs_cards/25_sympy__sympy-17318.md`
- Create: `bugs_cards/26_sympy__sympy-13647.md`
- Create: `bugs_cards/27_sympy__sympy-15875.md`
- Create: `bugs_cards/28_sympy__sympy-18211.md`
- Create: `bugs_cards/29_sympy__sympy-19954.md`
- Create: `bugs_cards/30_sympy__sympy-21612.md`
- Create: `bugs_cards/31_sympy__sympy-24539.md`
- Create: `bugs_cards/32_sympy__sympy-17139.md`
- Create: `bugs_cards/33_sympy__sympy-19495.md`
- Create: `bugs_cards/34_sympy__sympy-13615.md`
- Create: `bugs_cards/35_sympy__sympy-20801.md`
- Create: `bugs_cards/36_sympy__sympy-19346.md`

- [ ] **Step 1: Populate each template section**

For every file, copy `ticket_description` byte-for-byte into a quadruple-fenced
source-text block. Add a Russian title and explanation, state the corrected
behavior represented by the assertions, embed the matching test body as the
reproduction, list every exact pytest selector, and copy `patch_files` as code
paths. Ticket `17139` and every other ticket with multiple matching functions
must list all selectors and include all relevant assertion scenarios.

- [ ] **Step 2: Check the batch**

Run `rg -n 'sympy__sympy-XXXXX|Баг NN|Вставить|Описать|test_NAME|path/to' bugs_cards/{19..36}_*.md`.
Expected: no matches.

### Task 4: Create cards 37 through 54

**Files:**
- Create: `bugs_cards/37_sympy__sympy-24661.md`
- Create: `bugs_cards/38_sympy__sympy-19783.md`
- Create: `bugs_cards/39_sympy__sympy-16792.md`
- Create: `bugs_cards/40_sympy__sympy-19040.md`
- Create: `bugs_cards/41_sympy__sympy-21379.md`
- Create: `bugs_cards/42_sympy__sympy-21930.md`
- Create: `bugs_cards/43_sympy__sympy-13852.md`
- Create: `bugs_cards/44_sympy__sympy-20154.md`
- Create: `bugs_cards/45_sympy__sympy-20428.md`
- Create: `bugs_cards/46_sympy__sympy-13757.md`
- Create: `bugs_cards/47_sympy__sympy-13974.md`
- Create: `bugs_cards/48_sympy__sympy-24443.md`
- Create: `bugs_cards/49_sympy__sympy-21596.md`
- Create: `bugs_cards/50_sympy__sympy-22080.md`
- Create: `bugs_cards/51_sympy__sympy-13877.md`
- Create: `bugs_cards/52_sympy__sympy-18199.md`
- Create: `bugs_cards/53_sympy__sympy-15976.md`
- Create: `bugs_cards/54_sympy__sympy-13878.md`

- [ ] **Step 1: Populate each template section**

For every file, copy `ticket_description` byte-for-byte into a quadruple-fenced
source-text block. Add a Russian title and explanation, state the corrected
behavior represented by the assertions, embed the matching test body as the
reproduction, list every exact pytest selector, and copy `patch_files` as code
paths. Tickets `19783`, `21930`, `20154`, and `22080` must preserve every
matching test selector and scenario.

- [ ] **Step 2: Check the batch**

Run `rg -n 'sympy__sympy-XXXXX|Баг NN|Вставить|Описать|test_NAME|path/to' bugs_cards/{37..54}_*.md`.
Expected: no matches.

### Task 5: Validate and commit the complete card set

**Files:**
- Verify: `bugs_cards/[0-9][0-9]_sympy__sympy-*.md`

- [ ] **Step 1: Validate cardinality, names, IDs, source text, tests, paths, and code fences**

Run:

```bash
python3 - <<'PY'
import ast
import csv
from pathlib import Path

with open("bugs_cards/sympy_og_tickets.csv", newline="", encoding="utf-8") as source:
    rows = list(csv.DictReader(source))
tree = ast.parse(Path("sirius_tests/test_sympy_og_bugs.py").read_text(encoding="utf-8"))
tests = [
    node.name
    for node in tree.body
    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_og_")
]
cards = sorted(Path("bugs_cards").glob("[0-9][0-9]_sympy__sympy-*.md"))
if len(cards) != len(rows):
    raise SystemExit(f"Expected {len(rows)} cards, found {len(cards)}")
for index, row in enumerate(rows, 1):
    expected = Path("bugs_cards") / f"{index:02d}_{row['instance_id']}.md"
    if expected not in cards:
        raise SystemExit(f"Missing {expected}")
    text = expected.read_text(encoding="utf-8")
    number = row["instance_id"].rsplit("-", 1)[1]
    matching_tests = [name for name in tests if name.startswith(f"test_og_{number}_")]
    required = [row["instance_id"], row["ticket_description"].strip()]
    required.extend(f"::{name}" for name in matching_tests)
    required.extend(path.strip() for path in row["patch_files"].split("|") if path.strip())
    missing = [value for value in required if value not in text]
    if missing:
        raise SystemExit(f"{expected}: missing {missing}")
    if text.count("````") != 2 or text.count("```") % 2:
        raise SystemExit(f"{expected}: unbalanced Markdown fences")
print(f"{len(cards)} cards valid")
PY
```

Expected output: `54 cards valid`.

- [ ] **Step 2: Run repository checks**

Run:

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only 54 new card files are shown relative to
the plan commit.

- [ ] **Step 3: Commit the cards**

```bash
git add bugs_cards/[0-9][0-9]_sympy__sympy-*.md
git commit -m "docs: add Sirius OG bug cards"
```
