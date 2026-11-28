# Change title

- Date
- Type (app, feature, or hotfix)
- Branch
- Status (planned, in progress, blocked, or complete)
- Issue or pull request, if available

## Requirement and scope

Describe the need, affected areas, and expected behavior. For a hotfix, include
the observed symptom and confirmed cause when known.

## Acceptance criteria

- [ ] Describe an observable outcome.

## Implementation

Describe what changed and why. Trace the behavior from its entry point to its
result and link to the relevant code. For a hotfix, explain how the change
addresses the cause or observed failure.

For data work, describe the inputs, transformations or calculations in order,
outputs, and assumptions that affect the result. Include a small worked example
when it helps explain a calculation or edge case.

Include affected interfaces, permissions, data, configuration, jobs, and
rollout or rollback steps when applicable.

## Verification

List the commands or manual steps and their results. Record pending checks and
the reason they remain pending.

For a new storage model, record the Django admin check and the direct database
check described in the [data model admin rules](data-model-admin.md).

## Handoff

Describe remaining work, blockers, and the next action. Update this section
when another agent or developer picks up the change.
