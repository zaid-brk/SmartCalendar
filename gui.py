import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from main import create_event, schedule_tasks, get_calendar_events, find_free_slots
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return build('calendar', 'v3', credentials=creds)

def add_task():
    try:
        service = get_service()
        task_name = entry_task.get().strip()
        duration = int(entry_duration.get())
        deadline_str = entry_deadline.get().strip()

        if not task_name or not duration or not deadline_str:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        from datetime import timezone
        deadline = datetime.fromisoformat(deadline_str)
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)

        events = get_calendar_events(service)
        free_slots = find_free_slots(events)

        from datetime import timezone

        # Make sure all free slot datetimes are timezone-aware
        free_slots = [(s if s.tzinfo else s.replace(tzinfo=timezone.utc),
                       e if e.tzinfo else e.replace(tzinfo=timezone.utc))
                      for s, e in free_slots]

        # Pick first free slot that fits before deadline
        placed = False
        for start, end in free_slots:
            if end - start >= timedelta(minutes=duration) and end <= deadline:
                create_event(
                    service,
                    summary=task_name,
                    start_time=start.isoformat(),
                    end_time=(start + timedelta(minutes=duration)).isoformat(),
                    description=f"Auto-scheduled before {deadline}"
                )
                placed = True
                messagebox.showinfo("Success", f"Task '{task_name}' added to calendar!")
                break

        if not placed:
            messagebox.showwarning("No Slot Found", f"No free slot found before {deadline_str}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- UI ---------------- #
root = tk.Tk()
root.title("SmartCalendar")
root.geometry("400x300")
root.config(padx=20, pady=20)

tk.Label(root, text="Task Name:").pack()
entry_task = tk.Entry(root, width=40)
entry_task.pack()

tk.Label(root, text="Duration (minutes):").pack()
entry_duration = tk.Entry(root, width=40)
entry_duration.pack()

tk.Label(root, text="Deadline (YYYY-MM-DDTHH:MM:SS):").pack()
entry_deadline = tk.Entry(root, width=40)
entry_deadline.insert(0, (datetime.now() + timedelta(days=1)).replace(second=0, microsecond=0).isoformat())
entry_deadline.pack()

tk.Button(root, text="Add to Calendar", command=add_task, bg="#4CAF50", fg="white", width=20).pack(pady=15)

root.mainloop()
