from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import csv

# If modifying scopes, delete the token.json file.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_event(service, summary, start_time, end_time, description=None, location=None):
    """Creates a new event in your Google Calendar"""
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Chicago',  # change to your local timezone if needed
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Chicago',
        },
    }
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Event created: {event_result.get('htmlLink')}")

def main():
    creds = None

    # Load saved credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Authenticate if no valid token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Connect to Google Calendar API
    service = build('calendar', 'v3', credentials=creds)

    # 🔹 Example: print upcoming events
    print("\n🔹 Your next 5 events:")
    events_result = service.events().list(calendarId='primary', maxResults=5, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print("No upcoming events found.")
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, "-", event['summary'])

    # 🔹 Example: create a new event
    create_event(
        service,
        summary='CSCE 222 Exam',
        start_time='2025-10-24T14:00:00-05:00',
        end_time='2025-10-24T16:00:00-05:00',
        description='Discrete Structures Midterm Exam',
        location='Zachry Engineering Education Complex'
    )

    print("\n🔹 Auto-scheduling tasks from tasks.csv...")
    schedule_tasks(service, 'tasks.csv')

def get_calendar_events(service, days_ahead=7):
    """Fetch events for the next N days"""
    now = datetime.utcnow().isoformat() + 'Z'
    max_time = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=max_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

from datetime import datetime, timedelta, timezone
def find_free_slots(events, work_day_start=8, work_day_end=22):
    """Return list of free (start, end) datetime slots between events (timezone-safe)"""
    free_slots = []
    now = datetime.now(timezone.utc)
    today = now.replace(hour=work_day_start, minute=0, second=0, microsecond=0)
    end_of_day = today.replace(hour=work_day_end, minute=0)

    for event in events:
        start_str = event['start'].get('dateTime', event['start'].get('date'))
        end_str = event['end'].get('dateTime', event['end'].get('date'))
        try:
            start = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
        except Exception as e:
            print(f"Skipping malformed event: {e}")
            continue

        # Convert start/end to UTC if they have timezone info
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)

        if start > today:
            free_slots.append((today, start))
        today = max(today, end)
        if today > end_of_day:
            break

    if today < end_of_day:
        free_slots.append((today, end_of_day))

    return free_slots

def schedule_tasks(service, csv_file):
    """Schedule tasks into free calendar slots"""
    tasks = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tasks.append({
                'task': row['Task'],
                'duration': int(row['DurationMinutes']),
                'deadline': datetime.fromisoformat(row['Deadline'])
            })

    events = get_calendar_events(service)
    free_slots = find_free_slots(events)

    for task in tasks:
        duration = timedelta(minutes=task['duration'])
        placed = False
        for start, end in free_slots:
            if end - start >= duration and end <= task['deadline']:
                task_start = start
                task_end = start + duration
                create_event(
                    service,
                    summary=task['task'],
                    start_time=task_start.isoformat(),
                    end_time=task_end.isoformat(),
                    description=f"Auto-scheduled task before {task['deadline']}"
                )
                free_slots.remove((start, end))
                if end - task_end > timedelta(minutes=0):
                    free_slots.append((task_end, end))
                placed = True
                break
        if not placed:
            print(f"⚠️ Could not schedule: {task['task']} (no slot found before deadline)")

if __name__ == '__main__':
    main()
