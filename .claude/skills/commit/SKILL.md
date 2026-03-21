---
name: commit
user-invokable: true
description: "This skill should be used when the user asks to 'commit', 'create a commit', or 'git commit'. It creates conventional commits with FQCN scopes for Ansible collection content (roles, modules, plugins) and automatically splits changed files into separate, focused commits when they belong to different collection components."
---

You are executing the `commit` skill. Follow these steps precisely.

## Step 1: Resolve FQCN base

Read `galaxy.yml` and extract the `namespace` and `name` fields.
Set `FQCN_BASE = "<namespace>.<name>"` (e.g. `community.beszel`).

## Step 2: Discover changed files

Run `git status --short` with the Bash tool to list all modified, staged, and untracked files.

Categorise each file as:
- **Staged** — lines starting with a non-space first character (e.g. `M `, `A `, `D `)
- **Unstaged** — lines starting with a space in the first column (e.g. ` M`, ` D`)
- **Untracked** — lines starting with `??`

If nothing is changed, stop and inform the user there are no changes to commit.

## Step 3: Group files by component

Assign each changed file to a component bucket using these rules **in order**:

| File path pattern                                                  | Component scope                 | Example                      |
| ------------------------------------------------------------------ | ------------------------------- | ---------------------------- |
| `roles/<role_name>/…`                                              | `<FQCN_BASE>.<role_name>`       | `community.beszel.agent`     |
| `plugins/modules/<module_name>.py`                                 | `<FQCN_BASE>.<module_name>`     | `community.beszel.system`    |
| `plugins/<plugin_type>/<plugin_name>.py`                           | `<FQCN_BASE>.<plugin_name>`     | `community.beszel.my_filter` |
| `plugins/module_utils/…`                                           | `<FQCN_BASE>` (collection-wide) | `community.beszel`           |
| Everything else (galaxy.yml, docs, tests, ci, changelogs, meta, …) | `(none)` — collection-level     | —                            |

- `<role_name>` is the directory name directly under `roles/`.
- `<module_name>` is the filename without `.py`.
- `<plugin_type>` is the subdirectory under `plugins/` (e.g. `filter`, `lookup`, `callback`).
- `<plugin_name>` is the filename without `.py`.
- Never hard-code component names; always derive them from the file path.

After grouping, if **multiple components** are affected:
- List the proposed groupings to the user (which files go in which commit).
- Use `AskUserQuestion` to ask: "I found changes across multiple components and will create separate commits. Does this look right?\n\n<groupings>\n\nProceed? (yes/no or provide corrections)"
- If the user says no or provides corrections, adjust the groupings accordingly.

## Step 4: For each component group (in order)

Repeat the following sub-steps for each group:

### 4a: Infer commit type

Read the diff for the files in this group (`git diff HEAD -- <files>` for unstaged, `git diff --cached -- <files>` for staged) to inform your inference. Use the following mapping to select the commit type:

| Commit type prefix                                 | antsibull-changelog category |
| -------------------------------------------------- | ---------------------------- |
| `feat:` / `feature:`                               | `minor_changes`              |
| `fix:` / `bugfix:`                                 | `bugfixes`                   |
| `security:`                                        | `security_fixes`             |
| `feat!:` or `BREAKING CHANGE` in body              | `breaking_changes`           |
| `deprecate:` / `deprecated:`                       | `deprecated_features`        |
| `remove:` / `removed:`                             | `removed_features`           |
| `docs:` / `chore:` / `ci:` / `test:` / `refactor:` | `trivial`                    |

If the type is ambiguous, use `AskUserQuestion` to ask:
"What type of change is this for `<component>`? (feat/fix/docs/chore/refactor/ci/test/security/deprecate/remove/breaking)"

### 4b: Draft commit message

Follow conventional commits format:
- **With FQCN scope**: `<type>(<fqcn>): <imperative short description>`
- **Collection-level (no scope)**: `<type>: <imperative short description>`

Rules:
- Subject line ≤ 72 characters
- Lowercase after the colon and space
- No trailing period
- Use imperative mood (e.g. "add", "fix", "remove" — not "added", "fixes")
- For breaking changes, append a blank line and `BREAKING CHANGE: <explanation>` in the body

Examples:
```
feat(community.beszel.agent): add support for custom agent port
fix(community.beszel.hub): correct idempotency when hub token unset
feat!: drop support for Ansible < 2.15

BREAKING CHANGE: Ansible 2.14 and earlier are no longer supported.
docs: update README with new installation steps
```

### 4c: Confirm with user

Use `AskUserQuestion` to present the proposed commit message and ask for approval:

"Proposed commit for `<component>`:\n\n```\n<message>\n```\n\nApprove, or provide an edited message?"

If the user provides an edited message, use their version exactly.

### 4d: Stage files

Run `git add <file1> <file2> …` for all files in this component group.

### 4e: Create the commit

Run:
```bash
git commit -m "$(cat <<'EOF'
<approved message>
EOF
)"
```

### 4f: Confirm

Run `git log -1 --oneline` and show the output to the user.

## Step 5: Summary

After all commits are created, run:
```bash
git log --oneline -<n>
```
where `<n>` is the total number of commits just created. Display the output so the user can see all commits at a glance.
