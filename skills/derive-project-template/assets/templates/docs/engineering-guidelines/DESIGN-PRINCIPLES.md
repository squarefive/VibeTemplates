# Design Principles

This document provides software design guidance for AI coding agents working in
this repository. Use it when a change affects module boundaries, dependency
direction, layering, abstractions, or architecture-level decisions.

## Core Principles

- Keep modules cohesive and loosely coupled.
- Keep dependency direction explicit.
- Keep layer boundaries clear.
- Prefer local changes over broad rewrites.
- Introduce abstractions only when they reduce real complexity.

## Module Boundaries

Each module should have one clear responsibility. When a change adds behavior
that does not fit an existing module's responsibility, prefer creating or
choosing a more appropriate boundary over expanding an unrelated module.

Avoid hidden coupling through shared mutable globals, implicit side effects, or
cross-module knowledge that is not represented by clear functions, classes, or
interfaces.

## Layering Guidance

Separate UI, application orchestration, domain logic, data access, external API
adapters, and infrastructure concerns when the project structure supports it.

Do not force MVC, MVVM, Clean Architecture, or Hexagonal Architecture onto a
project that does not already need that structure. Use these patterns only as
references for separating responsibilities.

## Dependency Rules

Lower-level modules must not import higher-level UI, CLI, web, or orchestration
modules.

When a change requires crossing an existing layer boundary, update the relevant
architecture documentation or explain why the current boundary is insufficient
before coding.

## Abstraction Rules

Do not introduce a new abstraction for a single use case unless it clarifies an
existing boundary or removes meaningful duplication.

Prefer direct code when the behavior is local, stable, and easy to understand.
Prefer abstraction when repeated behavior has a stable contract and the
abstraction reduces the amount of context needed to make future changes safely.

## Change Impact

Keep changes close to the affected module whenever possible. If a change
requires touching multiple layers, verify that each touched layer has a clear
reason to change.

When adding, moving, deleting, or substantially changing source files, update
`docs/architecture/codebase-map.md` so AI coding agents can continue to navigate
the repository correctly.
