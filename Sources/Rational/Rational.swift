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
        guard den != 0 else {throw RationalError.zeroAtDenominator}
        let g = pgcd(num, den)
        self.num = num / g
        self.den = den / g
    }
}
