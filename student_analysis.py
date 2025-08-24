import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data from the CSV file
df = pd.read_csv('student_performance_dataset.csv')

# Display basic info about the dataframe
print("Data loaded successfully!")
print(f"DataFrame Shape: {df.shape}")
print("\nDataFrame Info:")
print(df.info())
print("\nFirst 5 rows:")
print(df.head())

# Check for missing values
print("\nMissing values in each column:")
print(df.isnull().sum())

# Convert data to long format for Seaborn
df_long = df.melt(
    id_vars=['Student_ID', 'Name', 'Class', 'Gender'],
    value_vars=['Math', 'Science', 'English'],
    var_name='Subject',
    value_name='Score'
)

print("\nLong format data (first 10 rows):")
print(df_long.head(10))

# Set visual style
sns.set_style("whitegrid")
plt.figure(figsize=(15, 12))

# Define color palettes
subject_palette = {'Math': '#ff6b6b', 'Science': '#4ecdc4', 'English': '#45b7d1'}
grade_palette = {'A+': '#2ecc71', 'A': '#27ae60', 'B': '#f39c12', 'C': '#e67e22', 'D': '#e74c3c', 'F': '#c0392b'}

# 1. Subject Distribution Box Plot (FIXED)
plt.subplot(2, 2, 1)
sns.boxplot(data=df_long, x='Subject', y='Score', hue='Subject', palette=subject_palette, legend=False)
plt.title('1. Score Distribution by Subject', fontsize=14, fontweight='bold')
plt.xlabel('Subject')
plt.ylabel('Score')

# 2. Correlation Heatmap
plt.subplot(2, 2, 2)
subject_corr = df[['Math', 'Science', 'English']].corr()
sns.heatmap(subject_corr, annot=True, cmap='RdYlGn', center=0, square=True, fmt='.2f')
plt.title('2. Subject Correlation Heatmap', fontsize=14, fontweight='bold')

# 3. Performance by Gender
plt.subplot(2, 2, 3)
sns.boxplot(data=df_long, x='Subject', y='Score', hue='Gender', palette='pastel')
plt.title('3. Performance by Gender', fontsize=14, fontweight='bold')
plt.xlabel('Subject')
plt.ylabel('Score')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# 4. Grade Distribution (FIXED)
plt.subplot(2, 2, 4)
grade_order = ['A+', 'A', 'B', 'C', 'D', 'F']
grade_counts = df['Grade'].value_counts().reindex(grade_order)
colors = [grade_palette[grade] for grade in grade_counts.index]
sns.barplot(x=grade_counts.index, y=grade_counts.values, hue=grade_counts.index, palette=colors, legend=False)
plt.title('4. Grade Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Grade')
plt.ylabel('Number of Students')
for i, count in enumerate(grade_counts.values):
    plt.text(i, count + 1, str(count), ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Additional Analysis
print("\n" + "="*50)
print("DETAILED PERFORMANCE ANALYSIS")
print("="*50)

# Overall statistics
print("\n📊 Overall Subject Averages:")
subject_avgs = df[['Math', 'Science', 'English']].mean().round(2)
for subject, avg in subject_avgs.items():
    print(f"   {subject}: {avg}")

# Subject strength analysis
strongest_subject = subject_avgs.idxmax()
weakest_subject = subject_avgs.idxmin()
print(f"\n🎯 Strongest Subject: {strongest_subject} ({subject_avgs[strongest_subject]})")
print(f"🎯 Weakest Subject: {weakest_subject} ({subject_avgs[weakest_subject]})")

# Top 5 performers
print("\n🏆 Top 5 Performers:")
top_students = df.nlargest(5, 'Percentage')[['Name', 'Class', 'Math', 'Science', 'English', 'Total', 'Percentage', 'Grade']]
print(top_students.to_string(index=False))

# Bottom 5 performers
print("\n⚠️  Bottom 5 Performers:")
bottom_students = df.nsmallest(5, 'Percentage')[['Name', 'Class', 'Math', 'Science', 'English', 'Total', 'Percentage', 'Grade']]
print(bottom_students.to_string(index=False))

# Class-wise performance
print("\n🏫 Class-wise Average Percentage:")
class_performance = df.groupby('Class')['Percentage'].agg(['mean', 'count']).round(2)
class_performance.columns = ['Average Percentage', 'Number of Students']
print(class_performance)

# Gender performance
print("\n👥 Gender-wise Performance:")
gender_performance = df.groupby('Gender')['Percentage'].mean().round(2)
print(gender_performance)

# Create individual student profile function
def plot_student_profile(student_name):
    student_data = df_long[df_long['Name'] == student_name]
    class_avg = df_long.groupby('Subject')['Score'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    
    # Plot class average as bars
    bars = plt.bar(class_avg['Subject'], class_avg['Score'], alpha=0.7, 
                  color='lightgrey', label='Class Average')
    
    # Plot student performance as line
    line = plt.plot(student_data['Subject'], student_data['Score'], 
                   marker='o', linewidth=2.5, markersize=8, 
                   label=student_name, color='#ff6b6b')
    
    # Add value labels on bars and points
    for i, (subject, avg_score) in enumerate(zip(class_avg['Subject'], class_avg['Score'])):
        plt.text(i, avg_score + 2, f'{avg_score:.1f}', ha='center', va='bottom', fontsize=10)
    
    for i, (subject, score) in enumerate(zip(student_data['Subject'], student_data['Score'])):
        plt.text(i, score + 2, f'{score}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.legend()
    plt.title(f'Performance Profile: {student_name} vs Class Average', fontsize=14, fontweight='bold')
    plt.ylabel('Score')
    plt.ylim(0, 110)
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Display student details
    student_info = df[df['Name'] == student_name].iloc[0]
    print(f"\n📋 Student Details for {student_name}:")
    print(f"   Class: {student_info['Class']}")
    print(f"   Gender: {student_info['Gender']}")
    print(f"   Math: {student_info['Math']} (Class Avg: {subject_avgs['Math']})")
    print(f"   Science: {student_info['Science']} (Class Avg: {subject_avgs['Science']})")
    print(f"   English: {student_info['English']} (Class Avg: {subject_avgs['English']})")
    print(f"   Total: {student_info['Total']}")
    print(f"   Percentage: {student_info['Percentage']}%")
    print(f"   Grade: {student_info['Grade']}")

# Example: Plot profile for top student
print("\n" + "="*50)
print("INDIVIDUAL STUDENT PROFILES")
print("="*50)

top_student_name = top_students.iloc[0]['Name']
print(f"\n⭐ Top Performer: {top_student_name}")
plot_student_profile(top_student_name)

# Example: Plot profile for bottom student
bottom_student_name = bottom_students.iloc[0]['Name']
print(f"\n🔻 Bottom Performer: {bottom_student_name}")
plot_student_profile(bottom_student_name)

# Save analysis results to Excel
try:
    with pd.ExcelWriter('student_performance_analysis.xlsx') as writer:
        df.to_excel(writer, sheet_name='Raw Data', index=False)
        top_students.to_excel(writer, sheet_name='Top Performers', index=False)
        bottom_students.to_excel(writer, sheet_name='Bottom Performers', index=False)
        class_performance.to_excel(writer, sheet_name='Class Performance')
    print("\n💾 Analysis results saved to 'student_performance_analysis.xlsx'")
except Exception as e:
    print(f"\n⚠️  Could not save Excel file: {e}")

print("\n" + "="*50)
print("ANALYSIS COMPLETE!")
print("="*50)