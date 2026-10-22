# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`Rational` is a small Swift Package Manager library (a single `Rational` library product) implementing a rational-number type. It is early-stage: `Sources/Rational/Rational.swift` holds the `Rational` struct (with `Equatable` and `CustomStringConvertible` conformances) and `Sources/Rational/Tools.swift` holds the public `pgcd` helper. `Sources/Demo/main.swift` is a throwaway executable target for trying the library by hand. `TODO.md` is the owner's roadmap; the owner is writing the code themselves, so don't implement roadmap items unless asked. There is no README, CI, or lint config.

## Commands

- Build: `swift build`
- Run all tests: `swift test`
- Try the library manually: `swift run Demo` (never put a `main.swift` in `Sources/Rational`: it turns the library target into an executable and breaks the build)
- Run a single test: `swift test --filter RationalTests/reduction` (filter is `<TestTarget>/<testName>` regex)

Tests use Swift Testing (`import Testing`, `@Test`, `#expect`), not XCTest. Tests use `@testable import Rational`, so internal members are accessible from tests.

## Notes

- `Package.swift` uses `swift-tools-version: 6.4` and enables the `ApproachableConcurrency` upcoming feature on the library, `Demo` and test targets; keep all targets' `swiftSettings` in sync.
- `Rational.init(num:den:)` is `public` and non-throwing: a zero denominator is a `precondition` failure (crash), not a thrown error. There is no error type (`RationalError` was removed). `init(num:)` and `init()` are convenience inits that delegate to it; new inits should do the same so the invariant lives in one place.
- Invariant enforced by `init`: the fraction is reduced by the gcd (`pgcd` assumes non-negative inputs, so callers pass `abs` values) and the sign lives on the numerator (`den` is always > 0, zero is `0/1`). Preserve this when adding equality, comparison, or arithmetic.
- `num`/`den` are `private(set)` and internal, so they are not visible from `Demo` or other packages. Expose them explicitly if the API is meant to be consumed externally.
- `==` compares by cross-multiplication (`lhs.num * rhs.den == lhs.den * rhs.num`), which can overflow `Int` for large values.
- `description` renders as `"\(num) / \(den)"` (spaces around the slash); the `Description` test asserts this exact format.
- `claude_history.md` at the repo root is a running log of actions taken in the repo; append an entry for each change you make.
