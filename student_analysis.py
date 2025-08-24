import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="Student Performance Analysis", 
    layout="wide",
    page_icon="🎓"
)

# Function to load external CSS
def load_css(file_name):
    """
    Load CSS from an external file
    """
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("CSS file not found. Using default styling.")

# Load external CSS
load_css("style.css")

# Title and description
st.markdown('<h1 class="main-header">🎓 Student Performance Analysis Dashboard</h1>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    This interactive dashboard analyzes student performance data to identify patterns, strengths, and areas for improvement.
    Explore the visualizations below to gain insights!
</div>
""", unsafe_allow_html=True)

# File uploader
with st.container():
    st.markdown("### 📁 Upload Your Data")
    uploaded_file = st.file_uploader("Upload your student performance CSV file", type="csv", label_visibility="collapsed")

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    
    # Display basic info
    st.markdown('<div class="sub-header">Dataset Overview</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">' + str(len(df)) + '</div><div class="metric-label">Total Students</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">' + str(df['Class'].nunique()) + '</div><div class="metric-label">Number of Classes</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">' + str(len(df.columns)) + '</div><div class="metric-label">Data Columns</div></div>', unsafe_allow_html=True)
    with col4:
        avg_percentage = df['Percentage'].mean().round(2)
        st.markdown(f'<div class="metric-card"><div class="metric-value">{avg_percentage}%</div><div class="metric-label">Average Percentage</div></div>', unsafe_allow_html=True)
    
    # Show data
    if st.checkbox("Show raw data", key="show_raw_data"):
        st.dataframe(df)
    
    # Convert to long format
    df_long = df.melt(
        id_vars=['Student_ID', 'Name', 'Class', 'Gender'],
        value_vars=['Math', 'Science', 'English'],
        var_name='Subject',
        value_name='Score'
    )
    
    # Define color palettes
    subject_palette = {'Math': '#ff6b6b', 'Science': '#4ecdc4', 'English': '#45b7d1'}
    grade_palette = {'A+': '#2ecc71', 'A': '#27ae60', 'B': '#f39c12', 'C': '#e67e22', 'D': '#e74c3c', 'F': '#c0392b'}
    
    # Visualizations
    st.markdown('<div class="sub-header">Performance Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Score Distribution by Subject")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(data=df_long, x='Subject', y='Score', hue='Subject', palette=subject_palette, legend=False, ax=ax)
        ax.set_title('Score Distribution by Subject')
        st.pyplot(fig)
        
        st.markdown("##### Performance by Gender")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(data=df_long, x='Subject', y='Score', hue='Gender', palette='pastel', ax=ax)
        ax.set_title('Performance by Gender')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)
    
    with col2:
        st.markdown("##### Subject Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(8, 6))
        subject_corr = df[['Math', 'Science', 'English']].corr()
        sns.heatmap(subject_corr, annot=True, cmap='RdYlGn', center=0, square=True, fmt='.2f', ax=ax)
        ax.set_title('Subject Correlation Heatmap')
        st.pyplot(fig)
        
        st.markdown("##### Grade Distribution")
        fig, ax = plt.subplots(figsize=(8, 6))
        grade_order = ['A+', 'A', 'B', 'C', 'D', 'F']
        grade_counts = df['Grade'].value_counts().reindex(grade_order)
        colors = [grade_palette[grade] for grade in grade_counts.index]
        sns.barplot(x=grade_counts.index, y=grade_counts.values, hue=grade_counts.index, palette=colors, legend=False, ax=ax)
        ax.set_title('Grade Distribution')
        ax.set_xlabel('Grade')
        ax.set_ylabel('Number of Students')
        for i, count in enumerate(grade_counts.values):
            ax.text(i, count + 0.1, str(count), ha='center', va='bottom')
        st.pyplot(fig)
    
    # Detailed Analysis
    st.markdown('<div class="sub-header">Detailed Analysis</div>', unsafe_allow_html=True)
    
    # Overall statistics
    st.markdown("##### Subject Averages")
    subject_avgs = df[['Math', 'Science', 'English']].mean().round(2)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{subject_avgs["Math"]}</div><div class="metric-label">Math Average</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{subject_avgs["Science"]}</div><div class="metric-label">Science Average</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{subject_avgs["English"]}</div><div class="metric-label">English Average</div></div>', unsafe_allow_html=True)
    
    # Top and bottom performers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🏆 Top 5 Performers")
        top_students = df.nlargest(5, 'Percentage')[['Name', 'Class', 'Math', 'Science', 'English', 'Total', 'Percentage', 'Grade']]
        st.dataframe(top_students)
    
    with col2:
        st.markdown("##### 📊 Bottom 5 Performers")
        bottom_students = df.nsmallest(5, 'Percentage')[['Name', 'Class', 'Math', 'Science', 'English', 'Total', 'Percentage', 'Grade']]
        st.dataframe(bottom_students)
    
    # Student selector for individual profiles
    st.markdown("##### 👤 Individual Student Profile")
    student_names = df['Name'].tolist()
    selected_student = st.selectbox("Select a student to view their profile:", student_names, label_visibility="collapsed")
    
    if selected_student:
        student_data = df_long[df_long['Name'] == selected_student]
        class_avg = df_long.groupby('Subject')['Score'].mean().reset_index()
        student_info = df[df['Name'] == selected_student].iloc[0]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot class average as bars
        bars = ax.bar(class_avg['Subject'], class_avg['Score'], alpha=0.7, 
                     color='lightgrey', label='Class Average')
        
        # Plot student performance as line
        line = ax.plot(student_data['Subject'], student_data['Score'], 
                      marker='o', linewidth=2.5, markersize=8, 
                      label=selected_student, color='#ff6b6b')
        
        # Add value labels
        for i, (subject, avg_score) in enumerate(zip(class_avg['Subject'], class_avg['Score'])):
            ax.text(i, avg_score + 2, f'{avg_score:.1f}', ha='center', va='bottom', fontsize=10)
        
        for i, (subject, score) in enumerate(zip(student_data['Subject'], student_data['Score'])):
            ax.text(i, score + 2, f'{score}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.legend()
        ax.set_title(f'Performance Profile: {selected_student} vs Class Average')
        ax.set_ylabel('Score')
        ax.set_ylim(0, 110)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        # Display student details in a card
        st.markdown(f'<div class="student-card">', unsafe_allow_html=True)
        st.markdown(f"**Student Details for {selected_student}**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Class:** {student_info['Class']}")
            st.write(f"**Gender:** {student_info['Gender']}")
        with col2:
            st.write(f"**Math:** {student_info['Math']} (Class Avg: {subject_avgs['Math']})")
            st.write(f"**Science:** {student_info['Science']} (Class Avg: {subject_avgs['Science']})")
        with col3:
            st.write(f"**English:** {student_info['English']} (Class Avg: {subject_avgs['English']})")
            st.write(f"**Total:** {student_info['Total']}")
        
        col4, col5 = st.columns(2)
        with col4:
            st.write(f"**Percentage:** {student_info['Percentage']}%")
        with col5:
            st.write(f"**Grade:** {student_info['Grade']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Download report
    st.markdown('<div class="sub-header">Download Report</div>', unsafe_allow_html=True)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Raw Data', index=False)
        top_students.to_excel(writer, sheet_name='Top Performers', index=False)
        bottom_students.to_excel(writer, sheet_name='Bottom Performers', index=False)
        class_performance = df.groupby('Class')['Percentage'].agg(['mean', 'count']).round(2)
        class_performance.columns = ['Average Percentage', 'Number of Students']
        class_performance.to_excel(writer, sheet_name='Class Performance')
    
    output.seek(0)
    
    st.download_button(
        label="📥 Download Full Analysis Report (Excel)",
        data=output,
        file_name="student_performance_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("📝 Please upload a CSV file to begin the analysis. Use the sample format below.")
    
    # Sample data structure
    sample_data = {
        'Student_ID': [1, 2, 3],
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'Class': ['10A', '10B', '10A'],
        'Gender': ['Male', 'Female', 'Male'],
        'Math': [85, 92, 78],
        'Science': [88, 95, 72],
        'English': [82, 88, 75],
        'Total': [255, 275, 225],
        'Percentage': [85.0, 91.7, 75.0],
        'Grade': ['A', 'A+', 'B']
    }
    
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df)