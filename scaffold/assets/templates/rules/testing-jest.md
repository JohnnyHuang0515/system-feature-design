# Testing — the JS runner (jest / vitest / mocha)

How we test in this project. Claude should read this before writing or modifying tests.

## Commands

- **Whole suite, every framework in this repo:** `{{TEST_CMD}}`

Everything below goes to **the JS runner itself**, not to the whole-suite command — where this repo runs more than one framework that command chains runners, and a flag on the end lands on the wrong one:

- **Watch mode:** `--watch`
- **One file:** the path, e.g. `path/to/file.test.ts`
- **With coverage:** `--coverage`
- **Update snapshots:** `-u` — only after confirming the change is intended

## Layout

- Co-locate tests with source: `foo.ts` → `foo.test.ts` in the same directory.
- Shared test utilities in `test/helpers/` or similar.
- Avoid a separate top-level `__tests__/` directory unless the project already uses one.

## Structure

Use `describe` blocks to group, `it` (or `test`) for cases. Nesting beyond two levels is a smell.

```ts
describe("Cart", () => {
  describe("total", () => {
    it("returns zero for empty cart", () => { /* ... */ });
    it("sums line items", () => { /* ... */ });
    it("applies discounts after tax", () => { /* ... */ });
  });
});
```

## Naming

- Test names are sentences: `it("returns zero for empty cart")`, not `it("test empty")`.
- File names: `foo.test.ts` for unit, `foo.integration.test.ts` for integration.

## Matchers

- Use the most specific matcher available: `toEqual` for deep equality, `toBe` for reference/primitive, `toMatchObject` for partial match.
- For async: `await expect(promise).resolves.toEqual(...)` or `.rejects.toThrow(...)`.
- Error message assertions should use `toThrow("specific message")` or a regex — not just `toThrow()`.

## Snapshots

- Use snapshots sparingly. They're great for stable serialized output, terrible for UI components that change often.
- Inline snapshots (`toMatchInlineSnapshot`) are easier to review than external files.
- When a snapshot changes, read the diff — don't blindly `-u`.

## Mocking

- Use `jest.mock()` / `vi.mock()` to mock modules; prefer `vi.spyOn()` for partial mocks.
- Always restore mocks: `afterEach(() => vi.restoreAllMocks())` or use `mockReset` config.
- For mock strategy (what to mock, when, boundary rules), see `.claude/references/testing-tdd.md`.

## React Testing (if applicable)

- Use `@testing-library/react`. Query by accessible role/name first, `data-testid` last.
- Test behaviour, not implementation — assert what the user sees, not which component rendered.
- For user events, use `userEvent` (from `@testing-library/user-event`), not `fireEvent`.

## Hard rules

- **Strip `.only` / `.skip` / `fdescribe` / `xit` before committing.**
- **Mock at the boundary**, around the code under test.
- **Every test earns its keep**: break the production code and confirm the test goes red.
- **Keep the default run fast** — split integration tests out.
