# 🚦 Traffic-AI Management System
Python • React • Node.js • YOLOv8

An AI-powered smart traffic management system that monitors real-time traffic using CCTV feeds, detects vehicles using deep learning, and dynamically optimizes traffic signals.

---

## 📌 Overview

Traffic-AI is designed to:
- Detect vehicles from live camera feeds
- Analyze traffic density in real-time
- Automatically adjust traffic signals
- Handle emergency vehicles
- Provide live dashboard and analytics

---

## 🚀 Features

### 🎥 CCTV Monitoring
- Multi-camera live feeds
- Real-time detection with bounding boxes

### 🧠 AI Detection
- YOLOv8 model
- Detects:
  - Car
  - Bike
  - Truck
  - Bus

### 📊 Traffic Analysis
- Vehicle count per lane
- Density levels:
  - Low
  - Medium
  - High

### 🚦 Smart Signal Control
- Dynamic green signal timing
- Lane-wise optimization
- Automatic congestion handling

### 🚑 Emergency Handling
- Ambulance detection
- Priority signal override

### 🗺️ Traffic Map
- Live congestion visualization
- Color indicators:
  - 🟢 Low
  - 🟡 Medium
  - 🔴 High

### 🚨 Alerts
- Traffic congestion alerts
- Emergency alerts
- Signal failure alerts

### 📈 Analytics
- Traffic trends
- Peak hour analysis
- Speed and congestion metrics

---

## 🛠️ Tech Stack

| Technology | Purpose |
|----------|--------|
| React.js | Frontend |
| Tailwind CSS | Styling |
| Node.js + Express | Backend |
| YOLOv8 | Detection |
| FastAPI | AI Service |
| MongoDB | Database |
| Socket.io | Realtime |
| Leaflet.js | Maps |

---

## 📂 Project Structure

traffic-ai/
│
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── services/
│
├── backend/
│   ├── controllers/
│   ├── routes/
│   ├── models/
│
├── ai-service/
│   └── main.py
│
└── README.md

---

## ⚙️ Working Flow

1. Camera feeds provide live video  
2. YOLOv8 detects vehicles  
3. Vehicles are counted per lane  
4. Traffic density is calculated  
5. Signal timing is adjusted  
6. Emergency vehicles trigger priority mode  
7. Dashboard updates in real-time  

---

## 📡 Architecture

Camera → YOLOv8 → FastAPI → Backend → WebSocket → Frontend

---

## 📥 Installation

### Clone Repo
git clone https://github.com/your-username/traffic-ai.git  
cd traffic-ai  

### Frontend
cd frontend  
npm install  
npm run dev  

### Backend
cd backend  
npm install  
npm start  

### AI Service
cd ai-service  
pip install -r requirements.txt  
uvicorn main:app --reload  

---

## 🤖 API

POST /detect  

Response:
{
  "detections": [
    {
      "label": "car",
      "confidence": 0.91,
      "bbox": [x, y, w, h]
    }
  ]
}

---

## 💡 Future Improvements

- Number plate recognition  
- Accident detection  
- Traffic prediction  
- Cloud deployment  
- Mobile app  

---

## ⚠️ Disclaimer

This project is for educational purposes only.

---

## 👨‍💻 Author

Abhinav Bahadur Singh  
GitHub: https://github.com/abhinavbahadursingh  

---

## 🚀 Conclusion

A smart traffic system combining AI + real-time processing to improve city traffic efficiency 🚦
