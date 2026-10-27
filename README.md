[فارسی](README.fa.md) | [English](README.md)

# Integrated Vehicle Recognition, Weighing & Monitoring

![Status: commercial](https://img.shields.io/badge/status-commercial-blue) ![Source: proprietary](https://img.shields.io/badge/production_source-proprietary-red) ![Central hosting: pending](https://img.shields.io/badge/central_hosting-pending-orange)

**A unified web system combining license-plate recognition, weighbridge weight acquisition, weighing forms and a security-management dashboard.**

Developed by **Melika Mehranpour**, the project evolved from field-tested desktop tools into a shared web application for vehicle recognition and weighing operations. This repository documents that progression through reviewed historical samples and photographs. The final integrated commercial implementation is private.

## Final integrated system

The final system brings the previously separate components into one web application:

- **Security-management dashboard:** a shared overview for the head of security.
- **License-plate recognition:** vehicle-camera recognition and the relevant operator workflow.
- **Weight acquisition:** weight supplied by the proprietary acquisition component.
- **Weighing forms:** the weighing workflow and its forms within the same application.
- **Data and monitoring:** database-backed records and management views in the common interface.

This is the final integrated product, rather than a collection of unrelated tools. Earlier desktop applications, the standalone web pilot, the dashboard and the form-transfer agent are documented below as development milestones.

For operational security and commercial confidentiality, **the final interface screenshots and production source are not published**. No weight-acquisition agent, device-reading algorithm, protocol, raw device data, executable or operational configuration is distributed here.

## Implementation and hosting status

| Area | Status |
|---|---|
| Unified web application | Integration completed, as reported by the developer |
| Dedicated central server | Procurement pending; centralized hosting is not presented as deployed |
| Historical standalone management dashboard | Runs locally on the head of security's workstation and reads the network SQL Server database |
| Desktop and standalone web pilots | Historical stages; see their individual deployment notes |
| Final commercial product source and screenshots | Private |

Application integration and centralized deployment are separate milestones. The local dashboard's network-database connection does not mean the final integrated web product has been deployed on a dedicated server.

## Development stages

| Stage | Engineering milestone | Documentation |
|---|---|---|
| 01 | Desktop recognition, four-frame operator selection, revised database integration and later single-result workflows | [Desktop plate reader](01-PlateRecognition-Desktop/) |
| 02 | Browser implementation of the four-candidate workflow, with operator selection and registration | [Web pilots 1.0.0 and 1.0.3](02-PlateRecognition-Web/) |
| 03 | Persian management dashboard, right-side navigation, database-backed views and hashed-password login | [Management dashboard](03-Management-Dashboard/) |
| 04 | Local Windows agent transfers plate parts into the existing weighing application's fields | [Form-agent integration](04-Weighbridge-Agent-Integration/) |
| 05 | Weight-reading development and the path into the unified product; proprietary implementation withheld | [Weight-reading stage](05-Weighbridge-Weight-Reading/) |
| Final | One web application combining the management dashboard, plate recognition, weight and weighing forms | Private commercial system; overview only |

Plate transfer and weight acquisition use different agents. Publishing selected historical plate-transfer snippets does not publish the weight-reading implementation.

## Technology represented in the historical samples

Python, OpenCV, YOLO, PyTorch, OCR, C#, Windows Forms, ASP.NET Core MVC, Razor, SQL Server, Dapper, Flask and JavaScript. These describe the reviewed development artifacts; they are not a disclosure of every dependency in the private final product.

## Repository contents

```text
01-PlateRecognition-Desktop/
02-PlateRecognition-Web/
03-Management-Dashboard/
04-Weighbridge-Agent-Integration/
05-Weighbridge-Weight-Reading/
README.md
README.fa.md
```

Each published stage includes English and Persian documentation. Screenshots are labeled by their verifiable version, shown as compact previews and linked to original images. Agent-transfer screenshots are pending actual workstation captures.

## Source availability and evidence

This is a portfolio and development-history repository, **not a complete buildable distribution**. It contains selected historical code fragments, masked configuration examples, reviewed photographs and log/output samples with their scope explained.

Production credentials, real password hashes, model weights, complete production code, sensitive operational settings and the final dashboard image are excluded. Historical sample behavior is not automatically attributed to the final product. Field reports, runtime logs and screenshot evidence are distinguished in stage documentation; no new device or production-runtime validation is implied by this documentation work.

## Version and release information

Historical version numbers are preserved within each component. **No overall commercial-product version has been assigned in this repository**, and this documentation update is not a release of the private product. Component numbers such as desktop 7.4.2 and web pilot 1.0.3 must not be read as the final system's version.

## Ownership

The commercial weight-acquisition component and final integrated implementation are proprietary.

**Copyright © 2026 Melika Mehranpour. All rights reserved.**

Publication of documentation or selected historical excerpts does not grant access to the private commercial implementation. Any third-party components retain their respective ownership and license terms.

---

## Author

👩‍💻 **Melika Mehranpour**

Senior Software Engineer | Full Stack .NET Developer | Enterprise Applications

### Technologies

C# • .NET • ASP.NET Core • SQL Server • PostgreSQL • Power BI • Python • .NET MAUI

### Connect with me

🔗 [LinkedIn](https://www.linkedin.com/in/melika-mehranpour-41b627161/) · 🔗 [GitHub](https://github.com/MelikaWorks)

---

## License

The final integrated commercial system and weight-acquisition implementation are proprietary and are not distributed in this repository. Copyright © 2026 Melika Mehranpour. All rights reserved.

Publication of documentation and selected historical excerpts does not grant a license to the private implementation. Third-party components retain their respective licenses.
