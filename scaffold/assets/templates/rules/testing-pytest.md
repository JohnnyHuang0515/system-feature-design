# Testing (pytest)

How we test in this project using pytest. Claude should read this before writing or modifying tests.

## Commands

- **Run all tests:** `{{TEST_CMD}}`

Everything else is `{{TEST_CMD}}` plus a pytest argument:

- **One file:** `tests/test_foo.py`
- **One test:** `tests/test_foo.py::test_bar`
- **With coverage:** `--cov={{PROJECT_NAME}} --cov-report=term-missing`
- **With output:** `-s`, to see print statements
- **Stop on first failure:** `-x`

## Layout

- Tests live in `tests/`, mirroring the source tree: `src/foo/bar.py` → `tests/foo/test_bar.py`.
- One `test_*.py` file per source file, usually.
- Shared fixtures go in `conftest.py` — at the level they're needed, not all at the root.

## Naming

- Files: `test_*.py`
- Functions: `test_*`
- Classes (if used): `Test*` — but prefer plain functions unless grouping helps.
- Test names describe the behaviour: `test_empty_cart_returns_zero_total`, not `test_get_total`.

## Fixtures

- Use `@pytest.fixture` for setup/teardown.
- Scope appropriately: `function` (default) for most, `module` or `session` only when setup is genuinely expensive.
- Name fixtures by what they *are*, not what they *do*: `user`, not `create_user`.

## Parametrize

Use `@pytest.mark.parametrize` for table-driven tests:

```python
@pytest.mark.parametrize("input,expected", [
    ("",        0),
    ("a",       1),
    ("hello",   5),
])
def test_length(input, expected):
    assert len(input) == expected
```

## Assertions

- Use plain `assert` — pytest's assertion introspection will show you useful output.
- For exceptions: `with pytest.raises(ValueError, match="specific message")`.
- For approximate numeric comparisons: `pytest.approx`.

## Mocking

- Use `pytest-mock`'s `mocker` fixture (preferred) or `unittest.mock.patch`.
- For mock strategy (what to mock, when, boundary rules), see `.claude/references/testing-tdd.md`.

## Markers

Project-specific markers (register in `pyproject.toml` or `pytest.ini`):
- `@pytest.mark.slow` — takes > 1 second; skip in fast runs with `-m "not slow"`.
- `@pytest.mark.integration` — hits real external services.

## Hard rules

- **Plain test functions** — reach for `unittest.TestCase` only against a specific need.
- **Every `pytest.skip()` links an issue.**
- **Keep the default suite fast** — `mark` the slow tests.
- **Each test builds its own fixtures**; module-level mutable state leaks between them.
