//
//  Tools.swift
//  Rational
//
//  Created by Adahy Plas on 22/10/2026.
//

import Foundation

public func pgcd(_ a: Int, _ b: Int) -> Int {
    b == 0 ? a : pgcd(b, a % b)
}

