import math
import os
import re
from pathlib import Path

import openpyxl
import pandas as pd

import c_file_runner


def check_ass(correct_output_path, user_output):
    correct_lines = read_output(correct_output_path)
    errors = 0

    tests_failed = set()
    aggregated_output = user_output
    aggregated_output = aggregated_output.lower()
    aggregated_output = aggregated_output.split('\n')
    aggregated_output = [agr.strip() for agr in aggregated_output]
    correct_lines = correct_lines.strip().split('\n')
    correct_lines_no_symbols = []
    for line in correct_lines:
        correct_lines_no_symbols.append(''.join(char for char in line if char.isalnum() or "|"))
    correct_lines = correct_lines_no_symbols
    correct_lines = [[sub.split('|') for sub in line.split(';')] for line in correct_lines]
    total_tests = len(correct_lines)

    for i, correct_options in enumerate(correct_lines):
        correct_options = correct_options[0]
        correct = False
        for option in correct_options:
            correct = check_if_contains(option, aggregated_output, extract_numbers(aggregated_output))
            if correct is True:
                continue
        if not correct:
            errors += 1
            tests_failed.add(f"Failed test {correct_lines[i]}.\n")

    correct_count = total_tests - errors
    # Calculate the grade
    grade = (correct_count / total_tests) * 100

    return grade, tests_failed


def read_output(path):
    try:
        with open(path, 'r') as file:
            correct_lines = file.readlines()
        correct_lines = ''.join(correct_lines)
    except IOError:
        print("Error reading input file")
        return 0
    return correct_lines


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
            out.replace(",", "")
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


def start_grading_process(root):
    processed_dir = root + "/Processed"
    output_dir = root + "/Output"
    input_text = root + "/input.txt"
    correct_output = root + "/output.txt"

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

    c_files = [os.path.join(processed_dir, file) for file in os.listdir(processed_dir) if file.endswith('.c')]

    data = pd.read_csv("C:/Grading/Now/students.csv", encoding='utf-8')
    student_data = {}

    results = []
    # Populate the dictionary
    for index, row in data.iterrows():
        codeboard = row['codeboard']
        ident = row['ident']
        id = str(int(row['id'])) if not math.isnan(row['id']) else "0"

        name_id_pair = [row['name'], ident, id]
        student_data[codeboard] = name_id_pair

    for index, c_file in enumerate(c_files, start=2):  # Start from row 2 for data
        print("report for", c_file, ":")
        # Grade the code
        output = c_file_runner.run_file(c_file, input_text)
        code_grade, tests_failed = check_ass(correct_output, output)

        print("code grade =", code_grade)

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

        results.append({"c_file": c_file, "report": report, "output": output, "grade": code_grade, "c_code": c_code})
    # Save the Excel workbook
    wb.save(root + "/grading_results.xlsx")

    return results
