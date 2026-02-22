# 🔍 Welding Defect Report Generator (XAI Based)

An AI-powered Welding Defect Detection and Explainable AI (XAI) Report Generator built using **FastAPI** and **YOLOv8**.

The system detects welding quality from images and classifies them into:

- **0 → Bad Weld**
- **1 → Good Weld**
- **2 → Defect**

It also generates structured inspection reports for analysis.

---

## 🚀 Features

- Welding defect detection using YOLOv8
- Explainable AI (XAI) insights
- Automated report generation
- FastAPI backend
- Web interface for image upload
- Local deployment support

---

## 🛠 Technologies Used

- Python  
- FastAPI  
- Uvicorn  
- YOLOv8 (Ultralytics)  
- PyTorch  
- OpenCV  
- NumPy  


---

## 📂 Project Structure


Welding-defect-report-generator/
│
├── app.py
├── detector.py
├── explain.py
├── report.py
├── defect_knowledge.py
│
├── best.pt
├── yolov8n.pt
│
├── templates/
│ └── index.html
│
├── README.md
├── .gitignore


### ⚠️ Not Included in Repository

The following folders are automatically generated during runtime and are excluded using `.gitignore`:


venv/
pycache/
runs/
uploads/
reports/


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository


git clone https://github.com/reemparkar2004/Welding-defect-report-generator.git

cd Welding-defect-report-generator


---

### 2️⃣ Create Virtual Environment


python -m venv venv


---

### 3️⃣ Activate Virtual Environment

**Windows:**

venv\Scripts\activate


---


### 5️⃣ Run the Application


python -m uvicorn app:app --reload


---

### 6️⃣ Open in Browser

Open the following URL in your browser:


http://127.0.0.1:8000


If the server runs successfully, you will see:


Uvicorn running on http://127.0.0.1:8000

{0: 'Bad Weld', 1: 'Good Weld', 2: 'Defect'}


---

## 📊 How It Works

1. User uploads a welding image.
2. YOLOv8 model detects defects.
3. The weld is classified into predefined categories.
4. XAI logic provides interpretability.
5. A structured inspection report is generated.

---
