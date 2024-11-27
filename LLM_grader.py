import os

from openai import OpenAI

prompt = "Check if the students output contains the key output points of the program as detailed bellow. Respond as 1)correct / incorrect <What is the problem> ...  only take into account imporant mistakes. disregard things like multiple prompting or spelling issues"

openai_api_key = os.environ.get('OPENAI_KEY')
root_dir = "C:/Grading/ass5"  # Replace with the path to your root directory
correct_output_folder = root_dir + "/output.txt"
output_dir = "C:/Grading/ass5/Output"  # Replace with the path to your Processed directory
#for file in output_dir:
files = os.listdir(output_dir)
outputs = []
with open(correct_output_folder, 'r') as f:
    correct_output = f.read()
for file in files:
    with open(output_dir + "/" + file, 'r') as f:
        output = f.read()
        outputs.append(output)


client = OpenAI(api_key=openai_api_key)

for output in outputs:
    print(files[outputs.index(output)])
    current_prompt = prompt + "\n Correct output: \n "+ correct_output + "\n student output:\n" + output
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": current_prompt}],
        temperature=1.5,
        model="gpt-3.5-turbo",
    )
    report = chat_completion.choices[0].message.content
    print(report)