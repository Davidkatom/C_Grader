import subprocess
import time


def compile(c_file):
    program_name = "program.exe"
    compile_command = f"gcc {c_file} -o {program_name}"
    result = subprocess.run(compile_command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        return 0
    return subprocess.Popen(program_name, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            universal_newlines=True, bufsize=1)


def run_file(c_file, input_file):
    process = compile(c_file)
    if process == 0:
        return "Compilation Error"

    try:
        with open(input_file, 'r') as file:
            input_lines = file.readlines()
    except IOError:
        return "Error reading input file"

    try:
        for input_data in input_lines:
            # Send input followed by a delay to allow the C program to process and respond
            send_input(process, input_data)
            time.sleep(0.1)  # Adjust as necessary based on how the program processes input

            # After sending all inputs, close stdin to signal no more input will be sent
        try:
            process.stdin.close()
        except OSError as e:
            print(f"Error closing stdin: {e}")
            # Optional: Additional handling, such as logging or cleaning up resources.
        # Read the final output
        output = process.stdout.read()
        print("Output:", output)
        # Don't forget to capture errors if any
        errors = process.stderr.read()
        if errors:
            print("Errors:", errors)
    finally:
        # Ensure the process is terminated
        process.terminate()
    # print(output)
    return output

def read_input_file(input_data):
    try:
        with open(input_data, 'r') as file:
            input_data = file.readlines()
    except IOError:
        return "Error reading input file"


def send_input(proc, input_data):
    try:
        proc.stdin.write(input_data)
        proc.stdin.flush()
    except OSError as e:
        # Optional: Add logic to handle the error, such as breaking out of the loop or terminating the process.
        return "Error sending input"  # Indicate failure
    return True  # Indicate success
