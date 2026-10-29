from io import BytesIO

import pandas as pd


def build_excel_report(results, original_df, support_threshold=40):
    """Create an Excel workbook with the main project results."""
    output = BytesIO()

    overview = pd.DataFrame({
        "Metric": [
            "Total students",
            "Class average",
            "Pass rate",
            "Students needing support",
            "Support threshold",
            "Strongest subject",
            "Weakest subject",
        ],
        "Value": [
            results["total_students"],
            round(results["class_average"], 2),
            round(results["pass_rate"], 2),
            len(results["students_needing_support"]),
            support_threshold,
            results["best_subject"],
            results["weakest_subject"],
        ],
    })

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        overview.to_excel(writer, sheet_name="Overview", index=False)
        results["ranked_students"].round(2).to_excel(
            writer, sheet_name="Rankings", index=False
        )
        results["subject_averages"].rename("Average Marks").to_frame().to_excel(
            writer, sheet_name="Subject Averages"
        )
        results["students_needing_support"].round(2).to_excel(
            writer, sheet_name="Needs Support", index=False
        )
        original_df.to_excel(writer, sheet_name="Uploaded Data", index=False)

    return output.getvalue()
