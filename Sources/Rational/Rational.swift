// The Swift Programming Language
// https://docs.swift.org/swift-book

import Foundation

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
    
    public init(num: Int) {
        self.init(num: num, den: 1)
    }
    
    public init() {
        self.init(num: 0)
    }
    
}

extension Rational: CustomStringConvertible {
    public var description: String {
        "\(num) / \(den)"
    }
}

extension Rational {
    // Addition
    public static func + (lhs: Rational, rhs: Rational) -> Rational {
        return Rational(num: lhs.num * rhs.den + lhs.den * rhs.num, den: lhs.den * rhs.den)
    }
    
    public static func + (lhs: Int, rhs: Rational) -> Rational {
        return Rational(num: lhs) + rhs
    }
    
    public static func + (lhs: Rational, rhs: Int) -> Rational {
        return lhs + Rational(num: rhs)
    }
    
    // Soustraction
    public static func - (lhs: Rational, rhs: Rational) -> Rational {
        return lhs + Rational(num: -rhs.num, den: rhs.den)
    }
    
    public static func - (lhs: Rational, rhs: Int) -> Rational {
        return lhs - Rational(num: rhs)
    }
    
    public static func - (lhs: Int, rhs: Rational) -> Rational {
        return Rational(num: lhs) - rhs
    }
    
    // Multiplication
    public static func * (lhs: Rational, rhs: Rational) -> Rational {
        return Rational(num: lhs.num * rhs.num, den: lhs.den * rhs.den)
    }
    
    public static func * (lhs: Int, rhs: Rational) -> Rational {
        return Rational(num: lhs) * rhs
    }
    
    public static func * (lhs: Rational, rhs: Int) -> Rational {
        return rhs * lhs
    }
    
    // Division
    public static func / (lhs: Rational, rhs: Rational) -> Rational {
        precondition(rhs.num != 0, "Cannot divide by zero.")
        return Rational(num: lhs.num * rhs.den, den: lhs.den * rhs.num)
    }
    
    public static func / (lhs: Rational, rhs: Int) -> Rational {
        return lhs / Rational(num: rhs)
    }
    
    public static func / (lhs: Int, rhs: Rational) -> Rational {
        return Rational(num: lhs) / rhs
    }
}

extension Rational: Equatable {
    public static func == (lhs: Rational, rhs: Rational) -> Bool {
        return lhs.num * rhs.den == lhs.den * rhs.num
    }
}
