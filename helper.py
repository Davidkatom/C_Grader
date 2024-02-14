import pandas as pd
import os

# Path: /scripts/excel_aggregator.py

import os
import pandas as pd
import glob

# Path: /scripts/excel_aggregator.py

def aggregate_grades_with_reports(base_dir):
    # Dictionary to store student grades and reports
    student_data = {}

    # Traverse through all Excel files in subfolders
    for excel_file in glob.glob(os.path.join(base_dir, 'Q*/[!~]*.xlsx')):
        # Extracting the assignment name from the directory
        assignment = os.path.basename(os.path.dirname(excel_file))

        # Read the Excel file
        df = pd.read_excel(excel_file)

        # Assuming student names are in the first column, grades in the second, and reports in the fourth
        for index, row in df.iterrows():
            student = row[df.columns[0]]
            grade = row[df.columns[1]]
            report = row[df.columns[3]]

            # Add or update the student's grade and report for the assignment
            if student not in student_data:
                student_data[student] = {}
            student_data[student][f'Grade_{assignment}'] = grade
            student_data[student][f'Report_{assignment}'] = report

    # Create a DataFrame from the dictionary
    final_df = pd.DataFrame.from_dict(student_data, orient='index')

    # Reset index to get student names as a column
    final_df.reset_index(inplace=True)
    final_df.rename(columns={'index': 'Student Name'}, inplace=True)

    # Save the DataFrame to a new Excel file
    final_df.to_excel(os.path.join(base_dir, 'aggregated_grades_reports.xlsx'), index=False)

    return final_df

def concatenate_c_files(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Dictionary to store grouped .c files by filename
    c_files_dict = {}

    # Recursively search for .c files in the input folder
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".c"):
                file_path = os.path.join(root, file)
                filename = os.path.splitext(file)[0]

                # Add the file content to the corresponding list in the dictionary
                if filename not in c_files_dict:
                    c_files_dict[filename] = []
                with open(file_path, "r", encoding="utf-8") as c_file:
                    c_files_dict[filename].append(c_file.read())

    # Concatenate and write grouped .c files to the output folder
    for filename, content_list in c_files_dict.items():
        output_file_path = os.path.join(output_folder, f"{filename}.c")
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write("\n".join(content_list))

    print("Concatenation of .c files completed.")

# # Example usage:

input_folder = "C:/Grading/ass1"
output_folder = "C:/Grading/ass1/Joined"
concatenate_c_files(input_folder, output_folder)

# base_dir = 'C:/Grading/ass1'
# aggregate_grades_with_reports(base_dir)



