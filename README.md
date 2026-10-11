# 📚 AI Study Planner

An interactive study planning application built using Python and Streamlit. It helps students organize their subjects, manage study time, prepare for exams, and track their study progress.

## 🚀 Features

* **📚 Subject Management:** Add and remove subjects, set exam dates, and select difficulty levels.
* **🎯 Smart Subject Prioritization:** Prioritizes subjects based on exam urgency and difficulty.
* **⏰ Daily Timetable:** Generates a daily study timetable based on available study hours and preferred starting time.
* **💡 Smart Study Recommendations:** Provides study suggestions based on subject difficulty and upcoming exams.
* **📅 Weekly Study Schedule:** Creates a seven-day study plan.
* **✅ Progress Tracker:** Track completed subjects and view overall progress.
* **📥 Download Study Plans:** Download daily and weekly schedules as CSV files.
* **⚙️ Customizable Settings:** Choose daily study hours and your preferred study starting time.
* **⏱️ Break Reminders:** Includes 10-minute breaks between daily study sessions.

## 🛠️ Technologies Used

* Python
* Streamlit
* Pandas
* Python Standard Library (`datetime`)

## 📂 Project Structure

```text
AI-Study-Planner/
│
├── app.py
├── planner.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 📋 Requirements

* Python 3.10 or later recommended
* pip (Python package installer)
* An internet connection for installing the required packages

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/gvssanthan/AI-Study-Planner.git
```

### Step 2: Open the Project Folder

```bash
cd AI-Study-Planner
```

### Step 3: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser. If it does not open automatically, use the local URL displayed in your terminal.

## 🖥️ How to Use

1. Launch the application.
2. Enter a subject name.
3. Select the subject's exam date.
4. Choose its difficulty level: Easy, Medium, or Hard.
5. Add your subjects.
6. Configure your daily study hours and starting time.
7. Click **Generate Smart Study Plan**.
8. View your subject priorities, daily timetable, recommendations, and weekly schedule.
9. Track your study progress using the checkboxes.
10. Download your daily or weekly study plan as a CSV file.

## 🧠 How It Works

The application uses a rule-based scheduling algorithm to prioritize subjects according to their difficulty and the time remaining before their exams.

Subjects with higher priority scores receive a larger share of the available daily study time.

The application then generates:

* A prioritized subject list.
* A daily timetable with breaks between sessions.
* Personalized study recommendations based on the available subject information.
* A seven-day study schedule.
* Progress tracking and downloadable CSV schedules.

**Note:** The current implementation uses rule-based logic rather than a trained machine learning model or an external generative AI service.

## 📌 Future Improvements

* AI-powered study recommendations.
* User login and personalized profiles.
* Persistent storage of subjects and study progress.
* Notifications for upcoming exams and study sessions.
* Topic-level study planning.
* Calendar integration.
* Study analytics and performance reports.

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork this repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## 📄 License

This project is available for educational purposes. You may add an appropriate open-source license, such as the MIT License, if you wish to permit reuse under its terms.

## 👨‍💻 Author

**Santhana Raj**

Developed as a student project using Python and Streamlit.
