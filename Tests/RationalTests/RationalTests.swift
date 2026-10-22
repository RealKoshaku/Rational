import Testing
@testable import Rational

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
    Case(num: -1, den: 2, expectedNum: -1, expectedDen: 2),
    Case(num: 1, den: -2, expectedNum: -1, expectedDen: 2),
    Case(num: -1, den: -2, expectedNum: 1, expectedDen: 2),
    Case(num: -6, den: -9, expectedNum: 2, expectedDen: 3),
    Case(num: 6, den: -9, expectedNum: -2, expectedDen: 3),
    Case(num: 0, den: 5, expectedNum: 0, expectedDen: 1),
    Case(num: 0, den: -5, expectedNum: 0, expectedDen: 1),
])
func reduction(_ c: Case) {
    let r = Rational(num: c.num, den: c.den)
    #expect(r.num == c.expectedNum)
    #expect(r.den == c.expectedDen)
}

@Test("Zero denominator is a precondition failure", arguments: [-3, 0, 4])
func zeroDenominator(num: Int) async {
    await #expect(processExitsWith: .failure) { [num] in
        _ = Rational(num: num, den: 0)
    }
}

@Test("Description", arguments: [
    (1, 2, "1 / 2"),
    (2, -4, "-1 / 2"),
    (0, 3, "0 / 1"),
])
func description(num: Int, den: Int, expected: String) {
    #expect(Rational(num: num, den: den).description == expected)
}
