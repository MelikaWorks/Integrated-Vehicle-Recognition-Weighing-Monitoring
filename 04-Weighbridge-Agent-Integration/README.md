[فارسی](README.fa.md) | [English](README.md)

# 04 — Weighbridge Form Integration through a Windows Agent

The Python plate reader sends recognized plate parts to a local C# agent, which fills numeric textboxes and the letter dropdown in the existing weighing application. This is UI integration, distinct from updating the latest weighing database row.

**Flow: plate reader → Windows agent → weighing plate fields → operator verification and weighing registration.**

| Stage | Scope |
|---|---|
| [Initial transfer test](01-Agent-Transfer-Test/) | Button-driven form discovery and plate transfer |
| [v7.4.0](02-v7.4.0-Form-Integration/) | Reader-to-agent link, local output, no SQL in the transfer path |
| [v7.4.2](03-v7.4.2-Database-Audit/) | One verified transfer followed by detection/audit database writes |

The agent does not press loaded, empty or print buttons. The operator and weighing application retain control of weighing transactions. Filling and reading fields back does not itself prove successful weighing registration. Execution requires the appropriate user session and access level for the weighing application.

## Publication and validation status

Published without screenshots for now; actual weighing-workstation captures will be added when supplied. Older v7.3.3 output/images retained in the archives are not presented as evidence of agent execution.

The v7.4.0 guide reports the initial button-driven test succeeded, while marking the new CLI link as unverified at that time. The [selected log](evidence/agent-session.selected.log) records v7.4.0/v7.4.2 startup and one user-session transfer failure. Startup is not proof of end-to-end success.

## Public material and configuration

Only Python/C# excerpts, bilingual notes and masked [camera](config/camera_config.json)/[database](config/db_config.json) examples are included. Passwords are `********`. Complete source, executables, real settings.py and credentials are excluded. The RAR and OCR timing text were not used as source or evidence of successful transfer.

The separately supplied Make-Settings(2).py reads database settings only from db_config.local.json. The helper inside the v7.4.2 package separates target settings from --local mode; these files should not be treated as interchangeable. Generating settings.py is not hashing or encryption. Public masked examples are not operational settings.

This publication review covered notes, selected methods, logs and links, not Windows compilation or execution.
