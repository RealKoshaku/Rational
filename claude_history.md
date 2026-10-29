# Journal des actions de Claude

- 2026-10-27 — `uv python pin 3.14` : `.python-version` passe de 3.13 à 3.14. `uv sync` : `.venv` recréé avec Python 3.14.7.
- 2026-10-27 — Création de `CLAUDE.md` via `/init` (commandes, architecture de `Rational`, conventions).
- 2026-10-27 — Commit de `CLAUDE.md` (et mise à jour de `claude_history.md`).
- 2026-10-28 — Mise à jour de `CLAUDE.md` via `/init` (commandes pytest, section Tests, dépendance pytest).
- 2026-10-28 — Amélioration de `tests/unit/test_rational.py` (normalisation, ZeroDivisionError, +, -, *, /, types non supportés).
- 2026-10-28 — Mise à jour de la section Tests de `CLAUDE.md`.
- 2026-10-28 — Commit et push des tests améliorés, de `CLAUDE.md` et de `claude_history.md`.
- 2026-10-28 — `tests/unit/test_rational.py` : les tests de +, -, * et / comparent maintenant `(num, den)` (vérifie aussi la normalisation).
- 2026-10-28 — Commit et push de la correction des tests (comparaison de tuples) et du saut de ligne final de `pyproject.toml`.
- 2026-10-28 — Création de `ROADMAP.md` (roadmap cochable du projet).
- 2026-10-28 — Commit et push de `ROADMAP.md`.
- 2026-10-29 — Mise à jour de `CLAUDE.md` via `/init` (dataclass figée, `__hash__`/`__eq__`, support des `int`, tests, ROADMAP).
- 2026-10-29 — Création de `tests/unit/test_rational_refonte.py` (nouvelle version des tests, basée sur `test_rational.py`).
- 2026-10-29 — Mise à jour de `CLAUDE.md` via `/init` (int dans `*` et `/`, plus de `__neg__`, test_rational_refonte.py).
- 2026-10-29 — Ajout dans `tests/unit/test_rational_refonte.py` des tests des opérations avec `int` (+, -, *, /, division par 0, refus des `bool`, propriétés).
