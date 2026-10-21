# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`Rational` is a small Swift Package Manager library (a single `Rational` library product) implementing a rational-number type. It is early-stage: `Sources/Rational/Rational.swift` currently holds only the `Rational` struct (`num`/`den`, reduced via a recursive `pgcd` helper in a throwing initializer) and a `RationalError.zeroAtDenominator` error. There is no README, CI, or lint config.

## Commands

- Build: `swift build`
- Run all tests: `swift test`
- Run a single test: `swift test --filter RationalTests/example` (filter is `<TestTarget>/<testName>` regex)

Tests use Swift Testing (`import Testing`, `@Test`, `#expect`), not XCTest. Tests use `@testable import Rational`, so internal members are accessible from tests.

## Notes

- `Package.swift` uses `swift-tools-version: 6.4` and enables the `ApproachableConcurrency` upcoming feature on both the library and test targets; keep both targets' `swiftSettings` in sync.
- `Rational`'s stored properties and initializer are currently internal (not `public`), and `RationalError` is internal; expose them explicitly if the library API is meant to be consumed externally.
- `pgcd` does not normalize sign, so a negative denominator or negative gcd result can yield non-canonical forms (e.g. a negative `den`); account for this when adding equality, comparison, or arithmetic.
