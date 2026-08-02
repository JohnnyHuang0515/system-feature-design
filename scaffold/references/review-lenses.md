# Review lenses

Conditional lenses for the `reviewer` agent's **Standards** axis. The General lens lives in the agent itself and runs on every diff; these two are read only when the diff actually touches their surface, because most diffs touch neither.

| Read this lens when the diff touches |
|---|
| **Security** — auth, authz, input validation, secrets, external HTTP, file ops on user paths, LLM tool-use authorization |
| **Prompt** — prompt files, system messages, few-shot examples, code that constructs prompts, LLM-calling code, response parsers |

---

## Security lens (when sensitive surfaces touched)

**Mindset:** assume attacker controls all untrusted inputs. What's the worst they can do?

### Trust boundaries
- Where does untrusted input enter? Trace forward: database, shell, file path, HTTP, prompt.

### Classic vulns

| Category | Check for |
|---|---|
| SQL injection | String concat in queries; unsafe ORM bypass |
| XSS | Unescaped output; `dangerouslySetInnerHTML`; `v-html`; `innerHTML =` |
| SSRF | HTTP to user-controlled URLs; no internal-IP blocklist |
| Path traversal | User paths without normalization + allow-list root |
| Command injection | Shell with user-controlled args; `subprocess(..., shell=True)` |
| IDOR | Missing per-object permission checks |
| CSRF | State-changing GETs; missing tokens on sensitive forms |
| Deserialization | `pickle.loads`, `yaml.load` (unsafe), `eval` on untrusted |

### Auth & secrets
- Auth required on protected endpoints?
- Authorization **per-object**, not just "is authenticated"?
- Passwords hashed with argon2/bcrypt (never MD5/SHA1)?
- Hard-coded credentials? `.env` in `.gitignore`?
- Secrets logged or sent to third-party APIs?

### LLM-specific (when LLMs involved)
- **Prompt injection:** user input concatenated into system prompts without delimiters?
- **Indirect prompt injection:** LLM reads external content (docs, emails) — treated as untrusted?
- **Tool-use authorization:** when LLM calls tools, the *user's* authz checked for each call?
- **Sensitive data in prompts:** only things *this user* is authorized to see?
- **LLM output rendered as HTML/markdown:** dangerous links or script tags possible?
- **Cost abuse:** per-user rate/cost cap?

---

## Prompt lens (when prompts / LLM code touched)

### Clarity
- Vague instructions ("be helpful", "write good code")? — meaningless.
- Unstated assumptions? Input format, output format, audience?
- Ambiguous constraints ("short") — needs "≤ 3 sentences" or "≤ 150 words".

### Output format
- Format specified when downstream code parses it?
- Format conflicts (says JSON but examples have code fences)?
- Unstructured output being parsed with regex? — suggest JSON mode / tool calls.

### Edge cases
- What happens on empty input? Off-topic input? Garbled input?
- Fallback / "I don't know" path? — otherwise the model hallucinates.
- User input interpolated without delimiters? — use `<user_input>...</user_input>` tags.

### Injection
- User content spliced into system prompt = vector.
- Mitigations: labeled tags, reiterate constraints *after* user content, structured output.

### Few-shot examples
- Cover the real input distribution, not toy cases?
- Negative / refusal example included?
- Examples internally consistent? Too many (>10) often hurt more than help.

### Token efficiency
- Dead weight — same instruction restated in different words?
- Huge prefix sent on every call when only part is needed per request — consider prompt caching?
- Unnecessary chain-of-thought in high-volume paths?

### LLM-calling code
- Retries with backoff?
- 429 handling?
- Reasonable timeout?
- Truncated output handled (`max_tokens` hit)?
- `temperature=0` for parsing-dependent flows?
- Prompt caching enabled where the prefix repeats?
- Logging (redacting PII)?

---
