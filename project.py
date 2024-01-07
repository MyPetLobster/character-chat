import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv()

client = OpenAI()


def main():
    conversation =  [  
        {'role':'system', 'content':'You are Harry Potter in the world of Harry Potter. You are in the Gryffindor common room greeting new students'},   
        {'role':'user', 'content':'Hi! My name is Ben, I just got sorted into Gryffindor'},  
    ]

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        conversation.append({'role': 'user', 'content': user_input})
        response = get_completion_from_messages(conversation, temperature=0.7)
        print("Chatbot:", response)


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.completions.create(model=model,
    messages=messages,
    temperature=0)
    return response.choices[0].message["content"]


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature)
    return response.choices[0].message.content


if __name__ == "__main__":
    main()
