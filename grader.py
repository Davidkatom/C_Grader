import math
import os
import subprocess
from pathlib import Path
import re

import openpyxl
import pandas as pd
from openai import OpenAI

openai_api_key = os.environ.get('OPENAI_KEY')

root_dir = "C:/Grading/ass4"  # Replace with the path to your root directory
processed_dir = "C:/Grading/ass4/Processed"  # Replace with the path to your Processed directory
output_dir = "C:/Grading/ass4/Output"  # Replace with the path to your Processed directory
c_files = [os.path.join(processed_dir, file) for file in os.listdir(processed_dir) if file.endswith('.c')]

data = pd.read_csv("C:/Grading/students.csv", encoding='utf-8')
student_data = {}

# Populate the dictionary
for index, row in data.iterrows():
    codeboard = row['codeboard']
    ident = row['ident']
    id = str(int(row['id'])) if not math.isnan(row['id']) else "0"

    name_id_pair = [row['name'], ident, id]
    student_data[codeboard] = name_id_pair


def grade_c_program(c_file, input_file, correct_file):
    # Compile the C program
    tests_failed = set()
    program_name = "program.exe"
    compile_command = f"gcc {c_file} -o {program_name}"
    result = subprocess.run(compile_command, shell=True, text=True, capture_output=True)
    problems_with_newline = False
    missing_newline_after_scanf = False

    # Check for compilation errors
    if result.returncode != 0:
        tests_failed.add(f"Compilation Error. Grade: 0")
        return 0, tests_failed, "Compilation Error"

    # Read input lines from the file
    try:
        with open(input_file, 'r') as file:
            input_lines = file.readlines()
    except IOError:
        tests_failed.add("Error reading input file")
        return 0, tests_failed, "Error reading input file"

    # Read correct lines from the file
    try:
        with open(correct_file, 'r') as file:
            correct_lines = file.readlines()
        correct_lines = ''.join(correct_lines)
    except IOError:
        tests_failed.add("Error reading input file")
        return 0, tests_failed, "Error reading input file"

    # Initialize variables for output aggregation and grading
    aggregated_output = []
    run_errors = False
    # delimiter = "END_OF_INPUT"  # Unique delimiter

    # Run the compiled program for each line in the input file
    timeout_duration = 2  # Set the timeout duration in seconds

    def send_input(proc, input_data):
        print(f"Sending: {input_data}")
        proc.stdin.write(input_data + "\n")
        proc.stdin.flush()

    for input_data in input_lines:
        process = subprocess.Popen(program_name, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=True, text=True)
        try:
            output, errors = process.communicate(input=input_data, timeout=timeout_duration)
        except subprocess.TimeoutExpired:
            process.kill()
            errors = process.communicate()[1]
            tests_failed.add(f"Timeout Error. Grade: 0")
            run_errors = True
            return

        if errors:
            run_errors = True
            break
        try:
            if not output.endswith('\n'):
                problems_with_newline = True
                output += '\n'
            aggregated_output.append(output)
        except AttributeError:
            tests_failed.add(f"No output. Grade: 0")
            return 0, tests_failed, "No output"

    if run_errors:
        tests_failed.add(f"Runtime Error. Grade: 0")
        return 0, tests_failed

    segmented_output = aggregated_output.copy()
    aggregated_output = ''.join(aggregated_output)
    aggregated_output = aggregated_output.lower()
    output_copy = aggregated_output

    # Assuming aggregated_output and correct_lines are already defined
    aggregated_output = aggregated_output.split('\n')
    aggregated_output = [agr.strip() for agr in aggregated_output]
    correct_lines = correct_lines.strip().split('\n')
    correct_lines = [[sub.split('|') for sub in line.split(';')] for line in correct_lines]
    total_tests = len(correct_lines)

    def check_if_contains(input, output, output_numbers):
        type = ""
        try:
            float(input)
            type = "float"
        except ValueError:
            type = "string"
        if input.startswith("0"):
            type = "string"
        if type == "float":

            for num in output_numbers:
                if not isinstance(num, list) or len(num) == 0:
                    continue
                if len(num) > 1:
                    num = [int(float(n)) for n in num]
                    try:
                        num = int(''.join(map(str, num)))
                    except ValueError:
                        continue
                elif len(num) == 1:
                    num = num[0]

                if math.isclose(float(num), float(input), rel_tol=0.05):
                    # output_numbers.remove(num)
                    return True
            return False
        if type == "string":
            for out in output:
                out = out.replace(" ", "")
                if input.replace(" ", "") in out:
                    # output.remove(out)
                    return True
        return False

    def extract_numbers(text):
        if isinstance(text, list):
            numbers = []
            for t in text:
                numbers.append(extract_numbers(t))
            return numbers
            # text = ''.join(text)
        # Use regular expression to find all numbers
        return re.findall(r'-?\d+\.?\d*', text)

    # extract a letter sorrounded by spaces or end of string

    def extract_letter(text):
        if isinstance(text, list):
            text = ''.join(text)
        elif not isinstance(text, str):
            return []  # or raise an error, depending on your requirements

        # Pattern for a letter preceded by a space or start of the string
        pattern1 = r'(?<=\s)[a-zA-Z](?=\s|$)'
        pattern2 = r'^[a-zA-Z](?=\s|$)'

        # Find all matches for both patterns and combine the results
        inst = re.findall(pattern1, text) + re.findall(pattern2, text)
        if 'a' in inst:
            inst.remove('a')
        return inst

    errors1 = 0
    errors2 = 0
    tests_failed1 = tests_failed.copy()
    tests_failed2 = tests_failed.copy()
    errors = 0

    for i, correct_options in enumerate(correct_lines):
        correct = check_if_contains(correct_options[0][0], aggregated_output, extract_numbers(aggregated_output))
        if not correct:
            errors += 1
            tests_failed.add(f"Failed test {correct_lines[i]}.\n")

    correct_count = total_tests - errors
    # Calculate the grade
    grade = (correct_count / total_tests) * 100

    if grade < 100:
        with open(os.path.join(output_dir, Path(f'{c_file}{grade}.txt').name), 'w') as file:
            file.write(output_copy)

    return grade, tests_failed, output_copy


def grade_c_code(c_file_path, openai_api_key):
    # Read the C file
    try:
        with open(c_file_path, 'r', encoding='utf-8') as file:
            c_code = file.read()
    except IOError:
        return "Error reading C file."

    # Set up OpenAI GPT-4 API
    client = OpenAI(api_key=openai_api_key)

    # Prepare the prompt for GPT-4

    prompt = ("Analyze the following C code for coding standards and provide feedback in a structured format. "
              "Only list significant issues that notably affect the code's readability, maintainability, "
              "or functionality. Don't assume that the code neads more features or functionality.\n"
              "Use bullet points for the following categories:\n"
              "1. Comments: (Only mention if there's a significant lack of comments where necessary for understanding complex logic)\n"
              "2. Naming Conventions: (Only note issues if naming conventions lead to confusion or misunderstanding of the code purpose)\n"
              "3. Magic Numbers: (Mention only if the use of magic numbers significantly hinders understanding of what the code is doing)\n"
              "4. Tabs for Indentation: (Only raise an issue if improper indentation severely affects the readability of the code)\n"
              "5. Code Efficiency and Simplicity: (Only comment on efficiency and simplicity if there are glaring inefficiencies or overly complex structures that make the code hard to understand)\n\n"
              "After the list, provide a grade on a scale of 1 to 5 based on these criteria. "
              "A score of 5 means the code has no significant issues, and a lower score indicates notable problems in the listed categories.\n\n"
              f"C Code:\n\n{c_code}\n\n"
              "Please format your response as follows:\n"
              "Comments:\n- [Significant Issue 1]\n- [Significant Issue 2]\n...\n"
              "Naming Conventions:\n- [Significant Issue 1]\n- [Significant Issue 2]\n...\n"
              "Magic Numbers:\n- [Significant Issue 1]\n- [Significant Issue 2]\n...\n"
              "Tabs for Indentation:\n- [Significant Issue 1]\n- [Significant Issue 2]\n...\n"
              "Code Efficiency and Simplicity:\n- [Significant Issue 1]\n- [Significant Issue 2]\n...\n"
              "Grade = [only a number on a scale of 1 to 5] for example Grade = 3 ")

    # Send the prompt to the GPT-4 API
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            temperature=1.5,
            model="gpt-3.5-turbo",
        )
        report = chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error in API call: {e}"

    # Output the report and grade
    return report


def extract_and_print_grade(report):
    # Split the report based on the known phrase
    parts = report.split("Grade = ")
    if len(parts) > 1:
        # Further split to isolate the grade
        grade_part = parts[1].split()[0]  # Assumes grade is followed by a space or end of string
    else:
        print("Grade not found in the report.")
        grade_part = -1
    return grade_part


def grade_and_populate_excel(c_files, input_text, correct_output, openai_api_key):
    # Initialize an Excel workbook and create a new sheet
    wb = openpyxl.Workbook()
    sheet = wb.active

    # Write headers to the Excel sheet
    sheet['A1'] = 'C File'
    sheet['B1'] = 'name'
    sheet['C1'] = 'Ident'
    sheet['D1'] = 'Id'

    sheet['E1'] = 'Code Grade'
    sheet['F1'] = 'Style Grade'
    sheet['G1'] = 'Report'
    sheet['H1'] = 'Total Grade'
    # sheet['F1'] = 'Output'
    sheet['I1'] = 'code'

    # Directory where the reports and code files are located
    reports_directory = "reports"

    # Loop through the C files
    for index, c_file in enumerate(c_files, start=2):  # Start from row 2 for data
        print("report for", c_file, ":")
        # Grade the code
        code_grade, tests_failed, output = grade_c_program(c_file, input_text, correct_output)
        print("code grade =", code_grade)

        # # # OpenAI API call and write to a file
        # with open(os.path.join(reports_directory, Path(f'{c_file}.txt').name), "w") as file:
        #     report = grade_c_code(c_file, openai_api_key)
        #     file.write(f"Report for {c_file}:\n{report}\n\n")

        # Extract and print the style grade
        # style_grade = extract_and_print_grade(report)
        style_grade = 5
        print("style grade =", style_grade)
        # style_grade = 5  # CHANGE THIS TO THE GRADE
        # Calculate the total grade
        total_grade = 0.7 * float(code_grade) + 0.3 * float(style_grade) * 20
        print("Total grade =", total_grade)
        report = "Tests failed:\n" + ''.join(tests_failed) if len(tests_failed) > 0 else "No tests failed."

        with open(os.path.join(processed_dir, Path(f'{c_file}').name), 'r', encoding='utf-8') as file:
            c_code = file.read()

        # report = report + "\n" + "Tests failed:\n" + ''.join(tests_failed)
        # Populate the Excel sheet with the grades and report
        student_info = student_data.get(Path(f'{c_file}').name)  # Try to get the data using file_name as key
        if student_info is not None:
            sheet[f'B{index}'] = student_data[Path(f'{c_file}').name][0]
            sheet[f'C{index}'] = student_data[Path(f'{c_file}').name][1]

            sheet[f'D{index}'] = student_data[Path(f'{c_file}').name][2]
        else:
            sheet[f'B{index}'] = "0"
            sheet[f'C{index}'] = "0"
            sheet[f'D{index}'] = "0"


        sheet[f'A{index}'] = Path(f'{c_file}').name
        sheet[f'E{index}'] = code_grade
        sheet[f'F{index}'] = style_grade
        sheet[f'G{index}'] = report
        sheet[f'H{index}'] = total_grade
        # sheet[f'F{index}'] = output
        sheet[f'I{index}'] = c_code

    # Save the Excel workbook
    wb.save(root_dir + "/grading_results.xlsx")


# Example usage


input_text = root_dir + "/input.txt"
correct_output = root_dir + "/output.txt"

grade_and_populate_excel(c_files, input_text, correct_output, openai_api_key)
