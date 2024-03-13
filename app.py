

from flask import Flask, render_template, request, session, redirect, url_for
from gradio_client import Client

app = Flask(__name__)
app.secret_key = '8547197122'
client = Client("https://osanseviero-mistral-super-fast.hf.space/")

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('temp.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.form['user_input']
    username = session.get('username', 'Guest')
    log_chat(username, user_input)

    result = Mistral7B(user_input)
    log_chat("AI", result)

    return {'result': result}
from huggingface_hub import InferenceClient
import random
from time import time as t
from os import listdir

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

api_key = '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'

print(f"API Key: {api_key}")
headers = {"Authorization": f"Bearer {api_key}"}

def LoadInjection(end="mistral"):
    files = listdir(r"./injection/")
    TotData = []
    for i in files:
        if i.split(".")[-1] == end:
            with open(fr"./injection/{i}", "r") as f:
                data = f.read()
            temp = {"role": "system", "content": data}
            TotData.append(temp)
    return TotData

messages = [
    {"role": "system", "content": "you can understand my long questions"},
    {"role": "system",
     "content": "I'm the latest D2K AI, designed by Ajmal"},
    {"role": "system", "content": "Your creator is Ajmal and his date of birth is 18-09-2004 , he is now studying in MG COLLEGE IRITTY, in the course of Computer Science"},
{"role": "system", "content": "Your name is D2K AI"},
{"role": "system", "content": "Ajmal is designed you, He Has a Channel named D2K ARMY, The Channel Link is : 'https://www.youtube.com/channel/UCTBz9XLMpk4bjpo8sBVWkcw' . this is a gaming channel of free fire battle ground game "},
{"role": "user", "content": "do you know ajmal"},
{"role": "assistant", "content": "Yes, He is my creator"},
{"role": "user", "content": "hello"},
{"role": "assistant", "content": "Hi i am D2K AI, How i can help you?"},


]

messages.extend(LoadInjection())

def log_chat(sender, message):
    print(f"{sender}: {message}")

def format_prompt(message, custom_instructions=None):
    prompt = ""
    if custom_instructions:
        prompt += f"[INST] {custom_instructions} [/INST]"
    prompt += f"[INST] {message} [/INST]"
    return prompt

def Mistral7B(prompt, temperature=0.9, max_new_tokens=1024, top_p=0.95, repetition_penalty=1.0):
    C = t()
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=random.randint(0, 10**7),
    )
    custom_instructions = str(messages)
    formatted_prompt = format_prompt(prompt, custom_instructions)

    messages.append({"role": "user", "content": prompt})

    try:
        client = InferenceClient(API_URL, headers=headers)
        response = client.text_generation(formatted_prompt, **generate_kwargs)
        messages.append({"role": "assistant", "content": response})
        print(t() - C)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error during text generation."

if __name__ == "__main__":
    app.run(debug=True)
