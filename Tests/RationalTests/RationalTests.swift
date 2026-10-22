import Testing
@testable import Rational

/// Shorthand for building a `Rational`.
private func r(_ num: Int, _ den: Int = 1) -> Rational {
    Rational(num: num, den: den)
}

/// Checks the invariant enforced by `init`: reduced fraction, `den > 0`, zero is `0/1`.
private func expectNormalized(_ x: Rational, sourceLocation: SourceLocation = #_sourceLocation) {
    #expect(x.den > 0, sourceLocation: sourceLocation)
    #expect(pgcd(abs(x.num), x.den) == (x.num == 0 ? x.den : 1), sourceLocation: sourceLocation)
    if x.num == 0 {
        #expect(x.den == 1, sourceLocation: sourceLocation)
    }
}

// MARK: - pgcd

@Test("pgcd", arguments: [
    (12, 18, 6),
    (18, 12, 6),
    (17, 5, 1),
    (7, 7, 7),
    (9, 1, 1),
    (0, 9, 9),
    (9, 0, 9),
    (100, 75, 25),
])
func pgcdValues(a: Int, b: Int, expected: Int) {
    #expect(pgcd(a, b) == expected)
}

// MARK: - Initialization

struct Case: Sendable, CustomTestStringConvertible {
    let num: Int
    let den: Int
    let expectedNum: Int
    let expectedDen: Int

    var testDescription: String { "\(num)/\(den) -> \(expectedNum)/\(expectedDen)" }
}

@Test("Reduction to lowest terms and sign normalization", arguments: [
    Case(num: 1, den: 2, expectedNum: 1, expectedDen: 2),
    Case(num: 2, den: 4, expectedNum: 1, expectedDen: 2),
    Case(num: 6, den: 9, expectedNum: 2, expectedDen: 3),
    Case(num: 7, den: 1, expectedNum: 7, expectedDen: 1),
    Case(num: 5, den: 5, expectedNum: 1, expectedDen: 1),
    Case(num: 10, den: 4, expectedNum: 5, expectedDen: 2),
    Case(num: -1, den: 2, expectedNum: -1, expectedDen: 2),
    Case(num: 1, den: -2, expectedNum: -1, expectedDen: 2),
    Case(num: -1, den: -2, expectedNum: 1, expectedDen: 2),
    Case(num: -6, den: -9, expectedNum: 2, expectedDen: 3),
    Case(num: 6, den: -9, expectedNum: -2, expectedDen: 3),
    Case(num: 0, den: 5, expectedNum: 0, expectedDen: 1),
    Case(num: 0, den: -5, expectedNum: 0, expectedDen: 1),
])
func reduction(_ c: Case) {
    let x = Rational(num: c.num, den: c.den)
    #expect(x.num == c.expectedNum)
    #expect(x.den == c.expectedDen)
}

@Test("init(num:) builds num/1", arguments: [5, 0, -3])
func integerInit(n: Int) {
    let x = Rational(num: n)
    #expect(x.num == n)
    #expect(x.den == 1)
}

@Test("init() is zero")
func defaultInit() {
    let x = Rational()
    #expect(x.num == 0)
    #expect(x.den == 1)
}

@Test("Zero denominator is a precondition failure", arguments: [-3, 0, 4])
func zeroDenominator(num: Int) async {
    await #expect(processExitsWith: .failure) { [num] in
        _ = Rational(num: num, den: 0)
    }
}

// MARK: - Description

@Test("Description", arguments: [
    (1, 2, "1 / 2"),
    (2, -4, "-1 / 2"),
    (0, 3, "0 / 1"),
    (5, 1, "5 / 1"),
])
func description(num: Int, den: Int, expected: String) {
    #expect(Rational(num: num, den: den).description == expected)
}

// MARK: - Equality

@Test("Equivalent fractions are equal", arguments: [
    (1, 2, 2, 4),
    (1, 2, -1, -2),
    (-1, 2, 1, -2),
    (0, 3, 0, -7),
    (6, 3, 2, 1),
])
func equalFractions(a: Int, b: Int, c: Int, d: Int) {
    #expect(r(a, b) == r(c, d))
}

@Test("Different fractions are not equal", arguments: [
    (1, 2, 1, 3),
    (1, 2, -1, 2),
    (0, 1, 1, 1),
    (2, 3, 3, 2),
])
func differentFractions(a: Int, b: Int, c: Int, d: Int) {
    #expect(r(a, b) != r(c, d))
}

@Test("Default init equals zero")
func defaultEqualsZero() {
    #expect(Rational() == r(0, 5))
}

// MARK: - Arithmetic

struct Operation: Sendable, CustomTestStringConvertible {
    let lhs: (Int, Int)
    let rhs: (Int, Int)
    let expected: (Int, Int)

    var testDescription: String { "\(lhs.0)/\(lhs.1), \(rhs.0)/\(rhs.1) -> \(expected.0)/\(expected.1)" }
}

@Test("Addition", arguments: [
    Operation(lhs: (1, 2), rhs: (1, 3), expected: (5, 6)),
    Operation(lhs: (1, 2), rhs: (1, 2), expected: (1, 1)),
    Operation(lhs: (1, 2), rhs: (-1, 2), expected: (0, 1)),
    Operation(lhs: (-1, 3), rhs: (-1, 6), expected: (-1, 2)),
    Operation(lhs: (0, 1), rhs: (3, 4), expected: (3, 4)),
    Operation(lhs: (7, 4), rhs: (1, 4), expected: (2, 1)),
])
func addition(_ o: Operation) {
    let result = r(o.lhs.0, o.lhs.1) + r(o.rhs.0, o.rhs.1)
    #expect(result == r(o.expected.0, o.expected.1))
    expectNormalized(result)
}

@Test("Subtraction", arguments: [
    Operation(lhs: (1, 2), rhs: (1, 3), expected: (1, 6)),
    Operation(lhs: (1, 3), rhs: (1, 2), expected: (-1, 6)),
    Operation(lhs: (1, 2), rhs: (1, 2), expected: (0, 1)),
    Operation(lhs: (1, 2), rhs: (-1, 2), expected: (1, 1)),
    Operation(lhs: (3, 4), rhs: (0, 1), expected: (3, 4)),
    Operation(lhs: (0, 1), rhs: (3, 4), expected: (-3, 4)),
])
func subtraction(_ o: Operation) {
    let result = r(o.lhs.0, o.lhs.1) - r(o.rhs.0, o.rhs.1)
    #expect(result == r(o.expected.0, o.expected.1))
    expectNormalized(result)
}

@Test("Multiplication", arguments: [
    Operation(lhs: (1, 2), rhs: (1, 3), expected: (1, 6)),
    Operation(lhs: (2, 3), rhs: (3, 2), expected: (1, 1)),
    Operation(lhs: (-1, 2), rhs: (1, 3), expected: (-1, 6)),
    Operation(lhs: (-1, 2), rhs: (-1, 3), expected: (1, 6)),
    Operation(lhs: (0, 1), rhs: (5, 7), expected: (0, 1)),
    Operation(lhs: (1, 1), rhs: (5, 7), expected: (5, 7)),
    Operation(lhs: (4, 9), rhs: (3, 8), expected: (1, 6)),
])
func multiplication(_ o: Operation) {
    let result = r(o.lhs.0, o.lhs.1) * r(o.rhs.0, o.rhs.1)
    #expect(result == r(o.expected.0, o.expected.1))
    expectNormalized(result)
}

@Test("Division", arguments: [
    Operation(lhs: (1, 2), rhs: (1, 3), expected: (3, 2)),
    Operation(lhs: (1, 2), rhs: (1, 2), expected: (1, 1)),
    Operation(lhs: (1, 2), rhs: (-1, 3), expected: (-3, 2)),
    Operation(lhs: (-1, 2), rhs: (-1, 3), expected: (3, 2)),
    Operation(lhs: (0, 1), rhs: (5, 7), expected: (0, 1)),
    Operation(lhs: (5, 7), rhs: (1, 1), expected: (5, 7)),
    Operation(lhs: (4, 9), rhs: (8, 3), expected: (1, 6)),
])
func division(_ o: Operation) {
    let result = r(o.lhs.0, o.lhs.1) / r(o.rhs.0, o.rhs.1)
    #expect(result == r(o.expected.0, o.expected.1))
    expectNormalized(result)
}

@Test("Division by a zero rational is a precondition failure", arguments: [(1, 2), (0, 1), (-3, 4)])
func divisionByZero(num: Int, den: Int) async {
    await #expect(processExitsWith: .failure) { [num, den] in
        _ = Rational(num: num, den: den) / Rational()
    }
}

@Test("Division by zero Int is a precondition failure")
func divisionByZeroInt() async {
    await #expect(processExitsWith: .failure) {
        _ = Rational(num: 1, den: 2) / 0
    }
}

// MARK: - Int overloads

@Test("Int overloads match the Rational operators")
func intOverloads() {
    let x = r(1, 2)

    #expect(x + 1 == r(3, 2))
    #expect(1 + x == r(3, 2))

    #expect(x - 1 == r(-1, 2))
    #expect(1 - x == r(1, 2))

    #expect(x * 3 == r(3, 2))
    #expect(3 * x == r(3, 2))

    #expect(x / 2 == r(1, 4))
    #expect(2 / x == r(4, 1))
}

// MARK: - Algebraic properties

private var samples: [Rational] { [r(1, 2), r(-2, 3), r(0, 1), r(5, 1), r(-7, 4), r(3, 10)] }

@Test("Addition and multiplication are commutative")
func commutativity() {
    for a in samples {
        for b in samples {
            #expect(a + b == b + a)
            #expect(a * b == b * a)
        }
    }
}

@Test("Neutral elements")
func neutralElements() {
    for a in samples {
        #expect(a + Rational() == a)
        #expect(a - Rational() == a)
        #expect(a * r(1) == a)
        #expect(a / r(1) == a)
    }
}

@Test("a - a is zero and a / a is one")
func inverseOperations() {
    for a in samples {
        #expect(a - a == Rational())
        if a != Rational() {
            #expect(a / a == r(1))
        }
    }
}

@Test("Results of all operations stay normalized")
func resultsAreNormalized() {
    for a in samples {
        for b in samples {
            expectNormalized(a + b)
            expectNormalized(a - b)
            expectNormalized(a * b)
            if b != Rational() {
                expectNormalized(a / b)
            }
        }
    }
}
