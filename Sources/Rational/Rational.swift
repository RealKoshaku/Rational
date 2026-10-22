// The Swift Programming Language
// https://docs.swift.org/swift-book

import Foundation

enum RationalError: Error {
    case zeroAtDenominator
}

public struct Rational {
    private(set) var num: Int
    private(set) var den: Int
    public init(num: Int, den: Int) {
        precondition(den != 0, "Zero at denominator") // a/b with b != 0
        
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
