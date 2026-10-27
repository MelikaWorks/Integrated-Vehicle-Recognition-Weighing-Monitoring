[فارسی](README.fa.md) | [English](README.md)

# 05 — Weighbridge Weight Reading and Integration Path

After plate recognition and the management dashboard, development progressed to acquiring weighbridge weight through a Windows tool and agent. According to the developer, an initial device connection was established, followed by receiving and displaying weight in a test application. The goal was to bring weight, plate recognition and weighing information into a shared management/security workflow.

## Development progression

| Stage | Outcome and status |
|---|---|
| Device connectivity | An initial tool established communication and received data |
| Weight reading | Field-test acquisition and display, as reported by the developer |
| Integration | Weight and plate capabilities were brought toward the weighing-management workflow; the final interface is not public |
| Central web hosting | Depended on procuring a server; centralized web deployment is not presented as completed |

The weight-reading agent is distinct from the [plate-to-weighing-form agent](../04-Weighbridge-Agent-Integration/). This section publishes only a high-level capability and development account.

## Public photographs

The first two photographs provide field-test context. The additional cropped photographs show the developer's test reader, weight agent output and local API response. Communication settings, raw data and addresses have been removed by cropping. Visible results are preserved from the supplied photographs; no generated or reconstructed imagery is used. These images are not calibration evidence or the final dashboard.

### 1. Actual weighbridge environment

<a href="screenshots/01-weighbridge-field-context.jpg"><img src="screenshots/01-weighbridge-field-context.jpg" width="300" alt="Field-test weighbridge environment"></a>

### 2. Existing weighing application in the test environment

<a href="screenshots/02-existing-weighing-application.jpg"><img src="screenshots/02-existing-weighing-application.jpg" width="500" alt="Existing weighing application displaying weight"></a>

This is the existing weighing application's screen, not the final product interface or independent proof of the new reader's correctness. Photographs were taken at different times and do not constitute a simultaneous comparison of two weight measurements. Click an image for the original size.


### 3. Test reader displaying 43,400 kg

<a href="screenshots/03-test-reader-weight.jpg"><img src="screenshots/03-test-reader-weight.jpg" width="500" alt="Test reader displaying 43,400 kg"></a>

### 4. Agent repeatedly reporting Weight=16470 and Stable=True

<a href="screenshots/04-agent-weight-output.jpg"><img src="screenshots/04-agent-weight-output.jpg" width="350" alt="Agent repeatedly reporting Weight=16470 and Stable=True"></a>

### 5. Local API response reporting connected=true, hasWeight=true, weight=16470 and stable=true

<a href="screenshots/05-local-api-weight.jpg"><img src="screenshots/05-local-api-weight.jpg" width="500" alt="Local API response reporting connected=true, hasWeight=true, weight=16470 and stable=true"></a>

These captures document different test moments. The 43,400 kg reader image and the earlier existing-application image displaying 43,420 are not a synchronized accuracy comparison. The agent and API photographs both display 16,470, at different timestamps. Click to view the published crop; unredacted originals are not included.

## Proprietary commercial component

This component has evolved into a commercial product. The weight acquisition and processing code, including its agent, is proprietary and is not published in this repository. Copyright © 2026 Melika Mehranpour. All rights reserved.

Communication/acquisition code, processing algorithms, protocol details, raw device data, runtime configuration, build files, binaries and the final integrated-dashboard image are excluded. Neither form code nor the WeighbridgeSystem archive is published. Public documentation does not provide the proprietary acquisition implementation.

This publication contains documentation and selected photographs only. No application execution, device test or measurement-accuracy verification was performed during this review.
