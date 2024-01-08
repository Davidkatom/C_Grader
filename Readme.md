# Automated C Code Grading System

## Overview

This repository contains a Python-based automated grading system for C programming assignments. It compiles, runs, and evaluates C programs against given inputs and expected outputs, and also uses OpenAI's GPT-4 to analyze coding style and standards. The system outputs detailed reports and grades, which are compiled into an Excel spreadsheet.

## Features

1. **Automated Compilation and Execution**: Grades C programs by compiling and running them with provided test inputs.
2. **Style and Standards Analysis**: Utilizes OpenAI GPT-4 to analyze the code for readability, maintainability, and coding standards.
3. **Detailed Reports**: Generates comprehensive reports outlining both functional correctness and coding style.
4. **Excel Integration**: Automatically populates an Excel workbook with grades and reports for each submission.
5. **Customizable Test Cases**: Supports different input and output files for testing various scenarios.

## Requirements

- Python 3.x
- GCC Compiler for C
- OpenPyXL Library
- OpenAI API Key

## Usage

1. **Setting Up**: Ensure Python 3, GCC, and OpenPyXL are installed. Obtain an OpenAI API key and set it as an environment variable `OPENAI_KEY`.

2. **Preparing Tests**: Place your C files, input, and correct output files in the specified directories.

3. **Running the Grader**:
   - Execute the main script to start the grading process.
   - The script will compile and run each C program, grade them based on output correctness, and then assess coding style using OpenAI's GPT-4.
   - The results, including a detailed report and grades, are saved into an Excel file.

4. **Viewing Results**: Open the generated `grading_results.xlsx` to view the detailed reports and grades for each submission.

## Customization

- Modify the input and output file paths in the script to match your test case files.
- Adjust the grading weights between functional correctness and coding style in the script.

## Support

For any issues or questions, please open an issue in the repository.

---

**Note**: This system is intended for educational purposes and as a tool to assist in grading. It should be used responsibly and with an understanding of its limitations.
