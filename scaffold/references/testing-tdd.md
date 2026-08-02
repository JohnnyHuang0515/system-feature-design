# TDD standards

Rules for writing tests before implementation. Read alongside the relevant `.claude/rules/testing*.md` file(s).

- **tester** follows these rules when writing tests from a plan.
- **implementer** follows these rules when tester's tests are missing and must write their own.
- **reviewer** uses these as the standard for judging test quality.

---

## Seams — where tests go

A **seam** is the public boundary you test at: the interface where behaviour is observable without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before any test is written, write the seams under test down and confirm them with the human. No test is written at an unconfirmed seam.

Ask: *what is the public interface here, and which seams should we test?*

You can't test everything. Agreeing the seams up front is how the effort lands on critical paths and complex logic instead of spreading evenly across every edge case.

`.claude/rules/codebase-design.md` carries the seam vocabulary — use its words exactly.

## The loop

Red → green, **one vertical slice at a time**: one seam, one test, one minimal implementation, then repeat.

- **Red before green.** Write the failing test first, then only enough code to pass it. Speculative features and tests anticipating a future cycle stay out.
- **Each test is a tracer bullet.** It responds to what the previous cycle taught you, which is why the cycle is worth its round trips.
- **Refactoring is not part of the loop.** It belongs to review (see the `reviewer` agent), not to red → green.

### Horizontal slicing is the anti-pattern

Writing every test first and then all the implementation looks efficient and isn't. Bulk tests verify *imagined* behaviour: they test the **shape** of things rather than user-facing behaviour, they go insensitive to real changes, and they lock in a test structure decided before anyone understood the implementation.

In this project's agent pipeline that means **`tester` and `implementer` alternate per slice** — one dispatch of `tester` writes the current slice's failing test, one dispatch of `implementer` makes it pass, and the next slice starts a new pair. A single `tester` dispatch that writes the whole suite is the anti-pattern wearing a pipeline costume.

## Test structure

Every test must follow AAA — use comments to separate the three phases:

```python
def test_expired_token_returns_401():
    # Arrange
    token = create_token(expires_at=one_hour_ago())
    client = AuthClient(token)

    # Act
    response = client.get("/profile")

    # Assert
    assert response.status_code == 401
```

---

## Test case coverage

For every behaviour in the plan, cover:

- **Happy path** — valid input produces the expected output
- **Boundaries** — empty, zero, max, off-by-one around any limit
- **Error paths** — invalid input returns the right error (not a crash)
- **Regression (bug fixes only)** — one test named `test_regression_<description>` that reproduces the exact reported symptom

---

## Mock rules

Mock external dependencies only. Never mock the code under test.

**Mock these:**
- Databases — at the repository/DAO boundary
- HTTP clients — at the client call (`requests.get`, `fetch`)
- Time — `datetime.now()`, `Date.now()`, `time.time()`
- External services — email, SMS, payment, third-party APIs
- Filesystems — unless the test is specifically about file I/O

**Never mock:**
- The code under test
- Pure functions
- Simple data/value objects
- Your own domain logic

**Mock at the boundary, not inside it:**
```python
# Wrong
mock(UserService._hash_password)

# Right
mock(bcrypt.hashpw)
```

---

## Query vs Command

- **Query** (returns a value) → assert the return value
- **Command** (causes a side effect) → assert the interaction at the boundary

```python
# Query — assert return value
assert user_service.find(42).email == "alice@example.com"

# Command — assert the boundary was called correctly
mailer.send.assert_called_once_with(to="alice@example.com", subject="Welcome")
```

Do not verify interactions for queries. Do not skip interaction verification for commands.

---

## Database tests

For code with real query logic, use an in-memory database (SQLite `:memory:`, H2, `pg_tmp`) — not a mock repository. Mocking the DB layer hides SQL errors and schema mismatches.

Mock the DB only when the test is about business logic that happens to call a repository, not about the data access itself.

---

## Design for testability

- **Dependency injection** — always write tests assuming dependencies are injected via constructor or arguments, not instantiated inside the class. `implementer` must accept injected instances; never instantiate external dependencies (DB connections, API clients) directly inside a class.
- **Test data minimalism** — only include fields relevant to the current assertion. Use a factory or fixture for the rest. Override only what the test cares about.
- **Explicit assertions** — assert specific attributes, not whole objects: `assert user.email == "alice@example.com"`, not `assert user == expected_user`.

---

## Async rules

- Never use `time.sleep()` or `await delay()` to wait for async results.
- Use polling/retry patterns or await the promise/future directly.
- All async tests must have an explicit timeout — default maximum 5 seconds.
- Use the correct async decorator (`@pytest.mark.asyncio`, `async () => {}` in Jest, etc.).

---

## Environment and cleanup

- Tests must not depend on external environment variables. Use `mock.patch.dict` or equivalent to set env vars per test.
- All env var changes must be restored in teardown.
- All filesystem writes must go to the OS temp directory and be deleted after the test.

---

## Test quality rules

- One logical assertion per test — if asserting 5 things, write 5 tests
- Name describes behaviour: `test_expired_token_returns_401`, not `test_auth_check_3`
- Each test builds its own fixtures — shared mutable state leaks between them
- Idempotent — running 10 times gives the same result
- Setup over 10 lines moves to a factory or a `conftest.py` fixture
- Assert the value the test is named for — `assert user.email == "alice@example.com"` earns its keep where `assert result is not None` catches nothing
- Assert the body alongside the status — a bare `assert response.status_code == 200` proves only that the route resolved
- Strip `.only` / `.skip` / `fdescribe` / `xit` before committing

---

## Tautological tests

A test whose assertion recomputes the expected value the way the code does passes by construction and can never disagree with the code:

```python
# Tautological — reimplements the function inside the assertion
assert add(a, b) == a + b

# Tautological — the snapshot was generated by the code under test
assert render(cart) == SNAPSHOT_FROM_LAST_RUN
```

Expected values come from an **independent source of truth**: a known-good literal, a worked example, the spec.

```python
# Real — the expected value came from the spec, not from add()
assert add(2, 3) == 5
```

The tell: change the implementation to something wrong and the test still passes.

## Contract alignment

- Tests must strictly follow the function signatures and types defined in the plan. Do not invent or change interfaces.
- If the plan says `getUser(id: string)`, the test must not call `getUser(id: number)`.
- If a signature is ambiguous in the plan, use the most idiomatic interpretation and document the assumption in the red state report.

---

## Non-determinism

Any logic involving randomness, ordering, or unique IDs must be stabilised:

- **Randomness** — mock the random generator or use a fixed seed
- **UUIDs** — mock UUID generators to return predictable values if the ID appears in the assertion
- **Unordered collections** — assert on sorted lists or use set-based comparison; never assert order unless the code explicitly sorts

---

## Red state requirement

Before handing off to implementer, every new test should be confirmed to fail. State the expected failure for each test:

```
test_create_user_returns_201 — will raise AttributeError: module has no attribute 'create_user'
test_invalid_email_returns_422 — will raise AssertionError: 200 != 422
```

Target the strongest failure possible without violating the agent's role:

- **Strong** — `AssertionError: 404 != 201` — proves the logic is wrong
- **Weak but acceptable for tester** — `ImportError: cannot import name 'create_user'` — proves the implementation is missing

Tester only writes tests. Tester must not create or modify production code, including minimal stubs, just to force a stronger red state. If the implementation does not exist yet, import errors, missing-symbol failures, or `NotImplementedError` failures are acceptable.

Implementer may create minimal production stubs as part of implementation if useful, then continue until the tests pass.

A test that might already pass before implementation is a broken test.
