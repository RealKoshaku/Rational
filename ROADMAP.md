# Roadmap

Projet d'apprentissage : une classe `Rational` (fraction) en Python.

## Fait

- [x] Constructeur normalisé (pgcd, dénominateur positif, `ZeroDivisionError`)
- [x] `__eq__`, `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__str__`
- [x] Tests `pytest` paramétrés (normalisation, opérateurs, types non supportés)
- [x] Configuration `pytest` dans `pyproject.toml`
- [x] `CLAUDE.md` et `claude_history.md`

## 1. Finitions de l'existant

- [x] Ajouter les annotations manquantes sur `__mul__` et `__truediv__` (`other: object`, `-> Rational`)
- [x] Ajouter `__repr__` (ex. `Rational(1, 2)`) et l'utiliser dans les messages d'échec de pytest
- [ ] Message d'erreur explicite pour la division par un `Rational` nul dans `__truediv__`
- [ ] Remplacer le stub `main()` de `src/rational/__init__.py` par un vrai point d'entrée (ou retirer le script `rational`)
- [ ] Compléter le `README.md` (description, installation, exemples d'utilisation)
- [ ] Mettre une vraie `description` dans `pyproject.toml`

## 2. Opérateurs manquants

- [ ] `__neg__` et `__abs__`
- [ ] `__bool__` (faux pour zéro)
- [x] `__hash__` cohérent avec `__eq__` (aujourd'hui la classe n'est pas hashable)
- [x] Comparaisons `__lt__`, `__le__`, `__gt__`, `__ge__` (ou `functools.total_ordering`)
- [ ] `__pow__` avec exposant entier (négatif inclus)
- [ ] Tests pour chaque nouvel opérateur

## 3. Interopérabilité

- [ ] Accepter les `int` dans les opérateurs (`Rational(1, 2) + 1`)
- [ ] Opérateurs inverses `__radd__`, `__rsub__`, `__rmul__`, `__rtruediv__` (`1 + Rational(1, 2)`)
- [ ] `__eq__` avec un `int` (`Rational(2, 1) == 2`)
- [ ] `__float__` et `__int__`
- [ ] Construction depuis une chaîne (`"3/4"`) et/ou un `float`
- [ ] Mettre à jour les tests : les cas « autre type » avec `int` ne doivent plus lever `TypeError`

## 4. Qualité et outillage

- [ ] Déplacer `pytest` dans un groupe de dépendances de développement
- [ ] Ajouter un linter/formatter (ex. `ruff`) et documenter la commande dans `CLAUDE.md`
- [ ] Ajouter un vérificateur de types (ex. `mypy` ou `pyright`)
- [ ] Mesurer la couverture de tests (`pytest-cov`)
- [ ] Tests par propriétés avec `hypothesis` (associativité, distributivité, `a - a == 0`)
- [ ] Intégration continue (GitHub Actions : `uv sync` puis `uv run pytest`)

## 5. Pour aller plus loin

- [ ] Réexporter `Rational` depuis `rational/__init__.py` (`from rational import Rational`)
- [ ] Rendre la classe immuable (`__slots__`, propriétés en lecture seule, ou `dataclass(frozen=True)`)
- [ ] Comparer avec `fractions.Fraction` de la bibliothèque standard
- [ ] Publier le paquet (build `uv_build`, puis `uv publish`)
