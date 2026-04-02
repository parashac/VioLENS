#  VioLENS — Real-Time Violence Detection from CCTV Footage

> A real-time violence detection system for CCTV and webcam footage, powered by **MobileNetV2 + LSTM** deep learning architecture.

---

##  Overview

**VioLENS** is a real-time system for detecting violent activity from CCTV and webcam footage. It is designed to assist in public safety monitoring by providing automated alerts when violent events are detected. The system uses a combination of deep learning techniques — specifically **MobileNetV2** for feature extraction and **LSTM** for temporal sequence modeling — to analyze video streams efficiently and accurately.

---

## ✨ Features

-  Real-time detection of **violent** and **non-violent** activities
-  Supports multiple video sources: **RTSP/IP cameras** and **local webcams**
-  Displays live **confidence probabilities** for each class
-  **Alert system** triggers when violence is detected
-  **Detection logs** with timestamps for each event
-  Lightweight architecture optimized for **real-time performance**

---

##  Methodology

### 1. Preprocessing & Frame Sampling
- Video streams are sampled at a fixed frame rate to extract **30-frame sequences**
- Frames are resized to **224×224** for compatibility with MobileNetV2
- Normalization ensures consistent input values for the model

### 2. Feature Extraction
- **MobileNetV2** is used as a backbone CNN to extract spatial features efficiently
- Its lightweight architecture allows real-time inference on CPU/GPU

### 3. Temporal Modeling
- **LSTM layers** capture temporal dependencies across frames
- Helps distinguish between violent and non-violent actions that may unfold over several seconds

### 4. Classification & Alerts
- Final fully connected layer with **Softmax** outputs probabilities for `Violent` and `Non-Violent` classes
- Alert system triggers on violent detection with **confidence thresholds**

---

## 🎬 Demo

### 🟢 Non-Violent Detection — Scene 2
https://github.com/user-attachments/assets/4388f626-3160-483f-a40f-286a6200104e

### 🔴 Violent Detection — Scene 2
https://github.com/user-attachments/assets/06406285-820f-4d92-9c79-78db98c8399e

### 🔴 Violent Detection — Scene 3

https://github.com/user-attachments/assets/271ddfaa-4b0c-4396-bcb1-5407f27a351d


---

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/VioLENS.git
cd VioLENS
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🖥️ Usage

### 1. Start the Flask backend

```bash
python app.py
```

### 2. Access the web interface

Open your browser and navigate to:

```
http://localhost:5000
```

### 3. Connect a video source

| Source | Steps |
|--------|-------|
| 📡 RTSP / IP Camera | Enter the stream URL in the input field and click **CONNECT** |
| 📷 Local Webcam | Click **START WEBCAM** |

The system will display live video, detection results, probability bars, and detection logs.


---

## ⚠️ Challenges

-  Collecting high-quality and balanced video data for violent and non-violent classes
-  Ensuring real-time inference with limited computational resources
-  Synchronizing LSTM temporal processing with live frame streaming
-  Maintaining stable RTSP and webcam connections across different network conditions

---


## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
