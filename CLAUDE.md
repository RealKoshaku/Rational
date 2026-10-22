# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`Rational` is a small Swift Package Manager library (a single `Rational` library product) implementing a rational-number type. It is early-stage: `Sources/Rational/Rational.swift` holds the `Rational` struct and `Sources/Rational/Tools.swift` holds the public `pgcd` helper. There is no README, CI, or lint config.

## Commands

- Build: `swift build`
- Run all tests: `swift test`
- Run a single test: `swift test --filter RationalTests/reduction` (filter is `<TestTarget>/<testName>` regex)

Tests use Swift Testing (`import Testing`, `@Test`, `#expect`), not XCTest. Tests use `@testable import Rational`, so internal members are accessible from tests.

## Notes

- `Package.swift` uses `swift-tools-version: 6.4` and enables the `ApproachableConcurrency` upcoming feature on both the library and test targets; keep both targets' `swiftSettings` in sync.
- `Rational.init(num:den:)` is `public` and non-throwing: a zero denominator is a `precondition` failure (crash), not a thrown error. `RationalError.zeroAtDenominator` is still declared (internal) but currently unused by the initializer.
- Invariant enforced by `init`: the fraction is reduced by the gcd (`pgcd` assumes non-negative inputs, so callers pass `abs` values) and the sign lives on the numerator (`den` is always > 0, zero is `0/1`). Preserve this when adding equality, comparison, or arithmetic.
- `num`/`den` are `private(set)` and internal; `RationalError` is internal. Expose them explicitly if the API is meant to be consumed externally.
