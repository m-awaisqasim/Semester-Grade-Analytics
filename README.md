# 🎓 Semester Grade Analytics

An interactive, Python-powered dashboard built to help students visualize their academic journey. This tool calculates **SGPA** (Semester GPA) and **CGPA** (Cumulative GPA) trends and provides insights into grade distributions using an Excel-based workflow.

## 🚀 Features

* **Automated Calculations:** Automatically computes SGPA and running CGPA from raw course data.
* **Interactive Trend Analysis:** Visualize performance across multiple semesters with interactive line charts.
* **Grade Distribution:** Break down your overall grades (As, Bs, Cs) into an easy-to-read doughnut chart.
* **Data Filtering:** Filter your academic history by specific semesters to focus on your progress.
* **Clean UI:** A modern, minimal interface built with Streamlit and Tailwind-inspired styling.

## 🛠️ Tech Stack

* **Language:** Python
* **Framework:** [Streamlit](https://streamlit.io/)
* **Data Handling:** Pandas & OpenPyXL
* **Visuals:** Plotly Interactive Graphs

## 📥 Installation & Setup

If you are running this locally or in **Project IDX**, follow these steps:

1. **Clone the Repository:**
```bash
git clone https://github.com/your-username/Semester-Grade-Analytics.git
cd "Semester Grade Analytics"

```


2. **Install Dependencies:**
```bash
pip install streamlit pandas plotly openpyxl

```


3. **Run the Application:**
```bash
python -m streamlit run "Semester Grade Analysis.py"

```



## 📊 Data Format

To ensure the dashboard works correctly, your Excel file (`.xlsx`) should contain a sheet with the following column headers:

| Semester | Code | Course Name | CrdHrs | Grade | Points |
| --- | --- | --- | --- | --- | --- |
| Fall 2025 | CS101 | Intro to Programming | 3 | A | 4.0 |
| Fall 2025 | MA102 | Calculus I | 4 | B+ | 3.3 |

> **Note:** Ensure there are no empty rows or missing values in the `CrdHrs` or `Points` columns to prevent calculation errors.

## 💡 How to Use

1. Launch the app using the `streamlit run` command.
2. In the web interface, upload your prepared Excel file.
3. Explore the metrics at the top and interact with the charts to analyze your performance.

---
