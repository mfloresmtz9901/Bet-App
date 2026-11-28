# Bet App project requirements

Developers, Codex, Claude, and other coding agents use this directory to track
the requirement, implementation, and verification of every app, feature, and
hotfix. Keep the change record on the same branch as the implementation so it
can be reviewed and merged with the code.

## Start a change

1. Check the current branch, worktree status, and any existing record for the
   task under [changes/](changes/). If continuing a task, use its existing
   branch and record. Preserve changes already made by other contributors.
2. For new work, create a branch from the appropriate base. Use a branch
   supplied by the developer when applicable. Otherwise use
   `app/<slug>`, `feature/<slug>`, or `hotfix/<slug>` for new apps,
   features, or hotfixes.
3. Copy the [change template](change-template.md) to
   `changes/YYYY-MM-DD-<slug>.md`. Record the requirement, scope, acceptance
   criteria, and branch before implementation. For an urgent hotfix, capture
   the symptom and intended fix first, then fill in the remaining details
   before handoff.

## Implement and verify

1. Follow the [development reference](development.md), the
   [code clarity rules](code-clarity.md), and existing repository conventions.
   Update the record when scope changes or a decision affects
   how the change works. Link to the relevant files and explain why the
   change was made and how it works.
2. Document relevant effects on routes, permissions, models and migrations,
   configuration, and background jobs. Include rollout and rollback steps
   when deployment or data is affected. For new storage models, follow the
   [data model admin rules](data-model-admin.md).
3. Run checks tied to the acceptance criteria. Record the commands or manual
   steps, their results, and any checks still pending with the reason.

## Hand off or finish

Update the record before handing work to another developer or agent. Record
what is implemented, what remains, and the next concrete step. Keep the same
record when switching between Claude and Codex. When opening a pull request,
link the record in its description. Mark it complete once the acceptance
criteria are met and verified.
