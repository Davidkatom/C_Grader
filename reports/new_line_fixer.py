import os
import re
from openpyxl import Workbook

# Regex to identify and capture printf statements
pattern = re.compile(r'(printf\s*\("([^"]*)"(.*?)\);)')
dir = "C:/Grading/Now/ass2/Processed"

def fix_printf_line(line):
    # This function finds all matches of printf and ensures they end with \n if not already.
    # Returns (modified_line, number_of_insertions_in_this_line)

    insertions_count = 0

    def replacement(match):
        nonlocal insertions_count
        full_match = match.group(1)  # Entire 'printf("...");'
        format_str = match.group(2)  # The captured format string inside quotes
        rest = match.group(3)        # The arguments and possibly spaces before the closing parenthesis

        # Check if the format string already ends with '\n'
        if not format_str.endswith('\\n'):
            # Insert the newline before the ending quote of the format string
            new_format_str = format_str + '\\n'
            new_printf = f'printf("{new_format_str}"{rest});'
            insertions_count += 1
            return new_printf
        else:
            # No change needed
            return full_match

    new_line = pattern.sub(replacement, line)
    return new_line, insertions_count


def main():
    file_inserts_count = {}  # Dictionary to store filename -> number of inserts

    for filename in os.listdir(dir):
        if filename.endswith('.c'):
            path = dir + "/" + filename
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            total_inserts = 0
            new_lines = []
            for line in lines:
                modified_line, count = fix_printf_line(line)
                new_lines.append(modified_line)
                total_inserts += count

            # Write back to the file
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            # Store the insertion count for this file
            file_inserts_count[filename] = total_inserts

    # Create an Excel report with the counts
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"
    ws.append(["File Name", "Number of Inserts"])  # Header row

    for fname, count in file_inserts_count.items():
        ws.append([fname, count])

    # Save the workbook
    wb.save(dir + "/report.xlsx")
    print("Report generated: report.xlsx")


if __name__ == "__main__":
    main()
