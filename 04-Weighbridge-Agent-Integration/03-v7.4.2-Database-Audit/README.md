[فارسی](README.fa.md) | [English](README.md)

# v7.4.2 — transfer plus database audit

After one verified transfer, the reader records transfer metadata locally and attempts detection/audit inserts. An audit failure must not resend the plate to the form. audit_service.py inserts plate_detection first and plate_reader_log with is_manual second, in one transaction. It does not query or update towzin_tb. It checks the audit towzin_code column type: a textual column receives an empty string; an incompatible numeric column stops registration rather than inventing zero or a latest weighing code. The service does not alter schema; required columns, including is_manual, must already exist. The supplied log shows v7.4.2 startup, not a confirmed successful transfer/audit cycle.

## Selected source and evidence status

`src` contains actual selected code fragments. Initialization, dependencies and other logic are omitted; this is not a runnable release. No Windows agent execution or database test was performed during this review.

Actual weighing-workstation screenshots will be added later. No placeholder images or broken image links are included. The [selected session log](../evidence/agent-session.selected.log) distinguishes application startup from successful transfer.

[Back to agent integration stages](../README.md)
