import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Section Grade Analysis", layout="wide")

st.title("📊 Single Section: Student Marks and Grade Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload Excel file with student marks (one section only)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)

        # Check for required columns
        required_columns = ['Total', 'Grade']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
        else:
            # Keep only Total and Grade columns
            df = df[required_columns]

            # Preview cleaned data
            st.subheader("📄 Cleaned Data Preview (Total and Grade only)")
            st.dataframe(df)

            # Count number of students in each grade
            grade_counts = df['Grade'].value_counts().reindex(['A*', 'A', 'B', 'C', 'D', 'E', 'U'], fill_value=0)

            # Calculate average mark
            average_mark = df['Total'].mean()

            # Count above/below average
            above_avg = (df['Total'] > average_mark).sum()
            below_avg = (df['Total'] <= average_mark).sum()

            # Display metrics
            st.subheader("📈 Summary Statistics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Average Mark", f"{average_mark:.2f}")
            col2.metric("Above Average", above_avg)
            col3.metric("Below Average", below_avg)

            # Plot grade distribution
            st.subheader("🎓 Grade Distribution")
            fig, ax = plt.subplots()
            sns.barplot(x=grade_counts.index, y=grade_counts.values, palette="viridis", ax=ax)
            ax.set_xlabel("Grade")
            ax.set_ylabel("Number of Students")
            ax.set_title("Number of Students in Each Grade")
            st.pyplot(fig)

            # Observations
            st.subheader("📝 Observations")

            most_common_grade = grade_counts.idxmax()
            obs = f"""
- **Average Total Mark:** {average_mark:.2f}
- **Students Above Average:** {above_avg}
- **Students Below Average:** {below_avg}
- **Most Common Grade:** {most_common_grade} ({grade_counts[most_common_grade]} students)
"""
            st.text(obs)

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload an Excel file to proceed.")
