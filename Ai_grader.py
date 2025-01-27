
from openai import OpenAI
root = "C://Grading//Now//ass6//"
client = OpenAI(api_key="sk-", base_url="https://api.deepseek.com")

#read from file:

with open(root + "c_code.c", "r", encoding='utf-8') as file:
    c_code = file.read()
with open(root + "questions.txt", "r", encoding='utf-8') as file:
    questions = file.read()


response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a c code checker. Check the following C code. Check the following things: 1)Will the program compile? 2)Will it give the correct output? 3) Does it do what it supposed to?. Just answer those questions without further bullshit. It should be approximately correct I dont care about the exactness of the output messege only the logic and spirit."},
        {"role": "user", "content": "question: " + questions + "code: " + c_code},
    ],
    stream=False
)

print(response.choices[0].message.content)