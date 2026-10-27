[فارسی](README.fa.md) | [English](README.md)

# v7.4.0 — plate reader to weighing form

Python invokes the local TowzinPlateAgent.exe through a bounded CLI request with plate parts and a request-specific temporary response file. It verifies exit code and exact response before reporting success. A timeout or partial response does not trigger an automatic repeat. The reader saves local output, but this workflow does not query or update the weighing database. The agent fills plate fields only; the operator still completes the actual weighing. The supplied guide says the new CLI link was not yet field-verified when written. The supplied log later records a v7.4.0 attempt failing because the weighing window was not open in the tool's user session; it is not evidence of end-to-end success.

## Selected source and evidence status

`src` contains actual selected code fragments. Initialization, dependencies and other logic are omitted; this is not a runnable release. No Windows agent execution or database test was performed during this review.

Actual weighing-workstation screenshots will be added later. No placeholder images or broken image links are included. The [selected session log](../evidence/agent-session.selected.log) distinguishes application startup from successful transfer.

[Back to agent integration stages](../README.md)
