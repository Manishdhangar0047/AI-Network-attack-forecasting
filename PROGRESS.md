# Project Progress Tracker — SIH26153

This file tracks the development progress of the AI-Based Network Attack Forecasting project.
Each team member should add a new entry whenever a task is completed or a significant update is made.

---

## Current Status

| Task                                       | Status          | Kaun Kar Raha Hai |
| ------------------------------------------ | --------------- | ----------------- |
| Dataset download + basic organization      | **Done**        | Member 1          |
| Dataset loading + attack/normal separation | **Done**        | Member 1          |
| Feature extraction pipeline                | **done**        | Member 1          |
| Baseline model (Logistic Regression)       | Not Started     | Member 3          |
| LSTM world model                           | Not Started     | Member 2          |
| Forecasting engine (K-step)                | Not Started     | Member 4          |
| MITRE ATT&CK stage mapping                 | Not Started     | Member 4          |
| SHAP explainability                        | Not Started     | Member 3          |
| Streamlit demo                             | Not Started     | Member 5          |
| README + docs                              | Not Started     | Member 5          |

**Status options:** Not Started / In Progress / Done / Blocked

---

## Progress Log

### 11 September 2026 — Member 1

* **Kya kiya:**

  * Network traffic dataset download karke project ke `dataset/` folder mein organize kiya.
  * Multiple CSV dataset files ko project structure mein add kiya.
  * `load_data.py` ke through CSV files detect aur load karne ka basic data pipeline implement kiya.
  * Dataset ki total rows aur columns check karne ka functionality add kiya.
  * `Label` column ke basis par **Benign (Normal)** aur **Attack** traffic ko separate kiya.
  * Label distribution check karne ka functionality add kiya.

* **Kya problem aayi:**

  * Large dataset ko GitHub repository mein directly upload karne ke issue ko identify kiya. Dataset ko repository code se separate rakhna better approach hai.

* **Agla kaam kya hai:**
  * Feature extraction aur preprocessing pipeline complete karna.
  * Large dataset ko memory-efficient chunk processing ke through process kiya.
  * Missing values, infinite values aur duplicate rows handle kiye.
  * Unnecessary columns remove kiye aur numeric ML features prepare kiye.
  * `Target` column create kiya: Benign = 0 aur Attack = 1.
  * Small representative sample dataset create kiya jo actual attack labels preserve karta hai.
  * Full dataset aur processed dataset ko `.gitignore` mein exclude kiya, taaki large files GitHub par upload na hon.
  * Required data-processing files aur sample dataset GitHub par push kiye.
---

## Completed Work

### Member 1 — Dataset & Data Loading

* Dataset collected and organized.
* Multiple CSV files identified.
* Basic CSV loading implemented.
* Dataset dimensions (rows and columns) can be checked.
* Benign and attack traffic separated using the `Label` column.
* Label distribution analysis added.

---

## Next Development Steps

1. Feature extraction and preprocessing
2. Baseline ML model development
3. LSTM-based forecasting
4. K-step forecasting engine
5. MITRE ATT&CK stage mapping
6. SHAP-based explainability
7. Streamlit dashboard/demo
8. Final README and project documentation
9. Testing and final integration
