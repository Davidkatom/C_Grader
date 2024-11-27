import os
import shutil

# List of your parent directories
folder_path = "C:/Grading/ass8/questions"
parent_folders = os.listdir(folder_path)
for folder in parent_folders:
    # Get the path of the current folder
    # Get the files in the current folder
    path = os.path.join(folder_path, folder)  # Adjust the path as necessary
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    # Ensure there is at least one file in the folder
    if files:
        # Taking the first file in the folder for simplicity
        file_name = files[0]
        file_path = os.path.join(path, file_name)

        # Define the new file path in the parent folder with the parent's name
        new_file_path = os.path.join(folder_path, folder + "_" + file_name)

        # Copy and rename the file to the parent folder
        shutil.copyfile(file_path, new_file_path)
        print(f"Copied and renamed {file_name} to {new_file_path}")
