import numpy as np
import pandas as pd

from validation import IDENTIFIER_COLUMNS


def analyze_students(df, support_threshold=40):
    """Calculate averages, rankings, subject results, and the support list."""
    identifiers = [col for col in IDENTIFIER_COLUMNS if col in df.columns]
    subjects = [col for col in df.columns if col not in identifiers]

    if not subjects:
        raise ValueError("No subject columns were found.")

    data = df.copy()
    marks = data[subjects].to_numpy(dtype=float)

    # Calculate each student's average and median.
    data["Average"] = np.mean(marks, axis=1)
    data["Median"] = np.median(marks, axis=1)

    # Rank students from highest average to lowest.
    rankings = data.sort_values("Average", ascending=False).reset_index(drop=True)
    rankings.insert(0, "Rank", np.arange(1, len(rankings) + 1))

    # Calculate each subject's class average.
    subject_averages = pd.Series(
        np.mean(marks, axis=0), index=subjects, name="Average Marks"
    ).sort_values(ascending=False)

    # A student needs support if any subject is below the threshold.
    needs_support = data[subjects].lt(support_threshold).any(axis=1)
    support_list = data.loc[needs_support].sort_values("Average").copy()

    return {
        "data_with_metrics": data,
        "total_students": len(data),
        "class_average": float(np.mean(marks)),
        "pass_rate": float(np.mean(np.all(marks >= support_threshold, axis=1)) * 100),
        "students_needing_support": support_list,
        "subject_averages": subject_averages,
        "best_subject": str(subject_averages.idxmax()),
        "weakest_subject": str(subject_averages.idxmin()),
        "ranked_students": rankings,
        "student_column": identifiers[0],
        "subject_columns": subjects,
    }
