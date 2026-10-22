# TODO — Module Rational

Prochaines étapes, dans un ordre conseillé. Chaque étape doit conserver l'invariant de `init` : fraction réduite, `den > 0`, zéro = `0/1`. Écris les tests **avant** ou **en même temps** que le code.

## 1. Fondations

- [x] Décider de l'API publique : rendre `num` et `den` lisibles de l'extérieur (`public private(set)`) ou non.
- [x] Décider du sort de `RationalError` : l'utiliser (init faillible / `throws`) ou le supprimer, puisque le `precondition` est déjà en place.
- [x] Ajouter un init pratique à partir d'un entier seul (`Rational(3)` = `3/1`).
- [ ] Réfléchir au débordement : `Int` peut déborder (`Int.min`, `abs`, produits en croix). Choisir une stratégie (crash, `multipliedReportingOverflow`, ou autre) et la documenter.

## 2. Conformances de base

- [ ] `Equatable` : grâce à la forme réduite, l'égalité peut comparer `num` et `den` directement (vérifier que c'est bien suffisant).
- [ ] `Hashable` : cohérent avec `==`.
- [ ] `Comparable` : comparer `a/b` et `c/d` sans passer par des flottants (attention au signe et au débordement).
- [ ] Tests : égalité de formes équivalentes (`1/2` == `2/4` == `-1/-2`), ordre avec des négatifs, zéro.

## 3. Arithmétique

- [ ] Addition, soustraction, multiplication, division (division par zéro rationnel = cas à traiter explicitement).
- [ ] Négation (`-x`) et valeur absolue.
- [ ] Inverse (réciproque) : que faire pour `0` ?
- [ ] Puissance entière (exposants négatifs inclus).
- [ ] Opérateurs composés (`+=`, `-=`, `*=`, `/=`).
- [ ] Tests : éléments neutres, commutativité/associativité, résultats toujours réduits, cas limites proches de `Int.max`.

## 4. Intégration avec Swift

- [ ] `ExpressibleByIntegerLiteral` (`let x: Rational = 3`).
- [ ] Éventuellement `Numeric` / `SignedNumeric` (voir ce que le protocole exige, notamment `magnitude`).
- [ ] Conversion vers `Double` et, optionnellement, depuis un `Double` (approximation par fractions continues).
- [ ] Séparer `description` (affichage lisible) d'une éventuelle `debugDescription`.
- [ ] Parsing depuis une chaîne (`"3/4"`) — décider du format accepté et du comportement en cas d'erreur.

## 5. Qualité et finitions

- [ ] Documenter l'API publique avec des commentaires `///`.
- [ ] `pgcd` : décider s'il reste `public` (utile ?) ou devient interne ; envisager une version itérative pour éviter la récursion.
- [ ] Ajouter un `README.md` (installation SPM, exemples d'usage).
- [ ] Ajouter une CI (par ex. GitHub Actions avec `swift test`).
- [ ] Penser à `Sendable`/`Codable` si le type doit voyager entre tâches ou être sérialisé.
