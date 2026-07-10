"""
Weekly Timetable Generator
--------------------------
Beginner-friendly version.

HOW TO RUN:
1. Open this folder in VS Code.
2. Open a terminal (Terminal > New Terminal).
3. Type:  python app.py
4. Press ENTER when asked.
   Your browser will open automatically with the timetable.
"""

import random
import threading
import webbrowser
from flask import Flask, render_template, jsonify

app = Flask(__name__)

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

TIME_SLOTS = [
    "9:00-10:00",
    "10:00-11:00",
    "11:15-12:15",
    "1:00-2:00",
    "2:00-3:00",
]

SUBJECTS = [
    "Python Programming",
    "Artificial Intelligence",
    "Mathematics",
    "Cloud Computing",
    "Data Science",
    "Cyber Security",
    "Elective",
]

FACULTY = {
    "Python Programming": "Dr. Meena",
    "Artificial Intelligence": "Dr. Ravi",
    "Mathematics": "Dr. Kumar",
    "Cloud Computing": "Dr. Kiran",
    "Data Science": "Dr. Arun",
    "Cyber Security": "Dr. Suresh",
    "Elective": "Dr. Deepa",
}

CLASSROOMS = ["Room-101", "Room-102", "Room-103"]

SUBJECT_TAGS = {
    "Python Programming": "rose",
    "Artificial Intelligence": "plum",
    "Mathematics": "mustard",
    "Cloud Computing": "sky",
    "Data Science": "sage",
    "Cyber Security": "clay",
    "Elective": "teal",
}


def generate_timetable():
    """Builds a week of classes: no subject repeats on the same day,
    and subjects are spread evenly across the week."""
    timetable = {day: [] for day in DAYS}
    usage_count = {subject: 0 for subject in SUBJECTS}

    for day in DAYS:
        candidates = sorted(SUBJECTS, key=lambda s: (usage_count[s], random.random()))
        day_subjects = candidates[: len(TIME_SLOTS)]
        random.shuffle(day_subjects)

        for slot, subject in zip(TIME_SLOTS, day_subjects):
            usage_count[subject] += 1
            timetable[day].append(
                {
                    "time": slot,
                    "subject": subject,
                    "faculty": FACULTY[subject],
                    "room": random.choice(CLASSROOMS),
                    "tag": SUBJECT_TAGS.get(subject, "sky"),
                }
            )
    return timetable


@app.route("/")
def index():
    legend = [{"subject": s, "faculty": FACULTY[s], "tag": SUBJECT_TAGS[s]} for s in SUBJECTS]
    return render_template("index.html", days=DAYS, slots=TIME_SLOTS, legend=legend)


@app.route("/api/generate")
def api_generate():
    return jsonify(generate_timetable())


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    print("=" * 50)
    print("   WEEKLY TIMETABLE GENERATOR")
    print("=" * 50)
    input("\nPress ENTER to start the app...")
    print("\nStarting... your browser will open in a moment.")
    print("(To stop the app, close this window or press CTRL+C)\n")
    threading.Timer(1.2, open_browser).start()
    app.run(debug=False)
