# Git Event Tracker

A full-stack web application built with **React** and **Flask** that visualizes Git events (pushes, merges, pull requests) in real-time. The app fetches events from a Flask API every 15 seconds and displays them in a styled HTML table using React.

---

## 📌 Use Case

This project helps developers and teams:
- Monitor Git activity in real-time (Push, Pull Request, Merge)
- Track contributions during collaborative development
- Visualize Git workflows in CI/CD pipelines
- Learn how to integrate a Flask backend with a React frontend

---

## 🧰 Tech Stack

- **Frontend**: React (JavaScript)
- **Backend**: Flask (Python)
- **API Endpoint**: `/events`
- **Polling Frequency**: 15 seconds
- **Styling**: Inline CSS

---

## 📁 Project Structure

project-root/
├── flask/
│ └── 01.py # Flask backend providing /events endpoint
│
├── react-app/
│ ├── public/
│ ├── src/
│ │ └── App.js # React component to fetch and display events
│ └── package.json
│
└── README.md # Project documentation


---

## ⚙️ How It Works

1. **Flask Backend (`01.py`)**  
   - Hosts an API route `/events` that returns Git activity data in JSON format.
   - Each event contains:
     - `action` (PUSH, MERGE, PULL_REQUEST)
     - `author`
     - `from_branch`, `to_branch`
     - `request_id`
     - `timestamp`

2. **React Frontend (`App.js`)**  
   - Periodically calls the `/events` endpoint every 15 seconds using `fetch()`.
   - Displays the events in a clean HTML table.
   - Adds `(local)` to the `from_branch` if present.

---

## 🚀 Getting Started

### Prerequisites

- Node.js & npm
- Python 3.7+
- Flask

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/git-event-tracker.git
cd git-event-tracker
cd flask
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install flask
python 01.py
cd ../react-app
npm install
npm start
