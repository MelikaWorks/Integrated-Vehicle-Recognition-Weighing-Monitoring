[فارسی](README.fa.md) | [English](README.md)

# Initial agent transfer test

The test tool locates native WinForms controls using their relative layout, enters numeric plate parts and selects the actual letter item. It does not use a fixed screen-click coordinate. The supplied test guide targets Windows Forms / .NET Framework 4.7.2. It does not connect to SQL or press loaded, empty or print controls. A readback check alone cannot prove that all internal weighing-application events were handled. The later v7.4.0 guide reports the button-driven transfer test succeeded; the original test guide predates that report. No test screenshot has yet been supplied.

## Selected source and evidence status

`src` contains actual selected code fragments. Initialization, dependencies and other logic are omitted; this is not a runnable release. No Windows agent execution or database test was performed during this review.

Actual weighing-workstation screenshots will be added later. No placeholder images or broken image links are included. The [selected session log](../evidence/agent-session.selected.log) distinguishes application startup from successful transfer.

[Back to agent integration stages](../README.md)
