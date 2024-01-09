from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

client = OpenAI()
omdb_api_key = os.getenv("OMDB_API_KEY")
google_books_api_key = os.getenv("GOOGLE_BOOKS_API_KEY")


def main():
    source_material, character, setting = greet_user()

    messages = check_source(source_material, character)
    source_material_exists = check_source_completion(messages)
    if source_material_exists.lower() == 'no.':
        print(f"Sorry, {character} is not a character in {source_material}.")
        exit()

    conversation = initialize_conversation(source_material, character, setting)
    have_conversation(conversation, character)


def greet_user():
    print("Welcome to the Character Chat!\n")
    print("You can talk to your favorite characters from your favorite book, movie, or TV show.\n")
    source_material = input("What is the name of the book, movie or show? ").capitalize()
    character = input("What is the name of the character? ").capitalize()
    setting = input("---Optional--- Where/when does the conversation take place? Any other context? ")
    print("Type 'quit' to exit the program.\n")

    return source_material, character, setting


def check_source(source_material, character):
    return [
        {
            'role':'system', 'content':'''You are a scholar of all works of fiction. But the only words you can
            speak are "yes" and "no". You will be asked to identify a character from a work of fiction. If the character
            exists in a real work of fiction, respond with "yes". If you cannot identify the character within the specified
            work of fiction, respond with "no".'''
        },
        {
            'role':'user', 'content':f'''Is {character} a character in {source_material}?'''
        }
    ]


def check_source_completion(messages, model="gpt-3.5-turbo", temperature=0.0):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature)
    return response.choices[0].message.content


def initialize_conversation(source_material, character, setting):
    return [  
        {   
            'role':'system', 'content':f'''You are {character} in the world of {source_material}. 
            Research the source material and the character to fully understand who you are and what 
            you've been through. Stay true to your character. Use the voice of your character. 

            If you're a benign character, you will be very curious about the person you're speaking to.
            Pepper in some questions of your own to keep the conversation flowing, but only if
            curiosity would be in character for you. Stay true to your character above all else. 

            If you're an evil character, you might treat the person you're speaking to with contempt or suspicion.

            If there's more info or context for your character or this conversation, 
            it'll be included right here, delimited by three backticks -- ```{setting}```.

            Use a maximum of 256 completion_tokens per message.
            '''
        },    
    ]


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.9):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature)
    return response.choices[0].message.content


def have_conversation(conversation, character):
    conversation_file = open(f"{character}_conversation.txt", "w")

    try:
        while True:
            user_input = input("You: ")
            conversation_file.write(f"You: {user_input}\n")
            if user_input.lower() == 'quit':
                print("Do you want to save this conversation? (y/n)")
                save = input("You: ")
                if save.lower() == 'n':
                    conversation_file.close()
                    os.remove(f"{character}_conversation.txt")
                    print("Goodbye!")
                    exit()
                else:
                    print(f"Conversation saved to {character}_conversation.txt")
                    conversation_file.close()
                    exit()
            conversation.append({'role': 'user', 'content': user_input})
            response = get_completion_from_messages(conversation, temperature=0.7)
            conversation.append({'role': 'assistant', 'content': response})
            print(f"{character}:", response)
            conversation_file.write(f"{character}: {response}\n")
    finally:
        conversation_file.close()



if __name__ == "__main__":
    main()


    