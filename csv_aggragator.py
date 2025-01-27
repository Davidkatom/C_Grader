import pandas as pd
import os

# Set the root directory
root = "C:/Grading/Now/ass4"

# Initialize a set to collect all unique student names
all_students = set()

# First pass: Collect all unique student names from all assignments
subfolders = [f.path for f in os.scandir(root) if f.is_dir()]

for subfolder in subfolders:
    folder_name = os.path.basename(subfolder)

    # Find Excel files in the subfolder
    excel_files = [f for f in os.listdir(subfolder) if f.endswith('.xlsx')]
    if not excel_files:
        continue  # Skip if no Excel file is found

    # Assume there's only one Excel file per subfolder
    excel_file = os.path.join(subfolder, excel_files[0])

    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Collect student names
    student_names = df['C File'].astype(str).str.strip()
    all_students.update(student_names)

# Initialize the cumulative DataFrame with all students
all_data = pd.DataFrame(index=sorted(all_students))

# Second pass: Process each assignment
for subfolder in subfolders:
    folder_name = os.path.basename(subfolder)

    # Find Excel files in the subfolder
    excel_files = [f for f in os.listdir(subfolder) if f.endswith('.xlsx')]
    if not excel_files:
        continue  # Skip if no Excel file is found

    # Assume there's only one Excel file per subfolder
    excel_file = os.path.join(subfolder, excel_files[0])

    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Select relevant columns and clean student names
    df = df[['C File', 'Report', 'Total Grade']]
    df['C File'] = df['C File'].astype(str).str.strip()
    df.drop_duplicates(subset='C File', inplace=True)
    df.set_index('C File', inplace=True)

    # Reindex the DataFrame to include all students
    df = df.reindex(all_data.index)

    # For students missing from the assignment, set 'Report' to 'MISSING'
    # df['Report'].fillna('MISSING', inplace=True)

    # Rename columns to include the question identifier
    df.rename(columns={
        'Report': f'{folder_name}_Report',
        'Total Grade': f'{folder_name}_Grade'
    }, inplace=True)

    # Merge the current DataFrame with the cumulative DataFrame
    all_data = all_data.join(df[[f'{folder_name}_Report', f'{folder_name}_Grade']])

# Save the merged data to a new Excel file
all_data.to_excel('C:/Grading/Now/ass4/merged_grades.xlsx')
