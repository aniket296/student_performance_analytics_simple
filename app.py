import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from validation import validate_students
from analysis import analyze_students
from export import build_excel_report


# Page setup
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide"
)

# Dark dashboard design
st.markdown("""
<style>
.stApp { background: #080b12; color: #f3f4f6; }
[data-testid="stHeader"] { background: #080b12; }
[data-testid="stSidebar"] { background: #101521; }
.block-container { padding-top: 1.5rem; }
.hero {
    background: linear-gradient(120deg, #111827, #1d4ed8);
    padding: 24px;
    border-radius: 16px;
    margin-bottom: 20px;
}
.hero h1 { color: white; margin: 0; }
.hero p { color: #dbeafe; margin-bottom: 0; }
[data-testid="stMetric"] {
    background: #121826;
    border: 1px solid #293244;
    padding: 14px;
    border-radius: 12px;
}
[data-testid="stMetricLabel"] { color: #b8c4d8 !important; }
[data-testid="stMetricValue"] { color: white !important; }
</style>
<div class="hero">
    <h1>📊 Student Performance Analytics</h1>
    <p>Analyze student marks, compare subjects, and find students who may need support.</p>
</div>
""", unsafe_allow_html=True)


# Dashboard settings
with st.sidebar:
    st.header("Dashboard Settings")
    support_threshold = st.slider(
        "Support threshold (marks)", 0, 100, 40, 5
    )
    st.caption("A student is flagged if any subject mark is below this value.")
    st.write("Accepted files: CSV and Excel (.xlsx)")


# Upload the student file
uploaded_file = st.file_uploader(
    "Upload student marks", type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.info("Upload a CSV or Excel file to begin.")
    st.stop()


# Read the file
try:
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Remove extra spaces from column names.
    df.columns = df.columns.astype(str).str.strip()

except Exception as error:
    st.error(f"Could not read this file: {error}")
    st.stop()


# Preview the uploaded data
with st.expander("👀 Preview uploaded dataset", expanded=True):
    st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
    st.dataframe(df, use_container_width=True, hide_index=True)


# Check the data and calculate results
try:
    validation_info = validate_students(df)
    df = validation_info["data"]
    results = analyze_students(df, support_threshold)
except (ValueError, KeyError, TypeError) as error:
    st.error(f"Unable to analyze this file: {error}")
    st.stop()


st.success(f"Successfully analyzed {results['total_students']} students.")


# Summary cards
st.subheader("Class Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", results["total_students"])
col2.metric("Class Average", f"{results['class_average']:.1f} / 100")
col3.metric("Pass Rate", f"{results['pass_rate']:.1f}%")
col4.metric("Needs Support", len(results["students_needing_support"]))


# Charts — design kept the same
st.divider()
left, right = st.columns([1.15, 1])

with left:
    st.subheader("📚 Average marks by subject")
    fig, ax = plt.subplots(figsize=(7, 4), facecolor="#121826")
    ax.set_facecolor("#121826")
    subject_avgs = results["subject_averages"].sort_values(ascending=True)
    bars = ax.barh(
        subject_avgs.index.astype(str),
        subject_avgs.values,
        color="#60a5fa"
    )
    ax.set_xlim(0, 100)
    ax.set_xlabel("Average marks (out of 100)", color="#e5e7eb")
    ax.set_ylabel("", color="#e5e7eb")
    ax.set_title("Subject-wise class performance", color="#f9fafb", pad=12)
    ax.tick_params(colors="#d1d5db")
    for spine in ax.spines.values():
        spine.set_color("#374151")
    ax.grid(axis="x", alpha=0.22, color="#9ca3af")
    ax.set_axisbelow(True)

    for bar, value in zip(bars, subject_avgs.values):
        ax.text(
            min(value + 1, 96),
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}",
            va="center",
            color="#f9fafb",
            fontsize=9
        )

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with right:
    st.subheader("📈 Distribution of student averages")
    averages = results["data_with_metrics"]["Average"].to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(7, 4), facecolor="#121826")
    ax.set_facecolor("#121826")
    ax.hist(
        averages,
        bins=min(10, max(5, len(averages))),
        edgecolor="#e5e7eb",
        color="#34d399",
        alpha=0.9
    )
    ax.axvline(
        np.mean(averages),
        color="#fbbf24",
        linestyle="--",
        linewidth=2,
        label=f"Mean: {np.mean(averages):.1f}"
    )
    ax.set_xlabel("Average marks", color="#e5e7eb")
    ax.set_ylabel("Number of students", color="#e5e7eb")
    ax.set_title("How student averages are distributed", color="#f9fafb", pad=12)
    ax.tick_params(colors="#d1d5db")
    for spine in ax.spines.values():
        spine.set_color("#374151")
    ax.legend(
        facecolor="#1f2937",
        edgecolor="#374151",
        labelcolor="#f9fafb"
    )
    ax.grid(axis="y", alpha=0.22, color="#9ca3af")
    ax.set_axisbelow(True)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# Student rankings
st.subheader("🏆 Student Rankings")
search = st.text_input("Search by student name or ID")
rankings = results["ranked_students"].copy()

if search:
    student_column = results["student_column"]
    rankings = rankings[
        rankings[student_column].astype(str).str.contains(
            search, case=False, na=False
        )
    ]

st.dataframe(rankings.round(2), use_container_width=True, hide_index=True)


# Subject insights
st.subheader("Subject Insights")
left, right = st.columns(2)
left.info(
    f"Strongest subject: **{results['best_subject']}** "
    f"({results['subject_averages'][results['best_subject']]:.1f} average marks)"
)
right.warning(
    f"Weakest subject: **{results['weakest_subject']}** "
    f"({results['subject_averages'][results['weakest_subject']]:.1f} average marks)"
)


# Students needing support
st.subheader(f"Students Needing Support (Any Subject Below {support_threshold})")
support = results["students_needing_support"]

if support.empty:
    st.success("No students are below the selected threshold in any subject.")
else:
    st.dataframe(support.round(2), use_container_width=True, hide_index=True)


# Download reports
st.subheader("📥 Download Reports")
col1, col2 = st.columns(2)

with col1:
    excel_report = build_excel_report(results, df, support_threshold)
    st.download_button(
        "Download Excel Report",
        data=excel_report,
        file_name="student_performance_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col2:
    st.download_button(
        "Download Rankings CSV",
        data=rankings.to_csv(index=False).encode("utf-8"),
        file_name="student_rankings.csv",
        mime="text/csv"
    )

st.caption("Built with Python, Pandas, NumPy, Matplotlib, and Streamlit.")
