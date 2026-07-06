# 🎓 CDAM - Python for Data Science LMS Masterclass Platform

[![Live Demo](https://img.shields.io/badge/Live_Demo-red?style=for-the-badge&logo=render&logoColor=white)](https://python-cdam-system.onrender.com)

An enterprise-grade, high-fidelity Learning Management System (LMS) inspired by the **Center for Data Analytics & Modelling (CDAM)** at **Chuka University**. Built with a modern, premium dark-red aesthetics design system, advanced automated anti-cheating proctoring, dynamic question builders, interactive code simulators, and full-featured role-based administrative dashboards.

---

## 🚀 Key Highlights & Enhancements

### 1. Premium UI/UX Design System
- **Corporate Dark-Red Aesthetics**: HSL tailored dark-red color palette with frosted-glass containers, vivid active states, custom animated progress rings, responsive sidebar navigations, and warning overlays.
- **Dynamic Interactions**: Micro-animations, scroll-fade reveals (IntersectionObserver), real-time counting numbers on stats panels, and responsive navigation controls.
- **Theme Versatility**: Fully integrated Light and Dark mode styles.

### 2. Multi-Level Curriculum & Student Dashboard
- **Profile Customization**: Register and track progress based on academic levels: **Beginner**, **Intermediate**, or **Professional**.
- **Student Performance Ring**: Conic-gradient analytics dashboard indicating percentage of sessions completed, active daily learning streak counts, and quiz average histories.
- **Interactive Session Workspaces**: Tab-oriented workspace panels supporting Markdown renders, responsive video frames, downloadable notes (PDF, Jupyter Notebooks, ZIPs), and an internal Python simulator runner.
- **Bookmarks & Q&A Discussion**: Bookmark sessions for quick access and participate in active community forums with comment voting.

### 3. Anti-Cheating Secure Proctoring Module
- **Automated Integrity Engine**: Protects exam environments using window focus detection (`window.blur`), tab changing limitations (`visibilitychange`), fullscreen constraint controls, blocked clipboard actions, and restricted shortcuts (PrintScreen, Ctrl+C, Ctrl+V, F12).
- **Incident Logger**: Tabulates and scores violation metrics, automatically terminating attempts when reaching the breach threshold.

### 4. Admin Management CMS & Proctoring Console
- **Session Editor CMS**: Create, update, publish/draft, delete, and numerically order course sessions. Upload multi-format files including Jupyter notebooks (`.ipynb`), slide decks, ZIP archives, CSV datasets, and PDF worksheets.
- **Proctoring Analytics Panel**: Audit live student exam records, monitoring tab switches, severity scores, and proctoring activity logs.
- **Assessment Builder**: Design, schedule (via start/end datetimes), configure policies (attempts limits, device locking), and dynamically generate MCQs, True/False, and essay questions.

---

## 🛠️ Tech Stack

- **Backend**: Python 3 (Flask), SQLite database engine, Flask-SQLAlchemy ORM.
- **Frontend**: Vanilla CSS variables, responsive HTML templates (Jinja2), FontAwesome icons, outfit font stack, Highlight.js code rendering.
- **Interactions**: Vanilla Javascript (DOM handlers, IntersectionObserver, counters, custom sandboxed code simulations).
- **Testing**: pytest suite.

---

## 📦 Run & Set Up Locally

### 1. Install System Dependencies
Execute from the project repository root:
```bash
pip install -r backend/requirements.txt
```

### 2. Run the Application Server
```bash
python backend/app.py
```
After executing, navigate to: `http://127.0.0.1:5000`



## 🧪 Run Automated Verification Tests
We maintain full coverage across backend CRUD endpoints, integrity violations, session progress, and auth rules.
```bash
python -m pytest backend/tests/test_app.py -v
```

---

## 🚀 Cloud Deployment
For step-by-step instructions on deploying the LMS platform to the cloud, see the [Vercel Deployment Guide](vercel_deployment_guide.md).

