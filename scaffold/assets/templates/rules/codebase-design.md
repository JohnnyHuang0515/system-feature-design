# Codebase design

Shared vocabulary for module shape. Use these words exactly — consistent language across `planner`, `implementer` and `reviewer` is the point.

## Vocabulary

**Module** — anything with an interface and an implementation. Scale-agnostic on purpose: a function, a class, a package, a slice spanning tiers. Say *module*, not unit / component / service.

**Interface** — everything a caller must know to use the module correctly: the type signature, plus invariants, ordering constraints, error modes, required configuration, performance characteristics. Say *interface*, not API / signature — those name only the type-level surface.

**Implementation** — what's inside. A module can be a small **adapter** over a large implementation (a Postgres repo) or a large adapter over a small one (an in-memory fake).

**Depth** — leverage at the interface: how much behaviour a caller or a test can exercise per unit of interface it has to learn. **Deep** = a lot of behaviour behind a small interface. **Shallow** = the interface is nearly as complex as the implementation.

**Seam** — a place where behaviour can be altered without editing in that place; the *location* where a module's interface lives. Where the seam goes is a separate decision from what sits behind it. Say *seam*, not boundary — boundary is taken by DDD's bounded context.

**Adapter** — a concrete thing satisfying an interface at a seam. Names a role, not a substance.

**Leverage** — what callers get from depth: more capability per unit of interface learned. One implementation pays back across N call sites and M tests.

**Locality** — what maintainers get from depth: change, bugs, knowledge and verification concentrate in one place. Fix once, fixed everywhere.

## Deep beats shallow

```
Deep                                Shallow (avoid)
┌────────────────────┐              ┌──────────────────────────────┐
│   Small interface  │              │      Large interface         │
├────────────────────┤              ├──────────────────────────────┤
│                    │              │  Thin implementation         │
│ Deep implementation│              └──────────────────────────────┘
│                    │
└────────────────────┘
```

Designing an interface, ask: can I cut a method? Can I simplify a parameter? Can I hide more inside?

A shallow module costs an agent the most. Logic scattered across five small modules means bouncing between five files to understand one flow — and once that exceeds the context window, the agent starts guessing.

## Principles

- **Depth is a property of the interface, not the implementation.** A deep module may be internally composed of small, swappable parts; they just aren't in the interface. Modules have **internal seams** (private, used by their own tests) as well as the **external seam** at the interface.
- **The deletion test.** Imagine deleting the module. Complexity reappears across N callers → it was earning its keep. Complexity vanishes → it was a pass-through, and inlining it makes the code clearer.
- **The interface is the test surface.** Callers and tests cross the same seam. Wanting to test *past* the interface means the module is the wrong shape.
- **One adapter is a hypothetical seam. Two adapters is a real one.** Introduce a seam once something actually varies across it.

Depth measured as implementation-lines ÷ interface-lines rewards padding the implementation. Measure depth as leverage.

## Designing for testability

**Accept dependencies, don't create them.**

```typescript
// Testable
function processOrder(order, paymentGateway) {}

// Hard to test
function processOrder(order) {
  const gateway = new StripeGateway();
}
```

**Return results rather than mutating.**

```typescript
// Testable
function calculateDiscount(cart): Discount {}

// Hard to test
function applyDiscount(cart): void {
  cart.total -= discount;
}
```

**Small surface area.** Fewer methods, fewer tests. Fewer params, simpler setup.

## Deepening: what the dependencies allow

Before merging a cluster of shallow modules, classify what it depends on. The category decides how the deepened module is tested across its seam.

| Category | What it is | How it's tested |
|---|---|---|
| **In-process** | Pure computation, in-memory state, no I/O | Always deepenable. Merge and test through the new interface. No adapter. |
| **Local-substitutable** | Has a local stand-in (PGLite for Postgres, in-memory filesystem) | Deepenable where the stand-in exists. Test with it running. The seam is internal — no port at the external interface. |
| **Remote but owned** | Your own services across a network boundary | Define a **port** at the seam. The deep module owns the logic; transport is an injected **adapter** — in-memory for tests, HTTP/gRPC/queue in production. |
| **True external** | Third-party you don't control (Stripe, Twilio) | The module takes the dependency as an injected port; tests supply a mock adapter. |

### Replace, don't layer

Once tests exist at the deepened module's interface, the old unit tests on the shallow modules are waste — **delete them**. Layering new tests on top of old ones keeps the shallow structure alive in the test suite even after the code has moved on.

New tests assert on observable outcomes through the interface, never on internal state, so they survive internal refactors. A test that has to change when the implementation changes is testing past the interface.

## Design it twice

Your first interface is unlikely to be the best one. When a module's shape matters, design it several ways before picking — and do it in parallel rather than iterating.

1. **Frame the problem space first.** Write out the constraints any interface must satisfy, the dependencies and their category from the table above, and a rough code sketch to make the constraints concrete. Show it to the human, then start immediately — they read while the work runs.
2. **Spawn 3+ agents in parallel**, each with a *different design constraint*, so the results genuinely diverge:
   - *Minimise the interface* — 1–3 entry points, maximum leverage per entry point
   - *Maximise flexibility* — many use cases and extension points
   - *Optimise for the most common caller* — make the default case trivial
   - *Ports and adapters* — where dependencies cross a seam
3. Each returns: the interface (types, methods, params, plus invariants, ordering and error modes), a usage example, what the implementation hides behind the seam, the dependency strategy, and where leverage is thick or thin.
4. **Present sequentially, then compare in prose** on **depth**, **locality** and **seam placement** — and finish with your own recommendation. A hybrid is a fine answer. A menu is not: be opinionated.

## Relationships

A **module** has exactly one **interface**. **Depth** is measured against that interface. A **seam** is where the interface lives, and an **adapter** sits at the seam satisfying it. Depth produces **leverage** for callers and **locality** for maintainers.
