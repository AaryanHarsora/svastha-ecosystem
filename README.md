<div align="center">

<!-- Animated Header Banner -->

<!-- Typing Animation -->
<a href="https://git.io/typing-svg">


<!-- Typing Animation -->
<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=1D9E75&center=true&vCenter=true&width=700&lines=Full-Stack+Healthcare+Ecosystem;Patient+Management+%2B+ML+Disease+Prediction;Pharmacy+Marketplace+%2B+Appointments;FastAPI+%2B+MariaDB+%2B+scikit-learn" alt="Typing SVG" />
</a>

<br/><br/>

<!-- Badges Row 1 -->
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-InnoDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![HTML5](https://img.shields.io/badge/Frontend-HTML%2FJS-E34F26?style=for-the-badge&logo=html5&logoColor=white)

<br/>

<!-- Badges Row 2 -->
![GitHub repo size](https://img.shields.io/github/repo-size/yourusername/svastha-ecosystem?style=flat-square&color=1D9E75)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/svastha-ecosystem?style=flat-square&color=1D9E75)
![Status](https://img.shields.io/badge/status-Active-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-Educational-green?style=flat-square)

</div>

---

## 🌿 What is Svastha?

**Svastha** *(Sanskrit: in good health)* is a complete mini healthcare platform built as a DBMS project at SVKM's NMIMS MPSTME. It connects patients, doctors, hospitals, pharmacies, and clinical ML models into one unified system backed by an 18-table normalized relational database.

> One platform. Six modules. End-to-end healthcare data management.

---

## ✨ How it Works

```
👤 Add Patient  ──►  📋 Enter Health Data  ──►  🔮 Predict Disease
                                                        │
                                                        ▼
🛒 Order Medications  ◄──  📅 Book Appointment  ◄──  💊 Get Recommendations
```

---

## 🚀 Features

<table>
  <tr>
    <td align="center" width="200">
      <b>🔍 Disease Prediction</b><br/>
      <sub>ML model trained on heart, cardio & kidney datasets. Computes risk scores from patient vitals.</sub>
    </td>
    <td align="center" width="200">
      <b>👤 Patient Records</b><br/>
      <sub>Full CRUD — register, update, and view complete patient medical history.</sub>
    </td>
    <td align="center" width="200">
      <b>💊 Recommendations</b><br/>
      <sub>Auto-suggests medications based on diagnosed conditions via a disease→drug knowledge base.</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="200">
      <b>📅 Appointments</b><br/>
      <sub>Book and manage doctor appointments with live status tracking (Scheduled / Completed / Cancelled).</sub>
    </td>
    <td align="center" width="200">
      <b>🛒 Marketplace</b><br/>
      <sub>Vendors, inventory tracking, and medication orders with automatic real-time stock deduction.</sub>
    </td>
    <td align="center" width="200">
      <b>📊 Risk Scoring</b><br/>
      <sub>Computes heart, cardio & kidney risk scores. Flags high-risk patients (score > 70) on dashboard.</sub>
    </td>
  </tr>
</table>

---

## 🏗️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🖥️ **Backend** | FastAPI 0.115 | REST API with Swagger docs at `/docs` |
| 🗄️ **Database** | MariaDB + SQLAlchemy 2.0 | 18-table relational schema, InnoDB |
| 🔌 **Driver** | PyMySQL | Python ↔ MariaDB connector |
| ✅ **Validation** | Pydantic v2 | Request/response schema validation |
| 🧠 **ML** | scikit-learn | Disease prediction pipeline |
| 🌐 **Frontend** | HTML + Vanilla JS | No-framework UI, connects via `fetch()` |
| 🔧 **Dev Tools** | Git + uvicorn | Version control + ASGI server |

---

## 📂 Project Structure

```
svastha-ecosystem/
│
├── 📁 backend/
│   ├── 📁 api/
│   │   ├── patients.py          # Patient CRUD + health data + risk scoring
│   │   ├── appointments.py      # Book, update, cancel appointments
│   │   ├── medications.py       # Medication catalogue management
│   │   ├── marketplace.py       # Inventory, vendors, orders
│   │   ├── recommendations.py   # Drug recommendations by patient
│   │   └── predict.py           # ML prediction endpoint
│   │
│   ├── 📁 models/               # SQLAlchemy ORM table definitions
│   ├── 📁 schemas/              # Pydantic request/response models
│   │
│   ├── 📁 db/
│   │   ├── database.py          # Connection pool + session factory
│   │   └── queries.py           # All 20 SQL queries
│   │
│   ├── 📁 ml/
│   │   ├── preprocess.py        # Data cleaning pipeline
│   │   ├── train.py             # Model training script
│   │   ├── predict.py           # Prediction logic
│   │   └── model.pkl            # Saved trained model
│   │
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # DB config + environment vars
│   └── requirements.txt
│
├── 📁 frontend/src/
│   ├── 📁 pages/
│   │   ├── index.html           # Dashboard — KPIs + high-risk patients
│   │   ├── patient.html         # Full patient management hub
│   │   ├── medications.html     # Catalogue + top sellers
│   │   ├── marketplace.html     # Inventory + order placement
│   │   ├── appointments.html    # Booking + status tracking
│   │   └── predict.html         # ML prediction form
│   └── 📁 static/
│       ├── api.js               # All API calls in one place
│       ├── app.js               # UI interaction logic
│       └── style.css
│
├── 📁 migrations/
│   ├── 001_initial_schema.sql   # 18 table definitions (UUID PKs, InnoDB)
│   ├── 002_seed_data.sql        # Realistic seed records
│   └── 003_indexes.sql          # Performance indexes
│
└── 📁 data/raw/
    ├── heart.csv                # UCI heart disease dataset
    ├── cardio_train.csv         # Cardiovascular risk dataset
    └── kidney_disease.csv       # Chronic kidney disease dataset
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11+
- MariaDB or MySQL
- pip

---

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/svastha-ecosystem.git
cd svastha-ecosystem
```

---

### 2️⃣ Create virtual environment & install dependencies

```bash
python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r backend/requirements.txt
```

---

### 3️⃣ Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=medical_db
DB_USER=root
DB_PASSWORD=yourpassword
```

---

### 4️⃣ Set up the database

```bash
mysql -u root -p < migrations/001_initial_schema.sql
mysql -u root -p < migrations/002_seed_data.sql
mysql -u root -p < migrations/003_indexes.sql
```

---

### 5️⃣ Start the backend

```bash
cd backend
uvicorn main:app --reload --port 8001
```

| URL | What's there |
|-----|-------------|
| `http://localhost:8001` | API root |
| `http://localhost:8001/docs` | Interactive Swagger docs |
| `http://localhost:8001/health` | Database health check |

---

### 6️⃣ Open the frontend

Open this directly in any browser — no build step needed:

```
frontend/src/pages/index.html
```

---

## 🔗 API Reference

<details>
<summary><b>👤 Patients</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/patients/` | List all patients |
| `POST` | `/patients/` | Register new patient |
| `PUT` | `/patients/{id}` | Update patient details |
| `DELETE` | `/patients/{id}` | Remove patient |
| `POST` | `/patients/{id}/health` | Submit health data + compute risk scores |
| `GET` | `/patients/{id}/risk` | Fetch risk score for patient |
| `GET` | `/patients/high-risk/list` | Patients with risk score > threshold |
| `GET` | `/patients/{id}/appointments` | Patient appointment history |
| `GET` | `/patients/{id}/orders` | Patient order history |
| `POST` | `/patients/{id}/symptoms` | Log a symptom for patient |

</details>

<details>
<summary><b>💊 Medications & Recommendations</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/medications/` | Full medication catalogue |
| `POST` | `/medications/` | Add new medication |
| `PUT` | `/medications/{id}` | Update medication |
| `DELETE` | `/medications/{id}` | Remove medication |
| `GET` | `/medications/top-selling` | Top 5 best sellers by quantity |
| `GET` | `/medications/cheapest-per-category` | Cheapest in-stock per category |
| `GET` | `/recommendations/{patient_id}` | Drug recommendations by diagnosis |

</details>

<details>
<summary><b>📅 Appointments</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/appointments/` | All appointments |
| `POST` | `/appointments/` | Book appointment |
| `PUT` | `/appointments/{id}` | Update status |
| `DELETE` | `/appointments/{id}` | Cancel appointment |
| `GET` | `/appointments/doctors` | List all doctors |
| `GET` | `/appointments/hospitals` | List all hospitals |

</details>

<details>
<summary><b>🛒 Marketplace</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/marketplace/stock` | Stock availability + status labels |
| `GET` | `/marketplace/inventory` | Inventory summary stats |
| `GET` | `/marketplace/vendors` | All vendors with supply stats |
| `POST` | `/marketplace/orders` | Place order (auto stock deduction) |
| `PUT` | `/marketplace/orders/{id}/status` | Update order status |
| `DELETE` | `/marketplace/orders/{id}` | Cancel order |
| `PUT` | `/marketplace/inventory/{id}` | Update inventory entry |

</details>

<details>
<summary><b>🔬 Diseases & Prediction</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/diseases/` | All diseases |
| `GET` | `/diseases/patient-count` | Disease prevalence stats |
| `GET` | `/diseases/symptoms` | All symptoms |
| `POST` | `/predict` | ML prediction from vitals |

</details>

---

## 🧠 Machine Learning Pipeline

```
Raw CSV Data          Preprocessing         Training            Inference
─────────────         ─────────────         ────────            ─────────
heart.csv        ──►  preprocess.py   ──►   train.py   ──►    model.pkl
cardio_train.csv                                                    │
kidney_disease.csv                                                  ▼
                                                             predict.py
                                                                    │
                                                                    ▼
                                                        POST /patients/{id}/health
                                                        Returns: heart / cardio /
                                                                 kidney / overall score
```

**Rule-based risk scoring factors:**

| Factor | Heart | Cardio | Kidney |
|--------|-------|--------|--------|
| Cholesterol > 240 mg/dl | +20 | +20 | — |
| Blood pressure > 140 mmHg | +15 | +25 | +15 |
| Fasting blood sugar high | +10 | — | — |
| Heart disease flag | +30 | — | — |
| Hypertension | — | — | +30 |
| Diabetes | — | — | +25 |
| Smoking | — | +15 | — |
| Alcohol use | — | +10 | — |

> **Overall score** = average of heart + cardio + kidney scores (0–100).  
> Patients scoring **above 70** are automatically flagged as high-risk on the dashboard.

---

## 🗄️ Database Design

**18 tables** across 6 functional domains:

```
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│  Core Infrastructure │   │   Medical Records    │   │    Knowledge Base   │
│  ─────────────────  │   │  ─────────────────── │   │  ───────────────── │
│  Hospitals           │   │  Diseases            │   │  Medications        │
│  Doctors             │   │  Patient_Diseases    │   │  Disease_Medications│
│  Patients            │   │  Symptoms            │   └─────────────────────┘
│  Appointments        │   │  Patient_Symptoms    │
└─────────────────────┘   └─────────────────────┘
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│    Marketplace       │   │     Analytics        │   │  Clinical Datasets  │
│  ─────────────────  │   │  ─────────────────── │   │  ───────────────── │
│  Vendors             │   │  Risk_Scores         │   │  Heart_Data         │
│  Inventory           │   └─────────────────────┘   │  Cardio_Data        │
│  Orders              │                              │  Kidney_Data        │
│  Order_Items         │                              └─────────────────────┘
└─────────────────────┘
```

- All primary keys use **UUID** (`CHAR(36)`)
- All tables use **InnoDB** engine
- Foreign keys use `ON DELETE CASCADE` or `ON DELETE RESTRICT` as appropriate
- Database is fully normalized to **BCNF**

---

## 🖥️ Frontend Pages

| Page | File | What it shows |
|------|------|--------------|
| Dashboard | `index.html` | KPI cards, high-risk patient list, disease stats |
| Patients | `patient.html` | Full hub — CRUD, health data, recommendations, orders |
| Medications | `medications.html` | Catalogue, top sellers, cheapest per category |
| Marketplace | `marketplace.html` | Stock table with status labels, vendor list, order form |
| Appointments | `appointments.html` | Booking form with doctor/hospital dropdowns |
| Prediction | `predict.html` | ML input form with risk score output |

---

## 🔮 Future Improvements

- [ ] JWT authentication + role-based access (admin / doctor / patient)
- [ ] React or Vue frontend with proper component architecture
- [ ] Real-time analytics dashboard with live WebSocket updates
- [ ] Advanced ML models — XGBoost, Random Forest ensemble
- [ ] Docker + cloud deployment (AWS / GCP / Railway)
- [ ] SMS / email notifications for appointments
- [ ] Prescription PDF generation

---

## 🤝 Contributing

```bash
# Fork → Clone → Branch → Code → PR

git checkout -b feature/your-feature-name
git commit -m "add: your feature description"
git push origin feature/your-feature-name
```

Open a Pull Request and describe what you changed and why.

---

## 📜 License

Built for **educational purposes** as a DBMS project.  
SVKM's NMIMS — Mukesh Patel School of Technology Management & Engineering  
A.Y. 2025-26

---

<div align="center">



<img src="https://capsule-render.vercel.app/api?type=waving&color=0:085041,100:1D9E75&height=100&section=footer" width="100%"/>

</div>
