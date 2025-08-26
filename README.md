# Measuring Movement, Not Just Motion  
### A Pose-Based DTW + LSTM Pipeline for Football Rehab  

**Author:** Jaime Tellie  
**Thesis:** MSc Data Analytics – August 2025  

---

## 📖 Overview  
This repository contains the full implementation of my MSc Data Analytics thesis:  

> *“Measuring Movement, Not Just Motion: A Pose-Based, DTW+LSTM Pipeline for Football Rehab.”*  

The project develops a physiotherapy- and football-centric pipeline to **evaluate movement quality from single-view videos**. By extracting joint angles using **MediaPipe Pose** and computing **windowed Dynamic Time Warping (DTW) degradation scores**, the system captures execution drift under fatigue or compensation. On top of this, **LSTM-based models** predict movement quality trends, enabling objective, clinician-aligned tracking for **return-to-play support**. 


📄 **Read the full thesis here:**  
[SDC_MSc_Data_Analytics_IV_Project_Thesis___Jaime_Tellie.pdf](./SDC_MSc_Data_Analytics_IV_Project_Thesis___Jaime_Tellie.pdf)  

---

## 🏗️ Pipeline Architecture  

1. **Video Preprocessing**  
   - Input videos → 30 FPS frame streams  
   - Missing landmarks handled via interpolation  
   - Consistent windowing: 30 frames (1s) with stride 10 (0.33s)  

2. **Pose Estimation & Angle Extraction**  
   - MediaPipe Pose (VIDEO mode)  
   - Joints: hips, knees, shoulders, elbows  
   - Per-frame joint angles computed via vector dot-product  

3. **Feature Engineering**  
   - **Angles (base features)**  
   - **ROM (Range of Motion)**  
   - **Angular Velocity (mean/max/std)**  
   - **Symmetry Dispersion** (L/R compensation)  
   - **DTW Degradation** vs. session baseline  

4. **Degradation Scoring (DTW)**  
   - Window-level DTW distance to reference execution  
   - Robust to tempo variation and drift  

5. **Sequence Modeling (LSTM/GRU)**  
   - Input: windowed angle features  
   - Architecture: Conv1D → GRU → Dense → Output  
   - Loss: Huber | Metrics: MAE, R²  

6. **Evaluation & Reporting**  
   - MAE, R² by exercise and feature set  
   - Visualizations: error plots, loss curves, prediction vs. target  
   - Natural-language summaries for clinical relevance  

---

## 📊 Results  

- **Basic features (angles only)** outperformed in **3/4 exercises**  
  - Squat: R² = 0.703, MAE = 0.085  
  - Lunges: R² = 0.612, MAE = 0.067  
  - Bench Press: R² = 0.560, MAE = 0.086  
- **Featured set (angles + engineered descriptors)** improved performance only for **Pull-Ups**  
  - R² = 0.657 vs. 0.612 (∆ +0.045)  

👉 Interpretation: Engineered features (ROM, velocity, symmetry) are useful when kinematics are complex (e.g., pull-ups) but can inject noise under low-quality landmark detection.  

---

## 🛠️ Tech Stack  

- **Pose Estimation**: MediaPipe Tasks API (Pose Landmarker)  
- **Video I/O**: OpenCV  
- **Data Handling**: NumPy, Pandas  
- **Modeling**: TensorFlow / Keras (LSTM, GRU, Conv1D hybrids)  
- **Experimentation**: YAML/JSON configs + reproducible seeds  
- **Visualization**: Matplotlib  

---

## 📌 Key Contributions  

- ⚽ **Football rehab focus**: Tracking fatigue, compensation, and return-to-play progress  
- 🧩 **Modular pipeline**: Preprocessing → DTW degradation → LSTM modeling  
- 📈 **Window-level scoring**: Clinician-aligned, robust to tempo variation  
- 🔎 **Interpretability**: DTW + symmetry dispersion as transparent metrics  
- 🧑‍⚕️ **Clinical relevance**: Mobility (ROM), tempo/load proxies (velocity), compensation/asymmetry  

---

## 🔮 Future Work  

- Multi-view or 3D pose (BlazePose 3D, VIBE)  
- Larger, balanced datasets with standardized capture  
- Real-time/edge deployment for in-clinic use  
- Extension to football-specific actions (e.g., free kicks, penalties)  
- Explainability overlays (attention on joints/time-steps)  