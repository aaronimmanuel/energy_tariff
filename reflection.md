# Reflection

The linked repository refers to four reflection questions in a separate lab
handout, but that handout is not included in the repository or workspace. These
four responses address the lab's stated learning goals and can be mapped to
the handout wording if it is provided.

## 1. How did static analysis help?

Pylint and Flake8 exposed maintainability and style problems that are easy to
miss during a quick manual read. Bandit identified the use of `eval` on user
input, which was the most serious issue because it could execute arbitrary
Python code. Tool output helped prioritize the fix, while runtime checks were
still needed for calculation and persistence behavior.

## 2. Which tool was most useful, and why?

Bandit was most useful for finding the unsafe `eval` call. Pylint gave broader
feedback on documentation, naming, and structure, while Flake8 made the
formatting and import issues quick to locate. They cover different concerns,
so the combined results were more useful than any single tool.

## 3. What required judgment beyond the tools?

The tools can identify suspicious constructs, but they cannot decide the
intended business rules. I treated readings as nonnegative, retained the
three-tier progressive tariff calculation, and made malformed saved data
visible instead of silently discarding it. I also checked the starter's
negative demo reading as a functional bug, not just a style finding.

## 4. How does static analysis contribute to maintainability?

Repeatable checks give future edits a consistent way to catch regressions.
Clear validation and error messages make failures easier to diagnose, and
documentation makes the meter and tariff behavior easier to review. Static
analysis complements runtime verification; it does not prove the calculations
or file handling work correctly for real use cases.
