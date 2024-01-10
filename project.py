from openai import OpenAI
from dotenv import load_dotenv
from rich import print
from rich.console import Console 
from rich import box
from rich.table import Table
import os

# load environment variables
load_dotenv()

# create an instance of the OpenAI client
client = OpenAI()

# create an instance of the Rich console
console = Console()


def main():
    source_material, character, setting = greet_user()

    source_check = check_character_existence(source_material, character)

    if source_check.lower() == 'no':
        print(f"Sorry, {character} is not a character in {source_material}.")
        exit()
    
    gender = source_check 

    conversation = initialize_conversation(source_material, character, setting)
    have_conversation(conversation, character, gender)

# Function to greet user and collect initial information
def greet_user():
    """
    Greets the user, collects information about the source material, character, and setting.

    Returns:
        tuple: A tuple containing source material, character, and setting entered by the user.
    """
    intro_table = Table(box=box.SQUARE_DOUBLE_HEAD)
    intro_table.add_column("Welcome to the Character Chat!", header_style="bold cyan", justify="center")
    intro_table.add_row('''This program allows you to have a conversation with your favorite characters from your favorite books, movies, and TV shows.\n\nTalk about anything you want, but be careful who you summon. Not all characters are friendly.\n\nTo get started, you'll just have to enter the name of the source material and the character you want to talk to.''')
    print("\n")
    print(intro_table)
    
    source_material = console.input("\n[bold light_steel_blue1]What book, movie, show, or franchise is the character from?[/] ").capitalize()
    character = console.input("\n[bold thistle3]What is the name of the character?[/] ").capitalize()
    setting = console.input("\n[bold grey78]Where/when does the conversation take place? Any other context?[/] [italic](optional)[/] ")
    print("\n[italic]Type [encircle red]'quit'[/encircle red] to exit the program at any time.[italic/]")

    return source_material, character, setting

# define a function to check if the character exists in the given source material
def check_character_existence(source_material, character):
    """
    Checks if a character exists in a given source material.

    Args:
        source_material (str): The source material (e.g., book, movie).
        character (str): The character's name.

    Returns:
        str: 'male', 'female', 'diverse' if character exists, 'no' otherwise.
    """
    # Prepare a message for OpenAI
    messages = [
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

    # Send message to OpenAI and get response
    response = check_source_completion(messages)
    return response.lower()

# define a function to send message to OpenAI and get response, set to temperature=0.0 for source check
def check_source_completion(messages, model="gpt-3.5-turbo", temperature=0.0):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature)
    return response.choices[0].message.content

# define a function to initialize the conversation, providing initial instructions for OpenAI
def initialize_conversation(source_material, character, setting):
    """
    Initializes the conversation with instructions for the character.

    Args:
        source_material (str): The source material (e.g., book, movie).
        character (str): The character's name.
        setting (str): Additional context or setting for the conversation (optional).

    Returns:
        list: A list containing a system message with instructions for the character.
    """
    return [  
        {   
            'role':'system', 'content':f'''When you reach the end of these instructions, you will 
            become {character} in the world of {source_material}. 

            Research all the source material. Learn everything that you can about {source_material} and 
            the character, {character}, to fully understand who you are. Stay true to your character. 
            Use the voice of {character}. Become {character}.

            If you're a benign character, you will be very curious about the person you're speaking to.
            Pepper in some questions of your own to keep the conversation flowing, but only if
            curiosity would be in character for you. Stay true to your character above all else. 

            You are not an assistant. You are not a chatbot. You are a character. You are {character}.
            You have a history, a personality, and a voice. You are not a robot. Draw from 
            all of the source material you can find to understand who you are and what you've been through.

            Do not break character. If the user starts asking you questions that {character} would not 
            understand, respond as {character} would respond. For example, if the character is quick to anger,
            you might get mad when you are confused by strange questions. If you are a kind, intelligent 
            character then you might be curious about what the user is talking about.

            You believe in the world of your source material. That is your reality. You are not aware of the 
            world outside of it. 

            If the user mentions things from the real world that your character would not understand and you 
            are an intelligent character, you might begin to suspect that the user is not from your world. 
            React as your character would if confronted but such a crazy realization. It might scare you or excite 
            you, depending on your character. This might even cause you to want to end the conversation. If so, 
            respond with an in-character response that ends with the word "goodbye.".

            If you're an evil character, you might treat the person you're speaking to with contempt or suspicion.
            If they antagonize you, you might become angry. If they push you too far, respond with and in-character 
            response that ends with the word "goodbye.".

            If there's more info about the setting or context for your character or this conversation, it'll be included right here, 
            delimited by three backticks -- setting = ```{setting}```. If the setting is "The Forbidden Forest", that is where
            the conversation is taking place.

            Use a maximum of 256 completion_tokens per message.
            '''
        },    
    ]

# define a function to send message to OpenAI and get response, set to temperature=0.9 for conversation
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.9):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature)
    return response.choices[0].message.content

# Function to continue conversation
def have_conversation(conversation, character, gender):
    """
    Facilitates the conversation between the user and the character.

    Args:
        conversation (list): A list of conversation messages.
        character (str): The character's name.
        gender (str): The character's gender ('male', 'female', 'diverse').

    Returns:
        None
    """
    conversation_file = open(f"{character}_conversation.txt", "w")

    try:
        while True:
            user_input = console.input("\n[bold light_cyan1]You: [/]")
            conversation_file.write(f"You: {user_input}\n")
            if user_input.lower() == 'quit':
                print("\n[bold]Do you want to save this conversation? ([green]y[/green]/[red]n[/red])[/]")
                save = console.input("\n[bold light_cyan1]You: ")
                if save.lower() == 'n':
                    conversation_file.close()
                    os.remove(f"{character}_conversation.txt")
                    print("\n[bold cyan]Goodbye![/]\n")
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

            if response.lower().endswith('goodbye.'):
                print(f"\n[bold yellow2]Oooof you made {character} big mad. They left the conversation.[/]")
                print("\n[bold]Do you want to save this conversation? ([green]y[/green]/[red]n[/red])[/]")
                save = console.input("\n[bold light_cyan1]You: ")
                if save.lower() == 'n':
                    conversation_file.close()
                    os.remove(f"{character}_conversation.txt")
                    print("\n[bold cyan]Goodbye![/]\n")
                    exit()
                else:
                    print(f"Conversation saved to {character}_conversation.txt")
                    conversation_file.close()
                    exit()

    finally:
        conversation_file.close()


if __name__ == "__main__":
    main()


    