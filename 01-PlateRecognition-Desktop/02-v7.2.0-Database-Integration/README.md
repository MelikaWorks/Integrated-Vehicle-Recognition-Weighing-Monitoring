[فارسی](README.fa.md) | [English](README.md)

# Stage 2 — v7.2.0 Database Integration and Four-Candidate Workflow

This stage documents SQL Server integration and the revision of plate registration. The developer first validated integration against a self-created test database, then connected to the original weighing application's database. That sequence is developer-reported; no separate test-database screenshot is identified in this package.

## Database evolution in the v7 family

| Step | Behavior | Outcome |
|---|---|---|
| Initial integration | Insert recognition into a dedicated audit/log table | First database-connected workflow |
| Original-database experiment | Retrieve the latest weighing code and update that row's plate | Abandoned because the latest row did not reliably belong to the current vehicle |
| Revised integration | Insert into `plate_reader_log` and `plate_detection` | No direct updates to the weighing table |

Exact minor-version boundaries for all database transitions are not established; this is a v7-family development sequence.

### Why the latest weighing row was insufficient

Recognition occurred before weighing, so the latest existing row could belong to a different visit. The first weighing created a transaction and the second completed it, in either order:

| Visit | First weighing | Second weighing |
|---|---|---|
| Collect material | Empty | Loaded, after loading |
| Deliver material | Loaded | Empty, after unloading |

Neither a fixed empty-first order nor a latest-code-plus-one rule describes this integration. The revised plate reader inserted the recognition into a detection table. The manager planned database-side linkage to weighing transactions; an implemented trigger or periodic processor is not verified by this package. The weighing application also supported manual plate entry.

## v7.2.0 operator workflow

1. Enter the camera IP manually and connect. This supplied interface reads camera login details from local configuration.
2. Test database connectivity and retrieve the latest weighing record/code.
3. Request recognition, review four candidates and select the correct result.
4. Register the result or use the manual plate-entry form. Repeat recognition, clear results and stop/reconnect the camera were also available.

Local logs and image/TXT/CSV output remained alongside database registration. The historical UI confirmation still refers to the latest weighing row; the actual write behavior depends on the accompanying database service.

## Selected code and source provenance

| File | Purpose |
|---|---|
| `operator_database_checks_excerpt.py` | Connection test, latest weighing and historical confirmation |
| `four_frame_selection_excerpt.py` | Four-frame selection and entry into manual fallback |
| `latest_weighing_read_excerpt.py` | Read-only weighing context |
| `historical_latest_row_update_excerpt.py` | Abandoned update path from `old vesion` |
| `detection_and_audit_insert_excerpt.py` | Revised audit/detection inserts |

These are actual source excerpts, not a complete runnable release. Omitted initialization, imports and application dependencies are identified in each file. The revised service retains the old `save_plate_to_latest` name but does not update the weighing table. The historical method also contains car, audit and auxiliary-table inserts; it is shown as historical evidence, not recommended integration code.

The archive also contains intermediate v7.2.1, v7.2.2 and v7.3.0 files; later interfaces are not published in this stage. Production configuration, credentials and model weights are excluded.

## Screenshots in workflow order

### 1. Manual IP-camera connection

<a href="screenshots/01-manual-camera-ip.png"><img src="screenshots/01-manual-camera-ip.png" width="320" alt="Manual IP-camera connection"></a>

### 2. Successful SQL Server connection test

<a href="screenshots/02-database-connection-test.png"><img src="screenshots/02-database-connection-test.png" width="260" alt="Successful SQL Server connection test"></a>

### 3. Four candidates and operator selection

<a href="screenshots/03-four-frame-candidates.png"><img src="screenshots/03-four-frame-candidates.png" width="260" alt="Four candidates and operator selection"></a>

### 4. Historical confirmation for the latest weighing row (window title: v7.1.1-dev-db)

<a href="screenshots/04-historical-latest-weighing-confirmation.png"><img src="screenshots/04-historical-latest-weighing-confirmation.png" width="260" alt="Historical confirmation for the latest weighing row (window title: v7.1.1-dev-db)"></a>

### 5. Manual plate-entry fallback

<a href="screenshots/05-manual-plate-entry.png"><img src="screenshots/05-manual-plate-entry.png" width="320" alt="Manual plate-entry fallback"></a>

## Configuration examples and settings generation

- [camera_config.json](config/camera_config.json) preserves the camera configuration fields.
- [db_config.json](config/db_config.json) preserves the database configuration fields.
- Passwords are replaced with `********`; hosts, account names and database names use placeholders. These are public examples, not working production settings.
- [Make-Settings.py](src/Make-Settings.py) contains the selected generation function. It reads the two local JSON files and writes `CAMERA_CONFIG` and `DATABASE_CONFIG` into `settings.py` using `pformat`. **This is neither password hashing nor encryption**: the generated file contains the configuration values in readable form. The published helper omits imports and the command-line entry point.
- The original helper expects both JSON files beside the local script. Public examples are under `config/` for documentation; copy and configure them locally when reproducing the build arrangement. Do not generate settings from the masked examples.
- Generated `settings.py` stays private and is ignored by the stage's `.gitignore`.

### Database-service excerpts

The supplied `database_service.py` manages SQL connection, queries, registration and transactions. It is intentionally not published in full. [Read context](src/latest_weighing_read_excerpt.py), [historical update](src/historical_latest_row_update_excerpt.py) and [revised detection/audit inserts](src/detection_and_audit_insert_excerpt.py) are separate excerpts so that the two historical write strategies are not confused.

### Screenshot recheck

The manual-IP screenshot uses the previously supplied masked image, rather than the newly supplied image with a visible internal IP. Database connection, four candidates, historical latest-row confirmation and manual plate entry are already shown above. The extra historical screenshot below has window title `v7.1.0-dev-db` and a save-confirmation message; it is not labeled v7.2.0.

<a href="screenshots/06-historical-v7.1.0-save-confirmation.png"><img src="screenshots/06-historical-v7.1.0-save-confirmation.png" width="260" alt="Historical v7.1.0 save confirmation"></a>

The single-result/separate-register screenshot is v7.2.2. The combined-detection screenshot is v7.3.0 and shows a save failure with retry available. Those screenshots, together with automatic startup, belong to stage 3 and are not presented as v7.2.0 evidence.

## Period output and log samples

The output folder was shared across multiple versions. CSV/TXT contain eight saved records whose timestamps fall under v7.2.2 sessions in the log; they are not presented as confirmed output from the v7.2.0 interface. A weighing code in an image filename, or a “saved in SQL Server” log message, does not alone prove that the weighing table was updated.

- [CSV](sample-output/outputs/plates.csv) and [TXT](sample-output/outputs/plates.txt): eight supplied records.
- [Selected log](sample-output/logs/passage_app.selected.log): original application-start and successful-save lines only. Environment error traces are omitted; this is not the full log.
- [Supplied dependencies](requirements.txt): original package declarations; no installation or runtime testing was performed.

<a href="sample-output/outputs/vehicle_49ع17479_towzin-384028_20261007_123536.jpg"><img src="sample-output/outputs/vehicle_49ع17479_towzin-384028_20261007_123536.jpg" width="320" alt="Saved vehicle image"></a>

<a href="sample-output/outputs/plate_49ع17479_towzin-384028_20261007_123536.jpg"><img src="sample-output/outputs/plate_49ع17479_towzin-384028_20261007_123536.jpg" width="200" alt="Saved plate image"></a>

Saved images are retained for comparison with OCR, not as independently verified accuracy measurements. Click an image for its original size.

[Back to desktop stages](../README.md)
