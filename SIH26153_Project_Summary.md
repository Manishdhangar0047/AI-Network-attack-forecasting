# SIH26153 — AI based Network Attack Forecasting from Network Traffic Data

**Organization:** National Technical Research Organisation (NTRO)
**Category:** Software | **Theme:** Blockchain & Cybersecurity
**Deadline:** 20 September 2026

## Problem (Simple Words)
Normal cybersecurity tools sirf ek packet dekh kar bolte hain "attack hai ya nahi". Humein ek AI system banana hai jo poori traffic **sequence** dekh kar predict kare ki attack **hone se pehle** hi ho sakta hai — aur ye bhi bataye ki attack kis stage mein hai (Recon → Initial Access → Lateral Movement → Command & Control → Exfiltration, MITRE ATT&CK framework ke hisaab se).

## Datasets Use Karenge
- CIC-IDS2018 (flow-level CSV) — primary
- CTU-13, UNSW-NB15, CICIoT2023 — alternative options

## Architecture (Pipeline)
1. **Raw traffic data** (PCAP/CSV)
2. **Feature extraction** — flow-level + packet-level features
3. **Baseline model** (Logistic Regression) + **World model** (LSTM sequence model) — dono train karke compare karenge
4. **Forecasting engine** — K-step attack prediction + MITRE ATT&CK stage mapping
5. **Explainability** — SHAP se batayenge kaunse features ne decision liya
6. **Demo interface** — Streamlit web app (offline chalega)

## Tech Stack
Python, Pandas, NumPy, PyTorch (LSTM model), scikit-learn (baseline), SHAP (explainability), Streamlit (demo), Scapy/PyShark (PCAP parsing), Git + GitHub (team collaboration)

## Team Roles (5 Members)
| Member | Role |
|---|---|
| 1 | Data Engineer — dataset cleaning, feature extraction pipeline |
| 2 | ML Engineer — LSTM world model design + training |
| 3 | ML Engineer — baseline model, evaluation metrics, SHAP explainability |
| 4 | Backend — K-step forecasting engine, attack stage mapping logic |
| 5 | Frontend/Docs — Streamlit demo, architecture doc, PPT, demo video |

## Setup Checklist (Sab Members Ke Liye)
1. Python 3.10+ install karo (PATH mein add karna mat bhulna)
2. VS Code install karo + Python extension
3. GitHub account banao, Git install karo
4. Shared repo clone karo: `git clone <repo-link>`
5. Virtual environment banao: `python -m venv venv`
6. Libraries install karo: `pip install pandas numpy scikit-learn torch streamlit shap scapy`
7. Roz kaam se pehle `git pull`, kaam ke baad `git add . && git commit -m "message" && git push`

## Final Deliverables
- Source code (GitHub link)
- README with setup instructions
- Architecture document (max 2 pages)
- Demo video (max 2 minutes)
- Technical presentation (max 5 slides)

## Errors Aaye To
Error message copy karke Claude app mein paste karo (naya chat khol ke) — turant fix mil jayega.
