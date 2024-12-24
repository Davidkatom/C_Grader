import os
import re
from openpyxl import Workbook

# Regex to identify and capture printf statements
pattern = re.compile(r'(printf\s*\("([^"]*)"(.*?)\);)')
dir = "C:/Grading/Now/ass4/Q1/Processed"

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
    file_counts = {}  # Dictionary to store filename -> (printf insertions, return 0 removals)

    for filename in os.listdir(dir):
        if filename.endswith('.c'):
            path = os.path.join(dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            printf_insertions = 0
            return_removals = 0
            new_lines = []
            for line in lines:
                # Skip lines containing 'return 0;' and count them
                if 'return 0;' in line.strip():
                    return_removals += 1
                    continue
                modified_line, count = fix_printf_line(line)
                new_lines.append(modified_line)
                printf_insertions += count

            # Write back to the file
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            # Store the counts for this file
            file_counts[filename] = (printf_insertions, return_removals)

    # Create an Excel report with the counts
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"
    ws.append(["File Name", "Number of printf Insertions", "Number of return 0; Removals"])  # Header row

    for fname, counts in file_counts.items():
        ws.append([fname, counts[0], counts[1]])

    # Save the workbook
    report_path = os.path.join(dir, "report.xlsx")
    wb.save(report_path)
    print(f"Report generated: {report_path}")


if __name__ == "__main__":
    main()
