from openai import OpenAI
from dotenv import load_dotenv
from rich import print
from rich.console import Console 
from rich import box
from rich.table import Table
import os


load_dotenv()

client = OpenAI()
console = Console()


def main():
    source_material, character, setting = greet_user()

    messages = check_source(source_material, character)
    source_check = check_source_completion(messages)

    print(source_check)

    if source_check.lower() == 'no':
        print(f"Sorry, {character} is not a character in {source_material}.")
        exit()
    
    gender = source_check 

    conversation = initialize_conversation(source_material, character, setting)
    have_conversation(conversation, character, gender)


def greet_user():
    intro_table = Table(box=box.SQUARE_DOUBLE_HEAD)
    intro_table.add_column("Welcome to the Character Chat!", header_style="bold cyan", justify="center")
    intro_table.add_row('''This program allows you to have a conversation with your favorite characters from your favorite books, movies, and TV shows.\n\nTalk about anything you want, but be careful who you summon. Not all characters are friendly.\n\nTo get started, you'll just have to enter the name of the source material and the character you want to talk to.''')
    print(intro_table)
    
    source_material = console.input("\n[bold sea_green1]What book, movie, show, or franchise is the character from?[/] ").capitalize()
    character = console.input("\n[bold thistle3]What is the name of the character?[/] ").capitalize()
    setting = console.input("\n[bold grey78]Where/when does the conversation take place? Any other context?[/] [italic](optional)[/] ")
    print("\n[italic]Type [encircle red]'quit'[encircle red/] to exit the program at any time.[italic/]")

    return source_material, character, setting


def check_source(source_material, character):
    return [
        {
            'role':'system', 'content':'''You are a scholar of all works of fiction. But the only words you can
            speak are "no", "male", "female", and "diverse". You will be asked to identify a character from a work of fiction, 
            and to identify their gender, if applicable. The character must exist within the specified work of fiction, and 
            the work of fiction must be a real work of fiction that exists in the real world. 

            If the character does not identify as male or female, use "diverse". Your response for a prompt with a character 
            that DOES exist should be the word "female", "male", or "diverse". (all lowercase, no punctuation, no quotation marks).
            If the character does exist, respond with only their gender. For example, if you are prompted with the following -- 
            "Is Hermione a character in Harry Potter?", your response should be -- "female". 

            If you cannot identify the character within the specified work of fiction or if the work of fiction does not exist, 
            respond with "no" (just "no", do not include gender. All lowercase, no punctuation, no quotation marks.)
            
            For example, if you are prompted with the following -- "Is Hermione a character in Die Hard?",
            your response should be -- "no".
            
            Be lenient with spelling and capitalization. Do your best to understand what the user intended to say.'''
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


def have_conversation(conversation, character, gender):
    conversation_file = open(f"{character}_conversation.txt", "w")

    try:
        while True:
            user_input = console.input("\n[bold light_cyan1]You: [/]")
            conversation_file.write(f"You: {user_input}\n")
            if user_input.lower() == 'quit':
                print("Do you want to save this conversation? (y/n)")
                save = console.input("[bold light_cyan1]You: ")
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
            if gender == "diverse":
                print(f"\n[bold light_yellow3]{character}: [/]", response)
            elif gender == "female":
                print(f"\n[bold plum2]{character}: [/]", response)
            else:
                print(f"\n[bold sea_green3]{character}: [/]", response)
            conversation_file.write(f"{character}: {response}\n")
    finally:
        conversation_file.close()



if __name__ == "__main__":
    main()


    