import os
import shutil

root_dir = "C:/Grading/Now/ass4/Q4/Pre"  # Replace with the path to your root directory
processed_dir = "C:/Grading/Now/ass4/Q4/Processed"  # Replace with the path to your Processed directory

# Create the Processed directory if it doesn't exist
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)
    print(f"Created directory {processed_dir}")

# Iterate through each student's folder in the root directory
for student in os.listdir(root_dir):
    student_path = os.path.join(root_dir, student)
    print(f"Processing {student}...")

    if os.path.isdir(student_path):
        # Get the highest numbered folder
        highest_folder = max([f for f in os.listdir(student_path) if f.isdigit()], key=int)
        highest_folder_path = os.path.join(student_path, highest_folder)
        highest_folder_path = os.path.join(highest_folder_path, "Root")
        # Move and rename C files
        for file in os.listdir(highest_folder_path):
            if file.endswith('.c'):
                source_file = os.path.join(highest_folder_path, file)
                destination_file = os.path.join(processed_dir, f"{student}.c")

                # Check if a file with the same name already exists
                if os.path.exists(destination_file):
                    print(f"File {destination_file} already exists. Skipping.")
                else:
                    shutil.move(source_file, destination_file)
                    print(f"Moved {source_file} to {destination_file}")

print("Processing completed.")
