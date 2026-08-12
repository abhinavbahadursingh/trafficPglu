# 🚦 Traffic Management System (trafficPglu)

**Python • OpenCV • YOLO • TensorFlow • SUMO • Firebase • Tkinter**

An AI-powered smart traffic management system focused on **Lucknow (LKO) traffic**. The repository is a
monorepo that combines computer-vision based **crash detection**, **real-time vehicle tracking & speed
estimation**, and **reinforcement-learning based adaptive traffic signal control** — all feeding into a
shared Firebase Realtime Database.

---

## 📌 Overview

The system solves three core problems in urban traffic management:

| Problem | Solution | Sub-project |
|---------|----------|-------------|
| 🚨 Vehicle crash detection from CCTV | Deep-learning detection models + alert pipeline | `crashDetectionSystem`, `vehicle-crash-detector` |
| 📡 Live vehicle monitoring | YOLO tracking, speed estimation, GPS mapping | `realTimeTracking` |
| 🚦 Traffic signal optimization | RL agents trained in a SUMO simulator | `rlSUmo-main` |

All detected events (vehicle positions, speeds, crashes/breakdowns) are pushed to a shared **Firebase
Realtime Database** with GPS coordinates converted from camera pixel positions via a homography matrix.

---

## 🗂️ Repository Structure

```
trafficPglu/
├── crashDetectionSystem/     # YOLO crash detection + training experiments
├── realTimeTracking/         # Real-time vehicle tracking, counting & speed
├── rlSUmo-main/              # RL-based traffic signal control (SUMO/TraCI)
├── vehicle-crash-detector/   # TensorFlow crash detector desktop app (Tkinter)
└── README.md
```

---

## 1️⃣ crashDetectionSystem

YOLO-based vehicle **crash detection** built around a custom-trained `best.pt` model (single class: `crash`).

### Components

| File | Purpose |
|------|---------|
| `traininingModel/crashDetection.py` | Runs the trained YOLO `best.pt` on a video and annotates frames |
| `traininingModel/data.yml` | Dataset config (`nc: 1`, class `crash`) for training |
| `Models/best.pt` | Trained YOLO crash-detection model weights |
| `Testing/detectoin.py` | Heuristic crash detection: sudden-deceleration + bounding-box IoU collision, pushes to Firebase |
| `Testing/backup.txt.py` | Alternative heuristic: stationary-vehicle detection after sudden stop |
| `Testing/crashToFirebase.py` | Uploads crash records (lat/lon/timestamp) to Firebase |
| `cv2use.py` | Simple OpenCV Haar-cascade vehicle detector (demo using `cars.xml`) |
| `test_images/`, `test_videos/` | Sample media for testing the model |
| `traininingModel/runs/` | Training/prediction run artifacts (batch images, args) |

### Features
- Custom-trained YOLO model for crash detection (trained on a `crash` dataset)
- Heuristic crash confirmation via speed drops and object collisions (IoU)
- Automatic Firebase upload of crash events with GPS location

---

## 2️⃣ realTimeTracking

Real-time **vehicle detection, tracking, counting, and speed estimation** on live CCTV feeds.

### Components

| File | Purpose |
|------|---------|
| `demo_working/mainRunFile.py` | Main pipeline: YOLO11 tracking, red/blue line counting (direction-wise), speed calculation, multithreaded Firebase upload |
| `demo_working/demo.py` | Tracking + per-vehicle speed, CSV logging, sudden-stop → accident push to Firebase |
| `demo_working/vehicleData.py` | Uploads per-vehicle positions (converted to GPS) to Firebase |
| `demo_working/speedData.py` | Logs speed to CSV + Firebase (per-track-id, time-indexed) |
| `demo_working/accident.py` | Pushes vehicle breakdown events to Firebase |
| `demo_working/gps.py` | Camera homography (`H`) → pixel-to-GPS conversion |
| `demo_working/firebase_auth.py` | Firebase Admin SDK initialization |
| `demo_working/threadindDemo.py` | Threaded object-tracking → Firebase queue demo |
| `demo_working/*.py` (others) | Experimental helpers (CSV writers, avg speed, background subtraction) |
| `demo_working/yolo11n.pt`, `yolov5s.pt` | Detection models |
| `speed_data/`, `*.csv` | Speed logs and average-speed artifacts |

### Features
- YOLO (v5 / v11) object tracking with persistent IDs
- Virtual **red/blue line** crossing counters for both directions
- Per-vehicle speed estimation (km/h) using pixel-distance + frames-per-second calibration
- GPS mapping of every tracked vehicle
- Accident/breakdown detection on sudden stops

---

## 3️⃣ rlSUmo-main

**Reinforcement Learning for adaptive traffic signal control**, simulated in **Eclipse SUMO** via TraCI.

### Components

| File | Purpose |
|------|---------|
| `traci5.FT.py` | **Fixed-time** baseline: static signal timing (used as baseline comparison) |
| `traci6.QL.py` | **Q-Learning** (tabular): state = queue lengths from 6 lane-area detectors + current phase; reward = negative total queue length |
| `traci7.DQL.py` | **Deep Q-Learning**: same formulation but with a Keras feed-forward Q-network (Adam, MSE) |
| `Traci4.py` | **Emergency vehicle preemption**: dynamically extends/shortens phases to give green light to `emergency` type vehicles |
| `RL.sumocfg`, `RL.net.xml`, `RL.rou.xml`, `RL.add.xml` | SUMO network (7 nodes, 2 traffic lights `Node2`/`Node5`), vehicle flows, and lane-area detectors |
| `Test1.*` | Alternative SUMO scenario with an emergency-vehicle trip |
| `e2_*.xml` | Detector output/validation files |

### RL Formulation
- **State**: `(q_EB_0, q_EB_1, q_EB_2, q_SB_0, q_SB_1, q_SB_2, current_phase)`
- **Actions**: `0 = keep phase`, `1 = switch phase` (with `MIN_GREEN_STEPS` guard)
- **Reward**: negative total queue length
- **Algorithms**: Fixed-time baseline → Q-Learning → Deep Q-Learning, with cumulative reward / queue-length plots

---

## 4️⃣ vehicle-crash-detector

A complete desktop **Vehicle Crash Detector** application (Tkinter GUI) powered by a **TensorFlow 2 Object
Detection** model.

### Components

| File | Purpose |
|------|---------|
| `main.py` | Entry point — launches the Tkinter app |
| `vcd_ui.py` | Main GUI (video source selection, detection toggle, progress bar) |
| `vehicle_crash_detection.py` | Loads the TF saved model, runs inference, saves snapshots, triggers Firebase alerts |
| `image_data_viewer.py` | Records viewer for saved crash images |
| `label_map.pbtxt` | Single class: `vehicle crash detected` |
| `inference_graph/saved_model` | Trained TensorFlow crash-detection model |
| `myfirebase/crash_to_firebase.py` | Uploads detected crashes (pixel → GPS) to Firebase |
| `dummyData.py` | Simulates crash events every 5 seconds for testing |
| `messages/` | Email templates for Hospital / Police Station / RTO |
| `outputs/` | Saved frame images, inside-label crops, and detection videos |
| `resources/icon/` | Application icons (Flaticon/Freepik) |

### Features
- Detect crashes from **video files** or **live camera** feeds
- Saves crash snapshots (full frame + sharpened crop) locally, viewable in the Records section
- Automatic Firebase alert with GPS location and timestamp
- Email/SMS alert templates for emergency services (Hospital, Police, RTO)

> **Note:** This sub-project was originally developed by [ashin-coder](https://github.com/ashin-coder)
> et al. and has been extended here with Firebase integration (`myfirebase/`).

---

## 🔄 Data Flow (shared Firebase)

```
CCTV / Video Feed
      │
      ▼
YOLO Detection + Tracking        (realTimeTracking)
      │  vehicle position (cx, cy) + speed
      ▼
Pixel → GPS homography           (gps.py / crash_to_firebase.py)
      │
      ▼
Firebase Realtime DB             traffic_data
      ├── vehicle_Data/  (positions, per-class totals)
      ├── speed_Data/    (per-track speed history)
      ├── vehicle_Breakdown/     (stalled / crashed vehicles)
      └── crash_vehicle/         (detected crashes)

Traffic signals ──► RL agent (Q-Learning / DQN) trained in SUMO (rlSUmo-main)
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.9 / 3.12 | Primary language |
| OpenCV (`cv2`) | Video capture, frame processing, visualization |
| Ultralytics YOLO (v5 / v8 / v11) | Object detection & multi-object tracking |
| TensorFlow 2 (Object Detection API) | Crash-detection saved-model inference |
| Eclipse SUMO + TraCI | Traffic micro-simulation & RL environment |
| Q-Learning / Deep Q-Learning (Keras) | Adaptive signal timing |
| Firebase Admin SDK (Realtime DB) | Central data store / alerting |
| Tkinter | Desktop GUI for crash detector |
| NumPy / pandas / matplotlib | Math, data logging, plots |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+ (some sub-projects were developed on 3.9 / 3.12)
- [Eclipse SUMO](https://eclipse.dev/sumo/) installed and `SUMO_HOME` set as an environment variable
- A Firebase project with a service-account JSON key and a Realtime Database URL

### 1. Install dependencies
Each sub-project is standalone. Install the common vision stack once:

```bash
pip install ultralytics opencv-python numpy pandas matplotlib
pip install firebase-admin
pip install tensorflow   # only needed for vehicle-crash-detector
```

### 2. Configure Firebase
Edit the hard-coded credential path & database URL in each `firebase_auth.py` /
`crash_to_firebase.py` / `myfirebase/crash_to_firebase.py` file, or better, switch them to environment
variables:

```python
cred = credentials.Certificate(os.environ["FIREBASE_SERVICE_ACCOUNT"])
databaseURL="https://<your-project>-default-rtdb.firebaseio.com/"
```

### 3. Run each module

```bash
# Real-time tracking (adjust the video path in the script)
python realTimeTracking/demo_working/mainRunFile.py

# YOLO crash detection on a video
python crashDetectionSystem/traininingModel/crashDetection.py

# RL signal control in SUMO (fixed-time / QL / DQL / emergency preemption)
python rlSUmo-main/traci5.FT.py
python rlSUmo-main/traci6.QL.py
python rlSUmo-main/traci7.DQL.py
python rlSUmo-main/Traci4.py

# Vehicle Crash Detector desktop app (TensorFlow model required)
python vehicle-crash-detector/main.py
```

---

## ⚠️ Important Notes

- **Hard-coded paths**: Many scripts contain absolute paths (e.g. `E:\codify_hackarena\...`) from the
  author's machine. Update these before running.
- **Firebase credentials**: The service-account JSON files are **not committed** (see `.gitignore`). You
  must supply your own key.
- **Models**: `Models/best.pt`, `yolo11n.pt`, `yolov5s.pt`, and `inference_graph/saved_model` are model
  weights/artifacts required at runtime.
- **Detection accuracy** depends on camera quality, viewing angle, and the trained dataset — the system is
  a demonstration/research prototype, not a certified safety system.

---

## 📝 TODO / Possible Extensions

- Replace hard-coded credential paths with environment variables / a config file
- Persist RL Q-tables / DQN weights so models can be reused after training
- Add a web dashboard to visualize the Firebase data in real time
- Fuse `crashDetectionSystem` (YOLO) with `vehicle-crash-detector` (TF) into one pipeline
- Calibrate the pixel-to-GPS homography per camera

---

## 👨‍💻 Author

**Abhinav Bahadur Singh**  
GitHub: [abhinavbahadursingh](https://github.com/abhinavbahadursingh)



---

## 📄 License

This project is for **demonstration and research purposes only**. Some test videos, images, and model
artifacts are sourced from the internet and may be subject to their original licenses. Refer to the
individual sub-project READMEs for details.
