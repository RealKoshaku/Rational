// The Swift Programming Language
// https://docs.swift.org/swift-book

import Foundation

enum RationalError: Error {
    case zeroAtDenominator
}

private func pgcd(_ a: Int, _ b: Int) -> Int {
    b == 0 ? a : pgcd(b, a % b)
}

public struct Rational {
    var num: Int
    var den: Int
    
    public init(num: Int, den: Int) throws {
        guard den != 0 else { throw RationalError.zeroAtDenominator }
        let gcd = pgcd(abs(num), abs(den))
        let sgn: Int = abs(den) / den // Compute the sign of den: -1 if den < 0 else 1 by definition of abs(.)
        self.num = sgn * num / gcd
        self.den = sgn * den / gcd
    }
    
}

extension Rational: CustomStringConvertible {
    public var description: String {
        "\(num) / \(den)"
    }
}
