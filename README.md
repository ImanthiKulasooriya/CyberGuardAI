# CyberGuard AI

**AI-Based Cybersecurity Threat Detection and Security Monitoring System**

CyberGuard AI is a full-stack machine learning project designed to classify network activity and identify potentially suspicious traffic. It combines a machine learning pipeline, a FastAPI backend, a React dashboard, and a SQLite database to support security monitoring and threat analysis.

## Features

- Machine learning-based network traffic classification
- Security dashboard with event statistics and risk summaries
- Security event monitoring and alert management
- Risk analysis and report generation
- CSV-based prediction workflow
- Database storage for security events and alerts
- Model evaluation and feature analysis reports

## Technologies Used

**Programming languages:** Python, JavaScript, SQL, HTML, CSS

**Machine learning and data processing:** Scikit-learn, Pandas, NumPy

**Backend:** FastAPI, SQLAlchemy

**Frontend:** React, Vite

**Database:** SQLite

**Dataset:** UNSW-NB15

**Development tools:** Git, GitHub, Visual Studio Code

## Machine Learning

The project uses the UNSW-NB15 network intrusion dataset for model development and evaluation. The machine learning workflow includes data inspection, preprocessing, exploratory data analysis, feature engineering, model training, and evaluation.

The repository includes scripts and reports supporting these stages. Consult the evaluation reports for the measured performance of each trained model.

## Application Components

- **Frontend:** React-based security monitoring dashboard.
- **Backend:** FastAPI endpoints for predictions, events, alerts, dashboard statistics, and reports.
- **Database:** SQLite database managed through SQLAlchemy.
- **Machine learning:** Python scripts and saved model artifacts used for network traffic prediction.

## Project Structure

```text
CyberGuardAI/
├── backend/
├── frontend/
├── ml/
├── models/
├── reports/
├── README.md
├── requirements.txt
└── .gitignore
```

The exact files may vary as the project develops.

## Getting Started

### Prerequisites

- Python installed
- Node.js and npm installed
- Git installed

### 1. Clone the repository

```bash
git clone https://github.com/ImanthiKulasooriya/CyberGuardAI.git
cd CyberGuardAI
```

### 2. Set up the Python environment

Create and activate a virtual environment if one is not already included:

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
pip install -r requirements.txt
```

If the repository uses a separate dependency file for machine learning, install the packages listed there as well.

### 3. Run the backend

From the project root, run:

```powershell
uvicorn backend.main:app --reload
```

Backend API: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

The backend also requires the saved model artifacts expected by the application to be available in their configured locations.

### 4. Run the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite in your terminal, commonly http://localhost:5173.

### Notes

The commands above assume that `backend.main:app` is the correct FastAPI entry point and that the root `requirements.txt` contains the backend dependencies. Update the instructions if your repository uses different paths or dependency files.

The raw dataset and local runtime database are not included. Obtain the dataset separately and follow the project's data preparation instructions when needed.

## Reports

The `reports/` directory contains exploratory data analysis visualizations, model evaluation results, and other generated analysis outputs.

## Future Improvements

- Add more comprehensive automated tests.
- Improve deployment and configuration management.
- Extend monitoring and model evaluation capabilities.
- Explore additional threat detection approaches.

## Author

**Imanthi Kulasooriya**

Software Engineering Undergraduate

GitHub: https://github.com/ImanthiKulasooriya
