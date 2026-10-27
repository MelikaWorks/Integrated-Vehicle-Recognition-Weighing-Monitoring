[فارسی](README.fa.md) | [English](README.md)

# 01 — Plate Recognition Desktop

The desktop development history is organized into three stages. Each published stage includes bilingual documentation, selected source excerpts and ordered screenshots.

| Stage | Scope | Status |
|---|---|---|
| [01 — v6.3.6 Local Recognition](01-v6.3.6-Local-Recognition/) | Manual IP-camera connection, four candidates and local storage | Available for review |
| [02 — v7.2.0 Database Integration](02-v7.2.0-Database-Integration/) | SQL integration and evolution of weighing-record registration | Available for review |
| [03 — v7.3.x Streamlined Workflow](03-v7.3.x-Streamlined-Workflow/) | Automatic connection, single-result workflow and manual fallback | Available for review |

The later SQL integration evolved from database logging to an experimental latest-weighing-row update, then to a dedicated detection table. Weighing could start with an empty or loaded vehicle: the first weighing created a transaction and the second completed it. Publication of the database stages will document these distinctions.

Python files are selected historical excerpts, not complete distributable releases. Screenshots are stored once and shared by both language versions.
