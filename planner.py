
from datetime import date, datetime, timedelta


def generate_study_plan(subjects, daily_hours):
    today = date.today()

    difficulty_scores = {
        "Easy": 1,
        "Medium": 2,
        "Hard": 3
    }

    plan = []

    for subject in subjects:
        days_left = (subject["exam_date"] - today).days
        difficulty = difficulty_scores.get(
            subject["difficulty"], 2
        )

        urgency = 1 / (max(days_left, 0) + 1)
        priority = difficulty * 0.6 + urgency * 4

        plan.append({
            "Subject": subject["name"],
            "Days Left": max(days_left, 0),
            "Difficulty": subject["difficulty"],
            "Priority Score": round(priority, 2)
        })

    plan.sort(
        key=lambda item: item["Priority Score"],
        reverse=True
    )

    if not plan:
        return []

    total_priority = sum(
        item["Priority Score"] for item in plan
    )

    for item in plan:
        total_minutes = round(
    daily_hours * 60 * item["Priority Score"] / total_priority
    )

    for item in plan:
        total_minutes = round(daily_hours * 60 * item["Priority Score"] / total_priority)

        item["Study Hours"] = total_minutes / 60
        item["Study Duration"] = (
            f"{total_minutes // 60} hour "
            f"{total_minutes % 60} minutes"
            )
    return plan


def generate_daily_timetable(plan, start_hour=9):
    timetable = []

    current_time = datetime.combine(
        date.today(), datetime.min.time()
    ).replace(hour=start_hour)

    for item in plan:
        minutes = round(item["Study Hours"] * 60)

        if minutes <= 0:
            continue

        end_time = current_time + timedelta(minutes=minutes)

        timetable.append({
            "Subject": item["Subject"],
            "Start Time": current_time.strftime("%I:%M %p"),
            "End Time": end_time.strftime("%I:%M %p"),
            "Duration": f"{minutes} minutes"
        })

        current_time = end_time + timedelta(minutes=10)

    return timetable


def generate_weekly_plan(subjects, daily_hours):
    """Generate a schedule for today and the next six days."""

    weekly_plan = []

    if not subjects or daily_hours <= 0:
        return weekly_plan

    today = date.today()

    for day_number in range(7):
        study_date = today + timedelta(days=day_number)

        # Prefer subjects whose exams have not passed.
        available = [
            subject for subject in subjects
            if subject["exam_date"] >= study_date
        ]

        # Still show a schedule if all exam dates have passed.
        if not available:
            available = subjects.copy()

        # Prioritize nearer exams, then harder subjects.
        difficulty_scores = {
            "Easy": 1,
            "Medium": 2,
            "Hard": 3
        }

        available.sort(
            key=lambda subject: (
                (subject["exam_date"] - study_date).days
                if subject["exam_date"] >= study_date
                else 9999,
                -difficulty_scores.get(
                    subject["difficulty"], 2
                )
            )
        )

        selected = available[:min(3, len(available))]
        hours_each = daily_hours / len(selected)
        allocated = 0.0

        for index, subject in enumerate(selected):
            if index == len(selected) - 1:
                hours = round(daily_hours - allocated, 2)
            else:
                hours = round(hours_each, 2)
                allocated += hours

            weekly_plan.append({
                "Date": study_date.strftime("%d-%m-%Y"),
                "Day": study_date.strftime("%A"),
                "Subject": subject["name"],
                "Study Duration": (
                     f"{int(hours * 60) // 60} hour "
                     f"{int(hours * 60) % 60} minutes"
                     )
            })

    return weekly_plan
