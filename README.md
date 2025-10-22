# 🧠 SmartCalendar

SmartCalendar is a Python app that connects to your Google Calendar, finds free time between your events, and automatically schedules tasks into those open slots. It also includes a simple GUI so you can add tasks manually without editing files.

---

## 🚀 Features
- Reads your real Google Calendar events
- Detects free time slots automatically
- Schedules tasks from a CSV file or GUI input
- Works fully offline after first Google sign-in
- Handles time zones correctly (UTC-safe)

---

## ⚙️ Requirements
- Python 3.9 or newer
- A Google account
- A Google Cloud project with the Calendar API enabled

---

## 🪜 Setup Instructions

### 1. Clone the repository
git clone https://github.com/<your-username>/SmartCalendar.git  
cd SmartCalendar

### 2. Create and activate a virtual environment
python3 -m venv venv  
source venv/bin/activate        # macOS/Linux  
venv\Scripts\activate           # Windows

### 3. Install dependencies
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib tk

### 4. Set up Google API credentials
1. Go to the Google Cloud Console: https://console.cloud.google.com/  
2. Create a new project → Enable the **Google Calendar API**  
3. In **APIs & Services → Credentials**, click **Create Credentials → OAuth Client ID → Desktop App**  
4. Download the credentials file, rename it to **credentials.json**, and place it in your SmartCalendar folder  
5. The first time you run the app, a browser window will ask for permission. After approval, a **token.json** file will be created automatically — don’t delete it.

---

## ▶️ How to Run the App

### Run the backend (auto-scheduling tasks from CSV)
python3 main.py

This will:
- Connect to your Google Calendar
- Show your next 5 events
- Automatically schedule tasks listed in **tasks.csv**

#### Example tasks.csv
Task,DurationMinutes,Deadline  
Finish project,120,2025-10-25T23:00:00-05:00  
Study Linear Algebra,90,2025-10-23T22:00:00-05:00  
Grocery shopping,60,2025-10-24T20:00:00-05:00

### Run the GUI (add tasks manually)
python3 gui.py

A small window will appear that lets you:
- Enter a **Task name**
- Set **Duration (minutes)**
- Enter **Deadline** (e.g. 2025-10-25T18:00:00)
- Click **Add to Calendar** → it finds the next open slot and adds the task.

---

## 🧩 Folder Structure
SmartCalendar/  
├── main.py              → backend logic (connects to Calendar + schedules CSV tasks)  
├── gui.py               → GUI interface for manual task adding  
├── credentials.json     → your Google API credentials (private)  
├── token.json           → generated automatically after first sign-in  
├── tasks.csv            → example task list  
└── README.md            → this documentation file  

---

## 🧠 Future Improvements
- Add task priorities or categories
- Show free-time blocks visually in the GUI
- Add dark mode styling

---

## 👤 Author
**Zaid Barakat**  
SmartCalendar — Google Calendar API  
Texas A&M University, College Station  
📧 zaiduchiha2007@gmail.com  

---

## 📜 License
Released under the MIT License — free to use and modify for personal or educational projects.
