# Shared agent workflow

- Date 2026-11-24
- Type documentation setup
- Branch `docs/shared-agent-workflow`
- Status complete

## Requirement and scope

Give developers, Codex, and Claude a shared way to document new apps,
features, and hotfixes so work can continue across agents.

## Acceptance criteria

- [x] Create a dedicated Git branch and project requirements directory.
- [x] Connect the repository entry files for Codex and Claude to the same guidance.
- [x] Provide a reusable change record with implementation, verification, and handoff sections.

## Implementation

[AGENTS.md](../../../AGENTS.md) links to the [shared workflow](../README.md)
and [development reference](../development.md).
[CLAUDE.md](../../../CLAUDE.md) imports the same files. The
[change template](../change-template.md) keeps the requirement and implementation
history together on the branch.

## Verification

Checked the active branch, local Markdown links, Claude import paths, and
whitespace. Application tests were skipped because only documentation changed.

## Handoff

Use the workflow and template for the next app, feature, or hotfix. Runtime
loading in Claude Code was outside this repository check.
