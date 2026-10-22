import Rational
print(Rational(num: 1, den: 0))
// Réduction
print(Rational(num: 6, den: 3))     // 2 / 1
print(Rational(num: 3, den: 6))     // 1 / 2
print(Rational(num: 10, den: 4))    // 5 / 2

// Normalisation du signe (le signe va sur le numérateur)
print(Rational(num: 3, den: -6))    // -1 / 2
print(Rational(num: -3, den: -6))   // 1 / 2
print(Rational(num: -3, den: 6))    // -1 / 2

// Zéro : toujours 0 / 1
print(Rational(num: 0, den: 5))     // 0 / 1
print(Rational(num: 0, den: -5))    // 0 / 1

// Déjà irréductible
print(Rational(num: 7, den: 13))    // 7 / 13

// Inits de commodité
print(Rational(num: 5))             // 5 / 1
print(Rational())                   // 0 / 1

// Égalité
print(Rational(num: 1, den: 2) == Rational(num: 2, den: 4))    // true
print(Rational(num: 1, den: 2) == Rational(num: -1, den: -2))  // true
print(Rational(num: 1, den: 2) == Rational(num: 1, den: 3))    // false
print(Rational(num: 0, den: 3) == Rational())                  // true

// pgcd (suppose des entrées positives)
print(pgcd(12, 18))                 // 6
print(pgcd(17, 5))                  // 1
print(pgcd(0, 9))                   // 9

// Dénominateur nul : plante volontairement (precondition), donc désactivé
// print(Rational(num: 1, den: 0))
