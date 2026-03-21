---
name: changelogs
user-invokable: true
description: "This skill should be used when the user asks to 'generate a changelog', 'create a changelog fragment', 'run antsibull-changelog', or wants to prepare a release changelog. It inspects commits on the current branch, categorises them using antsibull-changelog fragment categories, writes a changelog fragment YAML, and runs the changelog generation command."
---

You are executing the `changelogs` skill. Follow these steps precisely.

## Step 1: Pre-flight checks

1. Read `galaxy.yml` and extract the `version`, `namespace`, and `name` fields. Set `FQCN_BASE = "<namespace>.<name>"`.
2. Read `changelogs/changelog.yaml` and check whether that version already has an entry under `releases:`.
3. If the version already exists in the changelog:
   - Use `AskUserQuestion` to ask: "Version <version> already has a release entry in changelogs/changelog.yaml. Should I remove it and the corresponding fragment file before proceeding? (yes/no)"
   - If yes: Remove the version's entry from `changelogs/changelog.yaml` using the Edit tool, and delete `changelogs/fragments/<version>.yml` using Bash (`rm`).
   - If no: Stop and inform the user the skill was aborted.

## Step 2: Discover commits on the current branch

Run these commands with the Bash tool:

```bash
git rev-parse --abbrev-ref HEAD
```
Save the output as `<branch-name>` — this will be used as the fragment filename.

```bash
git log main..HEAD --oneline
```
List all commits not yet merged into main. If there are no commits, stop and tell the user there are no commits ahead of main.

```bash
git log main..HEAD --format="%H %s%n%b"
```
Get full commit subjects and bodies for better analysis.

```bash
git diff main..HEAD --name-only
```
Get all changed files to help detect which component/role is affected.

Ignore any commits whose subject contains `[skip ci]` or starts with `Merge `.

## Step 3: Map commits to antsibull-changelog categories

Use conventional commit prefixes as the primary signal:

| Commit prefix                                                | Fragment category         |
| ------------------------------------------------------------ | ------------------------- |
| `feat:` / `feature:`                                         | `minor_changes`           |
| `fix:` / `bugfix:`                                           | `bugfixes`                |
| `security:`                                                  | `security_fixes`          |
| `BREAKING CHANGE` in body, or `!` before `:` (e.g. `feat!:`) | `breaking_changes`        |
| `deprecate:` / `deprecated:`                                 | `deprecated_features`     |
| `remove:` / `removed:`                                       | `removed_features`        |
| `docs:` / `chore:` / `ci:` / `test:` / `refactor:`           | `trivial` — skip entirely |

For each non-trivial commit:

1. **Determine the component** using `FQCN_BASE` derived from `galaxy.yml` and the file paths changed by the commit. Apply these rules **in order**:

   | File path pattern                        | Component prefix                      |
   | ---------------------------------------- | ------------------------------------- |
   | `roles/<role_name>/…`                    | `<FQCN_BASE>.<role_name> - `          |
   | `plugins/modules/<module_name>.py`       | `<FQCN_BASE>.<module_name> - `        |
   | `plugins/<plugin_type>/<plugin_name>.py` | `<FQCN_BASE>.<plugin_name> - `        |
   | `plugins/module_utils/…`                 | `<FQCN_BASE> - `                      |
   | Everything else                          | *(no prefix — collection-level)*      |

   - `<role_name>` is the directory name directly under `roles/`.
   - `<module_name>` is the filename without `.py`.
   - `<plugin_name>` is the filename without `.py`.
   - If the commit message scope (e.g. `feat(community.beszel.agent):`) names a component, use that instead.
   - If the commit touches files spanning multiple components, omit the prefix.

2. **Write the description**: Use the commit subject (stripped of the `type:` prefix and leading space). Capitalise the first letter. Do not end with a period.

3. If a commit contains `BREAKING CHANGE:` in its body, extract that text as the description for a `breaking_changes` entry (in addition to or instead of the subject-derived entry).

## Step 4: Generate the fragment file

Write `changelogs/fragments/<branch-name>.yml` using the Write tool with this structure:

```yaml
---
release_summary: |
  Release <version> of the Ansible community collection for Beszel.

<category>:
  - <component><description>
```

Rules:
- Always include `release_summary`.
- Only include categories that have at least one entry.
- List entries in the order: `breaking_changes`, `security_fixes`, `minor_changes`, `bugfixes`, `deprecated_features`, `removed_features`.
- Each entry is a YAML list item (starts with `  - `).
- If a component prefix applies, include it before the description (e.g. `community.beszel.agent - Add foo variable`).

Example:

```yaml
---
release_summary: |
  Release 0.8.0 of the Ansible community collection for Beszel.

minor_changes:
  - community.beszel.agent - Add support for custom agent port configuration.
  - community.beszel.hub - Add hub_tls_cert role variable for TLS certificate path.

bugfixes:
  - community.beszel.agent - Fix idempotency issue when agent_token is not set.
```

## Step 5: Run changelog generation

Run:

```bash
uv run antsibull-changelog release -v
```

Report the full command output to the user. If the command fails, show the error and suggest the user check:
- The fragment YAML syntax
- Whether `uv` and `antsibull-changelog` are installed
- Whether the version in `galaxy.yml` matches what antsibull-changelog expects

## Step 6: Verify CHANGELOG.md and CHANGELOG.rst were updated

After a successful run, read both `CHANGELOG.md` and `CHANGELOG.rst` and confirm that the new version's release section is present in each file. Specifically check that:

1. `CHANGELOG.md` contains a heading for the new version (e.g. `## v<version>`) and the entries from the fragment.
2. `CHANGELOG.rst` contains a heading for the new version (e.g. `v<version>`) and the entries from the fragment.

If either file is missing the new version's section, report it as a warning and suggest the user re-run `uv run antsibull-changelog release -v` manually or check the antsibull-changelog configuration.
