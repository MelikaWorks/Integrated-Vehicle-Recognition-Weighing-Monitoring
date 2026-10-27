[فارسی](README.fa.md) | [English](README.md)

# Stage 1 — v6.3.6 Local Plate Recognition

This desktop pilot received a live IP-camera stream and processed four frames on operator request. It had no database integration.

## Operator workflow

1. Press IP Camera and enter the camera IP, username and password.
2. Connect, review the live stream and request plate recognition.
3. Copy and process four frames from the recent camera buffer; not all candidates necessarily produce valid results.
4. Select and save the correct result. Clear the candidates for the next vehicle.

## Features and limitations

- Repeat recognition, clear results, and stop the camera before reconnecting.
- Local TXT/CSV plate records, vehicle images, plate crops and application logs.
- No SQL Server integration and no manual plate-entry form.
- Recognition errors occurred at this stage. The screenshots show actual pilot behavior, not a claim of perfect accuracy.

## Selected source

The `src` folder contains excerpts from the actual camera connection, four-frame processing, candidate presentation/selection, local output and OCR decoding code. Omissions are marked. These files are not a complete runnable application. Model weights, connection details and production configuration are excluded.

## Screenshots in execution order

### 1. Initial four-candidate interface

<a href="screenshots/01-initial-interface.png"><img src="screenshots/01-initial-interface.png" width="320" alt="Initial four-candidate interface"></a>

### 2. Manual camera connection (IP masked in the supplied image)

<a href="screenshots/02-manual-camera-connection.png"><img src="screenshots/02-manual-camera-connection.png" width="320" alt="Manual camera connection (IP masked in the supplied image)"></a>

### 2.1. Enter the camera username

<a href="screenshots/02a-camera-username.png"><img src="screenshots/02a-camera-username.png" width="320" alt="Enter the camera username"></a>

### 2.2. Enter the camera password; characters are masked

<a href="screenshots/02b-camera-password.png"><img src="screenshots/02b-camera-password.png" width="320" alt="Enter the camera password; characters are masked"></a>

### 3. Connected live camera before recognition

<a href="screenshots/03-live-camera.png"><img src="screenshots/03-live-camera.png" width="260" alt="Connected live camera before recognition"></a>

### 4. Recognition results: one readable candidate and other failed candidates

<a href="screenshots/04-recognition-candidates.png"><img src="screenshots/04-recognition-candidates.png" width="260" alt="Recognition results: one readable candidate and other failed candidates"></a>

### 5. Local save confirmation and cleared candidates for the next vehicle

<a href="screenshots/05-local-save-confirmation.png"><img src="screenshots/05-local-save-confirmation.png" width="260" alt="Local save confirmation and cleared candidates for the next vehicle"></a>

## Saved output and runtime evidence

The supplied archive contains one saved recognition record, dated 2026-10-27 at 12:45:07, with source `ip_camera`. Its TXT/CSV result is `16ع45179`. The original vehicle frame and plate crop are included for comparison; the record is an OCR output, not independently verified ground truth or an accuracy benchmark.

| File | Evidence |
|---|---|
| [plates.csv](sample-output/outputs/plates.csv) | One structured record: timestamp, full plate, plate parts, special-plate flag and source |
| [plates.txt](sample-output/outputs/plates.txt) | Human-readable form of the same saved record |
| [passage_app.log](sample-output/logs/passage_app.log) | One application-start entry identifying version 6.3.6; this supplied log has no save-success event |

<a href="sample-output/outputs/vehicle_20261027_124507.jpg"><img src="sample-output/outputs/vehicle_20261027_124507.jpg" width="320" alt="Original saved vehicle frame"></a>

<a href="sample-output/outputs/plate_20261027_124507.jpg"><img src="sample-output/outputs/plate_20261027_124507.jpg" width="200" alt="Original saved plate crop"></a>

[requirements.txt](requirements.txt) preserves the dependency declarations supplied with this version; dependencies were not installed or runtime-tested during documentation review.

### Archive review notes

All seven numbered screenshots are represented in the documentation sequence: the username and password images already added match archive images 3 and 4 exactly. The supplied `README_FA.txt` describes an older v5.1 workflow, so it is not used as the operating guide for v6.3.6. Only selected Python excerpts are published, as intended.

Click an image to view its original size.

[Back to desktop stages](../README.md)
