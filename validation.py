import pandas as pd


# These columns identify students; they are not subject marks.
IDENTIFIER_COLUMNS = ["Name", "Roll No.", "Roll No", "Student ID", "Student", "ID"]


def validate_students(df):
    """Check that student details and subject marks are valid."""
    if df.empty:
        raise ValueError("The uploaded file has no student records.")

    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()

    identifiers = [col for col in IDENTIFIER_COLUMNS if col in df.columns]
    if not identifiers:
        raise ValueError("Include an identifier column: Name, Roll No., or Student ID.")

    for column in identifiers:
        if df[column].isna().any() or df[column].astype(str).str.strip().eq("").any():
            raise ValueError(f"Some values are missing in '{column}'.")

    subjects = [col for col in df.columns if col not in identifiers]
    if not subjects:
        raise ValueError("Include at least one subject column with marks.")

    for subject in subjects:
        marks = pd.to_numeric(df[subject], errors="coerce")

        if marks.isna().any():
            raise ValueError(f"'{subject}' has missing or non-numeric marks.")

        if ((marks < 0) | (marks > 100)).any():
            raise ValueError(f"Marks in '{subject}' must be between 0 and 100.")

        df[subject] = marks

    return {
        "data": df,
        "student_column": identifiers[0],
        "identifier_columns": identifiers,
        "subject_columns": subjects,
    }
