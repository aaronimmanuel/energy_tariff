# Lab 5: Energy Consumption & Tariff Calculator

This folder contains the completed work for the linked [starter repository](https://github.com/SETAPESU26/L5_03_energy_tariff).

## Run

Requires Python 3.10 or newer. The program uses only the Python standard
library, so no package installation is needed.

```powershell
python energy_system.py
```

Enter an optional nonnegative number of extra units when prompted, or press
Enter to skip it. Meter totals and reading history are saved in
`meters.json` in the current working directory. The program uses three
progressive tiers: the first 100 units, the next 200, and units above 300.

## Lab deliverables

- `energy_system.py`: cleaned calculator with input validation, safe JSON
  persistence, and the original tiered billing behavior.
- `issues.md`: issue table with severity/category, starter line references,
  descriptions, and fixes.
- `reflection.md`: four learning-outcome reflections. The linked repository
  references a separate handout for its exact prompts, which was not included.
- `reports/after/`: final Pylint, Flake8, and Bandit results.

The assignment also asks you to retain baseline reports while working. The
provided workspace had no starter checkout or baseline reports; `issues.md`
records this limitation. The repository README lists only the three files
above as final deliverables.
