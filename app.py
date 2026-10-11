
import streamlit as st
import pandas as pd
from datetime import date

from planner import (
    generate_study_plan,
    generate_daily_timetable,
    generate_weekly_plan
)


# =============== PAGE SETUP ===============

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="wide"
)

if "subjects" not in st.session_state:
    st.session_state.subjects = []

if "plan" not in st.session_state:
    st.session_state.plan = []

if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False

if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = {}

if "plan_version" not in st.session_state:
    st.session_state.plan_version = 0


# =============== TITLE ===============

st.title("📚 AI Study Planner")
st.write(
    "Plan your studies, manage your time, "
    "and prepare for exams smartly."
)

st.divider()


# =============== SETTINGS ===============

st.sidebar.header("⚙️ Planner Settings")

daily_hours = st.sidebar.slider(
    "Daily study hours",
    min_value=1,
    max_value=12,
    value=4
)

start_hour = st.sidebar.selectbox(
    "Study starting time",
    options=list(range(5, 22)),
    index=4,
    format_func=lambda hour: (
        f"{hour % 12 or 12}:00 "
        f"{'AM' if hour < 12 else 'PM'}"
    )
)


# =============== ADD SUBJECTS ===============

st.header("📝 Add Your Subjects")

with st.form("subject_form", clear_on_submit=True):
    subject_name = st.text_input(
        "Subject name",
        placeholder="Example: Mathematics"
    )

    exam_date = st.date_input(
        "Exam date",
        value=date.today(),
        min_value=date.today()
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    add_subject = st.form_submit_button("➕ Add Subject")

    if add_subject:
        cleaned_name = subject_name.strip()

        if not cleaned_name:
            st.warning("Please enter a subject name.")

        elif any(
            s["name"].lower() == cleaned_name.lower()
            for s in st.session_state.subjects
        ):
            st.warning("This subject already exists.")

        else:
            st.session_state.subjects.append({
                "name": cleaned_name,
                "exam_date": exam_date,
                "difficulty": difficulty
            })

            st.session_state.plan_generated = False
            st.success(f"{cleaned_name} added successfully!")


# =============== SUBJECT LIST ===============

if st.session_state.subjects:
    st.subheader("📖 Your Subjects")

    for index, subject in enumerate(
        st.session_state.subjects
    ):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(
                f"**{subject['name']}** | "
                f"Exam: {subject['exam_date']} | "
                f"Difficulty: {subject['difficulty']}"
            )

        with col2:
            if st.button(
                "🗑️ Remove",
                key=f"remove_{index}"
            ):
                st.session_state.subjects.pop(index)
                st.session_state.plan_generated = False
                st.rerun()

else:
    st.info("Add at least one subject to get started.")


# =============== GENERATE PLAN ===============

if st.button("🚀 Generate Smart Study Plan", type="primary"):
    if st.session_state.subjects:
        st.session_state.plan = generate_study_plan(
            st.session_state.subjects,
            daily_hours
        )

        st.session_state.plan_version += 1
        st.session_state.completed_tasks = {}
        st.session_state.plan_generated = True

    else:
        st.warning("Please add your subjects first.")


# =============== DISPLAY PLAN ===============

if st.session_state.plan_generated:
    plan = st.session_state.plan

    if plan:

        # 1. SUBJECT PRIORITY
        st.divider()
        st.header("🎯 1. Subject Priority")

        st.dataframe(
            pd.DataFrame(plan),
            use_container_width=True,
            hide_index=True
        )

        # 2. DAILY TIMETABLE
        st.divider()
        st.header("⏰ 2. Daily Timetable")

        daily_plan = generate_daily_timetable(
            plan, start_hour
        )

        if daily_plan:
            st.dataframe(
                pd.DataFrame(daily_plan),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No daily sessions available.")

        st.caption(
            "A 10-minute break is added between study sessions."
        )

        # 3. STUDY RECOMMENDATIONS
        st.divider()
        st.header("💡 3. Smart Study Recommendations")

        st.success(
            f"Start with **{plan[0]['Subject']}**, "
            "which currently has the highest priority."
        )

        for item in plan:
            st.subheader(f"📚 {item['Subject']}")

            if item["Days Left"] == 0:
                st.write(
                    "Review key topics if your exam is today."
                )
            elif item["Days Left"] <= 3:
                st.write(
                    "Your exam is close. Focus on revision "
                    "and practice questions."
                )
            elif item["Difficulty"] == "Hard":
                st.write(
                    "Break difficult topics into smaller sections "
                    "and practise them one by one."
                )
            elif item["Difficulty"] == "Medium":
                st.write(
                    "Review important concepts and solve exercises."
                )
            else:
                st.write(
                    "Revise key points and test yourself."
                )

            st.write(f"Suggested time: **{item['Study Duration']}**")

        # 4. WEEKLY SCHEDULE
        # This section is independent of the daily timetable.
        st.divider()
        st.header("📅 4. Seven-Day Study Schedule")

        weekly_plan = generate_weekly_plan(
            st.session_state.subjects,
            daily_hours
        )

        if weekly_plan:
            weekly_df = pd.DataFrame(weekly_plan)

            st.success(
                f"Weekly schedule created: "
                f"{len(weekly_df)} study sessions."
            )

            st.dataframe(
                weekly_df,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "📥 Download Weekly Schedule",
                data=weekly_df.to_csv(index=False),
                file_name="weekly_study_plan.csv",
                mime="text/csv",
                key="weekly_download"
            )
        else:
            st.warning(
                "No weekly schedule could be generated."
            )

        # 5. PROGRESS TRACKER
        st.divider()
        st.header("✅ 5. Study Progress Tracker")

        for index, item in enumerate(plan):
            key = (
                f"completed_{st.session_state.plan_version}_{index}"
            )

            if key not in st.session_state:
                st.session_state[key] = False

            st.checkbox(
                f"{item['Subject']} — "
                f"{item['Study Hours']:.2f} hours planned",
                key=key
                )

            st.session_state.completed_tasks[item["Subject"]] = (
                st.session_state[key]
            )

        total = len(plan)

        completed = sum(
            st.session_state.completed_tasks.get(
                item["Subject"], False
            )
            for item in plan
        )

        progress = completed / total if total else 0

        st.progress(progress)

        col1, col2 = st.columns(2)

        col1.metric(
            "Subjects Completed",
            f"{completed}/{total}"
        )

        col2.metric(
            "Overall Progress",
            f"{progress * 100:.0f}%"
        )

        if progress == 1:
            st.balloons()
            st.success("Great work! All subjects are completed.")

        # 6. DOWNLOAD DAILY PLAN
        st.divider()
        st.header("📥 6. Download Your Study Plan")

        st.download_button(
            "Download Daily Study Plan",
            data=pd.DataFrame(plan).to_csv(index=False),
            file_name="daily_study_plan.csv",
            mime="text/csv",
            key="daily_download"
        )

    else:
        st.warning("Your plan is empty. Generate it again.")


# =============== FOOTER ===============

st.divider()
st.caption("AI Study Planner | Python + Streamlit 📚")
