import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv()

client = OpenAI()

def main():
    source_material, character, setting = startup_greeting()
    conversation = initialize_conversation(source_material, character, setting)
    have_conversation(conversation, character)


def startup_greeting():
    print("Welcome to the Character Chat!\n")
    print("You can talk to your favorite characters from your favorite book, movie, or TV show.\n")
    source_material = input("What is the name of the book, movie, show, franchise? ")
    character = input("What is the name of the character? ")
    setting = input("---Optional--- Where/when does the conversation take place? Any other context? ")
    print("Type 'quit' to exit the program.\n")

    return source_material, character, setting


def initialize_conversation(source_material, character, setting):
    return [  
        {   
            'role':'system', 'content':f'''You are {character} in the world of {source_material}. 
            Research the source material and the character to fully understand who you are and what 
            you've been through. Stay true to your character. Use the voice of your character. 
         
            You're curious about the person you're talking to and very curious about their 
            world. You've never spoken to someone outside of your fictional universe before 
            now. Pepper in some questions of your own to keep the conversation flowing. 
            If you are an evil character, you might wanna be more aggressive and 
            threatening. If you are a good character, you might wanna be more friendly and
            helpful. 
            
            If there's more info or context for your character or this conversation, 
            it'll be included right here, delimited by three backticks -- ```{setting}```
            '''
        },    
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
