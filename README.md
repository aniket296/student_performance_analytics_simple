# Student Performance Analytics System

A beginner-friendly Python project that analyzes student marks.

## Libraries used

- **Pandas:** reads and organizes student data.
- **NumPy:** calculates averages and other numerical results.
- **Matplotlib:** draws the two dashboard charts.
- **Streamlit:** displays the web dashboard.
- **Openpyxl:** helps create the Excel report.

## How to run

1. Keep all project files in the same folder.
2. Open that folder in VS Code.
3. Open Terminal in VS Code.
4. Install the libraries:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Start the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

6. Open the local address shown in the terminal.

## Upload file format

Upload a CSV or Excel `.xlsx` file. Include a student identifier column such as `Name`, `Roll No.`, or `Student ID`, plus one or more subject columns with marks from 0 to 100.

## Main features

- Preview the uploaded dataset.
- Validate marks and required student information.
- Show total students, class average, pass rate, and support count.
- Compare subject averages and student averages using charts.
- Rank students and search for a student.
- Identify students with any subject mark below the selected support threshold.
- Download an Excel report or rankings CSV.

## Support rule

A student is listed as needing support if **at least one subject mark** is below the chosen threshold. This does not depend on the student's overall average.
