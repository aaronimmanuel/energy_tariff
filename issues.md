# Static analysis issue log

The line numbers below refer to the supplied starter `energy_system.py`.
High and medium severity issues are listed first. The first five are fixed in
the cleaned file.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Arbitrary code execution with `eval` | Security (High) | 66 | User-provided text is evaluated as Python, allowing arbitrary code execution. | Parse a numeric value with `float`, validate it, and report invalid input. |
| Mutable default history | Correctness (Medium) | 18 | `history=[]` is shared across calls, so readings leak between separate sessions/calls. | Store history in explicit module state and create a new entry for each call. |
| Negative usage accepted | Correctness (Medium) | 60 | The demo records `-50`, reducing a meter's accumulated usage and creating nonsensical bills. | Reject negative readings before changing state. |
| Broad exception silently masks failures | Reliability (Medium) | 38–40 | Bare `except` hides permission, parse, and programming errors by resetting all readings. | Handle missing files separately and surface malformed/unreadable data clearly. |
| File handles not safely closed | Reliability (Medium) | 37–49 | The load file is not closed explicitly, and a save error can skip `close()`. | Use context managers and explicit UTF-8 encoding for both operations. |
| Missing meter causes unhelpful key error | Robustness (Low) | 25 | `compute_bill` directly indexes a missing key without clear validation. | Keep the clear `KeyError` behavior and document that the meter must exist. |
| Global state and weak input validation | Maintainability | 8–16, 18 | Totals and rates are mutable globals; identifiers, units, rates, and input are unchecked. | Add type hints, validate user-facing values, and keep state changes explicit. |

## Verification summary

The cleaned program was checked with Pylint, Flake8, and Bandit. The full
reports are in `reports/after/`. The starter source and original report files
were not present in the supplied workspace, so `reports/before/` cannot be
recreated from an executed baseline here; the issue list is based on the
linked GitHub starter source.
