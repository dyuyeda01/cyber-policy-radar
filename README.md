# 🌐 Cyber Policy Radar

**Cyber Policy Radar** is a responsive, auto-updating dashboard that aggregates the latest cybersecurity policy and news articles from leading global sources.  
It provides a clean, modern interface that works seamlessly across desktop and mobile devices.  View it here: https://dyuyeda01.github.io/cyber-policy-radar/ 

---

## 🚀 Features

### 📰 Live Cyber Policy Aggregation
- Automatically fetches and compiles cybersecurity-related news and policy articles.
- Sources include: *The Hacker News, DarkReading, SecurityWeek, Lawfare, The Register, Cybersecurity Dive, and more.*
- RSS/Atom feeds parsed using Python and stored in JSON format (`data/articles.json`).

### 💻 Responsive Frontend
- Fully responsive single-page design — scales from mobile to desktop automatically.
- Uses CSS Grid with media queries for smooth transitions between 1-column (mobile) and 2-column (desktop) layouts.
- Clean, dark theme inspired by modern cybersecurity dashboards.

### 🧠 AI-Ready Architecture
- Code is structured to support AI enrichment (e.g., article summarization, sentiment, region tagging).
- When an OpenAI API key is available, the backend can auto-summarize and classify each article using GPT models.

### ⚙️ Automation
- GitHub Actions can automatically re-run `fetch_feeds.py` every 12 hours to refresh `articles.json`.
- Site redeploys automatically on GitHub Pages after every push.

### 🪄 Smooth UX
- Filters by **region** and **source**
- Free-text **search** for article titles
- Skips broken or missing images automatically (`onerror="this.remove()"`)
- Displays “Last updated” timestamp pulled directly from `articles.json`

---
⚠️ Disclaimer

This project is a personal side project created for educational and experimental purposes only.
All ideas and implementations are original and independently developed by the author, with assistance from ChatGPT for code generation and formatting.
All data used in this project is sourced entirely from publicly available and open sources.
Nothing in this repository is proprietary, affiliated with, or represents the author’s employer, clients, or business entities.
This project is not used for advertising, commercial services, or any official work-related purpose.
