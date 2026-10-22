# Rational

A small Swift package for computing with rational numbers (fractions of two `Int`s). It is an early-stage learning project: only construction, printing and equality exist so far.

## Requirements

Swift tools 6.4 or later (`swift-tools-version: 6.4`). No external dependencies.

## Add it to a project

No version tags exist yet, so depend on a local clone:

```sh
git clone git@github.com:RealKoshaku/Rational.git
```

Then, in your own `Package.swift` (also tools version 6.4 or later), with the clone next to your project (adjust the path otherwise):

```swift
// swift-tools-version: 6.4
import PackageDescription

let package = Package(
    name: "MyApp",
    dependencies: [
        .package(path: "../Rational"),
    ],
    targets: [
        .executableTarget(
            name: "MyApp",
            dependencies: [
                .product(name: "Rational", package: "Rational"),
            ]
        ),
    ]
)
```

## Build, test, run

```sh
swift build                                  # build
swift test                                   # all tests (Swift Testing, not XCTest)
swift test --filter RationalTests/reduction  # one test: <TestTarget>/<testName>
swift run Demo                               # run Sources/Demo/main.swift
```

`Demo` is a scratch executable for trying the library by hand; edit `Sources/Demo/main.swift` freely. Any active `Rational(num: _, den: 0)` in it traps (see below).

## Usage

```swift
import Rational

print(Rational(num: 6, den: 3))    // 2 / 1
print(Rational(num: 3, den: -6))   // -1 / 2
print(Rational(num: 0, den: -5))   // 0 / 1
print(Rational(num: 5))            // 5 / 1
print(Rational())                  // 0 / 1

print(Rational(num: 1, den: 2) == Rational(num: 2, den: 4))  // true
```

Public API: `Rational.init(num:den:)`, `init(num:)`, `init()`, `CustomStringConvertible`, `Equatable`, and `pgcd(_:_:)` (recursive Euclidean gcd; expects non-negative inputs).

## Behaviour

- **Always normalized.** Reduced by the gcd, sign on the numerator, denominator always `> 0`, zero is `0 / 1`. So `3/-6`, `-3/6` and `-1/2` are the same value.
- **Zero denominator crashes.** `Rational(num:den:)` is non-throwing; `den == 0` fails a `precondition` and traps. It is not a recoverable error.
- **Printing** is `"<num> / <den>"`, e.g. `-1 / 2`.
- **`Int` overflow is not handled.** Extreme inputs can trap.
- **`num` and `den` are not publicly readable.**

## Status

Early stage. Arithmetic, `Comparable`, `Hashable`, literals and more are not implemented yet; see [`TODO.md`](TODO.md) (in French) for the roadmap. No license file and no CI.
