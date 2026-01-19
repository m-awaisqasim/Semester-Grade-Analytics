
# 🎓 The Ultimate Academic Dashboard & GPA Forecaster

**Stop doing mental math. Start visualizing your success.**

This is a supercharged, interactive dashboard built to help you track your grades, crush your academic goals, and predict your future. Whether you are aiming for *Magna Cum Laude* or just trying to survive Calculus, this app has your back. 🚀

![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-red.svg)
![Made by Awais](https://img.shields.io/badge/Made%20by%20Awais-❤️-pink.svg)

---

## 🌟 Why You Need This

*   **Lightning-Fast Math:** Upload your transcript and watch Pandas calculate your SGPA and CGPA in milliseconds. No more spreadsheets, no more calculators.
*   **Stunning Visuals:** See your academic journey come to life with beautiful, interactive charts. Spot trends, identify tough semesters, and celebrate your wins.
*   **The "Crystal Ball" Feature:** 🔮 Use our **GPA Forecaster** to run "What If" scenarios. Find out exactly what GPA you need in your final semester to hit that 3.5 goal.
*   **Zero Stress Setup:** Includes a sample data generator so you can test the features immediately.

---

## 🚀 Get Started in 3 Steps

### 1. Grab the Code
Download `Semester Grade Analysis.py` and put it in a folder on your computer.

### 2. Fire Up the Terminal
Open your command prompt or terminal, navigate to that folder, and install the magic ingredients:

```bash
pip install streamlit pandas plotly openpyxl
```

### 3. Launch the App
Type this command and hit enter:

```bash
streamlit Semester Grade Analysis.py
```

Boom! Your default browser will pop open, and you're ready to roll. 🎉

---

## 📂 What Data Do I Need?

Just one simple Excel file (`.xlsx`). We need these specific columns (spelling matters!):

(Just showing as an example data)

| Semester | Code | Course Name | CrdHrs | Grade | Points |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Fall 2025 | CL1001 | IT - Lab | 1 | A+ | 4.0 |
| Spring 2026 | MG2008 | Data Analysis | 3 | A+ | 4.0 |

**Don't have a file?** No problem. Just click the **"Download Sample Excel File"** button right on the home page to generate a dummy transcript instantly.

---

## 📖 How to Use This App

### 1. Upload & Chill
Drag and drop your Excel file into the sidebar. The dashboard will instantly light up with your stats.

### 2. The Overview Tab 📊
*   **The Big Numbers:** Check the top cards for your current CGPA and total credits.
*   **The Trend Line:** See your semester performance (SGPA) vs. your overall average (CGPA).
*   **The Pie:** A tasty doughnut chart showing your grade breakdown.

### 3. The Deep Dive Tab 🔍
*   **Intensity Check:** See which semesters were brutal (high credit load) and which were a breeze.
*   **Course Scatter:** Discover if you actually perform better in those heavy 4-credit courses or the easy 1-credit labs.

### 4. The Future Is Now (GPA Forecaster) 🔮
This is the coolest part. Look for the **"GPA Forecaster"** in the sidebar.

1.  **Slide the "Remaining Credits"** to how many classes you have left.
2.  **Slide the "Expected Future SGPA"** to how well you think you'll do.
3.  **Watch the Magic:** A **Green Dashed Line** appears on your chart, showing you exactly where you'll graduate if you stick to that plan.
    *   *Goal:* See that line hit your target score! 🎯

---

## 🛠️ Built With the Good Stuff

*   **Frontend:** [Streamlit](https://streamlit.io/) (Fast, beautiful, Python-based)
*   **Data Wrangling:** [Pandas](https://pandas.pydata.org/) (The heavy lifter)
*   **Charts:** [Plotly](https://plotly.com/) (Interactive & Zoomable Cahrts)
*   **Excel Magic:** [OpenPyXL](https://openpyxl.readthedocs.io/)

---

**Ready to ace your semester? Upload your file and let's get visualizing!** 📈✨