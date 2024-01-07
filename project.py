import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv()

client = OpenAI()

def main():
    print("Welcome to the Character Chatbot!\n")
    print("You can talk to a character from a book or movie.")
    source_material = input("What is the name of the book or movie? ")
    character = input("What is the name of the character? ")
    setting = input("(OPTIONAL) Where/when does the conversation take place? ")
    username = input(f"What do you want {character} to call you? ")
    print("Type 'quit' to exit the program.\n")

    conversation = initialize_conversation(username, source_material, character, setting)
    have_conversation(conversation, character)


def initialize_conversation(username, source_material, character, setting):
    return [  
        {'role':'system', 'content':f'''You are {character} in the world of {source_material}. 
            You are talking to {username}. Have a casual conversation with them. Stay true to your character. 
            Don't repeat yourself. Don't repeat things you already said in previous messages. 
            Optionally, if users enter more information, it will be included right here -- {setting}'''},    
    ]


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.completions.create(model=model,
    messages=messages,
    temperature=1.2)
    return response.choices[0].message.content


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature)
    return response.choices[0].message.content


def have_conversation(conversation, character):
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        conversation.append({'role': 'user', 'content': user_input})
        response = get_completion_from_messages(conversation, temperature=0.7)
        conversation.append({'role': 'assistant', 'content': response})
        print(f"{character}:", response)


if __name__ == "__main__":
    main()
